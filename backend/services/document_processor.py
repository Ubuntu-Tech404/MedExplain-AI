import PyPDF2
from docx import Document
import json
import re
from typing import Dict, Any
import os

class DocumentProcessor:
    """Process medical documents (PDF, DOCX, TXT)"""
    
    def process_document(self, file_path: str, doc_type: str) -> Dict[str, Any]:
        """Process uploaded document"""
        
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        # Extract text based on file type
        text = self.extract_text(file_path)
        
        # Process based on document type
        if doc_type == "lab_report":
            return self.process_lab_report(text)
        elif doc_type == "doctor_note":
            return self.process_doctor_notes(text)
        elif doc_type == "prescription":
            return self.process_prescription(text)
        else:
            return self.process_general_document(text)
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_pdf_text(file_path)
        elif file_extension == '.docx':
            return self.extract_docx_text(file_path)
        elif file_extension in ['.txt', '.md']:
            return self.extract_txt_text(file_path)
        else:
            return ""
    
    def extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except:
            return ""
    
    def extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except:
            return ""
    
    def extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except:
            return ""
    
    def process_lab_report(self, text: str) -> Dict[str, Any]:
        """Extract lab results from report text"""
        
        # Common lab result patterns
        patterns = {
            "glucose": r"(?i)glucose[\s:]+([\d\.]+)\s*(mg/dL|mmol/L)?",
            "hba1c": r"(?i)hba1c|a1c[\s:]+([\d\.]+)\s*%?",
            "cholesterol": r"(?i)cholesterol[\s:]+([\d\.]+)\s*(mg/dL)?",
            "ldl": r"(?i)ldl[\s:]+([\d\.]+)\s*(mg/dL)?",
            "hdl": r"(?i)hdl[\s:]+([\d\.]+)\s*(mg/dL)?",
            "triglycerides": r"(?i)triglycerides[\s:]+([\d\.]+)\s*(mg/dL)?",
            "creatinine": r"(?i)creatinine[\s:]+([\d\.]+)\s*(mg/dL)?",
            "bun": r"(?i)bun|blood urea nitrogen[\s:]+([\d\.]+)\s*(mg/dL)?",
            "sodium": r"(?i)sodium[\s:]+([\d\.]+)\s*(mmol/L)?",
            "potassium": r"(?i)potassium[\s:]+([\d\.]+)\s*(mmol/L)?",
        }
        
        results = {}
        for test, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                try:
                    value = float(match.group(1))
                    results[test] = value
                except:
                    pass
        
        # Extract date if present
        date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\d{4}[/-]\d{1,2}[/-]\d{1,2})"
        date_match = re.search(date_pattern, text)
        if date_match:
            results["test_date"] = date_match.group(0)
        
        return {
            "type": "lab_report",
            "results": results,
            "raw_text_preview": text[:500] + "..." if len(text) > 500 else text,
            "extracted_values": len(results)
        }
    
    def process_doctor_notes(self, text: str) -> Dict[str, Any]:
        """Extract information from doctor's notes"""
        
        # Look for diagnosis
        diagnosis_patterns = [
            r"(?i)diagnosis:?\s*(.+)",
            r"(?i)impression:?\s*(.+)",
            r"(?i)assessment:?\s*(.+)"
        ]
        
        diagnosis = ""
        for pattern in diagnosis_patterns:
            match = re.search(pattern, text)
            if match:
                diagnosis = match.group(1).strip()
                break
        
        # Look for medications
        med_pattern = r"(?i)(?:medications|prescribed|rx)[:\s]+(.+)"
        med_match = re.search(med_pattern, text)
        medications = []
        if med_match:
            med_text = med_match.group(1)
            # Simple medication extraction
            medications = re.findall(r"\b[A-Z][a-z]+\b(?:\s+\d+[mgMG]+)?", med_text)
        
        # Look for follow-up
        followup_pattern = r"(?i)(?:follow[-\s]?up|return|re[-\s]?evaluate)[:\s]+(.+)"
        followup_match = re.search(followup_pattern, text)
        followup = followup_match.group(1).strip() if followup_match else ""
        
        return {
            "type": "doctor_note",
            "diagnosis": diagnosis,
            "medications": medications,
            "follow_up": followup,
            "note_preview": text[:300] + "..." if len(text) > 300 else text
        }
    
    def process_prescription(self, text: str) -> Dict[str, Any]:
        """Extract prescription information"""
        
        # Look for medication names
        med_pattern = r"(?i)\b(?:take|use|apply)\s+([A-Z][a-z]+\s*(?:\d+[mgMG/]+)?)"
        medications = re.findall(med_pattern, text)
        
        # Look for dosage
        dosage_pattern = r"(?i)(\d+\s*(?:mg|mcg|g|ml|tablet|cap)s?)\s*(?:per\s*(?:day|dose))?"
        dosages = re.findall(dosage_pattern, text)
        
        # Look for frequency
        freq_pattern = r"(?i)(?:once|twice|three times|four times|daily|weekly|monthly)"
        frequency = re.findall(freq_pattern, text)
        
        return {
            "type": "prescription",
            "medications": medications,
            "dosages": dosages,
            "frequency": frequency,
            "prescription_text": text
        }
    
    def process_general_document(self, text: str) -> Dict[str, Any]:
        """Process general medical document"""
        return {
            "type": "general",
            "content_preview": text[:200] + "..." if len(text) > 200 else text,
            "word_count": len(text.split())
        }