export interface MedicalExplanation {
  id: string;
  originalText: string;
  explanation: string;
  language: string;
  timestamp: string;
  confidence: string;
}

export interface Document {
  id: string;
  name: string;
  type: string;
  date: string;
  status: string;
  data?: any;
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

class LocalStorageService {
  private readonly KEYS = {
    EXPLANATIONS: 'mediclinic_explanations',
    DOCUMENTS: 'mediclinic_documents',
    LAB_RESULTS: 'mediclinic_lab_results',
    MEDICATIONS: 'mediclinic_medications',
    USER: 'mediclinic_user',
  };

  // Medical Explanations
  saveExplanation(explanation: MedicalExplanation): void {
    const explanations = this.getExplanations();
    explanations.unshift(explanation);
    localStorage.setItem(this.KEYS.EXPLANATIONS, JSON.stringify(explanations.slice(0, 50)));
  }

  getExplanations(): MedicalExplanation[] {
    const data = localStorage.getItem(this.KEYS.EXPLANATIONS);
    return data ? JSON.parse(data) : [];
  }

  // Documents
  saveDocument(document: Document): void {
    const documents = this.getDocuments();
    documents.unshift(document);
    localStorage.setItem(this.KEYS.DOCUMENTS, JSON.stringify(documents.slice(0, 100)));
  }

  getDocuments(): Document[] {
    const data = localStorage.getItem(this.KEYS.DOCUMENTS);
    return data ? JSON.parse(data) : [];
  }

  getRecentDocuments(limit: number = 5): Document[] {
    const documents = this.getDocuments();
    return documents.slice(0, limit);
  }

  // Lab Results
  saveLabResults(results: LabResult[]): void {
    localStorage.setItem(this.KEYS.LAB_RESULTS, JSON.stringify(results));
  }

  getLabResults(): LabResult[] {
    const data = localStorage.getItem(this.KEYS.LAB_RESULTS);
    if (data) return JSON.parse(data);

    // Generate demo data if none exists
    const demoData = this.generateDemoLabResults();
    this.saveLabResults(demoData);
    return demoData;
  }

  private generateDemoLabResults(): LabResult[] {
    const results: LabResult[] = [];
    const today = new Date();

    for (let i = 11; i >= 0; i--) {
      const date = new Date(today);
      date.setMonth(date.getMonth() - i);
      
      results.push({
        date: date.toISOString().split('T')[0],
        glucose: 85 + Math.random() * 40,
        hba1c: 5.0 + Math.random() * 2.5,
        cholesterol: 150 + Math.random() * 100,
        ldl: 70 + Math.random() * 80,
        hdl: 40 + Math.random() * 30,
        triglycerides: 100 + Math.random() * 150,
        creatinine: 0.8 + Math.random() * 0.4,
        bun: 10 + Math.random() * 10,
        sodium: 138 + Math.random() * 4,
        potassium: 4.0 + Math.random() * 0.8,
      });
    }

    return results;
  }

  // Medications
  saveMedication(medication: Medication): void {
    const medications = this.getMedications();
    const index = medications.findIndex(m => m.id === medication.id);
    
    if (index >= 0) {
      medications[index] = medication;
    } else {
      medications.push(medication);
    }
    
    localStorage.setItem(this.KEYS.MEDICATIONS, JSON.stringify(medications));
  }

  getMedications(): Medication[] {
    const data = localStorage.getItem(this.KEYS.MEDICATIONS);
    return data ? JSON.parse(data) : [];
  }

  deleteMedication(id: string): void {
    const medications = this.getMedications().filter(m => m.id !== id);
    localStorage.setItem(this.KEYS.MEDICATIONS, JSON.stringify(medications));
  }

  // User
  saveUser(user: any): void {
    localStorage.setItem(this.KEYS.USER, JSON.stringify(user));
  }

  getUser(): any {
    const data = localStorage.getItem(this.KEYS.USER);
    return data ? JSON.parse(data) : null;
  }

  logout(): void {
    localStorage.removeItem(this.KEYS.USER);
  }

  // Clear all (for testing)
  clearAll(): void {
    Object.values(this.KEYS).forEach(key => {
      localStorage.removeItem(key);
    });
  }
}

export default new LocalStorageService();