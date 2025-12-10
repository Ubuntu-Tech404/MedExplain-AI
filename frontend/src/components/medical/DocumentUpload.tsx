import React, { useState, useCallback } from 'react';
import { 
  Upload, 
  FileText, 
  X, 
  Eye, 
  Download, 
  Trash2,
  CheckCircle,
  Clock,
  AlertCircle,
  FolderUp,
  FileType,
  Image as ImageIcon
} from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import ApiService from '../../services/api';
import LocalStorageService from '../../services/localStorage';
import toast from 'react-hot-toast';

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: 'lab_report' | 'doctor_note' | 'prescription' | 'image' | 'other';
  status: 'uploading' | 'processing' | 'completed' | 'error';
  progress: number;
  uploadedAt: string;
  previewUrl?: string;
  processedData?: any;
}

const DocumentUpload: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [selectedType, setSelectedType] = useState<string>('lab_report');
  const [isUploading, setIsUploading] = useState(false);

  const documentTypes = [
    { id: 'lab_report', label: 'Lab Report', icon: FileText, color: 'text-blue-600' },
    { id: 'doctor_note', label: "Doctor's Note", icon: FileText, color: 'text-green-600' },
    { id: 'prescription', label: 'Prescription', icon: FileText, color: 'text-purple-600' },
    { id: 'medical_image', label: 'Medical Image', icon: ImageIcon, color: 'text-orange-600' },
    { id: 'other', label: 'Other Document', icon: FileType, color: 'text-gray-600' },
  ];

  const onDrop = useCallback((acceptedFiles: File[]) => {
    handleFiles(acceptedFiles);
  }, [selectedType]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc', '.docx'],
      'text/plain': ['.txt'],
      'image/*': ['.jpg', '.jpeg', '.png', '.gif'],
    },
    maxSize: 100 * 1024 * 1024, // 100MB
  });

  const handleFiles = async (files: File[]) => {
    setIsUploading(true);
    
    for (const file of files) {
      const fileId = Date.now().toString() + Math.random().toString(36).substr(2, 9);
      
      // Add to local state
      const newFile: UploadedFile = {
        id: fileId,
        name: file.name,
        size: file.size,
        type: selectedType as any,
        status: 'uploading',
        progress: 0,
        uploadedAt: new Date().toISOString(),
      };
      
      setUploadedFiles(prev => [newFile, ...prev]);
      
      try {
        // Upload to backend
        const formData = new FormData();
        formData.append('file', file);
        formData.append('document_type', selectedType);
        formData.append('patient_id', 'demo-patient');
        
        const response = await ApiService.uploadDocument(formData);
        
        // Update file status
        setUploadedFiles(prev => prev.map(f => 
          f.id === fileId 
            ? { 
                ...f, 
                status: 'completed', 
                progress: 100,
                processedData: response.processed_data,
                previewUrl: response.file_url
              } 
            : f
        ));
        
        // Save to local storage
        LocalStorageService.saveDocument({
          id: fileId,
          name: file.name,
          type: selectedType,
          date: new Date().toLocaleDateString(),
          status: 'processed',
          data: response.processed_data
        });
        
        toast.success(`${file.name} uploaded successfully!`);
        
      } catch (error) {
        setUploadedFiles(prev => prev.map(f => 
          f.id === fileId 
            ? { ...f, status: 'error', progress: 0 } 
            : f
        ));
        toast.error(`Failed to upload ${file.name}`);
      }
    }
    
    setIsUploading(false);
  };

  const handleRemoveFile = (fileId: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
    toast.success('File removed');
  };

  const handlePreview = (file: UploadedFile) => {
    if (file.previewUrl) {
      window.open(file.previewUrl, '_blank');
    } else {
      toast.error('No preview available');
    }
  };

  const handleDownload = (file: UploadedFile) => {
    // In a real app, this would download the file
    toast.success(`Downloading ${file.name}...`);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'uploading':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'processing':
        return <Clock className="w-4 h-4 text-blue-500 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'uploading':
        return 'bg-yellow-100 text-yellow-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeColor = (type: string) => {
    const typeConfig = documentTypes.find(t => t.id === type);
    return typeConfig?.color || 'text-gray-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="medical-card">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-teal-500 to-teal-700 rounded-xl flex items-center justify-center">
                <FolderUp className="w-6 h-6 text-white" />
              </div>
              <span>Medical Documents</span>
            </h1>
            <p className="text-gray-600 mt-2">
              Upload lab reports, doctor's notes, prescriptions, and medical images
            </p>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="badge-info">
              AI Processing Available
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Upload Zone */}
        <div className="lg:col-span-2 space-y-6">
          {/* Document Type Selection */}
          <div className="medical-card">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Document Type</h3>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              {documentTypes.map((type) => {
                const Icon = type.icon;
                return (
                  <button
                    key={type.id}
                    onClick={() => setSelectedType(type.id)}
                    className={`flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all ${
                      selectedType === type.id
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <Icon className={`w-6 h-6 mb-2 ${type.color}`} />
                    <span className="text-sm font-medium text-gray-700">{type.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Upload Zone */}
          <div className="medical-card">
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
                isDragActive
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
              }`}
            >
              <input {...getInputProps()} />
              
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Upload className="w-8 h-8 text-primary-600" />
              </div>
              
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {isDragActive ? 'Drop files here' : 'Drag & drop files'}
              </h3>
              
              <p className="text-gray-600 mb-6">
                or click to browse. Supports PDF, DOCX, TXT, and images (max 100MB)
              </p>
              
              <button className="btn-primary px-8">
                Browse Files
              </button>
              
              <div className="mt-6 text-sm text-gray-500">
                <div className="flex items-center justify-center gap-6">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    <span>PDF, DOCX</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <ImageIcon className="w-4 h-4" />
                    <span>JPG, PNG</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <FileType className="w-4 h-4" />
                    <span>TXT</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Upload Stats */}
        <div className="space-y-6">
          {/* Upload Stats */}
          <div className="medical-card">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Upload Statistics</h3>
            <div className="space-y-4">
              {[
                { label: 'Total Files', value: uploadedFiles.length, icon: FileText },
                { label: 'Processed', value: uploadedFiles.filter(f => f.status === 'completed').length, icon: CheckCircle },
                { label: 'Pending', value: uploadedFiles.filter(f => f.status === 'uploading' || f.status === 'processing').length, icon: Clock },
                { label: 'Errors', value: uploadedFiles.filter(f => f.status === 'error').length, icon: AlertCircle },
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
                    <span className="text-2xl font-bold text-gray-900">{stat.value}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="medical-card">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full btn-secondary flex items-center justify-center gap-2">
                <Eye className="w-4 h-4" />
                View All Documents
              </button>
              <button className="w-full btn-primary flex items-center justify-center gap-2">
                <Download className="w-4 h-4" />
                Export Documents
              </button>
              {uploadedFiles.length > 0 && (
                <button 
                  onClick={() => setUploadedFiles([])}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 text-red-600 bg-red-50 hover:bg-red-100 rounded-xl border border-red-200 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                  Clear All
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="medical-card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">Uploaded Files</h3>
            <div className="text-sm text-gray-500">
              {uploadedFiles.length} file{uploadedFiles.length !== 1 ? 's' : ''}
            </div>
          </div>
          
          <div className="space-y-3">
            {uploadedFiles.map((file) => (
              <div 
                key={file.id} 
                className="flex flex-col sm:flex-row sm:items-center gap-4 p-4 bg-gray-50 rounded-xl border border-gray-200"
              >
                {/* File Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3">
                    <div className={`p-3 rounded-lg bg-white ${getTypeColor(file.type)}`}>
                      <FileText className="w-6 h-6" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <h4 className="font-medium text-gray-900 truncate">{file.name}</h4>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${getStatusColor(file.status)}`}>
                          {file.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
                        <span>{formatFileSize(file.size)}</span>
                        <span>•</span>
                        <span>{new Date(file.uploadedAt).toLocaleDateString()}</span>
                        <span>•</span>
                        <span className="capitalize">{file.type.replace('_', ' ')}</span>
                      </div>
                      
                      {/* Progress Bar */}
                      {file.status === 'uploading' && (
                        <div className="mt-2">
                          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-primary-500 transition-all duration-300"
                              style={{ width: `${file.progress}%` }}
                            ></div>
                          </div>
                          <div className="text-xs text-gray-500 mt-1 text-right">
                            {file.progress}%
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                
                {/* Actions */}
                <div className="flex items-center gap-2">
                  {file.status === 'completed' && (
                    <>
                      <button
                        onClick={() => handlePreview(file)}
                        className="p-2 text-gray-600 hover:text-primary-600 hover:bg-white rounded-lg transition-colors"
                        title="Preview"
                      >
                        <Eye className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => handleDownload(file)}
                        className="p-2 text-gray-600 hover:text-primary-600 hover:bg-white rounded-lg transition-colors"
                        title="Download"
                      >
                        <Download className="w-5 h-5" />
                      </button>
                    </>
                  )}
                  
                  <button
                    onClick={() => handleRemoveFile(file.id)}
                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Remove"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Processing Information */}
      {uploadedFiles.some(f => f.status === 'completed' && f.processedData) && (
        <div className="medical-card">
          <h3 className="text-lg font-bold text-gray-900 mb-4">AI Processing Results</h3>
          <div className="space-y-4">
            {uploadedFiles
              .filter(f => f.status === 'completed' && f.processedData)
              .map((file) => (
                <div key={file.id} className="p-4 bg-primary-50 rounded-xl border border-primary-200">
                  <div className="flex items-center gap-3 mb-3">
                    <FileText className="w-5 h-5 text-primary-600" />
                    <h4 className="font-medium text-gray-900">{file.name}</h4>
                  </div>
                  
                  {file.processedData?.type === 'lab_report' && (
                    <div className="text-sm text-gray-700">
                      <div className="mb-2">
                        <span className="font-medium">Extracted Results:</span> {file.processedData.extracted_values} values
                      </div>
                      {file.processedData.results && Object.keys(file.processedData.results).length > 0 && (
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                          {Object.entries(file.processedData.results).map(([key, value]) => (
                            <div key={key} className="bg-white p-2 rounded-lg text-center">
                              <div className="text-xs text-gray-500 uppercase">{key}</div>
                              <div className="font-semibold">{value}</div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                  
                  {file.processedData?.type === 'doctor_note' && (
                    <div className="text-sm text-gray-700">
                      <div className="mb-2">
                        <span className="font-medium">Diagnosis:</span> {file.processedData.diagnosis || 'Not specified'}
                      </div>
                      {file.processedData.medications && file.processedData.medications.length > 0 && (
                        <div>
                          <span className="font-medium">Medications:</span>{' '}
                          {file.processedData.medications.join(', ')}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;