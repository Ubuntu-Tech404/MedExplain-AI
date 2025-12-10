import React, { useState, useEffect } from "react";
import {
  FileText,
  Filter,
  Search,
  Download,
  Eye,
  Trash2,
  Upload,
  Folder,
  Calendar,
  User,
  MoreVertical,
} from "lucide-react";
import Header from "../components/layout/Header";
import MobileNav from "../components/layout/MobileNav";
import DocumentUpload from "../components/medical/DocumentUpload";
import ApiService from "../services/api";
import LocalStorageService from "../services/localStorage";
import toast from "react-hot-toast";

interface DocumentItem {
  id: string;
  name: string;
  type: "lab_report" | "doctor_note" | "prescription" | "image" | "other";
  size: number;
  uploadedAt: string;
  patientName: string;
  status: "processed" | "pending" | "error";
  previewUrl?: string;
}

const Documents: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState<string>("all");
  const [loading, setLoading] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<DocumentItem | null>(null);
  const [activeTab, setActiveTab] = useState("documents");

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setLoading(true);
    try {
      // Load from local storage first
      const localDocs = LocalStorageService.getDocuments();

      // If no local docs, generate demo data
      if (localDocs.length === 0) {
        const demoDocs = generateDemoDocuments();
        setDocuments(demoDocs);
      } else {
        const formattedDocs = localDocs.map((doc) => ({
          id: doc.id,
          name: doc.name,
          type: doc.type as any,
          size: 1024 * 1024, // 1MB default
          uploadedAt: doc.date,
          patientName: "John Smith",
          status: doc.status as any,
        }));
        setDocuments(formattedDocs);
      }
    } catch (error) {
      toast.error("Error loading documents");
    } finally {
      setLoading(false);
    }
  };

  const generateDemoDocuments = (): DocumentItem[] => {
    return [
      {
        id: "1",
        name: "Blood_Work_Report_Nov_2024.pdf",
        type: "lab_report",
        size: 2.4 * 1024 * 1024, // 2.4MB
        uploadedAt: "2024-11-15",
        patientName: "John Smith",
        status: "processed",
      },
      {
        id: "2",
        name: "Doctor_Notes_Diabetes.pdf",
        type: "doctor_note",
        size: 1.8 * 1024 * 1024,
        uploadedAt: "2024-11-10",
        patientName: "John Smith",
        status: "processed",
      },
      {
        id: "3",
        name: "Prescription_Metformin.pdf",
        type: "prescription",
        size: 0.8 * 1024 * 1024,
        uploadedAt: "2024-11-05",
        patientName: "John Smith",
        status: "processed",
      },
      {
        id: "4",
        name: "ECG_Results_Image.jpg",
        type: "image",
        size: 3.2 * 1024 * 1024,
        uploadedAt: "2024-10-28",
        patientName: "John Smith",
        status: "processed",
      },
      {
        id: "5",
        name: "Insurance_Claim_Form.pdf",
        type: "other",
        size: 1.5 * 1024 * 1024,
        uploadedAt: "2024-10-20",
        patientName: "John Smith",
        status: "pending",
      },
    ];
  };

  const documentTypes = [
    { id: "all", label: "All Documents", icon: Folder, color: "text-gray-600" },
    {
      id: "lab_report",
      label: "Lab Reports",
      icon: FileText,
      color: "text-blue-600",
    },
    {
      id: "doctor_note",
      label: "Doctor's Notes",
      icon: FileText,
      color: "text-green-600",
    },
    {
      id: "prescription",
      label: "Prescriptions",
      icon: FileText,
      color: "text-purple-600",
    },
    {
      id: "image",
      label: "Medical Images",
      icon: FileText,
      color: "text-orange-600",
    },
    { id: "other", label: "Other", icon: Folder, color: "text-gray-600" },
  ];

  const filteredDocs = documents.filter((doc) => {
    const matchesSearch =
      doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doc.patientName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === "all" || doc.type === filterType;
    return matchesSearch && matchesFilter;
  });

  const handlePreview = (doc: DocumentItem) => {
    toast.success(`Previewing ${doc.name}`);
    // In production, open PDF viewer
  };

  const handleDownload = (doc: DocumentItem) => {
    toast.success(`Downloading ${doc.name}`);
    // In production, download file
  };

  const handleDelete = (docId: string) => {
    setDocuments((prev) => prev.filter((d) => d.id !== docId));
    toast.success("Document deleted");
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const getTypeColor = (type: string) => {
    const typeConfig = documentTypes.find((t) => t.id === type);
    return typeConfig?.color || "text-gray-600";
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "processed":
        return "bg-green-100 text-green-800";
      case "pending":
        return "bg-yellow-100 text-yellow-800";
      case "error":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-16 md:pb-0">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-blue-600 to-teal-600 rounded-2xl p-6 text-white shadow-lg">
            <div className="flex flex-col md:flex-row md:items-center justify-between">
              <div>
                <h1 className="text-2xl md:text-3xl font-bold mb-2">
                  Medical Documents
                </h1>
                <p className="text-blue-100 opacity-90">
                  Upload, manage, and access all your medical documents in one
                  place
                </p>
              </div>
              <button
                onClick={() => setShowUpload(true)}
                className="mt-4 md:mt-0 bg-white text-blue-600 hover:bg-blue-50 px-6 py-3 rounded-xl font-semibold flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Upload Documents
              </button>
            </div>
          </div>
        </div>

        {/* Upload Modal */}
        {showUpload && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">
                    Upload Documents
                  </h2>
                  <button
                    onClick={() => setShowUpload(false)}
                    className="p-2 hover:bg-gray-100 rounded-lg">
                    <span className="text-2xl text-gray-500">×</span>
                  </button>
                </div>
                <DocumentUpload />
              </div>
            </div>
          </div>
        )}

        {/* Search and Filter */}
        <div className="medical-card mb-6">
          <div className="flex flex-col md:flex-row md:items-center gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search documents by name or patient..."
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
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="input-field py-2">
                  {documentTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>

              <button className="btn-primary flex items-center gap-2">
                <Download className="w-4 h-4" />
                Export All
              </button>
            </div>
          </div>
        </div>

        {/* Document Type Tabs */}
        <div className="mb-6">
          <div className="flex overflow-x-auto scrollbar-hide space-x-2 pb-2">
            {documentTypes.map((type) => {
              const Icon = type.icon;
              const count = documents.filter(
                (d) => type.id === "all" || d.type === type.id
              ).length;

              return (
                <button
                  key={type.id}
                  onClick={() => setFilterType(type.id)}
                  className={`flex-shrink-0 flex items-center gap-2 px-4 py-3 rounded-xl transition-all ${
                    filterType === type.id
                      ? "bg-primary-600 text-white shadow-md"
                      : "bg-white text-gray-600 border border-gray-200"
                  }`}>
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{type.label}</span>
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs ${
                      filterType === type.id ? "bg-white/20" : "bg-gray-100"
                    }`}>
                    {count}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Documents Grid */}
        {loading ? (
          <div className="medical-card text-center py-12">
            <div className="w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading documents...</p>
          </div>
        ) : filteredDocs.length > 0 ? (
          <div className="medical-card">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredDocs.map((doc) => (
                <div
                  key={doc.id}
                  className="bg-gray-50 rounded-xl border border-gray-200 p-4 hover:border-primary-300 transition-all">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div
                        className={`p-3 rounded-lg bg-white ${getTypeColor(
                          doc.type
                        )}`}>
                        <FileText className="w-6 h-6" />
                      </div>
                      <div>
                        <span
                          className={`text-xs px-2 py-1 rounded-full ${getStatusColor(
                            doc.status
                          )}`}>
                          {doc.status}
                        </span>
                      </div>
                    </div>

                    <div className="relative group">
                      <button className="p-1 hover:bg-gray-200 rounded-lg">
                        <MoreVertical className="w-5 h-5 text-gray-500" />
                      </button>

                      <div className="absolute right-0 mt-2 w-32 bg-white rounded-lg shadow-lg border border-gray-200 py-1 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
                        <button
                          onClick={() => handlePreview(doc)}
                          className="w-full px-3 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-2">
                          <Eye className="w-4 h-4" />
                          Preview
                        </button>
                        <button
                          onClick={() => handleDownload(doc)}
                          className="w-full px-3 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-2">
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                        <div className="border-t border-gray-200 my-1"></div>
                        <button
                          onClick={() => handleDelete(doc.id)}
                          className="w-full px-3 py-2 text-left text-red-600 hover:bg-red-50 flex items-center gap-2">
                          <Trash2 className="w-4 h-4" />
                          Delete
                        </button>
                      </div>
                    </div>
                  </div>

                  <h3 className="font-bold text-gray-900 mb-2 truncate">
                    {doc.name}
                  </h3>

                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex items-center gap-2">
                      <User className="w-4 h-4" />
                      <span>{doc.patientName}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      <span>
                        Uploaded:{" "}
                        {new Date(doc.uploadedAt).toLocaleDateString()}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4" />
                      <span>{formatFileSize(doc.size)}</span>
                    </div>
                  </div>

                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handlePreview(doc)}
                        className="btn-secondary flex-1 text-sm py-2">
                        <Eye className="w-4 h-4 inline mr-1" />
                        View
                      </button>
                      <button
                        onClick={() => handleDownload(doc)}
                        className="btn-primary flex-1 text-sm py-2">
                        <Download className="w-4 h-4 inline mr-1" />
                        Download
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="medical-card text-center py-12">
            <Folder className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              No documents found
            </h3>
            <p className="text-gray-600 mb-6">
              {searchTerm
                ? "Try a different search term"
                : "Upload your first document to get started"}
            </p>
            <button
              onClick={() => setShowUpload(true)}
              className="btn-primary inline-flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Upload Documents
            </button>
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
          {[
            {
              label: "Total Documents",
              value: documents.length,
              color: "bg-blue-500",
            },
            {
              label: "Lab Reports",
              value: documents.filter((d) => d.type === "lab_report").length,
              color: "bg-green-500",
            },
            {
              label: "Doctor's Notes",
              value: documents.filter((d) => d.type === "doctor_note").length,
              color: "bg-purple-500",
            },
            { label: "Storage Used", value: "24.5 MB", color: "bg-orange-500" },
          ].map((stat, index) => (
            <div key={index} className="medical-card">
              <div className="flex items-center gap-3">
                <div
                  className={`w-12 h-12 ${stat.color} rounded-xl flex items-center justify-center`}>
                  <Folder className="w-6 h-6 text-white" />
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-900">
                    {stat.value}
                  </div>
                  <div className="text-sm text-gray-500">{stat.label}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      <MobileNav activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
};

export default Documents;
