import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

class ApiService {
  async checkHealth() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/health`);
      return response.data;
    } catch (error) {
      return { status: 'unavailable' };
    }
  }

  async explainMedicalText(text: string, language: string = 'english') {
    const formData = new FormData();
    formData.append('text', text);
    formData.append('language', language);
    
    const response = await axios.post(`${API_BASE_URL}/api/explain`, formData);
    return response.data;
  }

  async explainDiagnosis(diagnosis: string, notes: string = '') {
    const formData = new FormData();
    formData.append('diagnosis', diagnosis);
    formData.append('notes', notes);
    
    const response = await axios.post(`${API_BASE_URL}/api/explain-diagnosis`, formData);
    return response.data;
  }

  async analyzeLabResults(labData: any) {
    const response = await axios.post(`${API_BASE_URL}/api/analyze-lab`, labData);
    return response.data;
  }

  async explainMedication(medication: string) {
    const formData = new FormData();
    formData.append('medication', medication);
    
    const response = await axios.post(`${API_BASE_URL}/api/explain-medication`, formData);
    return response.data;
  }

  async uploadDocument(formData: FormData) {
    const response = await axios.post(`${API_BASE_URL}/api/upload-document`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getPatientSummary(patientId: string = 'demo-patient') {
    const response = await axios.get(`${API_BASE_URL}/api/patient/${patientId}/summary`);
    return response.data;
  }

  async getDocuments(patientId: string = 'demo-patient') {
    const response = await axios.get(`${API_BASE_URL}/api/documents/${patientId}`);
    return response.data;
  }

  async generateChart(chartData: any) {
    const response = await axios.post(`${API_BASE_URL}/api/generate-chart`, chartData);
    return response.data;
  }

  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    
    const response = await axios.post(`${API_BASE_URL}/api/auth/login`, formData);
    return response.data;
  }
}

export default new ApiService();