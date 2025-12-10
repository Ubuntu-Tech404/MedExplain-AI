import os
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseService:
    """Supabase database service for medical data"""
    
    def __init__(self):
        self.connected = False
        self.client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize Supabase client"""
        try:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_ANON_KEY")
            
            if supabase_url and supabase_key:
                self.client: Client = create_client(supabase_url, supabase_key)
                self.connected = True
                logger.info("Supabase client initialized successfully")
                
                # Initialize tables if in demo mode
                if os.getenv("DEMO_MODE", "true").lower() == "true":
                    self.initialize_demo_tables()
            else:
                logger.warning("Supabase credentials not found, using local storage")
                self.connected = False
                
        except Exception as e:
            logger.error(f"Error initializing Supabase client: {e}")
            self.connected = False
    
    def initialize_demo_tables(self):
        """Initialize demo tables if they don't exist"""
        try:
            # This is a simplified version - in production, use migrations
            logger.info("Initializing demo tables...")
            
            # We'll use a simple approach for demo
            # In production, you would use SQL migrations
            self.demo_data = {
                "patients": [],
                "documents": [],
                "lab_results": [],
                "medications": [],
                "appointments": []
            }
            
        except Exception as e:
            logger.error(f"Error initializing demo tables: {e}")
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user (simplified for demo)"""
        if not self.connected:
            # Demo authentication
            if email == "demo@mediclinic.com" and password == "demo123":
                return {
                    "id": "demo-patient-001",
                    "email": email,
                    "name": "Demo Patient",
                    "role": "patient",
                    "created_at": datetime.now().isoformat()
                }
            return None
        
        try:
            # Real Supabase authentication
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "name": response.user.user_metadata.get("name", ""),
                    "role": response.user.user_metadata.get("role", "patient"),
                    "created_at": response.user.created_at
                }
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
        
        return None
    
    def save_document(self, document_data: Dict) -> bool:
        """Save document metadata to database"""
        try:
            if not self.connected:
                # Store locally for demo
                if "documents" not in self.demo_data:
                    self.demo_data["documents"] = []
                
                document_data["id"] = f"doc_{datetime.now().timestamp()}"
                document_data["created_at"] = datetime.now().isoformat()
                self.demo_data["documents"].append(document_data)
                return True
            
            # Real Supabase insert
            response = self.client.table("documents").insert(document_data).execute()
            return len(response.data) > 0
            
        except Exception as e:
            logger.error(f"Error saving document: {e}")
            return False
    
    def get_patient_documents(self, patient_id: str) -> List[Dict]:
        """Get all documents for a patient"""
        try:
            if not self.connected:
                # Return demo data
                return [
                    {
                        "id": "doc_001",
                        "patient_id": patient_id,
                        "filename": "blood_test.pdf",
                        "document_type": "lab_report",
                        "file_path": "/static/uploads/demo_lab.pdf",
                        "processed_data": {
                            "type": "lab_report",
                            "results": {
                                "glucose": 95,
                                "hba1c": 5.8,
                                "cholesterol": 210,
                                "ldl": 130,
                                "hdl": 45,
                                "triglycerides": 180
                            },
                            "raw_text_preview": "Blood test results..."
                        },
                        "uploaded_at": "2024-01-15T10:30:00"
                    },
                    {
                        "id": "doc_002",
                        "patient_id": patient_id,
                        "filename": "doctor_note.docx",
                        "document_type": "doctor_note",
                        "file_path": "/static/uploads/demo_note.docx",
                        "processed_data": {
                            "type": "doctor_note",
                            "diagnosis": "Type 2 Diabetes",
                            "medications": ["Metformin"],
                            "follow_up": "3 months",
                            "note_preview": "Patient presents with..."
                        },
                        "uploaded_at": "2024-01-10T14:20:00"
                    }
                ]
            
            # Real Supabase query
            response = self.client.table("documents")\
                .select("*")\
                .eq("patient_id", patient_id)\
                .order("uploaded_at", desc=True)\
                .execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error getting patient documents: {e}")
            return []
    
    def save_lab_results(self, patient_id: str, lab_data: Dict) -> bool:
        """Save lab results to database"""
        try:
            lab_record = {
                "patient_id": patient_id,
                "lab_data": lab_data,
                "test_date": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat(),
                "analyzed": True,
                "analysis_results": {}
            }
            
            if not self.connected:
                if "lab_results" not in self.demo_data:
                    self.demo_data["lab_results"] = []
                
                lab_record["id"] = f"lab_{datetime.now().timestamp()}"
                self.demo_data["lab_results"].append(lab_record)
                return True
            
            # Real Supabase insert
            response = self.client.table("lab_results").insert(lab_record).execute()
            return len(response.data) > 0
            
        except Exception as e:
            logger.error(f"Error saving lab results: {e}")
            return False
    
    def get_lab_history(self, patient_id: str, limit: int = 10) -> List[Dict]:
        """Get lab result history for a patient"""
        try:
            if not self.connected:
                # Generate demo history
                history = []
                for i in range(3):
                    history.append({
                        "id": f"lab_00{i+1}",
                        "patient_id": patient_id,
                        "lab_data": {
                            "glucose": 95 + i*5,
                            "hba1c": 5.8 + i*0.1,
                            "cholesterol": 210 - i*10,
                            "ldl": 130 - i*5,
                            "hdl": 45 + i*2
                        },
                        "test_date": f"2024-0{i+1}-15T10:30:00",
                        "created_at": f"2024-0{i+1}-15T10:30:00"
                    })
                return history
            
            # Real Supabase query
            response = self.client.table("lab_results")\
                .select("*")\
                .eq("patient_id", patient_id)\
                .order("test_date", desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error getting lab history: {e}")
            return []
    
    def save_medication(self, patient_id: str, medication_data: Dict) -> bool:
        """Save medication information"""
        try:
            med_record = {
                "patient_id": patient_id,
                "medication_name": medication_data.get("name"),
                "dosage": medication_data.get("dosage"),
                "frequency": medication_data.get("frequency"),
                "instructions": medication_data.get("instructions"),
                "start_date": medication_data.get("start_date"),
                "end_date": medication_data.get("end_date"),
                "prescribing_doctor": medication_data.get("doctor"),
                "created_at": datetime.now().isoformat()
            }
            
            if not self.connected:
                if "medications" not in self.demo_data:
                    self.demo_data["medications"] = []
                
                med_record["id"] = f"med_{datetime.now().timestamp()}"
                self.demo_data["medications"].append(med_record)
                return True
            
            # Real Supabase insert
            response = self.client.table("medications").insert(med_record).execute()
            return len(response.data) > 0
            
        except Exception as e:
            logger.error(f"Error saving medication: {e}")
            return False
    
    def get_medications(self, patient_id: str) -> List[Dict]:
        """Get patient medications"""
        try:
            if not self.connected:
                # Demo medications
                return [
                    {
                        "id": "med_001",
                        "patient_id": patient_id,
                        "medication_name": "Metformin",
                        "dosage": "500mg",
                        "frequency": "Twice daily",
                        "instructions": "Take with meals",
                        "start_date": "2024-01-01",
                        "prescribing_doctor": "Dr. Smith"
                    },
                    {
                        "id": "med_002",
                        "patient_id": patient_id,
                        "medication_name": "Lisinopril",
                        "dosage": "10mg",
                        "frequency": "Once daily",
                        "instructions": "Take in the morning",
                        "start_date": "2024-01-15",
                        "prescribing_doctor": "Dr. Johnson"
                    }
                ]
            
            # Real Supabase query
            response = self.client.table("medications")\
                .select("*")\
                .eq("patient_id", patient_id)\
                .order("start_date", desc=True)\
                .execute()
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error getting medications: {e}")
            return []
    
    def save_appointment(self, appointment_data: Dict) -> bool:
        """Save appointment information"""
        try:
            if not self.connected:
                if "appointments" not in self.demo_data:
                    self.demo_data["appointments"] = []
                
                appointment_data["id"] = f"appt_{datetime.now().timestamp()}"
                appointment_data["created_at"] = datetime.now().isoformat()
                self.demo_data["appointments"].append(appointment_data)
                return True
            
            # Real Supabase insert
            response = self.client.table("appointments").insert(appointment_data).execute()
            return len(response.data) > 0
            
        except Exception as e:
            logger.error(f"Error saving appointment: {e}")
            return False
    
    def get_appointments(self, patient_id: str, upcoming: bool = True) -> List[Dict]:
        """Get patient appointments"""
        try:
            if not self.connected:
                # Demo appointments
                appointments = [
                    {
                        "id": "appt_001",
                        "patient_id": patient_id,
                        "doctor_name": "Dr. Smith",
                        "specialty": "Endocrinology",
                        "date": "2024-02-15T10:00:00",
                        "duration": "30 minutes",
                        "reason": "Diabetes follow-up",
                        "status": "scheduled",
                        "location": "Main Clinic, Room 302"
                    },
                    {
                        "id": "appt_002",
                        "patient_id": patient_id,
                        "doctor_name": "Dr. Johnson",
                        "specialty": "Cardiology",
                        "date": "2024-03-01T14:30:00",
                        "duration": "45 minutes",
                        "reason": "Cardiovascular risk assessment",
                        "status": "scheduled",
                        "location": "Heart Center, Room 105"
                    }
                ]
                
                if upcoming:
                    now = datetime.now()
                    appointments = [a for a in appointments if datetime.fromisoformat(a["date"]) > now]
                
                return appointments
            
            # Real Supabase query
            query = self.client.table("appointments")\
                .select("*")\
                .eq("patient_id", patient_id)
            
            if upcoming:
                now = datetime.now().isoformat()
                query = query.gte("date", now)
            
            response = query.order("date", asc=True).execute()
            return response.data
            
        except Exception as e:
            logger.error(f"Error getting appointments: {e}")
            return []
    
    def update_patient_profile(self, patient_id: str, profile_data: Dict) -> bool:
        """Update patient profile"""
        try:
            if not self.connected:
                # Update demo data
                if "patients" not in self.demo_data:
                    self.demo_data["patients"] = []
                
                # Find or create patient
                for i, patient in enumerate(self.demo_data["patients"]):
                    if patient.get("id") == patient_id:
                        self.demo_data["patients"][i].update(profile_data)
                        return True
                
                # Create new patient
                profile_data["id"] = patient_id
                profile_data["created_at"] = datetime.now().isoformat()
                self.demo_data["patients"].append(profile_data)
                return True
            
            # Real Supabase upsert
            profile_data["id"] = patient_id
            response = self.client.table("patients").upsert(profile_data).execute()
            return len(response.data) > 0
            
        except Exception as e:
            logger.error(f"Error updating patient profile: {e}")
            return False
    
    def get_patient_profile(self, patient_id: str) -> Dict:
        """Get patient profile"""
        try:
            if not self.connected:
                # Demo profile
                return {
                    "id": patient_id,
                    "name": "Demo Patient",
                    "email": "demo@mediclinic.com",
                    "date_of_birth": "1975-06-15",
                    "gender": "male",
                    "blood_type": "O+",
                    "height_cm": 175,
                    "weight_kg": 80,
                    "allergies": ["Penicillin"],
                    "chronic_conditions": ["Type 2 Diabetes", "Hypertension"],
                    "emergency_contact": {
                        "name": "Jane Doe",
                        "relationship": "Spouse",
                        "phone": "+1-555-0123"
                    },
                    "created_at": "2024-01-01T00:00:00"
                }
            
            # Real Supabase query
            response = self.client.table("patients")\
                .select("*")\
                .eq("id", patient_id)\
                .execute()
            
            return response.data[0] if response.data else {}
            
        except Exception as e:
            logger.error(f"Error getting patient profile: {e}")
            return {}
    
    def save_health_metrics(self, patient_id: str, metrics: Dict) -> bool:
        """Save health metrics (vital signs, etc.)"""
        try:
            metric_record = {
                "patient_id": patient_id,
                "metrics": metrics,
                "recorded_at": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            if not self.connected:
                # Store locally
                if "health_metrics" not in self.demo_data:
                    self.demo_data["health_metrics"] = []
                
                metric_record["id"] = f"metric_{datetime.now().timestamp()}"
                self.demo_data["health_metrics"].append(metric_record)
                return True
            
            # Real Supabase insert
            response = self.client.table("health_metrics").insert(metric_record).execute()
            return len(response.data) > 0
            
        except Exception as e:
            logger.error(f"Error saving health metrics: {e}")
            return False
    
    def get_health_metrics_history(self, patient_id: str, metric_type: str = None, limit: int = 50) -> List[Dict]:
        """Get history of health metrics"""
        try:
            if not self.connected:
                # Generate demo metrics
                history = []
                for i in range(10):
                    history.append({
                        "id": f"metric_00{i+1}",
                        "patient_id": patient_id,
                        "metrics": {
                            "heart_rate": 70 + i,
                            "blood_pressure": {"systolic": 120 + i, "diastolic": 80},
                            "temperature": 98.6,
                            "weight_kg": 80 - i*0.5
                        },
                        "recorded_at": f"2024-01-{10+i:02d}T08:00:00"
                    })
                return history
            
            # Real Supabase query
            query = self.client.table("health_metrics")\
                .select("*")\
                .eq("patient_id", patient_id)
            
            response = query.order("recorded_at", desc=True).limit(limit).execute()
            
            # Filter by metric type if specified
            if metric_type and response.data:
                filtered_data = []
                for record in response.data:
                    if metric_type in record.get("metrics", {}):
                        filtered_data.append(record)
                return filtered_data
            
            return response.data
            
        except Exception as e:
            logger.error(f"Error getting health metrics history: {e}")
            return []