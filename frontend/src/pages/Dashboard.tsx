import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  FileText, 
  Pill, 
  BarChart3, 
  AlertCircle,
  Upload,
  Brain,
  TrendingUp,
  Clock,
  User,
  Bell,
  Search
} from 'lucide-react';
import Header from '../components/layout/Header';
import MobileNav from '../components/layout/MobileNav';
import MedicalExplainer from '../components/medical/MedicalExplainer';
import DocumentUpload from '../components/medical/DocumentUpload';
import LabResults from '../components/medical/LabResults';
import MedicationTracker from '../components/medical/MedicationTracker';
import DiagnosisCard from '../components/medical/DiagnosisCard';
import ApiService from '../services/api';
import LocalStorageService from '../services/localStorage';
import toast from 'react-hot-toast';

const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [healthSummary, setHealthSummary] = useState<any>(null);
  const [recentDocuments, setRecentDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const summary = await ApiService.getPatientSummary();
      setHealthSummary(summary);
      
      const docs = LocalStorageService.getRecentDocuments();
      setRecentDocuments(docs);
    } catch (error) {
      toast.error('Error loading dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const quickStats = [
    { 
      icon: Activity, 
      label: 'Health Score', 
      value: '85/100', 
      change: '+2%', 
      color: 'text-primary-600',
      bgColor: 'bg-primary-50'
    },
    { 
      icon: FileText, 
      label: 'Documents', 
      value: '24', 
      change: '+3', 
      color: 'text-medical-teal',
      bgColor: 'bg-teal-50'
    },
    { 
      icon: Pill, 
      label: 'Medications', 
      value: '5', 
      change: '-1', 
      color: 'text-medical-purple',
      bgColor: 'bg-purple-50'
    },
    { 
      icon: BarChart3, 
      label: 'Tests This Month', 
      value: '3', 
      change: '+1', 
      color: 'text-medical-orange',
      bgColor: 'bg-orange-50'
    },
  ];

  const alerts = [
    { id: 1, type: 'critical', title: 'High Blood Pressure', time: '2 hours ago', icon: AlertCircle },
    { id: 2, type: 'warning', title: 'Medication Due', time: '4 hours ago', icon: Pill },
    { id: 3, type: 'info', title: 'Lab Results Ready', time: '1 day ago', icon: FileText },
  ];

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'explainer', label: 'AI Explainer', icon: Brain },
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'analysis', label: 'Analysis', icon: BarChart3 },
    { id: 'medications', label: 'Medications', icon: Pill },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-16 md:pb-0">
      {/* Header */}
      <Header />
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Welcome Banner */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-6 text-white shadow-lg">
            <div className="flex flex-col md:flex-row md:items-center justify-between">
              <div>
                <h1 className="text-2xl md:text-3xl font-bold mb-2">Welcome back, John!</h1>
                <p className="text-primary-100 opacity-90">
                  Your health dashboard is updated with latest reports and insights
                </p>
              </div>
              <div className="mt-4 md:mt-0">
                <div className="flex items-center gap-4">
                  <div className="text-center">
                    <div className="text-sm text-primary-200">Last Checkup</div>
                    <div className="text-lg font-semibold">Nov 15, 2024</div>
                  </div>
                  <div className="h-12 w-px bg-primary-400"></div>
                  <div className="text-center">
                    <div className="text-sm text-primary-200">Next Appointment</div>
                    <div className="text-lg font-semibold">Dec 20, 2024</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Mobile Navigation Tabs */}
        <div className="md:hidden mb-6">
          <div className="flex overflow-x-auto scrollbar-hide space-x-2 pb-2">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-shrink-0 flex items-center gap-2 px-4 py-2.5 rounded-xl transition-all ${
                    activeTab === tab.id
                      ? 'bg-primary-600 text-white shadow-md'
                      : 'bg-white text-gray-600 border border-gray-200'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Desktop Navigation */}
        <div className="hidden md:block mb-8">
          <div className="flex space-x-1 bg-white p-1.5 rounded-2xl shadow-sm border border-gray-100">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-xl transition-all ${
                    activeTab === tab.id
                      ? 'bg-primary-50 text-primary-700 border border-primary-200'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <>
              {/* Quick Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {quickStats.map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <div key={index} className="medical-card">
                      <div className="flex items-start justify-between">
                        <div className={`p-2.5 rounded-lg ${stat.bgColor}`}>
                          <Icon className={`w-6 h-6 ${stat.color}`} />
                        </div>
                        <span className={`text-sm font-medium ${stat.value.includes('+') ? 'text-green-600' : 'text-red-600'}`}>
                          {stat.change}
                        </span>
                      </div>
                      <div className="mt-4">
                        <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                        <div className="text-sm text-gray-500 mt-1">{stat.label}</div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Health Alerts */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="medical-card">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                      <AlertCircle className="w-5 h-5 text-medical-orange" />
                      Health Alerts
                    </h2>
                    <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                      View All
                    </button>
                  </div>
                  
                  <div className="space-y-3">
                    {alerts.map((alert) => {
                      const Icon = alert.icon;
                      return (
                        <div key={alert.id} className={`p-4 rounded-xl border ${
                          alert.type === 'critical' ? 'border-medical-red/20 bg-red-50' :
                          alert.type === 'warning' ? 'border-medical-orange/20 bg-orange-50' :
                          'border-primary-200 bg-primary-50'
                        }`}>
                          <div className="flex items-center gap-3">
                            <div className={`p-2 rounded-lg ${
                              alert.type === 'critical' ? 'bg-red-100 text-red-600' :
                              alert.type === 'warning' ? 'bg-orange-100 text-orange-600' :
                              'bg-primary-100 text-primary-600'
                            }`}>
                              <Icon className="w-4 h-4" />
                            </div>
                            <div className="flex-1">
                              <div className="font-medium text-gray-900">{alert.title}</div>
                              <div className="text-sm text-gray-500 mt-1">{alert.time}</div>
                            </div>
                            <button className="text-gray-400 hover:text-gray-600">
                              <Clock className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Recent Documents */}
                <div className="medical-card">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                      <FileText className="w-5 h-5 text-medical-teal" />
                      Recent Documents
                    </h2>
                    <button className="btn-primary flex items-center gap-2">
                      <Upload className="w-4 h-4" />
                      Upload
                    </button>
                  </div>
                  
                  <div className="space-y-3">
                    {recentDocuments.slice(0, 4).map((doc) => (
                      <div key={doc.id} className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-xl transition-colors">
                        <div className="p-2.5 bg-primary-50 rounded-lg">
                          <FileText className="w-5 h-5 text-primary-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-gray-900 truncate">{doc.name}</div>
                          <div className="text-sm text-gray-500 flex items-center gap-2">
                            <span>{doc.type}</span>
                            <span>•</span>
                            <span>{doc.date}</span>
                          </div>
                        </div>
                        <span className={`badge ${
                          doc.status === 'processed' ? 'badge-success' :
                          doc.status === 'pending' ? 'badge-warning' :
                          'badge-info'
                        }`}>
                          {doc.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* AI Quick Explainer */}
              <MedicalExplainer compact={true} />
            </>
          )}

          {/* AI Explainer Tab */}
          {activeTab === 'explainer' && (
            <MedicalExplainer compact={false} />
          )}

          {/* Documents Tab */}
          {activeTab === 'documents' && (
            <DocumentUpload />
          )}

          {/* Analysis Tab */}
          {activeTab === 'analysis' && (
            <LabResults />
          )}

          {/* Medications Tab */}
          {activeTab === 'medications' && (
            <MedicationTracker />
          )}
        </div>
      </main>

      {/* Mobile Bottom Navigation */}
      <MobileNav activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
};

export default Dashboard;