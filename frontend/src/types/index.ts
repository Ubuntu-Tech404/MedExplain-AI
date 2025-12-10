export interface User {
  id: string;
  email: string;
  name: string;
  token: string;
  role?: 'patient' | 'doctor' | 'admin';
}

export interface MedicalExplanation {
  id: string;
  originalText: string;
  explanation: string;
  language: string;
  timestamp: string;
  confidence: 'high' | 'medium' | 'low';
  sources?: string[];
}

export interface Document {
  id: string;
  name: string;
  type: 'lab_report' | 'doctor_note' | 'prescription' | 'medical_image' | 'other';
  size: number;
  status: 'uploading' | 'processing' | 'completed' | 'error';
  uploadedAt: string;
  previewUrl?: string;
  processedData?: any;
}

export interface LabResult {
  date: string;
  glucose: number;
  hba1c: number;
  cholesterol: number;
  ldl: number;
  hdl: number;
  triglycerides: number;
  creatinine?: number;
  bun?: number;
  sodium?: number;
  potassium?: number;
  [key: string]: any;
}

export interface Medication {
  id: string;
  name: string;
  dosage: string;
  frequency: string;
  timing: string[];
  purpose: string;
  instructions: string;
  sideEffects: string[];
  interactions: string[];
  startDate: string;
  endDate?: string;
  status: 'active' | 'completed' | 'missed';
  lastTaken?: string;
  nextDose?: string;
  aiExplanation?: string;
}

export interface Appointment {
  id: string;
  date: string;
  time: string;
  type: string;
  doctor: string;
  location: string;
  status: 'scheduled' | 'completed' | 'cancelled';
}

export interface HealthAlert {
  id: string;
  type: 'critical' | 'warning' | 'info';
  title: string;
  message: string;
  time: string;
  read: boolean;
}

export interface ChartData {
  date: string;
  value: number;
  referenceMin?: number;
  referenceMax?: number;
}