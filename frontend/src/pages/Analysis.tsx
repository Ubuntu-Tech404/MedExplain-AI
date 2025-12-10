import React, { useState } from "react";
import {
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Download,
} from "lucide-react";

const Analysis: React.FC = () => {
  const [activeTab, setActiveTab] = useState("lab");

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-teal-600 to-cyan-600 rounded-2xl p-6 text-white shadow-lg">
            <h1 className="text-2xl md:text-3xl font-bold mb-2">
              Health Analysis
            </h1>
            <p className="text-teal-100 opacity-90">
              Comprehensive analysis of your health metrics
            </p>
          </div>
        </div>

        {/* Simple Content */}
        <div className="medical-card">
          <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-teal-600" />
            Analysis Dashboard
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {[
              {
                label: "Health Score",
                value: "85/100",
                icon: CheckCircle,
                color: "text-green-600",
              },
              {
                label: "Tests This Month",
                value: "3",
                icon: BarChart3,
                color: "text-blue-600",
              },
              {
                label: "Active Alerts",
                value: "1",
                icon: AlertTriangle,
                color: "text-orange-600",
              },
              {
                label: "Trend Status",
                value: "Improving",
                icon: TrendingUp,
                color: "text-teal-600",
              },
            ].map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div
                  key={index}
                  className="p-4 bg-white rounded-xl border border-gray-200">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg bg-gray-50 ${stat.color}`}>
                      <Icon className="w-6 h-6" />
                    </div>
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

          {/* Quick Stats */}
          <div className="mb-8">
            <h3 className="text-lg font-bold text-gray-900 mb-4">
              Recent Analysis
            </h3>
            <div className="space-y-3">
              {[
                {
                  title: "Blood Work Analysis",
                  status: "Completed",
                  date: "Nov 15, 2024",
                },
                {
                  title: "Diabetes Control Report",
                  status: "In Progress",
                  date: "Nov 10, 2024",
                },
                {
                  title: "Heart Health Check",
                  status: "Completed",
                  date: "Nov 5, 2024",
                },
              ].map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                  <div>
                    <div className="font-medium text-gray-900">
                      {item.title}
                    </div>
                    <div className="text-sm text-gray-500">{item.date}</div>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${
                      item.status === "Completed"
                        ? "bg-green-100 text-green-800"
                        : "bg-blue-100 text-blue-800"
                    }`}>
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button className="btn-primary flex items-center gap-2">
              <Download className="w-4 h-4" />
              Export Report
            </button>
            <button className="btn-secondary">Generate New Analysis</button>
          </div>
        </div>

        {/* Success Message */}
        <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-xl">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-6 h-6 text-green-600" />
            <div>
              <div className="font-medium text-green-800">
                Analysis Page Loaded Successfully
              </div>
              <div className="text-sm text-green-600">
                The page is working correctly
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analysis;
