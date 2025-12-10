import React, { useState, useEffect } from 'react';
import { X, Save, Trash2 } from 'lucide-react';

interface MedicationModalProps {
  medication?: any;
  onClose: () => void;
  onSave: (medication: any) => void;
  onDelete?: () => void;
}

const MedicationModal: React.FC<MedicationModalProps> = ({
  medication,
  onClose,
  onSave,
  onDelete
}) => {
  const [formData, setFormData] = useState({
    name: '',
    dosage: '',
    frequency: 'Once daily',
    timing: ['08:00'],
    purpose: '',
    instructions: '',
    sideEffects: [] as string[],
    interactions: [] as string[],
    startDate: new Date().toISOString().split('T')[0],
    endDate: '',
    status: 'active' as 'active' | 'completed' | 'missed'
  });

  const [sideEffectInput, setSideEffectInput] = useState('');
  const [interactionInput, setInteractionInput] = useState('');

  useEffect(() => {
    if (medication) {
      setFormData({
        name: medication.name || '',
        dosage: medication.dosage || '',
        frequency: medication.frequency || 'Once daily',
        timing: medication.timing || ['08:00'],
        purpose: medication.purpose || '',
        instructions: medication.instructions || '',
        sideEffects: medication.sideEffects || [],
        interactions: medication.interactions || [],
        startDate: medication.startDate || new Date().toISOString().split('T')[0],
        endDate: medication.endDate || '',
        status: medication.status || 'active'
      });
    }
  }, [medication]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      ...formData,
      id: medication?.id || Date.now().toString()
    });
  };

  const addSideEffect = () => {
    if (sideEffectInput.trim()) {
      setFormData(prev => ({
        ...prev,
        sideEffects: [...prev.sideEffects, sideEffectInput.trim()]
      }));
      setSideEffectInput('');
    }
  };

  const removeSideEffect = (index: number) => {
    setFormData(prev => ({
      ...prev,
      sideEffects: prev.sideEffects.filter((_, i) => i !== index)
    }));
  };

  const addInteraction = () => {
    if (interactionInput.trim()) {
      setFormData(prev => ({
        ...prev,
        interactions: [...prev.interactions, interactionInput.trim()]
      }));
      setInteractionInput('');
    }
  };

  const removeInteraction = (index: number) => {
    setFormData(prev => ({
      ...prev,
      interactions: prev.interactions.filter((_, i) => i !== index)
    }));
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">
              {medication ? 'Edit Medication' : 'Add New Medication'}
            </h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Medication Name *
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                className="input-field"
                placeholder="e.g., Metformin"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Dosage *
              </label>
              <input
                type="text"
                value={formData.dosage}
                onChange={(e) => setFormData(prev => ({ ...prev, dosage: e.target.value }))}
                className="input-field"
                placeholder="e.g., 500mg"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Frequency *
              </label>
              <select
                value={formData.frequency}
                onChange={(e) => setFormData(prev => ({ ...prev, frequency: e.target.value }))}
                className="input-field"
                required
              >
                <option value="Once daily">Once daily</option>
                <option value="Twice daily">Twice daily</option>
                <option value="Three times daily">Three times daily</option>
                <option value="Four times daily">Four times daily</option>
                <option value="Weekly">Weekly</option>
                <option value="As needed">As needed</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={formData.status}
                onChange={(e) => setFormData(prev => ({ 
                  ...prev, 
                  status: e.target.value as 'active' | 'completed' | 'missed' 
                }))}
                className="input-field"
              >
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="missed">Missed</option>
              </select>
            </div>
          </div>

          {/* Timing */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Timing (24-hour format)
            </label>
            <div className="flex flex-wrap gap-2">
              {formData.timing.map((time, index) => (
                <div key={index} className="flex items-center gap-2 bg-gray-100 px-3 py-2 rounded-lg">
                  <input
                    type="time"
                    value={time}
                    onChange={(e) => {
                      const newTiming = [...formData.timing];
                      newTiming[index] = e.target.value;
                      setFormData(prev => ({ ...prev, timing: newTiming }));
                    }}
                    className="bg-transparent border-none outline-none"
                  />
                  <button
                    type="button"
                    onClick={() => {
                      const newTiming = formData.timing.filter((_, i) => i !== index);
                      setFormData(prev => ({ ...prev, timing: newTiming }));
                    }}
                    className="text-gray-500 hover:text-red-500"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, timing: [...prev.timing, '08:00'] }))}
                className="px-4 py-2 text-primary-600 hover:text-primary-700 bg-primary-50 rounded-lg"
              >
                + Add Time
              </button>
            </div>
          </div>

          {/* Purpose & Instructions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Purpose *
              </label>
              <input
                type="text"
                value={formData.purpose}
                onChange={(e) => setFormData(prev => ({ ...prev, purpose: e.target.value }))}
                className="input-field"
                placeholder="e.g., Type 2 Diabetes"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Instructions
              </label>
              <input
                type="text"
                value={formData.instructions}
                onChange={(e) => setFormData(prev => ({ ...prev, instructions: e.target.value }))}
                className="input-field"
                placeholder="e.g., Take with food"
              />
            </div>
          </div>

          {/* Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Date *
              </label>
              <input
                type="date"
                value={formData.startDate}
                onChange={(e) => setFormData(prev => ({ ...prev, startDate: e.target.value }))}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Date (optional)
              </label>
              <input
                type="date"
                value={formData.endDate}
                onChange={(e) => setFormData(prev => ({ ...prev, endDate: e.target.value }))}
                className="input-field"
              />
            </div>
          </div>

          {/* Side Effects */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Side Effects
            </label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={sideEffectInput}
                onChange={(e) => setSideEffectInput(e.target.value)}
                className="input-field flex-1"
                placeholder="e.g., Nausea"
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSideEffect())}
              />
              <button
                type="button"
                onClick={addSideEffect}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {formData.sideEffects.map((effect, index) => (
                <div
                  key={index}
                  className="flex items-center gap-2 bg-yellow-100 text-yellow-800 px-3 py-1.5 rounded-full"
                >
                  <span>{effect}</span>
                  <button
                    type="button"
                    onClick={() => removeSideEffect(index)}
                    className="text-yellow-700 hover:text-yellow-900"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Interactions */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Interactions to Avoid
            </label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={interactionInput}
                onChange={(e) => setInteractionInput(e.target.value)}
                className="input-field flex-1"
                placeholder="e.g., Alcohol, Grapefruit juice"
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addInteraction())}
              />
              <button
                type="button"
                onClick={addInteraction}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {formData.interactions.map((interaction, index) => (
                <div
                  key={index}
                  className="flex items-center gap-2 bg-red-100 text-red-800 px-3 py-1.5 rounded-full"
                >
                  <span>{interaction}</span>
                  <button
                    type="button"
                    onClick={() => removeInteraction(index)}
                    className="text-red-700 hover:text-red-900"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-200">
            <div>
              {medication && onDelete && (
                <button
                  type="button"
                  onClick={onDelete}
                  className="flex items-center gap-2 px-4 py-2 text-red-600 bg-red-50 hover:bg-red-100 rounded-lg border border-red-200"
                >
                  <Trash2 className="w-4 h-4" />
                  Delete
                </button>
              )}
            </div>
            
            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn-primary flex items-center gap-2 px-6 py-2"
              >
                <Save className="w-4 h-4" />
                {medication ? 'Update' : 'Add'} Medication
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MedicationModal;