import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import Dict, List, Optional
import os
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LlamaMedicalService:
    """Llama 3.2 11B Medical AI Service"""
    
    def __init__(self):
        logger.info("Initializing Llama 3.2 11B Medical Service...")
        self.model_loaded = False
        self.initialize_models()
        
        # Medical knowledge base
        self.medical_knowledge = self.load_medical_knowledge()
        self.initialize_rag_system()
        
        # Medical translation dictionary
        self.medical_dictionary = {
            # Cardiovascular
            "myocardial infarction": "heart attack",
            "hypertension": "high blood pressure",
            "arrhythmia": "irregular heartbeat",
            "tachycardia": "fast heart rate",
            "bradycardia": "slow heart rate",
            "hyperlipidemia": "high cholesterol",
            "edema": "swelling",
            "thrombosis": "blood clot",
            
            # Diabetes
            "hyperglycemia": "high blood sugar",
            "hypoglycemia": "low blood sugar",
            "polyuria": "frequent urination",
            "polydipsia": "excessive thirst",
            "polyphagia": "excessive hunger",
            
            # General
            "prognosis": "expected outcome",
            "etiology": "cause",
            "pathology": "disease process",
            "contraindication": "reason not to use",
            "benign": "not cancerous",
            "malignant": "cancerous",
            "chronic": "long-lasting",
            "acute": "sudden/severe",
            "remission": "no symptoms period",
            "metastasis": "cancer spread",
        }
    
    def initialize_models(self):
        """Initialize Llama 3.2 11B model"""
        try:
            HF_TOKEN = os.getenv("HF_TOKEN")
            MODEL_NAME = "meta-llama/Llama-3.2-11B"
            
            logger.info(f"Loading model: {MODEL_NAME}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                MODEL_NAME,
                token=HF_TOKEN,
                trust_remote_code=True
            )
            
            # Load model with quantization for memory efficiency
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                token=HF_TOKEN,
                torch_dtype=torch.float16,
                device_map="auto" if torch.cuda.is_available() else None,
                load_in_8bit=True,  # 8-bit quantization for 11B model
                trust_remote_code=True
            )
            
            # Create pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.1,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # LangChain wrapper
            self.llm = HuggingFacePipeline(pipeline=self.pipeline)
            
            # Embeddings for RAG
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            self.model_loaded = True
            logger.info("Llama 3.2 11B model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading Llama model: {e}")
            self.model_loaded = False
    
    def load_medical_knowledge(self) -> List[str]:
        """Load medical knowledge base"""
        return [
            "Diabetes: Condition where blood sugar is too high. Type 2: body doesn't use insulin properly.",
            "Hypertension: High blood pressure (>130/80 mmHg). Can cause heart disease, stroke.",
            "Cholesterol: Fatty substance in blood. LDL bad, HDL good. High LDL increases heart risk.",
            "Heart Attack: Blood flow to heart blocked. Symptoms: chest pain, shortness of breath.",
            "Metformin: Diabetes medication. Lowers glucose production in liver.",
            "Lisinopril: Blood pressure medication. Relaxes blood vessels.",
            "Atorvastatin: Cholesterol medication. Reduces cholesterol production.",
            "Healthy diet: Fruits, vegetables, whole grains, lean proteins. Limit salt, sugar, saturated fat.",
            "Exercise: 30 minutes daily improves heart health, diabetes control, blood pressure.",
            "Blood tests: Check glucose, cholesterol, kidney function. Often require fasting.",
            "Medication side effects: Report nausea, dizziness, rash to doctor.",
            "Symptoms to watch: Chest pain, severe headache, vision changes, difficulty breathing."
        ]
    
    def initialize_rag_system(self):
        """Initialize RAG system for medical knowledge"""
        if not self.model_loaded:
            return
        
        # Create documents
        from langchain.schema import Document
        documents = [Document(page_content=text) for text in self.medical_knowledge]
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        split_docs = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            persist_directory="./medical_knowledge_db"
        )
        
        # Create prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a medical expert explaining complex medical information to patients in simple, easy-to-understand language.

Medical Context: {context}

Patient Question: {question}

Please provide a clear, simple explanation that:
1. Uses everyday language (no medical jargon)
2. Is accurate but easy to understand
3. Includes practical advice
4. Is reassuring but honest

Simple Explanation:"""
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )
    
    def explain_medical_text(self, text: str, context: str = "") -> Dict:
        """Explain medical text using Llama 3.2"""
        if not self.model_loaded:
            return self._fallback_explanation(text)
        
        try:
            # First check dictionary
            simple_term = self._check_medical_dictionary(text)
            if simple_term:
                return {
                    "original": text,
                    "explanation": simple_term,
                    "confidence": "high",
                    "source": "dictionary",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Use RAG for detailed explanation
            query = f"Explain in simple terms for a patient: {text}"
            if context:
                query += f" Context: {context}"
            
            result = self.qa_chain({"query": query})
            
            explanation = result["result"]
            sources = [doc.page_content for doc in result.get("source_documents", [])]
            
            # Clean up explanation
            explanation = self._clean_explanation(explanation)
            
            return {
                "original": text,
                "explanation": explanation,
                "confidence": "medium",
                "sources": sources[:2],
                "model": "Llama 3.2 11B",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in explanation: {e}")
            return self._fallback_explanation(text)
    
    def explain_diagnosis(self, diagnosis: str, notes: str = "") -> Dict:
        """Explain medical diagnosis with context"""
        if not self.model_loaded:
            return self._fallback_diagnosis_explanation(diagnosis)
        
        try:
            prompt = f"""
            Diagnosis: {diagnosis}
            Doctor's Notes: {notes}
            
            Please explain this diagnosis to a patient in simple terms:
            1. What does this diagnosis mean in everyday language?
            2. What are the main symptoms or effects?
            3. What causes this condition?
            4. What treatments are available?
            5. What lifestyle changes can help?
            
            Keep explanations simple, clear, and reassuring.
            """
            
            result = self.pipeline(
                prompt,
                max_new_tokens=500,
                temperature=0.7,
                do_sample=True
            )
            
            explanation = result[0]['generated_text']
            
            # Extract the explanation part
            lines = explanation.split('\n')
            explanation_lines = []
            for line in lines:
                if any(keyword in line.lower() for keyword in ['means', 'symptoms', 'causes', 'treatments', 'lifestyle']):
                    explanation_lines.append(line)
            
            final_explanation = '\n'.join(explanation_lines) if explanation_lines else explanation[:400]
            
            return {
                "diagnosis": diagnosis,
                "simple_explanation": final_explanation,
                "notes": notes,
                "explained_at": datetime.now().isoformat(),
                "model": "Llama 3.2 11B"
            }
            
        except Exception as e:
            logger.error(f"Error explaining diagnosis: {e}")
            return self._fallback_diagnosis_explanation(diagnosis)
    
    def analyze_lab_results(self, lab_data: Dict) -> Dict:
        """Analyze lab results with AI"""
        if not self.model_loaded:
            return self._fallback_lab_analysis(lab_data)
        
        try:
            # Format lab data for AI
            lab_text = json.dumps(lab_data, indent=2)
            
            prompt = f"""
            Analyze these lab results and provide a patient-friendly summary:
            
            Lab Results:
            {lab_text}
            
            Please provide:
            1. Overall health status summary
            2. Any concerning values (highlight in red/orange/green)
            3. What each abnormal value means
            4. Recommendations for follow-up
            5. Questions to ask the doctor
            
            Use simple language that a patient can understand.
            """
            
            result = self.pipeline(
                prompt,
                max_new_tokens=600,
                temperature=0.6,
                do_sample=True
            )
            
            analysis = result[0]['generated_text']
            
            # Categorize results
            categorization = self._categorize_lab_results(lab_data)
            
            return {
                "analysis": analysis,
                "categorization": categorization,
                "analyzed_at": datetime.now().isoformat(),
                "model": "Llama 3.2 11B"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing lab results: {e}")
            return self._fallback_lab_analysis(lab_data)
    
    def explain_medication(self, medication: str) -> Dict:
        """Explain medication purpose and side effects"""
        prompt = f"""
        Medication: {medication}
        
        Explain this medication to a patient:
        1. What is it for? (main purpose)
        2. How does it work? (simple mechanism)
        3. Common side effects
        4. Important warnings
        5. How to take it properly
        
        Keep it simple and practical.
        """
        
        try:
            result = self.pipeline(
                prompt,
                max_new_tokens=400,
                temperature=0.7,
                do_sample=True
            )
            
            explanation = result[0]['generated_text']
            
            return {
                "medication": medication,
                "explanation": explanation,
                "explained_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error explaining medication: {e}")
            return {
                "medication": medication,
                "explanation": f"{medication} is a medication prescribed by your doctor. Take as directed and report any side effects.",
                "explained_at": datetime.now().isoformat()
            }
    
    def _check_medical_dictionary(self, text: str) -> Optional[str]:
        """Check if text matches medical dictionary"""
        text_lower = text.lower()
        for term, explanation in self.medical_dictionary.items():
            if term in text_lower:
                return f"'{term}' means {explanation}."
        return None
    
    def _clean_explanation(self, explanation: str) -> str:
        """Clean up AI explanation"""
        # Remove technical phrases
        replacements = {
            "it is important to note that": "",
            "in medical terms": "",
            "clinically speaking": "",
            "the patient should": "you should",
            "the individual": "you"
        }
        
        cleaned = explanation
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        return cleaned.strip()
    
    def _categorize_lab_results(self, lab_data: Dict) -> Dict:
        """Categorize lab results into critical levels"""
        categories = {}
        
        # Reference ranges
        ranges = {
            "glucose": (70, 100),
            "hba1c": (4.0, 5.6),
            "cholesterol": (125, 200),
            "ldl": (0, 100),
            "hdl": (40, 60),
            "triglycerides": (0, 150)
        }
        
        for test, value in lab_data.items():
            if test in ranges:
                min_val, max_val = ranges[test]
                if value < min_val * 0.8 or value > max_val * 1.3:
                    categories[test] = {"level": "critical", "color": "red"}
                elif value < min_val * 0.9 or value > max_val * 1.2:
                    categories[test] = {"level": "slightly_critical", "color": "orange"}
                else:
                    categories[test] = {"level": "normal", "color": "green"}
        
        return categories
    
    def _fallback_explanation(self, text: str) -> Dict:
        """Fallback explanation when model fails"""
        return {
            "original": text,
            "explanation": f"This appears to be about '{text}'. In medical terms, this relates to health conditions or treatments that should be discussed with your healthcare provider.",
            "confidence": "low",
            "timestamp": datetime.now().isoformat(),
            "note": "Using fallback explanation"
        }
    
    def _fallback_diagnosis_explanation(self, diagnosis: str) -> Dict:
        """Fallback diagnosis explanation"""
        return {
            "diagnosis": diagnosis,
            "simple_explanation": f"{diagnosis} is a medical condition that requires proper medical care. Your doctor can provide detailed information about treatment options and management.",
            "explained_at": datetime.now().isoformat()
        }
    
    def _fallback_lab_analysis(self, lab_data: Dict) -> Dict:
        """Fallback lab analysis"""
        return {
            "analysis": "Please consult with your healthcare provider for proper analysis of these lab results.",
            "categorization": {},
            "analyzed_at": datetime.now().isoformat()
        }