import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime

class VisualizationService:
    """Generate medical visualizations and charts"""
    
    def generate_chart(self, chart_type: str, data: Dict) -> Dict:
        """Generate chart based on type and data"""
        
        chart_methods = {
            "blood_work": self.generate_blood_work_chart,
            "vital_signs": self.generate_vital_signs_chart,
            "risk_assessment": self.generate_risk_assessment_chart,
            "health_timeline": self.generate_health_timeline,
            "medication_schedule": self.generate_medication_schedule,
            "lab_trends": self.generate_lab_trends_chart,
            "health_score": self.generate_health_score_chart,
            "body_systems": self.generate_body_systems_chart
        }
        
        if chart_type in chart_methods:
            return chart_methods[chart_type](data)
        else:
            return self.generate_default_chart(data)
    
    def generate_blood_work_chart(self, data: Dict) -> Dict:
        """Generate blood work results chart"""
        
        # Prepare data
        tests = []
        values = []
        references_min = []
        references_max = []
        colors = []
        status_texts = []
        
        for test_name, test_data in data.get("results", {}).items():
            tests.append(test_name.upper())
            values.append(test_data.get("value", 0))
            references_min.append(test_data.get("min_reference", 0))
            references_max.append(test_data.get("max_reference", 0))
            colors.append(test_data.get("color", "#6B7280"))
            status_texts.append(test_data.get("status_text", "Unknown"))
        
        # Create figure
        fig = go.Figure()
        
        # Add reference range area
        fig.add_trace(go.Scatter(
            x=tests,
            y=references_max,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            name='Reference Max'
        ))
        
        fig.add_trace(go.Scatter(
            x=tests,
            y=references_min,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(100, 200, 100, 0.2)',
            showlegend=False,
            name='Reference Range'
        ))
        
        # Add actual values
        fig.add_trace(go.Bar(
            x=tests,
            y=values,
            marker_color=colors,
            text=status_texts,
            textposition='outside',
            name='Your Results'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text="Blood Work Results Analysis",
                font=dict(size=20, family="Arial", color="#1F2937")
            ),
            xaxis=dict(
                title="Test Type",
                tickangle=45,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title="Value",
                gridcolor='lightgray'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            hovermode='x unified',
            height=500
        )
        
        # Add annotations for critical values
        for i, (test, value) in enumerate(zip(tests, values)):
            ref_min = references_min[i]
            ref_max = references_max[i]
            if value < ref_min * 0.9 or value > ref_max * 1.1:
                fig.add_annotation(
                    x=test,
                    y=value,
                    text="⚠️",
                    showarrow=False,
                    font=dict(size=20),
                    yshift=30
                )
        
        # Convert to HTML
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        return {
            "chart_type": "blood_work",
            "chart_html": chart_html,
            "data_summary": {
                "total_tests": len(tests),
                "normal": sum(1 for s in status_texts if s == "Normal"),
                "abnormal": sum(1 for s in status_texts if s != "Normal"),
                "critical": sum(1 for s in status_texts if s == "Critical")
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_vital_signs_chart(self, data: Dict) -> Dict:
        """Generate vital signs dashboard"""
        
        vitals = data.get("vitals", {
            "heart_rate": {"value": 72, "unit": "bpm", "status": "normal"},
            "blood_pressure": {"systolic": 120, "diastolic": 80, "status": "normal"},
            "temperature": {"value": 98.6, "unit": "°F", "status": "normal"},
            "respiratory_rate": {"value": 16, "unit": "breaths/min", "status": "normal"},
            "oxygen_saturation": {"value": 98, "unit": "%", "status": "normal"}
        })
        
        # Create gauge charts for each vital
        charts = []
        
        for vital_name, vital_data in vitals.items():
            if isinstance(vital_data, dict) and "value" in vital_data:
                value = vital_data["value"]
                status = vital_data.get("status", "normal")
                unit = vital_data.get("unit", "")
                
                # Define ranges based on vital
                if vital_name == "heart_rate":
                    min_val, max_val = 40, 120
                    threshold_colors = ["#EF4444", "#F59E0B", "#10B981", "#F59E0B", "#EF4444"]
                    threshold_values = [40, 60, 80, 100, 120]
                elif vital_name == "blood_pressure":
                    # Handle blood pressure separately
                    continue
                elif vital_name == "temperature":
                    min_val, max_val = 95, 104
                    threshold_colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444"]
                    threshold_values = [95, 97, 99, 104]
                else:
                    min_val, max_val = value * 0.5, value * 1.5
                    threshold_colors = ["#10B981", "#F59E0B", "#EF4444"]
                    threshold_values = [min_val, (min_val + max_val) / 2, max_val]
                
                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=value,
                    title=dict(text=f"{vital_name.replace('_', ' ').title()}"),
                    domain=dict(x=[0, 1], y=[0, 1]),
                    gauge=dict(
                        axis=dict(range=[min_val, max_val]),
                        bar=dict(color= self._get_status_color(status)),
                        steps=[
                            dict(range=[threshold_values[i], threshold_values[i+1]], 
                                 color=threshold_colors[i])
                            for i in range(len(threshold_colors)-1)
                        ],
                        threshold=dict(
                            line=dict(color="black", width=4),
                            thickness=0.75,
                            value=value
                        )
                    ),
                    number=dict(suffix=f" {unit}")
                ))
                
                fig.update_layout(
                    height=250,
                    margin=dict(l=10, r=10, t=50, b=10),
                    paper_bgcolor='white'
                )
                
                chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
                charts.append({
                    "name": vital_name,
                    "chart": chart_html,
                    "value": value,
                    "unit": unit,
                    "status": status
                })
        
        # Special handling for blood pressure
        if "blood_pressure" in vitals:
            bp_data = vitals["blood_pressure"]
            fig = go.Figure()
            
            fig.add_trace(go.Indicator(
                mode="number+gauge",
                value=bp_data.get("systolic", 120),
                title=dict(text="Systolic BP"),
                domain=dict(row=0, column=0),
                gauge=dict(
                    axis=dict(range=[80, 180]),
                    bar=dict(color="#3B82F6"),
                    steps=[
                        dict(range=[80, 120], color="#10B981"),
                        dict(range=[120, 130], color="#F59E0B"),
                        dict(range=[130, 180], color="#EF4444")
                    ]
                ),
                number=dict(suffix=" mmHg")
            ))
            
            fig.add_trace(go.Indicator(
                mode="number+gauge",
                value=bp_data.get("diastolic", 80),
                title=dict(text="Diastolic BP"),
                domain=dict(row=0, column=1),
                gauge=dict(
                    axis=dict(range=[40, 120]),
                    bar=dict(color="#3B82F6"),
                    steps=[
                        dict(range=[40, 80], color="#10B981"),
                        dict(range=[80, 90], color="#F59E0B"),
                        dict(range=[90, 120], color="#EF4444")
                    ]
                ),
                number=dict(suffix=" mmHg")
            ))
            
            fig.update_layout(
                grid=dict(rows=1, columns=2),
                height=300,
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor='white'
            )
            
            chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
            charts.append({
                "name": "blood_pressure",
                "chart": chart_html,
                "systolic": bp_data.get("systolic"),
                "diastolic": bp_data.get("diastolic"),
                "status": bp_data.get("status", "normal")
            })
        
        # Create dashboard HTML
        dashboard_html = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 20px;">
            {''.join([chart['chart'] for chart in charts])}
        </div>
        """
        
        return {
            "chart_type": "vital_signs",
            "dashboard_html": dashboard_html,
            "charts": charts,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_risk_assessment_chart(self, data: Dict) -> Dict:
        """Generate risk assessment radar chart"""
        
        risks = data.get("risks", [
            {"category": "Cardiovascular", "score": 65},
            {"category": "Metabolic", "score": 45},
            {"category": "Renal", "score": 30},
            {"category": "Respiratory", "score": 25},
            {"category": "Neurological", "score": 20},
            {"category": "Immunological", "score": 15}
        ])
        
        categories = [r["category"] for r in risks]
        scores = [r["score"] for r in risks]
        
        # Close the radar chart
        categories = categories + [categories[0]]
        scores = scores + [scores[0]]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            fillcolor='rgba(59, 130, 246, 0.3)',
            line=dict(color='rgb(59, 130, 246)'),
            name='Risk Score'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='lightgray',
                    angle=45
                ),
                angularaxis=dict(
                    gridcolor='lightgray',
                    linecolor='gray'
                )
            ),
            showlegend=False,
            title=dict(
                text="Health Risk Assessment",
                font=dict(size=18, family="Arial")
            ),
            paper_bgcolor='white',
            height=500
        )
        
        # Add risk zones
        fig.add_trace(go.Scatterpolar(
            r=[20, 20, 20, 20, 20, 20, 20],
            theta=categories,
            fill='toself',
            fillcolor='rgba(16, 185, 129, 0.2)',
            line=dict(color='rgba(16, 185, 129, 0)'),
            name='Low Risk'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[50, 50, 50, 50, 50, 50, 50],
            theta=categories,
            fill='tonext',
            fillcolor='rgba(245, 158, 11, 0.2)',
            line=dict(color='rgba(245, 158, 11, 0)'),
            name='Medium Risk'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[80, 80, 80, 80, 80, 80, 80],
            theta=categories,
            fill='tonext',
            fillcolor='rgba(239, 68, 68, 0.2)',
            line=dict(color='rgba(239, 68, 68, 0)'),
            name='High Risk'
        ))
        
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # Calculate overall risk
        avg_score = sum(scores[:-1]) / len(scores[:-1]) if len(scores) > 1 else 0
        
        return {
            "chart_type": "risk_assessment",
            "chart_html": chart_html,
            "risk_summary": {
                "overall_risk": round(avg_score, 1),
                "highest_risk": max(scores[:-1]) if scores else 0,
                "highest_category": categories[scores.index(max(scores[:-1]))] if scores else "None",
                "risk_level": "Low" if avg_score < 30 else "Medium" if avg_score < 60 else "High"
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_health_timeline(self, data: Dict) -> Dict:
        """Generate health timeline visualization"""
        
        events = data.get("events", [
            {"date": "2023-01-15", "event": "Annual Checkup", "type": "checkup", "status": "completed"},
            {"date": "2023-03-22", "event": "Lab Tests", "type": "lab", "status": "completed"},
            {"date": "2023-06-10", "event": "Cardiology Consultation", "type": "consultation", "status": "completed"},
            {"date": "2023-09-05", "event": "Medication Adjustment", "type": "medication", "status": "completed"},
            {"date": "2024-01-20", "event": "Next Checkup", "type": "checkup", "status": "scheduled"}
        ])
        
        # Sort events by date
        events.sort(key=lambda x: x["date"])
        
        # Prepare data
        dates = [e["date"] for e in events]
        event_names = [e["event"] for e in events]
        event_types = [e["type"] for e in events]
        statuses = [e.get("status", "completed") for e in events]
        
        # Color mapping
        type_colors = {
            "checkup": "#3B82F6",
            "lab": "#10B981",
            "consultation": "#8B5CF6",
            "medication": "#F59E0B",
            "procedure": "#EF4444"
        }
        
        status_symbols = {
            "completed": "●",
            "scheduled": "○",
            "cancelled": "✕",
            "pending": "◌"
        }
        
        # Create timeline
        fig = go.Figure()
        
        for i, (date, event, event_type, status) in enumerate(zip(dates, event_names, event_types, statuses)):
            color = type_colors.get(event_type, "#6B7280")
            symbol = status_symbols.get(status, "●")
            
            fig.add_trace(go.Scatter(
                x=[date],
                y=[i],
                mode='markers+text',
                marker=dict(
                    size=20,
                    color=color,
                    symbol=symbol,
                    line=dict(width=2, color='white')
                ),
                text=[event],
                textposition="right",
                textfont=dict(size=12),
                name=event_type,
                hovertemplate=f"<b>{event}</b><br>Date: {date}<br>Type: {event_type}<br>Status: {status}<extra></extra>"
            ))
        
        # Add connecting lines
        for i in range(len(dates)-1):
            fig.add_trace(go.Scatter(
                x=[dates[i], dates[i+1]],
                y=[i, i+1],
                mode='lines',
                line=dict(color='lightgray', width=1, dash='dash'),
                showlegend=False,
                hoverinfo='none'
            ))
        
        fig.update_layout(
            title=dict(
                text="Medical Timeline",
                font=dict(size=18, family="Arial")
            ),
            xaxis=dict(
                title="Date",
                gridcolor='lightgray',
                showgrid=True
            ),
            yaxis=dict(
                visible=False
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            hovermode='closest'
        )
        
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        return {
            "chart_type": "health_timeline",
            "chart_html": chart_html,
            "timeline_summary": {
                "total_events": len(events),
                "completed": sum(1 for e in events if e.get("status") == "completed"),
                "upcoming": sum(1 for e in events if e.get("status") in ["scheduled", "pending"]),
                "last_event": events[-1]["event"] if events else "None",
                "next_event": next((e for e in events if e.get("status") in ["scheduled", "pending"]), {}).get("event", "None")
            },
            "generated_at": datetime.now().isoformat()
        }
    
    def _get_status_color(self, status: str) -> str:
        """Get color based on status"""
        colors = {
            "normal": "#10B981",
            "good": "#10B981",
            "borderline": "#F59E0B",
            "warning": "#F97316",
            "critical": "#EF4444",
            "high": "#EF4444",
            "medium": "#F59E0B",
            "low": "#10B981"
        }
        return colors.get(status, "#6B7280")
    
    def generate_default_chart(self, data: Dict) -> Dict:
        """Generate default chart when type not specified"""
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="number",
            value=data.get("value", 0),
            title=dict(text="Health Metric"),
            number=dict(font=dict(size=48))
        ))
        
        fig.update_layout(
            paper_bgcolor='white',
            height=300
        )
        
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        return {
            "chart_type": "default",
            "chart_html": chart_html,
            "message": "Default chart generated",
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_lab_trends_chart(self, data: Dict) -> Dict:
        """Generate lab trends over time"""
        trends = data.get("trends", {})
        
        if not trends:
            return {"error": "No trend data available"}
        
        fig = go.Figure()
        
        for test_name, trend_data in trends.items():
            if "values" in trend_data and "dates" in trend_data:
                dates = trend_data["dates"]
                values = trend_data["values"]
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    name=test_name.upper(),
                    line=dict(width=2),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title=dict(
                text="Lab Results Trends Over Time",
                font=dict(size=18, family="Arial")
            ),
            xaxis=dict(
                title="Date",
                gridcolor='lightgray',
                showgrid=True
            ),
            yaxis=dict(
                title="Value",
                gridcolor='lightgray',
                showgrid=True
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            height=500,
            hovermode='x unified'
        )
        
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        return {
            "chart_type": "lab_trends",
            "chart_html": chart_html,
            "trends_analyzed": len(trends),
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_health_score_chart(self, data: Dict) -> Dict:
        """Generate health score gauge chart"""
        
        health_score = data.get("score", 75)
        max_score = data.get("max_score", 100)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title=dict(text="Overall Health Score"),
            domain=dict(x=[0, 1], y=[0, 1]),
            gauge=dict(
                axis=dict(range=[0, max_score]),
                bar=dict(color=self._get_health_score_color(health_score, max_score)),
                steps=[
                    dict(range=[0, max_score*0.4], color="#EF4444"),
                    dict(range=[max_score*0.4, max_score*0.7], color="#F59E0B"),
                    dict(range=[max_score*0.7, max_score*0.85], color="#3B82F6"),
                    dict(range=[max_score*0.85, max_score], color="#10B981")
                ],
                threshold=dict(
                    line=dict(color="black", width=4),
                    thickness=0.75,
                    value=health_score
                )
            ),
            number=dict(suffix=f"/{max_score}", font=dict(size=40))
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=80, b=20),
            paper_bgcolor='white',
            font=dict(family="Arial")
        )
        
        # Add status text
        status_text = self._get_health_status_text(health_score, max_score)
        fig.add_annotation(
            x=0.5,
            y=0.3,
            text=status_text,
            showarrow=False,
            font=dict(size=16, color=self._get_health_score_color(health_score, max_score))
        )
        
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        return {
            "chart_type": "health_score",
            "chart_html": chart_html,
            "score": health_score,
            "max_score": max_score,
            "status": status_text,
            "generated_at": datetime.now().isoformat()
        }
    
    def _get_health_score_color(self, score: float, max_score: float) -> str:
        """Get color for health score"""
        percentage = (score / max_score) * 100
        
        if percentage >= 85:
            return "#10B981"
        elif percentage >= 70:
            return "#3B82F6"
        elif percentage >= 50:
            return "#F59E0B"
        else:
            return "#EF4444"
    
    def _get_health_status_text(self, score: float, max_score: float) -> str:
        """Get status text for health score"""
        percentage = (score / max_score) * 100
        
        if percentage >= 85:
            return "Excellent Health"
        elif percentage >= 70:
            return "Good Health"
        elif percentage >= 50:
            return "Fair Health"
        elif percentage >= 30:
            return "Needs Improvement"
        else:
            return "Needs Attention"
    
    def generate_body_systems_chart(self, data: Dict) -> Dict:
        """Generate body systems overview chart"""
        
        systems = data.get("systems", {
            "Cardiovascular": {"score": 85, "issues": ["Slightly high LDL"]},
            "Respiratory": {"score": 90, "issues": []},
            "Digestive": {"score": 75, "issues": ["Occasional heartburn"]},
            "Musculoskeletal": {"score": 80, "issues": ["Mild back pain"]},
            "Neurological": {"score": 95, "issues": []},
            "Endocrine": {"score": 70, "issues": ["Borderline glucose"]},
            "Renal": {"score": 88, "issues": []},
            "Immune": {"score": 85, "issues": []}
        })
        
        categories = list(systems.keys())
        scores = [systems[cat]["score"] for cat in categories]
        issues = [len(systems[cat].get("issues", [])) for cat in categories]
        
        # Create bar chart
        fig = go.Figure()
        
        # Add health score bars
        fig.add_trace(go.Bar(
            x=categories,
            y=scores,
            name="Health Score",
            marker_color=[self._get_health_score_color(score, 100) for score in scores],
            text=scores,
            textposition='auto',
            hovertemplate="<b>%{x}</b><br>Score: %{y}<br>Issues: %{customdata}<extra></extra>",
            customdata=issues
        ))
        
        # Add issues overlay
        fig.add_trace(go.Scatter(
            x=categories,
            y=[max(scores) + 5] * len(categories),
            mode='markers',
            marker=dict(
                size=[i * 5 + 10 for i in issues],
                color='rgba(239, 68, 68, 0.5)',
                symbol='circle',
                line=dict(width=1, color='rgba(239, 68, 68, 1)')
            ),
            name="Issues",
            text=[f"{i} issue(s)" if i != 1 else "1 issue" for i in issues],
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>"
        ))
        
        fig.update_layout(
            title=dict(
                text="Body Systems Health Overview",
                font=dict(size=18, family="Arial")
            ),
            xaxis=dict(
                title="Body System",
                tickangle=45,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title="Health Score (0-100)",
                range=[0, 105],
                gridcolor='lightgray'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            barmode='group',
            height=500,
            hovermode='x unified'
        )
        
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # Calculate summary
        total_issues = sum(issues)
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            "chart_type": "body_systems",
            "chart_html": chart_html,
            "summary": {
                "systems_analyzed": len(systems),
                "average_score": round(avg_score, 1),
                "total_issues": total_issues,
                "best_system": categories[scores.index(max(scores))] if scores else "None",
                "needs_attention": [cat for cat, issue_count in zip(categories, issues) if issue_count > 0]
            },
            "generated_at": datetime.now().isoformat()
        }