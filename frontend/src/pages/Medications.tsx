import React, { useState } from "react";
import {
  Pill,
  Clock,
  Calendar,
  AlertTriangle,
  CheckCircle,
  Plus,
  Search,
  Filter,
  Bell,
  Download,
  History,
} from "lucide-react";
import Header from "../components/layout/Header";
import MobileNav from "../components/layout/MobileNav";
import MedicationTracker from "../components/medical/MedicationTracker";

const Medications: React.FC = () => {
  const [activeTab, setActiveTab] = useState("current");
  const [searchTerm, setSearchTerm] = useState("");

  const tabs = [
    { id: "current", label: "Current Medications", icon: Pill },
    { id: "schedule", label: "Schedule", icon: Clock },
    { id: "history", label: "History", icon: History },
    { id: "interactions", label: "Interactions", icon: AlertTriangle },
  ];

  const upcomingMedications = [
    {
      id: 1,
      name: "Metformin",
      time: "8:00 AM",
      status: "due",
      dosage: "500mg",
    },
    {
      id: 2,
      name: "Lisinopril",
      time: "8:00 AM",
      status: "taken",
      dosage: "10mg",
    },
    {
      id: 3,
      name: "Atorvastatin",
      time: "8:00 PM",
      status: "upcoming",
      dosage: "20mg",
    },
  ];

  const medicationStats = [
    { label: "Active Medications", value: 3, color: "text-green-600" },
    { label: "Taken Today", value: 2, color: "text-blue-600" },
    { label: "Due Soon", value: 1, color: "text-orange-600" },
    { label: "Missed This Week", value: 0, color: "text-red-600" },
  ];

  const handleSetReminder = () => {
    alert("Setting medication reminders...");
  };

  const handleRefillRequest = () => {
    alert("Requesting medication refill...");
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-16 md:pb-0">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-6 text-white shadow-lg">
            <div className="flex flex-col md:flex-row md:items-center justify-between">
              <div>
                <h1 className="text-2xl md:text-3xl font-bold mb-2">
                  Medication Management
                </h1>
                <p className="text-purple-100 opacity-90">
                  Track, manage, and understand your medications with AI
                  assistance
                </p>
              </div>
              <div className="mt-4 md:mt-0 flex items-center gap-3">
                <button
                  onClick={handleSetReminder}
                  className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-xl font-medium flex items-center gap-2">
                  <Bell className="w-5 h-5" />
                  Set Reminders
                </button>
                <button className="bg-white text-purple-600 hover:bg-purple-50 px-4 py-2 rounded-xl font-semibold flex items-center gap-2">
                  <Plus className="w-5 h-5" />
                  Add Medication
                </button>
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
                      ? "bg-purple-50 text-purple-700 border border-purple-200"
                      : "text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                  }`}>
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Search and Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <div className="medical-card">
              <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search medications..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="input-field pl-10"
                    />
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-2">
                    <Filter className="w-5 h-5 text-gray-500" />
                    <select className="input-field py-2">
                      <option>All Status</option>
                      <option>Active</option>
                      <option>Completed</option>
                      <option>Missed</option>
                    </select>
                  </div>
                  <button className="btn-primary flex items-center gap-2">
                    <Download className="w-4 h-4" />
                    Export List
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {medicationStats.map((stat, index) => (
              <div key={index} className="medical-card">
                <div className="text-2xl font-bold text-gray-900">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-500">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            {activeTab === "current" && <MedicationTracker />}

            {activeTab === "schedule" && (
              <div className="medical-card">
                <h2 className="text-xl font-bold text-gray-900 mb-6">
                  Medication Schedule
                </h2>
                <div className="space-y-4">
                  {upcomingMedications.map((med) => (
                    <div
                      key={med.id}
                      className={`p-4 rounded-xl border ${
                        med.status === "due"
                          ? "border-yellow-200 bg-yellow-50"
                          : med.status === "taken"
                          ? "border-green-200 bg-green-50"
                          : "border-blue-200 bg-blue-50"
                      }`}>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div
                            className={`p-3 rounded-lg ${
                              med.status === "due"
                                ? "bg-yellow-100 text-yellow-600"
                                : med.status === "taken"
                                ? "bg-green-100 text-green-600"
                                : "bg-blue-100 text-blue-600"
                            }`}>
                            <Pill className="w-6 h-6" />
                          </div>
                          <div>
                            <h3 className="font-bold text-gray-900">
                              {med.name}
                            </h3>
                            <p className="text-gray-600">{med.dosage}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-semibold text-gray-900">
                            {med.time}
                          </div>
                          <span
                            className={`text-sm px-2 py-1 rounded-full ${
                              med.status === "due"
                                ? "bg-yellow-100 text-yellow-800"
                                : med.status === "taken"
                                ? "bg-green-100 text-green-800"
                                : "bg-blue-100 text-blue-800"
                            }`}>
                            {med.status}
                          </span>
                        </div>
                      </div>
                      {med.status === "due" && (
                        <div className="mt-4 pt-4 border-t border-yellow-200">
                          <button className="w-full btn-primary py-2">
                            Mark as Taken
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Upcoming Medications */}
            <div className="medical-card">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Clock className="w-5 h-5 text-orange-500" />
                Today's Schedule
              </h3>
              <div className="space-y-3">
                {[
                  { time: "8:00 AM", meds: ["Metformin", "Lisinopril"] },
                  { time: "2:00 PM", meds: [] },
                  { time: "8:00 PM", meds: ["Atorvastatin"] },
                ].map((slot, index) => (
                  <div key={index} className="p-3 bg-gray-50 rounded-xl">
                    <div className="font-medium text-gray-900 mb-2">
                      {slot.time}
                    </div>
                    {slot.meds.length > 0 ? (
                      <div className="space-y-1">
                        {slot.meds.map((med, idx) => (
                          <div
                            key={idx}
                            className="flex items-center gap-2 text-sm">
                            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span className="text-gray-700">{med}</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-sm text-gray-500">
                        No medications
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="medical-card">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button className="w-full btn-secondary flex items-center justify-center gap-2">
                  <Bell className="w-4 h-4" />
                  Set Reminder
                </button>
                <button
                  onClick={handleRefillRequest}
                  className="w-full btn-primary flex items-center justify-center gap-2">
                  <Pill className="w-4 h-4" />
                  Request Refill
                </button>
                <button className="w-full flex items-center justify-center gap-2 px-4 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl border border-gray-300 transition-colors">
                  <Calendar className="w-4 h-4" />
                  View Calendar
                </button>
              </div>
            </div>

            {/* Medication Tips */}
            <div className="medical-card bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200">
              <h3 className="text-lg font-bold text-gray-900 mb-3">
                💡 Medication Tips
              </h3>
              <ul className="space-y-2 text-sm text-gray-700">
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                  <span>Take medications at the same time daily</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                  <span>Never skip doses without consulting your doctor</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                  <span>Report any side effects immediately</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                  <span>Keep medications in original containers</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      <MobileNav activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
};

export default Medications;
