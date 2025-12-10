from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiagnosisExplainer:
    """Medical diagnosis explanation and education service"""
    
    def __init__(self):
        # Medical knowledge base for common diagnoses
        self.diagnosis_knowledge = self._load_diagnosis_knowledge()
        
        # Treatment options database
        self.treatments = self._load_treatment_options()
        
        # Symptom checker
        self.symptom_patterns = self._load_symptom_patterns()
    
    def _load_diagnosis_knowledge(self) -> Dict:
        """Load medical knowledge for common diagnoses"""
        return {
            "type_2_diabetes": {
                "common_name": "Type 2 Diabetes",
                "description": "A chronic condition where the body doesn't use insulin properly.",
                "causes": [
                    "Insulin resistance",
                    "Genetic factors",
                    "Obesity",
                    "Physical inactivity",
                    "Poor diet"
                ],
                "symptoms": [
                    "Increased thirst and urination",
                    "Fatigue",
                    "Blurred vision",
                    "Slow healing wounds",
                    "Tingling in hands/feet"
                ],
                "complications": [
                    "Heart disease",
                    "Nerve damage (neuropathy)",
                    "Kidney damage",
                    "Eye damage (retinopathy)",
                    "Foot problems"
                ],
                "severity_levels": {
                    "mild": "Managed with diet and exercise",
                    "moderate": "Requires oral medications",
                    "severe": "Requires insulin therapy"
                }
            },
            "hypertension": {
                "common_name": "High Blood Pressure",
                "description": "Condition where blood pressure is consistently too high.",
                "causes": [
                    "Genetic factors",
                    "High salt diet",
                    "Obesity",
                    "Stress",
                    "Lack of exercise"
                ],
                "symptoms": [
                    "Often no symptoms",
                    "Headaches",
                    "Shortness of breath",
                    "Nosebleeds (rare)",
                    "Dizziness"
                ],
                "complications": [
                    "Heart attack",
                    "Stroke",
                    "Heart failure",
                    "Kidney disease",
                    "Vision loss"
                ],
                "severity_levels": {
                    "stage1": "130-139/80-89 mmHg",
                    "stage2": "≥140/90 mmHg",
                    "hypertensive_crisis": ">180/120 mmHg"
                }
            },
            "hyperlipidemia": {
                "common_name": "High Cholesterol",
                "description": "High levels of fats (lipids) in the blood.",
                "causes": [
                    "Poor diet",
                    "Lack of exercise",
                    "Obesity",
                    "Genetics",
                    "Diabetes"
                ],
                "symptoms": [
                    "Usually no symptoms",
                    "Xanthomas (fatty deposits under skin)",
                    "Corneal arcus (white ring around iris)"
                ],
                "complications": [
                    "Atherosclerosis",
                    "Heart attack",
                    "Stroke",
                    "Peripheral artery disease"
                ]
            },
            "coronary_artery_disease": {
                "common_name": "Heart Disease",
                "description": "Narrowing of coronary arteries due to plaque buildup.",
                "causes": [
                    "High cholesterol",
                    "High blood pressure",
                    "Smoking",
                    "Diabetes",
                    "Family history"
                ],
                "symptoms": [
                    "Chest pain (angina)",
                    "Shortness of breath",
                    "Fatigue",
                    "Heart palpitations",
                    "Dizziness"
                ],
                "complications": [
                    "Heart attack",
                    "Heart failure",
                    "Arrhythmia",
                    "Sudden cardiac arrest"
                ]
            },
            "copd": {
                "common_name": "COPD (Chronic Obstructive Pulmonary Disease)",
                "description": "Chronic inflammatory lung disease causing obstructed airflow.",
                "causes": [
                    "Smoking (primary cause)",
                    "Air pollution",
                    "Genetic factors",
                    "Occupational exposure"
                ],
                "symptoms": [
                    "Chronic cough",
                    "Shortness of breath",
                    "Wheezing",
                    "Chest tightness",
                    "Frequent respiratory infections"
                ],
                "complications": [
                    "Respiratory infections",
                    "Heart problems",
                    "Lung cancer",
                    "Pulmonary hypertension"
                ]
            }
        }
    
    def _load_treatment_options(self) -> Dict:
        """Load treatment options for various conditions"""
        return {
            "type_2_diabetes": {
                "lifestyle": [
                    "Healthy diet (low sugar, high fiber)",
                    "Regular exercise (150 min/week)",
                    "Weight management",
                    "Blood sugar monitoring"
                ],
                "medications": [
                    "Metformin",
                    "Sulfonylureas",
                    "DPP-4 inhibitors",
                    "GLP-1 receptor agonists",
                    "Insulin"
                ],
                "monitoring": [
                    "HbA1c every 3-6 months",
                    "Regular foot exams",
                    "Annual eye exams",
                    "Kidney function tests"
                ]
            },
            "hypertension": {
                "lifestyle": [
                    "Reduce salt intake",
                    "DASH diet",
                    "Regular exercise",
                    "Stress management",
                    "Limit alcohol"
                ],
                "medications": [
                    "ACE inhibitors",
                    "ARBs",
                    "Calcium channel blockers",
                    "Diuretics",
                    "Beta blockers"
                ],
                "monitoring": [
                    "Regular blood pressure checks",
                    "Home monitoring recommended",
                    "Annual kidney function tests"
                ]
            },
            "hyperlipidemia": {
                "lifestyle": [
                    "Heart-healthy diet",
                    "Regular exercise",
                    "Weight loss if needed",
                    "Smoking cessation"
                ],
                "medications": [
                    "Statins",
                    "Ezetimibe",
                    "PCSK9 inhibitors",
                    "Fibrates"
                ],
                "monitoring": [
                    "Lipid panel every 4-12 weeks initially",
                    "Then every 3-12 months",
                    "Liver function tests with statins"
                ]
            }
        }
    
    def _load_symptom_patterns(self) -> Dict:
        """Load symptom patterns for common conditions"""
        return {
            "fatigue": ["type_2_diabetes", "hypertension", "anemia", "thyroid"],
            "chest_pain": ["coronary_artery_disease", "hypertension", "anxiety"],
            "shortness_of_breath": ["copd", "heart_failure", "asthma", "anemia"],
            "frequent_urination": ["type_2_diabetes", "uti", "prostate"],
            "headache": ["hypertension", "migraine", "tension"],
            "dizziness": ["hypertension", "inner_ear", "anemia", "dehydration"],
            "tingling_extremities": ["type_2_diabetes", "vitamin_b12", "nerve"]
        }
    
    def explain_diagnosis(self, diagnosis: str, patient_context: Dict = None) -> Dict:
        """Provide comprehensive explanation of a diagnosis"""
        
        # Clean and normalize diagnosis
        normalized_diag = self._normalize_diagnosis(diagnosis)
        
        # Get explanation from knowledge base
        explanation = self._get_diagnosis_explanation(normalized_diag)
        
        # Add personalized context if available
        if patient_context:
            explanation = self._personalize_explanation(explanation, patient_context)
        
        # Add treatment options
        treatment_options = self._get_treatment_options(normalized_diag)
        
        # Generate next steps
        next_steps = self._generate_next_steps(normalized_diag, patient_context)
        
        # Create comprehensive response
        response = {
            "diagnosis": diagnosis,
            "normalized_diagnosis": normalized_diag,
            "explanation": explanation,
            "treatment_options": treatment_options,
            "next_steps": next_steps,
            "educational_resources": self._get_educational_resources(normalized_diag),
            "questions_for_doctor": self._generate_doctor_questions(normalized_diag),
            "explained_at": datetime.now().isoformat(),
            "source": "Medical Knowledge Base"
        }
        
        return response
    
    def _normalize_diagnosis(self, diagnosis: str) -> str:
        """Normalize diagnosis to standard format"""
        diagnosis_lower = diagnosis.lower()
        
        # Map variations to standard terms
        diagnosis_map = {
            "diabetes": "type_2_diabetes",
            "diabetes mellitus type 2": "type_2_diabetes",
            "type ii diabetes": "type_2_diabetes",
            "high blood pressure": "hypertension",
            "htn": "hypertension",
            "high cholesterol": "hyperlipidemia",
            "dyslipidemia": "hyperlipidemia",
            "heart disease": "coronary_artery_disease",
            "cad": "coronary_artery_disease",
            "chronic obstructive pulmonary disease": "copd",
            "chronic bronchitis": "copd",
            "emphysema": "copd"
        }
        
        for key, value in diagnosis_map.items():
            if key in diagnosis_lower:
                return value
        
        # Try to find partial matches
        for known_diag in self.diagnosis_knowledge.keys():
            if known_diag in diagnosis_lower or diagnosis_lower in known_diag:
                return known_diag
        
        return diagnosis_lower.replace(" ", "_")
    
    def _get_diagnosis_explanation(self, diagnosis: str) -> Dict:
        """Get explanation from knowledge base"""
        if diagnosis in self.diagnosis_knowledge:
            return self.diagnosis_knowledge[diagnosis]
        
        # Generic explanation for unknown diagnoses
        return {
            "common_name": diagnosis.replace("_", " ").title(),
            "description": f"{diagnosis.replace('_', ' ').title()} is a medical condition that requires proper diagnosis and treatment by healthcare professionals.",
            "causes": ["Consult with your doctor for specific causes"],
            "symptoms": ["Symptoms vary - discuss with healthcare provider"],
            "complications": ["Proper management is important to prevent complications"],
            "note": "This is a general explanation. Please consult your healthcare provider for personalized information."
        }
    
    def _personalize_explanation(self, explanation: Dict, context: Dict) -> Dict:
        """Personalize explanation based on patient context"""
        personalized = explanation.copy()
        
        # Add age-specific information
        age = context.get("age")
        if age:
            if age > 65:
                personalized["age_considerations"] = [
                    "Higher risk of complications",
                    "Medication adjustments may be needed",
                    "Regular monitoring is important"
                ]
            elif age < 40:
                personalized["age_considerations"] = [
                    "Early intervention is beneficial",
                    "Focus on lifestyle changes",
                    "Long-term management plan needed"
                ]
        
        # Add severity context
        severity = context.get("severity", "moderate")
        if "severity_levels" in personalized:
            personalized["current_severity"] = severity
            personalized["severity_description"] = personalized["severity_levels"].get(severity, "")
        
        # Add lifestyle factors
        lifestyle = context.get("lifestyle_factors", {})
        if lifestyle:
            personalized["lifestyle_recommendations"] = []
            
            if lifestyle.get("smoking"):
                personalized["lifestyle_recommendations"].append("Smoking cessation is strongly recommended")
            
            if lifestyle.get("sedentary"):
                personalized["lifestyle_recommendations"].append("Increase physical activity gradually")
            
            if lifestyle.get("diet_poor"):
                personalized["lifestyle_recommendations"].append("Consult with a nutritionist for dietary changes")
        
        return personalized
    
    def _get_treatment_options(self, diagnosis: str) -> Dict:
        """Get treatment options for diagnosis"""
        if diagnosis in self.treatments:
            return self.treatments[diagnosis]
        
        # Generic treatment options
        return {
            "lifestyle": [
                "Healthy diet",
                "Regular exercise",
                "Stress management",
                "Adequate sleep"
            ],
            "medications": ["Consult doctor for appropriate medications"],
            "monitoring": ["Regular follow-up with healthcare provider"]
        }
    
    def _generate_next_steps(self, diagnosis: str, context: Dict = None) -> List[str]:
        """Generate recommended next steps"""
        next_steps = []
        
        # Immediate steps
        next_steps.append("Schedule follow-up appointment with your doctor")
        next_steps.append("Discuss treatment plan options")
        next_steps.append("Get any recommended lab tests")
        
        # Diagnosis-specific steps
        if diagnosis == "type_2_diabetes":
            next_steps.append("Get a glucose meter and learn to use it")
            next_steps.append("Schedule appointment with diabetes educator")
            next_steps.append("Get referral to nutritionist")
        
        elif diagnosis == "hypertension":
            next_steps.append("Get a home blood pressure monitor")
            next_steps.append("Start tracking blood pressure daily")
            next_steps.append("Reduce salt intake immediately")
        
        elif diagnosis == "hyperlipidemia":
            next_steps.append("Start heart-healthy diet")
            next_steps.append("Begin regular exercise program")
            next_steps.append("Schedule follow-up lipid panel")
        
        # Context-specific steps
        if context:
            if context.get("new_diagnosis", False):
                next_steps.append("Join patient support group")
                next_steps.append("Research reliable medical information")
            
            if context.get("severe", False):
                next_steps.append("Consider second opinion")
                next_steps.append("Explore all treatment options")
        
        return next_steps
    
    def _get_educational_resources(self, diagnosis: str) -> List[Dict]:
        """Get educational resources for diagnosis"""
        resources = {
            "type_2_diabetes": [
                {"title": "American Diabetes Association", "url": "https://diabetes.org"},
                {"title": "Understanding Type 2 Diabetes", "type": "book"},
                {"title": "Blood Sugar Monitoring Guide", "type": "guide"}
            ],
            "hypertension": [
                {"title": "American Heart Association", "url": "https://heart.org"},
                {"title": "DASH Diet Guide", "type": "guide"},
                {"title": "Blood Pressure Management", "type": "video_series"}
            ],
            "hyperlipidemia": [
                {"title": "Managing High Cholesterol", "type": "book"},
                {"title": "Heart-Healthy Recipes", "type": "cookbook"},
                {"title": "National Heart, Lung, and Blood Institute", "url": "https://nhlbi.nih.gov"}
            ]
        }
        
        return resources.get(diagnosis, [
            {"title": "Talk to your healthcare provider for resources", "type": "advice"}
        ])
    
    def _generate_doctor_questions(self, diagnosis: str) -> List[str]:
        """Generate questions to ask the doctor"""
        questions = [
            "What is the expected progression of this condition?",
            "What treatment options are available?",
            "What are the side effects of recommended treatments?",
            "How will we monitor progress?",
            "What lifestyle changes are most important?",
            "What are the warning signs that require immediate attention?",
            "How often should I have follow-up appointments?",
            "Are there any support groups or resources you recommend?"
        ]
        
        # Diagnosis-specific questions
        if diagnosis == "type_2_diabetes":
            questions.extend([
                "What should my target blood sugar levels be?",
                "How often should I check my blood sugar?",
                "What should I do if my blood sugar is too high or too low?"
            ])
        
        elif diagnosis == "hypertension":
            questions.extend([
                "What should my target blood pressure be?",
                "How often should I check my blood pressure at home?",
                "What readings should prompt me to call you?"
            ])
        
        return questions
    
    def analyze_symptoms(self, symptoms: List[str], patient_info: Dict = None) -> Dict:
        """Analyze symptoms and suggest possible conditions"""
        
        # Normalize symptoms
        normalized_symptoms = [s.lower().replace(" ", "_") for s in symptoms]
        
        # Find matching conditions
        possible_conditions = {}
        
        for symptom in normalized_symptoms:
            if symptom in self.symptom_patterns:
                for condition in self.symptom_patterns[symptom]:
                    if condition not in possible_conditions:
                        possible_conditions[condition] = []
                    possible_conditions[condition].append(symptom)
        
        # Rank by number of matching symptoms
        ranked_conditions = sorted(
            possible_conditions.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        # Generate response
        analysis = {
            "symptoms_provided": symptoms,
            "possible_conditions": [],
            "recommendations": [],
            "urgency_level": "routine",
            "analyzed_at": datetime.now().isoformat()
        }
        
        for condition, matching_symptoms in ranked_conditions[:5]:  # Top 5
            analysis["possible_conditions"].append({
                "condition": condition.replace("_", " ").title(),
                "matching_symptoms": len(matching_symptoms),
                "symptom_list": [s.replace("_", " ") for s in matching_symptoms]
            })
        
        # Determine urgency
        urgent_symptoms = {"chest_pain", "severe_headache", "difficulty_breathing", "fainting"}
        if any(s in urgent_symptoms for s in normalized_symptoms):
            analysis["urgency_level"] = "urgent"
            analysis["recommendations"].append("Seek medical attention immediately")
        elif len(symptoms) >= 3:
            analysis["urgency_level"] = "soon"
            analysis["recommendations"].append("Schedule doctor appointment within 1-2 weeks")
        else:
            analysis["urgency_level"] = "routine"
            analysis["recommendations"].append("Monitor symptoms and mention at next checkup")
        
        # Add general recommendations
        analysis["recommendations"].append("Keep track of symptom frequency and severity")
        analysis["recommendations"].append("Note any triggers or patterns")
        
        return analysis
    
    def compare_treatments(self, diagnosis: str, treatment_a: str, treatment_b: str) -> Dict:
        """Compare two treatment options"""
        
        # Get treatment information
        treatments_info = self.treatments.get(diagnosis, {})
        
        comparison = {
            "diagnosis": diagnosis,
            "treatments": {},
            "comparison": {},
            "considerations": []
        }
        
        # Check if treatments are in our database
        all_meds = []
        for category in ["medications", "lifestyle"]:
            if category in treatments_info:
                all_meds.extend(treatments_info[category])
        
        # Simple comparison logic
        if treatment_a.lower() in [t.lower() for t in all_meds]:
            comparison["treatments"]["a"] = {
                "name": treatment_a,
                "type": "known_treatment",
                "commonly_used_for": diagnosis.replace("_", " ")
            }
        else:
            comparison["treatments"]["a"] = {
                "name": treatment_a,
                "type": "general_treatment",
                "note": "Consult doctor for specific information"
            }
        
        if treatment_b.lower() in [t.lower() for t in all_meds]:
            comparison["treatments"]["b"] = {
                "name": treatment_b,
                "type": "known_treatment",
                "commonly_used_for": diagnosis.replace("_", " ")
            }
        else:
            comparison["treatments"]["b"] = {
                "name": treatment_b,
                "type": "general_treatment",
                "note": "Consult doctor for specific information"
            }
        
        # Add general considerations
        comparison["considerations"].append("Discuss all options with your healthcare provider")
        comparison["considerations"].append("Consider side effects and interactions")
        comparison["considerations"].append("Factor in cost and insurance coverage")
        comparison["considerations"].append("Consider lifestyle impact and convenience")
        
        return comparison