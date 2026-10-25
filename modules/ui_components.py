"""
UI Components, Custom Construction Intelligence Theme, and Interactive Visualizations.
Designed for high-contrast readability, civil engineering aesthetics, and seamless dark/light compatibility.
"""

import streamlit as st
import plotly.graph_objects as go
import json

def apply_custom_theme():
    """Inject polished, modern construction-tech CSS styles."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* Main typography & smoothness */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            letter-spacing: -0.01em;
        }

        /* Construction Tech Header Banner */
        .platform-hero {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-left: 6px solid #F59E0B;
            border-radius: 12px;
            padding: 1.5rem 1.8rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 0 15px rgba(245, 158, 11, 0.08);
        }

        .platform-hero h1 {
            color: #F8FAFC;
            font-size: 2.1rem;
            font-weight: 800;
            margin: 0 0 0.35rem 0;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }

        .platform-hero p {
            color: #94A3B8;
            font-size: 0.95rem;
            margin: 0;
            line-height: 1.5;
        }

        /* Engineering Metric Tile */
        .metric-card {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 12px;
            padding: 1.1rem 1.25rem;
            margin-bottom: 0.75rem;
            backdrop-filter: blur(8px);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(245, 158, 11, 0.4);
        }

        .metric-card-label {
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #94A3B8;
            margin-bottom: 0.35rem;
        }

        .metric-card-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #F8FAFC;
            line-height: 1.2;
            font-family: 'JetBrains Mono', monospace;
        }

        .metric-card-subtext {
            font-size: 0.8rem;
            color: #64748B;
            margin-top: 0.35rem;
        }

        /* Status & Severity Pills */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.28rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .badge-critical {
            background: rgba(239, 68, 68, 0.18);
            color: #FCA5A5;
            border: 1px solid rgba(239, 68, 68, 0.45);
        }

        .badge-high {
            background: rgba(249, 115, 22, 0.18);
            color: #FDBA74;
            border: 1px solid rgba(249, 115, 22, 0.45);
        }

        .badge-medium {
            background: rgba(245, 158, 11, 0.18);
            color: #FDE68A;
            border: 1px solid rgba(245, 158, 11, 0.45);
        }

        .badge-low {
            background: rgba(59, 130, 246, 0.18);
            color: #93C5FD;
            border: 1px solid rgba(59, 130, 246, 0.45);
        }

        .badge-compliant {
            background: rgba(16, 185, 129, 0.18);
            color: #6EE7B7;
            border: 1px solid rgba(16, 185, 129, 0.45);
        }

        .badge-attention {
            background: rgba(245, 158, 11, 0.18);
            color: #FDE047;
            border: 1px solid rgba(245, 158, 11, 0.45);
        }

        /* Engineering Callout Box */
        .engineering-callout {
            background: rgba(15, 23, 42, 0.85);
            border-left: 4px solid #38BDF8;
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
            border-top: 1px solid rgba(56, 189, 248, 0.2);
            border-right: 1px solid rgba(56, 189, 248, 0.1);
            border-bottom: 1px solid rgba(56, 189, 248, 0.1);
        }

        .engineering-callout h4 {
            color: #38BDF8;
            margin: 0 0 0.4rem 0;
            font-size: 0.95rem;
            font-weight: 700;
        }

        .engineering-callout p {
            color: #CBD5E1;
            margin: 0;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        /* Weather Alert Banner */
        .weather-banner-urgent {
            background: linear-gradient(135deg, rgba(220, 38, 38, 0.2) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-left: 5px solid #EF4444;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0B1120;
            border-right: 1px solid rgba(148, 163, 184, 0.1);
        }

        /* Streamlit Tab Customization */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(15, 23, 42, 0.6);
            padding: 6px;
            border-radius: 10px;
            border: 1px solid rgba(148, 163, 184, 0.15);
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            border-radius: 8px;
            font-weight: 600;
            color: #94A3B8;
            padding: 0 16px;
            border: none;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background-color: #F59E0B !important;
            color: #0F172A !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
        }

        /* Code & Monospace blocks */
        code {
            font-family: 'JetBrains Mono', monospace !important;
            background: rgba(15, 23, 42, 0.8) !important;
            color: #F59E0B !important;
            border-radius: 4px;
            padding: 2px 6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_hero_banner():
    """Render top application brand banner."""
    st.markdown(
        """
        <div class="platform-hero">
            <h1>🏗️ Multimodal Construction Intelligence Platform</h1>
            <p>
                <strong>Autonomous Civil Engineering & Site Safety AI Suite</strong> • Powered by Google Gemini Vision & Deep Reasoning • 
                Calibrated to <code>OSHA 1926</code>, <code>IS 456:2000</code>, <code>IS 875</code>, and National Building Code of India (NBC).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric_card(title: str, value: str, subtext: str = "", icon: str = "📊", value_color: str = "#F8FAFC"):
    """Render a styled metric tile."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-card-label">{icon} {title}</div>
            <div class="metric-card-value" style="color: {value_color};">{value}</div>
            <div class="metric-card-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_severity_badge(severity: str) -> str:
    """Return HTML string for severity badge."""
    sev = severity.strip().capitalize()
    if sev == "Critical":
        return f'<span class="badge badge-critical">🚨 CRITICAL</span>'
    elif sev == "High":
        return f'<span class="badge badge-high">⚠️ HIGH</span>'
    elif sev == "Medium":
        return f'<span class="badge badge-medium">⚡ MEDIUM</span>'
    else:
        return f'<span class="badge badge-low">ℹ️ LOW</span>'


def render_status_badge(status: str) -> str:
    """Return HTML string for overall status badge."""
    stat_lower = status.lower()
    if "compliant" in stat_lower and "not" not in stat_lower and "non" not in stat_lower:
        return f'<span class="badge badge-compliant">✅ COMPLIANT</span>'
    elif "critical" in stat_lower or "violation" in stat_lower:
        return f'<span class="badge badge-critical">🛑 CRITICAL VIOLATIONS</span>'
    else:
        return f'<span class="badge badge-attention">⚠️ ACTION REQUIRED</span>'


def render_risk_gauge(score: int, title: str = "Structural Health Index", max_val: int = 100):
    """Render a high-precision Plotly circular gauge chart."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": title, "font": {"size": 16, "color": "#E2E8F0"}},
            number={"suffix": "/100", "font": {"size": 28, "color": "#F8FAFC", "family": "JetBrains Mono"}},
            gauge={
                "axis": {"range": [0, max_val], "tickwidth": 1, "tickcolor": "#64748B"},
                "bar": {"color": "#F59E0B", "thickness": 0.28},
                "bgcolor": "#1E293B",
                "borderwidth": 1,
                "bordercolor": "#334155",
                "steps": [
                    {"range": [0, 40], "color": "rgba(239, 68, 68, 0.45)"},
                    {"range": [40, 75], "color": "rgba(245, 158, 11, 0.45)"},
                    {"range": [75, 100], "color": "rgba(16, 185, 129, 0.45)"},
                ],
                "threshold": {
                    "line": {"color": "#EF4444", "width": 3},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC"},
        height=240,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def render_json_download(data: dict, filename: str, label: str = "📥 Download JSON Dossier"):
    """Helper to offer downloadable JSON."""
    json_str = json.dumps(data, indent=2)
    st.download_button(
        label=label,
        data=json_str,
        file_name=filename,
        mime="application/json",
        use_container_width=True
    )
