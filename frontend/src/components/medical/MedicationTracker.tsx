import React, { useState, useEffect } from "react";
import {
  Pill,
  Clock,
  Calendar,
  AlertTriangle,
  CheckCircle,
  Plus,
  Edit2,
  Trash2,
  Bell,
  Info,
  Search,
  Filter,
  Download, // FIXED: Added missing import
} from "lucide-react";
import ApiService from "../../services/api";
import LocalStorageService from "../../services/localStorage";
import toast from "react-hot-toast";
import MedicationModal from "./MedicationModal";

interface Medication {
  id: string;
  name: string;
  dosage: string;
  frequency: string;
  timing: string[];
  startDate: string;
  endDate?: string;
  purpose: string;
  instructions: string;
  sideEffects: string[];
  interactions: string[];
  status: "active" | "completed" | "missed";
  lastTaken?: string;
  nextDose?: string;
  aiExplanation?: string;
}

const MedicationTracker: React.FC = () => {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [selectedMed, setSelectedMed] = useState<Medication | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMedications();
  }, []);

  const loadMedications = () => {
    const meds = LocalStorageService.getMedications();
    // Add demo data if none
    if (meds.length === 0) {
      const demoMeds = generateDemoMedications();
      setMedications(demoMeds);
      demoMeds.forEach((med) => LocalStorageService.saveMedication(med));
    } else {
      setMedications(meds);
    }
  };

  const generateDemoMedications = (): Medication[] => {
    return [
      {
        id: "1",
        name: "Metformin",
        dosage: "500mg",
        frequency: "Twice daily",
        timing: ["08:00", "20:00"],
        startDate: "2024-01-15",
        purpose: "Type 2 Diabetes",
        instructions: "Take with meals",
        sideEffects: ["Nausea", "Diarrhea", "Stomach pain"],
        interactions: ["Alcohol", "Contrast dye"],
        status: "active",
        lastTaken: new Date().toISOString(),
        nextDose: new Date(Date.now() + 12 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: "2",
        name: "Lisinopril",
        dosage: "10mg",
        frequency: "Once daily",
        timing: ["08:00"],
        startDate: "2024-02-20",
        purpose: "Hypertension",
        instructions: "Take in the morning",
        sideEffects: ["Cough", "Dizziness", "Headache"],
        interactions: ["Diuretics", "NSAIDs"],
        status: "active",
        lastTaken: new Date().toISOString(),
        nextDose: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: "3",
        name: "Atorvastatin",
        dosage: "20mg",
        frequency: "Once daily",
        timing: ["20:00"],
        startDate: "2024-03-10",
        purpose: "High Cholesterol",
        instructions: "Take at bedtime",
        sideEffects: ["Muscle pain", "Liver problems"],
        interactions: ["Grapefruit juice", "Other statins"],
        status: "active",
        lastTaken: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        nextDose: new Date().toISOString(),
      },
    ];
  };

  const handleExplainMedication = async (medication: Medication) => {
    setLoading(true);
    try {
      const explanation = await ApiService.explainMedication(medication.name);

      // Update medication with AI explanation
      const updatedMeds = medications.map((med) =>
        med.id === medication.id
          ? { ...med, aiExplanation: explanation.explanation }
          : med
      );

      setMedications(updatedMeds);
      setSelectedMed({ ...medication, aiExplanation: explanation.explanation });
      toast.success("AI explanation generated!");
    } catch (error) {
      toast.error("Failed to generate explanation");
    } finally {
      setLoading(false);
    }
  };

  const handleMarkTaken = (medicationId: string) => {
    const updatedMeds = medications.map((med) => {
      if (med.id === medicationId) {
        const now = new Date();
        const nextDose = new Date(
          now.getTime() + getNextDoseInterval(med.frequency)
        );

        return {
          ...med,
          lastTaken: now.toISOString(),
          nextDose: nextDose.toISOString(),
          status: "active" as const,
        };
      }
      return med;
    });

    setMedications(updatedMeds);
    toast.success("Medication marked as taken");
  };

  const getNextDoseInterval = (frequency: string): number => {
    const intervals: Record<string, number> = {
      "Once daily": 24 * 60 * 60 * 1000,
      "Twice daily": 12 * 60 * 60 * 1000,
      "Three times daily": 8 * 60 * 60 * 1000,
      "Four times daily": 6 * 60 * 60 * 1000,
      Weekly: 7 * 24 * 60 * 60 * 1000,
    };
    return intervals[frequency] || 24 * 60 * 60 * 1000;
  };

  const filteredMeds = medications.filter((med) => {
    const matchesSearch =
      med.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      med.purpose.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === "all" || med.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const upcomingMeds = medications.filter((med) => {
    if (!med.nextDose) return false;
    const nextDose = new Date(med.nextDose);
    const now = new Date();
    const oneHourFromNow = new Date(now.getTime() + 60 * 60 * 1000);
    return nextDose <= oneHourFromNow && med.status === "active";
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-100 text-green-800";
      case "missed":
        return "bg-red-100 text-red-800";
      case "completed":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case "missed":
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case "completed":
        return <CheckCircle className="w-4 h-4 text-blue-500" />;
      default:
        return null;
    }
  };

  const formatTime = (dateString?: string) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="medical-card">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-700 rounded-xl flex items-center justify-center">
                <Pill className="w-6 h-6 text-white" />
              </div>
              <span>Medication Tracker</span>
            </h1>
            <p className="text-gray-600 mt-2">
              Manage your medications with AI-powered explanations and reminders
            </p>
          </div>

          <button
            onClick={() => setShowModal(true)}
            className="btn-primary flex items-center gap-2">
            <Plus className="w-5 h-5" />
            Add Medication
          </button>
        </div>
      </div>

      {/* Upcoming Medications Alert */}
      {upcomingMeds.length > 0 && (
        <div className="medical-card bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <Bell className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">
                  Upcoming Medications
                </h3>
                <p className="text-sm text-gray-600">
                  {upcomingMeds.length} medication
                  {upcomingMeds.length !== 1 ? "s" : ""} due soon
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {upcomingMeds.map((med) => (
                <div
                  key={med.id}
                  className="px-3 py-1 bg-white rounded-lg border border-orange-200">
                  <div className="text-sm font-medium">{med.name}</div>
                  <div className="text-xs text-gray-500">
                    {formatTime(med.nextDose)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Search and Filter */}
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
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="input-field py-2">
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="missed">Missed</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Medications List */}
        <div className="lg:col-span-2">
          <div className="medical-card">
            <h2 className="text-xl font-bold text-gray-900 mb-6">
              Your Medications
            </h2>

            <div className="space-y-4">
              {filteredMeds.length > 0 ? (
                filteredMeds.map((medication) => (
                  <div
                    key={medication.id}
                    className={`p-4 rounded-xl border ${
                      medication.status === "missed"
                        ? "border-red-200 bg-red-50"
                        : medication.status === "completed"
                        ? "border-blue-200 bg-blue-50"
                        : "border-gray-200 bg-gray-50"
                    }`}>
                    <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                      {/* Medication Info */}
                      <div className="flex-1">
                        <div className="flex items-start justify-between">
                          <div>
                            <h3 className="font-bold text-lg text-gray-900 flex items-center gap-2">
                              {medication.name}
                              <span
                                className={`badge ${getStatusColor(
                                  medication.status
                                )}`}>
                                {getStatusIcon(medication.status)}
                                <span className="ml-1">
                                  {medication.status}
                                </span>
                              </span>
                            </h3>
                            <p className="text-gray-600 mt-1">
                              {medication.purpose}
                            </p>
                          </div>

                          <div className="text-right">
                            <div className="text-2xl font-bold text-gray-900">
                              {medication.dosage}
                            </div>
                            <div className="text-sm text-gray-500">
                              {medication.frequency}
                            </div>
                          </div>
                        </div>

                        {/* Timing */}
                        <div className="flex items-center gap-4 mt-4">
                          <div className="flex items-center gap-2">
                            <Clock className="w-4 h-4 text-gray-500" />
                            <span className="text-sm text-gray-700">
                              Times: {medication.timing.join(", ")}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Calendar className="w-4 h-4 text-gray-500" />
                            <span className="text-sm text-gray-700">
                              Started:{" "}
                              {new Date(
                                medication.startDate
                              ).toLocaleDateString()}
                            </span>
                          </div>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-3 mt-4">
                          <button
                            onClick={() => handleMarkTaken(medication.id)}
                            className="btn-secondary text-sm px-3 py-1.5"
                            disabled={medication.status === "completed"}>
                            Mark as Taken
                          </button>

                          <button
                            onClick={() => handleExplainMedication(medication)}
                            disabled={loading}
                            className="btn-primary text-sm px-3 py-1.5 flex items-center gap-1">
                            {loading && medication.id === selectedMed?.id ? (
                              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            ) : (
                              <Info className="w-4 h-4" />
                            )}
                            Explain with AI
                          </button>

                          <button
                            onClick={() => {
                              setSelectedMed(medication);
                              setShowModal(true);
                            }}
                            className="p-1.5 text-gray-600 hover:text-gray-900">
                            <Edit2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Side Effects & Interactions */}
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <div className="flex flex-wrap gap-2">
                        {medication.sideEffects
                          .slice(0, 3)
                          .map((effect, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
                              {effect}
                            </span>
                          ))}
                        {medication.interactions
                          .slice(0, 2)
                          .map((interaction, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                              Avoid: {interaction}
                            </span>
                          ))}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <Pill className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                  <p>No medications found</p>
                  <p className="text-sm mt-1">Add medications to get started</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Stats */}
          <div className="medical-card">
            <h3 className="text-lg font-bold text-gray-900 mb-4">
              Medication Stats
            </h3>
            <div className="space-y-4">
              {[
                {
                  label: "Total Medications",
                  value: medications.length,
                  color: "text-purple-600",
                },
                {
                  label: "Active",
                  value: medications.filter((m) => m.status === "active")
                    .length,
                  color: "text-green-600",
                },
                {
                  label: "Taken Today",
                  value: medications.filter((m) => {
                    const today = new Date().toDateString();
                    return (
                      m.lastTaken &&
                      new Date(m.lastTaken).toDateString() === today
                    );
                  }).length,
                  color: "text-blue-600",
                },
                {
                  label: "Due Soon",
                  value: upcomingMeds.length,
                  color: "text-orange-600",
                },
              ].map((stat, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                  <span className="font-medium text-gray-700">
                    {stat.label}
                  </span>
                  <span className={`text-2xl font-bold ${stat.color}`}>
                    {stat.value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* AI Explanation */}
          {selectedMed?.aiExplanation && (
            <div className="medical-card bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200">
              <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
                <Info className="w-5 h-5 text-blue-600" />
                AI Explanation
              </h3>
              <div className="text-sm text-gray-700 leading-relaxed">
                {selectedMed.aiExplanation.slice(0, 200)}...
                <button className="text-primary-600 hover:text-primary-700 text-sm font-medium mt-2 block">
                  Read full explanation
                </button>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="medical-card">
            <h3 className="text-lg font-bold text-gray-900 mb-4">
              Quick Actions
            </h3>
            <div className="space-y-3">
              <button className="w-full btn-secondary flex items-center justify-center gap-2">
                <Calendar className="w-4 h-4" />
                View Schedule
              </button>
              <button className="w-full btn-primary flex items-center justify-center gap-2">
                <Bell className="w-4 h-4" />
                Set Reminders
              </button>
              <button className="w-full flex items-center justify-center gap-2 px-4 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-xl border border-gray-300 transition-colors">
                <Download className="w-4 h-4" />{" "}
                {/* FIXED: Now Download is imported */}
                Export List
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Medication Schedule */}
      <div className="medical-card">
        <h2 className="text-xl font-bold text-gray-900 mb-6">
          Today's Schedule
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            "Morning (6AM-12PM)",
            "Afternoon (12PM-6PM)",
            "Evening (6PM-12AM)",
          ].map((timeSlot, index) => {
            const slotMeds = medications.filter((med) => {
              if (med.status !== "active") return false;
              const hour = new Date().getHours();
              return (
                (index === 0 && hour >= 6 && hour < 12) ||
                (index === 1 && hour >= 12 && hour < 18) ||
                (index === 2 && hour >= 18)
              );
            });

            return (
              <div
                key={index}
                className="p-4 bg-gray-50 rounded-xl border border-gray-200">
                <h3 className="font-bold text-gray-900 mb-3">{timeSlot}</h3>
                <div className="space-y-3">
                  {slotMeds.length > 0 ? (
                    slotMeds.map((med) => (
                      <div
                        key={med.id}
                        className="flex items-center gap-3 p-3 bg-white rounded-lg">
                        <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                          <Pill className="w-4 h-4 text-purple-600" />
                        </div>
                        <div className="flex-1">
                          <div className="font-medium text-gray-900">
                            {med.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {med.dosage}
                          </div>
                        </div>
                        <button
                          onClick={() => handleMarkTaken(med.id)}
                          className="px-3 py-1 bg-green-100 text-green-700 text-sm rounded-lg hover:bg-green-200">
                          Taken
                        </button>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-4 text-gray-500 text-sm">
                      No medications scheduled
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <MedicationModal
          medication={selectedMed}
          onClose={() => {
            setShowModal(false);
            setSelectedMed(null);
          }}
          onSave={(medication) => {
            if (selectedMed) {
              // Update existing
              setMedications((prev) =>
                prev.map((m) => (m.id === medication.id ? medication : m))
              );
            } else {
              // Add new
              const newMed = { ...medication, id: Date.now().toString() };
              setMedications((prev) => [newMed, ...prev]);
            }
            setShowModal(false);
            setSelectedMed(null);
            toast.success("Medication saved!");
          }}
          onDelete={() => {
            if (selectedMed) {
              setMedications((prev) =>
                prev.filter((m) => m.id !== selectedMed.id)
              );
              setShowModal(false);
              setSelectedMed(null);
              toast.success("Medication deleted!");
            }
          }}
        />
      )}
    </div>
  );
};

export default MedicationTracker;
