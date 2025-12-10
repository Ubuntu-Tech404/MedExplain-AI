import React from 'react';
import { 
  Activity, 
  FileText, 
  Pill, 
  BarChart3,
  Brain,
  User
} from 'lucide-react';

interface MobileNavProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const MobileNav: React.FC<MobileNavProps> = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'overview', label: 'Home', icon: Activity },
    { id: 'explainer', label: 'AI', icon: Brain },
    { id: 'documents', label: 'Docs', icon: FileText },
    { id: 'analysis', label: 'Labs', icon: BarChart3 },
    { id: 'medications', label: 'Meds', icon: Pill },
    { id: 'profile', label: 'Me', icon: User },
  ];

  return (
    <nav className="mobile-nav">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex flex-col items-center p-2 rounded-xl transition-all ${
              activeTab === tab.id
                ? 'text-primary-600 bg-primary-50'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <Icon className="w-6 h-6" />
            <span className="text-xs mt-1 font-medium">{tab.label}</span>
          </button>
        );
      })}
    </nav>
  );
};

export default MobileNav;