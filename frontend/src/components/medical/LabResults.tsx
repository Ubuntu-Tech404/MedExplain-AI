import React, { useState, useEffect } from "react";
import {
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Download,
  Filter,
  RefreshCw,
  Zap,
  PieChart,
  LineChart as LineChartIcon,
  Activity,
  Clock,
} from "lucide-react";
import toast from "react-hot-toast";

const LabResults: React.FC = () => {
  const [labData, setLabData] = useState<any[]>([]);
  const [selectedTest, setSelectedTest] = useState<string>("glucose");
  const [timeRange, setTimeRange] = useState<string>("6m");
  const [loading, setLoading] = useState(false);
  const [aiAnalysis, setAiAnalysis] = useState<any>(null);

  // Define helper functions at the TOP
  const getUnit = (test: string) => {
    const units: Record<string, string> = {
      glucose: "mg/dL",
      hba1c: "%",
      cholesterol: "mg/dL",
      ldl: "mg/dL",
      hdl: "mg/dL",
      triglycerides: "mg/dL",
    };
    return units[test] || "";
  };

  const formatTestName = (test: string) => {
    return test
      .replace(/([A-Z])/g, " $1")
      .replace(/^./, (str) => str.toUpperCase());
  };

  const getReferenceRange = (test: string) => {
    const ranges: Record<string, { min: number; max: number }> = {
      glucose: { min: 70, max: 100 },
      hba1c: { min: 4.0, max: 5.6 },
      cholesterol: { min: 125, max: 200 },
      ldl: { min: 0, max: 100 },
      hdl: { min: 40, max: 60 },
      triglycerides: { min: 0, max: 150 },
    };
    return ranges[test] || { min: 0, max: 100 };
  };

  useEffect(() => {
    loadLabData();
  }, []);

  const loadLabData = async () => {
    setLoading(true);
    try {
      // Generate demo data
      const data = generateMockLabData();
      setLabData(data);

      // Mock AI analysis
      setAiAnalysis({
        analysis:
          "Your lab results show good overall health. Blood sugar levels are within normal range.",
        categorization: {
          glucose: { level: "normal", color: "green" },
          cholesterol: { level: "normal", color: "green" },
          hba1c: { level: "normal", color: "green" },
        },
        analyzed_at: new Date().toISOString(),
      });
    } catch (error) {
      console.error("Error loading lab data:", error);
      toast.error("Error loading lab data");
    } finally {
      setLoading(false);
    }
  };

  const generateMockLabData = () => {
    const today = new Date();
    const data = [];

    for (let i = 11; i >= 0; i--) {
      const date = new Date(today);
      date.setMonth(date.getMonth() - i);

      data.push({
        date: date.toISOString().split("T")[0],
        glucose: 90 + Math.random() * 20,
        hba1c: 5.4 + Math.random() * 0.5,
        cholesterol: 180 + Math.random() * 40,
        ldl: 100 + Math.random() * 30,
        hdl: 50 + Math.random() * 20,
        triglycerides: 120 + Math.random() * 50,
      });
    }

    return data;
  };

  const getLatestValues = () => {
    if (labData.length === 0) return [];
    const latest = labData[labData.length - 1];

    const tests = [
      "glucose",
      "hba1c",
      "cholesterol",
      "ldl",
      "hdl",
      "triglycerides",
    ];
    return tests.map((test) => {
      const value = latest[test];
      const range = getReferenceRange(test);
      let status = "normal";

      if (value < range.min * 0.9 || value > range.max * 1.1) {
        status = "critical";
      } else if (value < range.min * 0.95 || value > range.max * 1.05) {
        status = "slightly_critical";
      }

      return {
        test,
        value: value.toFixed(1),
        unit: getUnit(test),
        status,
        reference: `${range.min}-${range.max}`,
      };
    });
  };

  const latestValues = getLatestValues();
  const filteredData =
    timeRange === "all" ? labData : labData.slice(-parseInt(timeRange));

  const testOptions = [
    { id: "glucose", label: "Glucose", color: "#3b82f6" },
    { id: "hba1c", label: "HbA1c", color: "#8b5cf6" },
    { id: "cholesterol", label: "Cholesterol", color: "#10b981" },
    { id: "ldl", label: "LDL", color: "#ef4444" },
    { id: "hdl", label: "HDL", color: "#f59e0b" },
  ];

  const timeRanges = [
    { id: "3m", label: "3 Months" },
    { id: "6m", label: "6 Months" },
    { id: "1y", label: "1 Year" },
    { id: "all", label: "All Time" },
  ];

  const handleAnalyzeWithAI = async () => {
    setLoading(true);
    setTimeout(() => {
      setAiAnalysis({
        analysis:
          "AI analysis shows your health is improving. Continue with your current regimen.",
        analyzed_at: new Date().toISOString(),
      });
      setLoading(false);
      toast.success("AI analysis completed!");
    }, 1000);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "normal":
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case "slightly_critical":
        return <AlertTriangle className="w-4 h-4 text-orange-500" />;
      case "critical":
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "normal":
        return "bg-green-100 text-green-800";
      case "slightly_critical":
        return "bg-orange-100 text-orange-800";
      case "critical":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="medical-card">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-teal-500 to-teal-700 rounded-xl flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <span>Lab Results Analysis</span>
            </h1>
            <p className="text-gray-600 mt-2">
              Visualize and analyze your blood work
            </p>
          </div>

          <button
            onClick={handleAnalyzeWithAI}
            disabled={loading}
            className="btn-primary flex items-center gap-2">
            {loading ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Zap className="w-4 h-4" />
            )}
            Analyze with AI
          </button>
        </div>
      </div>

      {/* Latest Results */}
      <div className="medical-card">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Latest Results</h2>

        {loading ? (
          <div className="text-center py-8">
            <div className="w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading lab data...</p>
          </div>
        ) : latestValues.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {latestValues.map((item: any, index) => (
              <div
                key={index}
                className={`p-4 rounded-xl border ${
                  item.status === "critical"
                    ? "border-red-200 bg-red-50"
                    : item.status === "slightly_critical"
                    ? "border-orange-200 bg-orange-50"
                    : "border-green-200 bg-green-50"
                }`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm font-medium text-gray-700">
                    {formatTestName(item.test)}
                  </div>
                  {getStatusIcon(item.status)}
                </div>
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {item.value}
                  <span className="text-sm font-normal text-gray-500 ml-1">
                    {item.unit}
                  </span>
                </div>
                <div className="text-xs text-gray-500">
                  Ref: {item.reference} {item.unit}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <BarChart3 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600">No lab data available</p>
            <button onClick={loadLabData} className="mt-4 btn-primary">
              Load Demo Data
            </button>
          </div>
        )}
      </div>

      {/* Test Selection */}
      <div className="medical-card">
        <h3 className="text-lg font-bold text-gray-900 mb-4">
          Select Test to Analyze
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
          {testOptions.map((test) => (
            <button
              key={test.id}
              onClick={() => setSelectedTest(test.id)}
              className={`flex flex-col items-center p-4 rounded-xl border-2 transition-all ${
                selectedTest === test.id
                  ? "border-primary-500 bg-primary-50"
                  : "border-gray-200 hover:border-gray-300"
              }`}>
              <div
                className="w-8 h-8 rounded-full mb-2"
                style={{ backgroundColor: test.color }}></div>
              <span className="text-sm font-medium text-gray-700">
                {test.label}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* AI Analysis */}
      {aiAnalysis && (
        <div className="medical-card bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-blue-600" />
            AI Analysis Summary
          </h3>
          <div className="p-4 bg-white/80 rounded-xl border border-blue-100">
            <div className="text-gray-800">{aiAnalysis.analysis}</div>
            <div className="text-sm text-gray-500 mt-2">
              {new Date(aiAnalysis.analyzed_at).toLocaleDateString()}
            </div>
          </div>
        </div>
      )}

      {/* Quick Stats */}
      <div className="medical-card">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Stats</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            {
              label: "Total Tests",
              value: labData.length,
              icon: BarChart3,
              color: "text-blue-600",
            },
            {
              label: "Normal Results",
              value: latestValues.filter((v: any) => v.status === "normal")
                .length,
              icon: CheckCircle,
              color: "text-green-600",
            },
            {
              label: "Need Attention",
              value: latestValues.filter((v: any) => v.status !== "normal")
                .length,
              icon: AlertTriangle,
              color: "text-orange-600",
            },
            {
              label: "Time Range",
              value: timeRange === "all" ? "All" : timeRange,
              icon: Clock,
              color: "text-purple-600",
            },
          ].map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="p-4 bg-gray-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <Icon className={`w-6 h-6 ${stat.color}`} />
                  <div>
                    <div className="text-2xl font-bold text-gray-900">
                      {stat.value}
                    </div>
                    <div className="text-sm text-gray-500">{stat.label}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default LabResults;
