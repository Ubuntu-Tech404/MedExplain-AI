export const saveReport = (report) => {
  try {
    const reports = getReports();
    const reportWithId = {
      ...report,
      id: `report_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      createdAt: new Date().toISOString()
    };
    
    reports.unshift(reportWithId);
    // Keep only last 20 reports
    const limitedReports = reports.slice(0, 20);
    localStorage.setItem('medexplain_reports', JSON.stringify(limitedReports));
    
    return reportWithId;
  } catch (error) {
    console.error('Error saving report:', error);
    return null;
  }
};

export const getReports = () => {
  try {
    const reports = localStorage.getItem('medexplain_reports');
    return reports ? JSON.parse(reports) : [];
  } catch (error) {
    console.error('Error getting reports:', error);
    return [];
  }
};

export const getReportById = (id) => {
  const reports = getReports();
  return reports.find(report => report.id === id);
};

export const deleteReport = (id) => {
  try {
    const reports = getReports();
    const filteredReports = reports.filter(report => report.id !== id);
    localStorage.setItem('medexplain_reports', JSON.stringify(filteredReports));
    return true;
  } catch (error) {
    console.error('Error deleting report:', error);
    return false;
  }
};

export const clearAllReports = () => {
  try {
    localStorage.removeItem('medexplain_reports');
    return true;
  } catch (error) {
    console.error('Error clearing reports:', error);
    return false;
  }
};

export const getUserPreferences = () => {
  try {
    const prefs = localStorage.getItem('medexplain_preferences');
    return prefs ? JSON.parse(prefs) : {
      language: 'English',
      fontSize: 'medium',
      theme: 'light',
      notifications: true
    };
  } catch (error) {
    return {
      language: 'English',
      fontSize: 'medium',
      theme: 'light',
      notifications: true
    };
  }
};

export const saveUserPreferences = (preferences) => {
  try {
    localStorage.setItem('medexplain_preferences', JSON.stringify(preferences));
    return true;
  } catch (error) {
    console.error('Error saving preferences:', error);
    return false;
  }
};