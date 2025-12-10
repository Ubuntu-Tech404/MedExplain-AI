import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalAnalyzer:
    """Medical data analysis and categorization"""
    
    def __init__(self):
        # Reference ranges for common lab tests
        self.reference_ranges = {
            "glucose": {"min": 70, "max": 100, "unit": "mg/dL", "category": "Metabolic"},
            "hba1c": {"min": 4.0, "max": 5.6, "unit": "%", "category": "Metabolic"},
            "cholesterol": {"min": 125, "max": 200, "unit": "mg/dL", "category": "Cardiovascular"},
            "ldl": {"min": 0, "max": 100, "unit": "mg/dL", "category": "Cardiovascular"},
            "hdl": {"min": 40, "max": 60, "unit": "mg/dL", "category": "Cardiovascular"},
            "triglycerides": {"min": 0, "max": 150, "unit": "mg/dL", "category": "Cardiovascular"},
            "creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL", "category": "Renal"},
            "bun": {"min": 7, "max": 20, "unit": "mg/dL", "category": "Renal"},
            "sodium": {"min": 135, "max": 145, "unit": "mmol/L", "category": "Electrolytes"},
            "potassium": {"min": 3.5, "max": 5.0, "unit": "mmol/L", "category": "Electrolytes"},
            "wbc": {"min": 4.5, "max": 11.0, "unit": "10^3/uL", "category": "Hematology"},
            "hemoglobin": {"min": 13.5, "max": 17.5, "unit": "g/dL", "category": "Hematology"},
            "platelets": {"min": 150, "max": 450, "unit": "10^3/uL", "category": "Hematology"}
        }
        
        # Condition risk thresholds
        self.risk_thresholds = {
            "diabetes": {"hba1c": 6.5, "glucose_fasting": 126},
            "hypertension": {"systolic": 130, "diastolic": 80},
            "hyperlipidemia": {"ldl": 130, "triglycerides": 200},
            "kidney_disease": {"creatinine": 1.3, "bun": 25}
        }
        
        # Health status colors
        self.status_colors = {
            "normal": {"color": "#10B981", "text": "Normal"},
            "borderline": {"color": "#F59E0B", "text": "Borderline"},
            "critical": {"color": "#EF4444", "text": "Critical"},
            "warning": {"color": "#F97316", "text": "Warning"},
            "good": {"color": "#3B82F6", "text": "Good"}
        }
    
    def categorize_lab_results(self, lab_data: Dict) -> Dict:
        """Categorize lab results with detailed analysis"""
        categorized = {}
        
        for test_name, test_value in lab_data.items():
            if isinstance(test_value, (int, float)) and test_name in self.reference_ranges:
                ref = self.reference_ranges[test_name]
                min_val = ref["min"]
                max_val = ref["max"]
                
                # Calculate deviation percentage
                if test_value < min_val:
                    deviation = ((min_val - test_value) / min_val) * 100
                    status = self._get_status_below(min_val, test_value)
                elif test_value > max_val:
                    deviation = ((test_value - max_val) / max_val) * 100
                    status = self._get_status_above(max_val, test_value)
                else:
                    deviation = 0
                    status = "normal"
                
                categorized[test_name] = {
                    "value": test_value,
                    "unit": ref["unit"],
                    "category": ref["category"],
                    "status": status,
                    "color": self.status_colors[status]["color"] if status in self.status_colors else "#6B7280",
                    "status_text": self.status_colors[status]["text"] if status in self.status_colors else "Unknown",
                    "min_reference": min_val,
                    "max_reference": max_val,
                    "deviation_percent": round(deviation, 2),
                    "interpretation": self._get_interpretation(test_name, test_value, status)
                }
        
        return categorized
    
    def _get_status_below(self, min_val: float, actual: float) -> str:
        """Determine status for values below reference"""
        deviation = ((min_val - actual) / min_val) * 100
        if deviation > 30:
            return "critical"
        elif deviation > 15:
            return "warning"
        else:
            return "borderline"
    
    def _get_status_above(self, max_val: float, actual: float) -> str:
        """Determine status for values above reference"""
        deviation = ((actual - max_val) / max_val) * 100
        if deviation > 30:
            return "critical"
        elif deviation > 15:
            return "warning"
        else:
            return "borderline"
    
    def _get_interpretation(self, test_name: str, value: float, status: str) -> str:
        """Generate interpretation for lab result"""
        interpretations = {
            "glucose": {
                "normal": "Normal fasting blood glucose level.",
                "borderline": "Slightly elevated blood glucose. Monitor diet.",
                "warning": "High blood glucose. May indicate prediabetes.",
                "critical": "Very high blood glucose. Possible diabetes."
            },
            "hba1c": {
                "normal": "Good long-term blood sugar control.",
                "borderline": "Moderate blood sugar control. Lifestyle changes recommended.",
                "warning": "Poor blood sugar control. May indicate diabetes.",
                "critical": "Very poor blood sugar control. Diabetes likely."
            },
            "ldl": {
                "normal": "Optimal LDL cholesterol level.",
                "borderline": "Borderline high LDL cholesterol.",
                "warning": "High LDL cholesterol. Increased heart disease risk.",
                "critical": "Very high LDL cholesterol. High heart disease risk."
            },
            "hdl": {
                "normal": "Good HDL cholesterol level.",
                "borderline": "Borderline low HDL cholesterol.",
                "warning": "Low HDL cholesterol. Increased heart disease risk.",
                "critical": "Very low HDL cholesterol. High heart disease risk."
            },
            "creatinine": {
                "normal": "Normal kidney function.",
                "borderline": "Slightly elevated creatinine. Monitor kidney function.",
                "warning": "High creatinine. Possible kidney impairment.",
                "critical": "Very high creatinine. Kidney dysfunction likely."
            }
        }
        
        if test_name in interpretations and status in interpretations[test_name]:
            return interpretations[test_name][status]
        
        return f"Value is {status} compared to reference range."
    
    def calculate_health_score(self, lab_data: Dict) -> Dict:
        """Calculate overall health score from lab results"""
        if not lab_data:
            return {"score": 0, "status": "Insufficient Data"}
        
        scores = []
        max_score = 100
        total_weight = 0
        
        # Weights for different test categories
        weights = {
            "Metabolic": 0.3,
            "Cardiovascular": 0.3,
            "Renal": 0.2,
            "Hematology": 0.1,
            "Electrolytes": 0.1
        }
        
        categorized = self.categorize_lab_results(lab_data)
        
        for test, data in categorized.items():
            if "category" in data and "status" in data:
                category = data["category"]
                status = data["status"]
                
                # Assign points based on status
                status_points = {
                    "normal": 100,
                    "good": 90,
                    "borderline": 70,
                    "warning": 40,
                    "critical": 10
                }
                
                if status in status_points:
                    weight = weights.get(category, 0.1)
                    scores.append(status_points[status] * weight)
                    total_weight += weight
        
        if scores and total_weight > 0:
            avg_score = sum(scores) / total_weight
        else:
            avg_score = 0
        
        # Determine overall health status
        if avg_score >= 85:
            health_status = "Excellent"
            status_color = "#10B981"
        elif avg_score >= 70:
            health_status = "Good"
            status_color = "#3B82F6"
        elif avg_score >= 50:
            health_status = "Fair"
            status_color = "#F59E0B"
        else:
            health_status = "Needs Attention"
            status_color = "#EF4444"
        
        return {
            "score": round(avg_score, 1),
            "status": health_status,
            "status_color": status_color,
            "category_breakdown": categorized,
            "calculated_at": datetime.now().isoformat()
        }
    
    def detect_risk_factors(self, lab_data: Dict, patient_age: int = 50) -> Dict:
        """Detect medical risk factors from lab data"""
        risks = []
        
        # Diabetes risk
        if "hba1c" in lab_data and lab_data["hba1c"] >= 5.7:
            risk_level = "high" if lab_data["hba1c"] >= 6.5 else "moderate"
            risks.append({
                "condition": "Diabetes",
                "risk_level": risk_level,
                "indicators": [f"HbA1c: {lab_data['hba1c']}%"],
                "recommendations": [
                    "Consult endocrinologist",
                    "Monitor blood sugar regularly",
                    "Diet and exercise changes"
                ]
            })
        
        # Cardiovascular risk
        cardiovascular_risk = False
        cv_indicators = []
        
        if "ldl" in lab_data and lab_data["ldl"] > 130:
            cardiovascular_risk = True
            cv_indicators.append(f"LDL: {lab_data['ldl']} mg/dL")
        
        if "triglycerides" in lab_data and lab_data["triglycerides"] > 150:
            cardiovascular_risk = True
            cv_indicators.append(f"Triglycerides: {lab_data['triglycerides']} mg/dL")
        
        if "hdl" in lab_data and lab_data["hdl"] < 40:
            cardiovascular_risk = True
            cv_indicators.append(f"HDL: {lab_data['hdl']} mg/dL")
        
        if cardiovascular_risk:
            risks.append({
                "condition": "Cardiovascular Disease",
                "risk_level": "moderate",
                "indicators": cv_indicators,
                "recommendations": [
                    "Cardiology consultation",
                    "Heart-healthy diet",
                    "Regular exercise",
                    "Cholesterol management"
                ]
            })
        
        # Kidney disease risk
        if "creatinine" in lab_data and lab_data["creatinine"] > 1.2:
            risks.append({
                "condition": "Kidney Disease",
                "risk_level": "moderate" if lab_data["creatinine"] <= 2.0 else "high",
                "indicators": [f"Creatinine: {lab_data['creatinine']} mg/dL"],
                "recommendations": [
                    "Nephrology consultation",
                    "Monitor kidney function",
                    "Stay hydrated",
                    "Avoid NSAIDs"
                ]
            })
        
        # Age-adjusted risk
        if patient_age > 60:
            for risk in risks:
                if risk["risk_level"] == "moderate":
                    risk["risk_level"] = "high"
                    risk["recommendations"].append("Age increases risk - more frequent monitoring needed")
        
        return {
            "detected_risks": risks,
            "total_risks": len(risks),
            "highest_risk": max([r["risk_level"] for r in risks], default="low"),
            "analyzed_at": datetime.now().isoformat()
        }
    
    def generate_trend_analysis(self, historical_data: List[Dict]) -> Dict:
        """Analyze trends from historical lab data"""
        if len(historical_data) < 2:
            return {"message": "Insufficient historical data for trend analysis"}
        
        trends = {}
        
        # Group by test name
        test_data = {}
        for record in historical_data:
            date = record.get("date", datetime.now().isoformat())
            for test, value in record.items():
                if isinstance(value, (int, float)):
                    if test not in test_data:
                        test_data[test] = []
                    test_data[test].append({"date": date, "value": value})
        
        # Analyze each test trend
        for test, data_points in test_data.items():
            if len(data_points) >= 2:
                # Sort by date
                sorted_data = sorted(data_points, key=lambda x: x["date"])
                values = [dp["value"] for dp in sorted_data]
                dates = [dp["date"] for dp in sorted_data]
                
                # Calculate trend
                if len(values) >= 2:
                    first_val = values[0]
                    last_val = values[-1]
                    percent_change = ((last_val - first_val) / first_val) * 100 if first_val != 0 else 0
                    
                    # Determine trend direction
                    if abs(percent_change) < 5:
                        direction = "stable"
                        trend_color = "#6B7280"
                    elif percent_change > 0:
                        direction = "increasing"
                        trend_color = "#EF4444" if test in ["glucose", "ldl", "creatinine"] else "#10B981"
                    else:
                        direction = "decreasing"
                        trend_color = "#10B981" if test in ["glucose", "ldl", "creatinine"] else "#EF4444"
                    
                    trends[test] = {
                        "direction": direction,
                        "percent_change": round(percent_change, 1),
                        "first_value": first_val,
                        "last_value": last_val,
                        "first_date": dates[0],
                        "last_date": dates[-1],
                        "data_points": len(values),
                        "trend_color": trend_color,
                        "recommendation": self._get_trend_recommendation(test, direction, percent_change)
                    }
        
        return {
            "trends": trends,
            "analyzed_tests": len(trends),
            "analysis_period": f"{sorted_data[0]['date']} to {sorted_data[-1]['date']}",
            "generated_at": datetime.now().isoformat()
        }
    
    def _get_trend_recommendation(self, test_name: str, direction: str, percent_change: float) -> str:
        """Generate recommendation based on trend"""
        recommendations = {
            "glucose": {
                "increasing": "Blood sugar increasing. Review diet and medication.",
                "decreasing": "Blood sugar improving. Continue current management.",
                "stable": "Blood sugar stable. Maintain current regimen."
            },
            "ldl": {
                "increasing": "LDL cholesterol rising. Consider diet changes or medication adjustment.",
                "decreasing": "LDL cholesterol improving. Continue current treatment.",
                "stable": "LDL cholesterol stable. Maintain current approach."
            },
            "hba1c": {
                "increasing": "Long-term blood sugar control worsening. Review diabetes management.",
                "decreasing": "Blood sugar control improving. Good progress.",
                "stable": "Blood sugar control stable. Continue monitoring."
            }
        }
        
        if test_name in recommendations and direction in recommendations[test_name]:
            return recommendations[test_name][direction]
        
        return f"Value is {direction}. Discuss with healthcare provider."
    
    def generate_health_report(self, lab_data: Dict, patient_info: Dict = None) -> Dict:
        """Generate comprehensive health report"""
        
        # Categorize results
        categorized = self.categorize_lab_results(lab_data)
        
        # Calculate health score
        health_score = self.calculate_health_score(lab_data)
        
        # Detect risk factors
        patient_age = patient_info.get("age", 50) if patient_info else 50
        risk_factors = self.detect_risk_factors(lab_data, patient_age)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(categorized, risk_factors)
        
        # Overall assessment
        overall_assessment = self._generate_overall_assessment(health_score, risk_factors)
        
        return {
            "patient_info": patient_info or {},
            "lab_results": categorized,
            "health_score": health_score,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "overall_assessment": overall_assessment,
            "generated_at": datetime.now().isoformat(),
            "report_id": f"MED_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
    
    def _generate_recommendations(self, categorized: Dict, risk_factors: Dict) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Based on abnormal results
        for test, data in categorized.items():
            if data.get("status") in ["warning", "critical"]:
                rec = f"Follow up on {test} ({data['value']} {data['unit']}) - {data['interpretation']}"
                recommendations.append(rec)
        
        # Based on risk factors
        for risk in risk_factors.get("detected_risks", []):
            for rec in risk.get("recommendations", []):
                if rec not in recommendations:
                    recommendations.append(rec)
        
        # General health recommendations
        recommendations.append("Schedule follow-up appointment with primary care physician")
        recommendations.append("Maintain healthy diet and regular exercise")
        recommendations.append("Monitor any symptoms and report changes to doctor")
        
        return recommendations
    
    def _generate_overall_assessment(self, health_score: Dict, risk_factors: Dict) -> str:
        """Generate overall assessment text"""
        score = health_score.get("score", 0)
        status = health_score.get("status", "Unknown")
        risk_count = risk_factors.get("total_risks", 0)
        
        if score >= 85:
            return f"Excellent overall health with score of {score}. Continue healthy lifestyle."
        elif score >= 70:
            return f"Good health with score of {score}. Some areas need monitoring."
        elif score >= 50:
            return f"Fair health with score of {score}. {risk_count} risk factor(s) identified. Medical attention recommended."
        else:
            return f"Health needs attention with score of {score}. {risk_count} risk factor(s) identified. Urgent medical review recommended."