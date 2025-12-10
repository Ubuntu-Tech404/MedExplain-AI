import React, { useState } from 'react';
import { 
  User, 
  Mail, 
  Phone, 
  Calendar, 
  MapPin, 
  Shield,
  Edit2,
  Save,
  Upload,
  Bell,
  Globe,
  Heart
} from 'lucide-react';
import Header from '../components/layout/Header';
import MobileNav from '../components/layout/MobileNav';
import { useAuth } from '../contexts/AuthContext';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [editing, setEditing] = useState(false);
  const [activeTab, setActiveTab] = useState('personal');
  const [profileData, setProfileData] = useState({
    name: user?.name || 'Dr. John Smith',
    email: user?.email || 'john.smith@mediclinic.ai',
    phone: '+1 (555) 123-4567',
    dob: '1975-03-15',
    address: '123 Medical Center Drive, Suite 400\nHealth City, HC 12345',
    bloodType: 'O+',
    allergies: ['Penicillin', 'Peanuts'],
    emergencyContact: {
      name: 'Sarah Smith',
      relationship: 'Spouse',
      phone: '+1 (555) 987-6543'
    }
  });

  const tabs = [
    { id: 'personal', label: 'Personal Info', icon: User },
    { id: 'medical', label: 'Medical Info', icon: Heart },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'security', label: 'Security', icon: Shield },
  ];

  const handleSave = () => {
    setEditing(false);
    // In production, save to API
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Handle image upload
      console.log('Uploading image:', file);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-16 md:pb-0">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Header */}
        <div className="mb-8">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <div className="flex flex-col md:flex-row md:items-center gap-6">
              {/* Profile Image */}
              <div className="relative">
                <div className="w-24 h-24 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl flex items-center justify-center">
                  <User className="w-12 h-12 text-white" />
                </div>
                <label className="absolute bottom-0 right-0 p-2 bg-white rounded-full shadow-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                  <Upload className="w-4 h-4 text-gray-600" />
                </label>
              </div>

              {/* Profile Info */}
              <div className="flex-1">
                <div className="flex items-start justify-between">
                  <div>
                    {editing ? (
                      <input
                        type="text"
                        value={profileData.name}
                        onChange={(e) => setProfileData(prev => ({ ...prev, name: e.target.value }))}
                        className="text-2xl font-bold text-gray-900 bg-gray-100 rounded-lg px-3 py-1"
                      />
                    ) : (
                      <h1 className="text-2xl font-bold text-gray-900">{profileData.name}</h1>
                    )}
                    <div className="flex items-center gap-2 mt-2">
                      <Mail className="w-4 h-4 text-gray-500" />
                      {editing ? (
                        <input
                          type="email"
                          value={profileData.email}
                          onChange={(e) => setProfileData(prev => ({ ...prev, email: e.target.value }))}
                          className="text-gray-600 bg-gray-100 rounded-lg px-2 py-1"
                        />
                      ) : (
                        <span className="text-gray-600">{profileData.email}</span>
                      )}
                    </div>
                    <div className="flex items-center gap-4 mt-4">
                      <div className="flex items-center gap-2">
                        <Phone className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-700">{profileData.phone}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-gray-500" />
                        <span className="text-gray-700">Physician</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {editing ? (
                      <button
                        onClick={handleSave}
                        className="btn-primary flex items-center gap-2"
                      >
                        <Save className="w-4 h-4" />
                        Save
                      </button>
                    ) : (
                      <button
                        onClick={() => setEditing(true)}
                        className="btn-secondary flex items-center gap-2"
                      >
                        <Edit2 className="w-4 h-4" />
                        Edit Profile
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="flex overflow-x-auto scrollbar-hide space-x-1 bg-white p-1.5 rounded-2xl shadow-sm border border-gray-100">
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
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {activeTab === 'personal' && (
              <div className="medical-card">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Personal Information</h2>
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Date of Birth
                      </label>
                      {editing ? (
                        <input
                          type="date"
                          value={profileData.dob}
                          onChange={(e) => setProfileData(prev => ({ ...prev, dob: e.target.value }))}
                          className="input-field"
                        />
                      ) : (
                        <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-xl">
                          <Calendar className="w-5 h-5 text-gray-500" />
                          <span>{profileData.dob}</span>
                        </div>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Blood Type
                      </label>
                      {editing ? (
                        <select
                          value={profileData.bloodType}
                          onChange={(e) => setProfileData(prev => ({ ...prev, bloodType: e.target.value }))}
                          className="input-field"
                        >
                          <option value="A+">A+</option>
                          <option value="A-">A-</option>
                          <option value="B+">B+</option>
                          <option value="B-">B-</option>
                          <option value="O+">O+</option>
                          <option value="O-">O-</option>
                          <option value="AB+">AB+</option>
                          <option value="AB-">AB-</option>
                        </select>
                      ) : (
                        <div className="p-3 bg-red-50 text-red-700 rounded-xl font-semibold text-center">
                          {profileData.bloodType}
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Address
                    </label>
                    {editing ? (
                      <textarea
                        value={profileData.address}
                        onChange={(e) => setProfileData(prev => ({ ...prev, address: e.target.value }))}
                        className="input-field h-32"
                        rows={4}
                      />
                    ) : (
                      <div className="flex items-start gap-2 p-3 bg-gray-50 rounded-xl">
                        <MapPin className="w-5 h-5 text-gray-500 mt-0.5" />
                        <span className="whitespace-pre-line">{profileData.address}</span>
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Allergies
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {profileData.allergies.map((allergy, index) => (
                        <span
                          key={index}
                          className="px-3 py-1.5 bg-red-100 text-red-800 rounded-full text-sm font-medium"
                        >
                          {allergy}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'medical' && (
              <div className="medical-card">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Medical Information</h2>
                <div className="space-y-6">
                  {/* Emergency Contact */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Emergency Contact</h3>
                    <div className="bg-blue-50 rounded-xl p-6 border border-blue-200">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div>
                          <div className="text-sm text-gray-500 mb-1">Name</div>
                          <div className="font-medium text-gray-900">{profileData.emergencyContact.name}</div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-500 mb-1">Relationship</div>
                          <div className="font-medium text-gray-900">{profileData.emergencyContact.relationship}</div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-500 mb-1">Phone</div>
                          <div className="font-medium text-gray-900">{profileData.emergencyContact.phone}</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Medical History */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Medical History</h3>
                    <div className="space-y-3">
                      {[
                        { condition: 'Type 2 Diabetes', diagnosed: '2018', status: 'Managed' },
                        { condition: 'Hypertension', diagnosed: '2020', status: 'Controlled' },
                        { condition: 'High Cholesterol', diagnosed: '2021', status: 'Improving' },
                      ].map((item, index) => (
                        <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                          <div>
                            <div className="font-medium text-gray-900">{item.condition}</div>
                            <div className="text-sm text-gray-500">Diagnosed: {item.diagnosed}</div>
                          </div>
                          <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                            {item.status}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="medical-card">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Profile Stats</h3>
              <div className="space-y-4">
                {[
                  { label: 'Account Created', value: '2 years ago', icon: Calendar },
                  { label: 'Last Login', value: 'Today', icon: User },
                  { label: 'Documents', value: '24 files', icon: FileText },
                  { label: 'Active Medications', value: '3', icon: Pill },
                ].map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-white rounded-lg">
                          <Icon className="w-5 h-5 text-gray-600" />
                        </div>
                        <span className="font-medium text-gray-700">{stat.label}</span>
                      </div>
                      <span className="text-gray-900">{stat.value}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Settings Card */}
            <div className="medical-card">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Settings</h3>
              <div className="space-y-3">
                <button className="w-full flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Bell className="w-5 h-5 text-gray-500" />
                    <span>Notifications</span>
                  </div>
                  <div className="w-10 h-6 bg-primary-500 rounded-full relative">
                    <div className="w-4 h-4 bg-white rounded-full absolute right-1 top-1"></div>
                  </div>
                </button>
                <button className="w-full flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Globe className="w-5 h-5 text-gray-500" />
                    <span>Language</span>
                  </div>
                  <span className="text-gray-500">English</span>
                </button>
                <button className="w-full flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Shield className="w-5 h-5 text-gray-500" />
                    <span>Privacy</span>
                  </div>
                  <span className="text-gray-500">›</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>

      <MobileNav activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
};

// Helper component
const Settings: React.FC = () => <div />;

export default Profile;