"""
Module: Site Safety & PPE Audit (Epic 2)
Analyzes worker PPE compliance and site hazards under OSHA 1926 and IS 456 / IS 2925 standards.
"""

import streamlit as st
import pandas as pd
from PIL import Image
import io
import json
from modules.ui_components import (
    render_metric_card,
    render_severity_badge,
    render_status_badge,
    render_risk_gauge,
    render_json_download
)
from sample_data.samples import (
    generate_sample_ppe_image,
    DEMO_PPE_AUDIT_DATA
)

SAFETY_AUDIT_SYSTEM_PROMPT = """
You are a Principal Construction Safety Auditor certified in OSHA 1926 Safety & Health Regulations for Construction,
IS 456:2000, IS 2925 (Industrial Safety Helmets), IS 15809 (High-Visibility Warning Clothes), IS 3521 (Industrial Safety Harnesses),
and IS 15298 (Protective Footwear).

Analyze the provided construction site photo with extreme rigor:
1. Detect all visible construction personnel and evaluate their Personal Protective Equipment (PPE).
2. Check for:
   - Industrial Safety Helmets / Hard Hats (OSHA 1926.100, IS 2925)
   - High-Visibility Retroreflective Safety Vests (OSHA 1926.201, IS 15809)
   - Fall Protection / Full Body Harnesses with Lanyard Anchors (OSHA 1926.501, IS 3521)
   - Steel-Toe Safety Footwear (OSHA 1926.96, IS 15298)
   - Eye/Face/Respiratory protection where applicable.
3. Identify all environmental, physical, and operational site hazards (e.g. unprotected edges, scaffolding gaps, crane swing radius, trench shoring, trip hazards).
4. Assign an objective safety_score from 0 to 100 based on standard OSHA violation penalty weighting.
5. Provide actionable engineering and administrative remedies for every hazard found.

Return STRICT JSON complying with this structure:
{
  "safety_score": 75,
  "overall_status": "Compliant" | "Needs Corrective Action" | "Critical Violations",
  "workers_detected": 3,
  "regulatory_framework": "OSHA 1926 / IS 456 / IS 2925",
  "ppe_compliance": [
    {
      "item": "Industrial Safety Helmets",
      "standard": "OSHA 1926.100 / IS 2925",
      "detected_count": "2 of 3 compliant",
      "compliant": false,
      "observation": "Detailed finding"
    }
  ],
  "hazards": [
    {
      "hazard": "Hazard name",
      "severity": "Low" | "Medium" | "High" | "Critical",
      "location_context": "Exact location in scene",
      "corrective_remedy": "Specific corrective remedy citing engineering action",
      "regulatory_code": "OSHA 1926.xxx / IS yyy"
    }
  ],
  "executive_summary": "High-level summary of site condition"
}
"""

def render_site_safety_tab(gemini_client):
    """Render Tab 1: Site Safety & PPE Audit."""
    st.markdown("### 🛡️ Site Safety & Autonomous PPE Compliance Audit")
    st.markdown(
        "Upload real-time CCTV or field drone captures to audit worker PPE compliance "
        "and benchmark jobsite hazards against **OSHA 1926** and Indian Standard **IS 456 / IS 2925** safety codes."
    )

    col_up, col_preview = st.columns([1.1, 1.2], gap="large")

    image_bytes = None
    image_mime = "image/jpeg"
    source_label = ""

    with col_up:
        st.markdown("#### 📤 Input Construction Scene")
        uploader_file = st.file_uploader(
            "Choose a site photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="ppe_uploader",
            help="High-resolution aerial, scaffolding, or ground photos recommended."
        )

        st.markdown("##### ⚡ Quick Demonstration Presets:")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚨 Load Violation Scene", use_container_width=True, key="btn_ppe_viol"):
                st.session_state["ppe_sample_type"] = "violation"
                st.session_state["ppe_image_cache"] = generate_sample_ppe_image("violation")
                st.session_state["ppe_source_label"] = "Preset: Elevated Scaffolding Violations"
        with col_btn2:
            if st.button("✅ Load Compliant Scene", use_container_width=True, key="btn_ppe_comp"):
                st.session_state["ppe_sample_type"] = "compliant"
                st.session_state["ppe_image_cache"] = generate_sample_ppe_image("compliant")
                st.session_state["ppe_source_label"] = "Preset: Fully Equipped Compliant Crew"

        # Determine which image to use
        if uploader_file is not None:
            image_bytes = uploader_file.getvalue()
            image_mime = uploader_file.type
            source_label = f"Uploaded File: {uploader_file.name}"
        elif "ppe_image_cache" in st.session_state:
            image_bytes = st.session_state["ppe_image_cache"]
            source_label = st.session_state.get("ppe_source_label", "Sample Demo Image")

        audit_btn = st.button("🔍 Execute Safety & PPE Audit", type="primary", use_container_width=True, disabled=(image_bytes is None))

    with col_preview:
        st.markdown("#### 📸 Selected Visual Context")
        if image_bytes:
            st.image(image_bytes, caption=source_label, use_container_width=True)
        else:
            st.info("👈 Upload a site photograph or select a quick demonstration preset to begin audit.")

    st.markdown("---")

    # Execution Trigger
    if audit_btn and image_bytes:
        with st.spinner("🤖 Multimodal Engine inspecting worker PPE & surveying site hazards..."):
            prompt = (
                "Conduct a rigorous OSHA 1926 and IS 456 construction safety audit on this image. "
                "Count workers, verify helmet, vest, footwear, and harness compliance. "
                "Identify hazards with severity ratings and specific remedial actions. Return JSON."
            )
            
            # Select demo fallback based on sample type if demo triggered
            fallback = DEMO_PPE_AUDIT_DATA
            if st.session_state.get("ppe_sample_type") == "compliant":
                fallback = {
                    "safety_score": 96,
                    "overall_status": "Compliant",
                    "workers_detected": 2,
                    "regulatory_framework": "OSHA 1926 / IS 456 & IS 2925",
                    "ppe_compliance": [
                        {"item": "Industrial Safety Helmets", "standard": "OSHA 1926.100 / IS 2925", "detected_count": "2 of 2 compliant", "compliant": True, "observation": "All personnel wearing certified yellow Type 1 HDPE hard hats with chin straps secured."},
                        {"item": "High-Visibility Retroreflective Vests", "standard": "OSHA 1926.201 / IS 15809", "detected_count": "2 of 2 compliant", "compliant": True, "observation": "Dual horizontal fluorescent silver reflective bands visible on high-contrast orange garments."},
                        {"item": "Fall Arrest Harness & Anchorage", "standard": "OSHA 1926.501 / IS 3521", "detected_count": "2 of 2 compliant", "compliant": True, "observation": "Full-body fall arrest harnesses with dorsal D-ring and dual lanyard shock absorbers anchored to certified anchor line."},
                        {"item": "Steel-Toe Protective Footwear", "standard": "OSHA 1926.96 / IS 15298", "detected_count": "2 of 2 compliant", "compliant": True, "observation": "Heavy-duty anti-static safety boots with 200J steel toe caps observed."}
                    ],
                    "hazards": [
                        {"hazard": "Minor Material Staging Near Access Path", "severity": "Low", "location_context": "Staging area 3m behind worker", "corrective_remedy": "Ensure 1-meter clear access perimeter is maintained at all times.", "regulatory_code": "OSHA 1926.250"}
                    ],
                    "executive_summary": "Exemplary site safety adherence. Full PPE compliance detected across all workers. Perimeter lifelines actively secured."
                }

            audit_result = gemini_client.analyze_multimodal(
                image_bytes=image_bytes,
                mime_type=image_mime,
                prompt=prompt,
                system_instruction=SAFETY_AUDIT_SYSTEM_PROMPT,
                fallback_data=fallback,
                is_json=True
            )

            st.session_state["ppe_audit_result"] = audit_result

    # Display Results if available
    if "ppe_audit_result" in st.session_state:
        result = st.session_state["ppe_audit_result"]
        st.markdown("### 📋 Executive Safety Audit Dossier")

        # Top KPIs
        score = result.get("safety_score", 70)
        status = result.get("overall_status", "Needs Attention")
        workers = result.get("workers_detected", 0)
        hazards = result.get("hazards", [])
        crit_count = sum(1 for h in hazards if h.get("severity", "").lower() == "critical")

        c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1.2])
        with c1:
            score_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 60 else "#EF4444")
            render_metric_card("Site Safety Score", f"{score}/100", f"OSHA & IS Standard Rating", "🛡️", score_color)
        with c2:
            render_metric_card("Workers Audited", str(workers), "Personnel Detected", "👷", "#38BDF8")
        with c3:
            crit_color = "#EF4444" if crit_count > 0 else "#10B981"
            render_metric_card("Critical Hazards", str(crit_count), "Immediate Action Items", "🚨", crit_color)
        with c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-card-label">Overall Audit Status</div>
                    <div style="margin-top: 0.6rem;">{render_status_badge(status)}</div>
                    <div class="metric-card-subtext" style="margin-top: 0.75rem;">Standard: IS 456 / OSHA 1926</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Executive Summary Callout
        summary_text = result.get("executive_summary", "Site audit completed.")
        st.markdown(
            f"""
            <div class="engineering-callout">
                <h4>📌 Chief Safety Officer Briefing</h4>
                <p>{summary_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Two Column Breakdown: PPE Detection Checklist vs Site Hazards
        col_ppe, col_hazards = st.columns([1.1, 1.3], gap="large")

        with col_ppe:
            st.markdown("#### 🦺 PPE Compliance Matrix")
            ppe_list = result.get("ppe_compliance", [])
            if ppe_list:
                for item in ppe_list:
                    compliant = item.get("compliant", False)
                    icon = "✅" if compliant else "❌"
                    status_text = "COMPLIANT" if compliant else "NON-COMPLIANT"
                    badge_style = "badge-compliant" if compliant else "badge-critical"
                    
                    st.markdown(
                        f"""
                        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <strong style="color: #F8FAFC; font-size: 0.95rem;">{icon} {item.get('item', 'Item')}</strong>
                                <span class="badge {badge_style}">{status_text}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 4px;">
                                <strong>Standard:</strong> <code>{item.get('standard', 'OSHA 1926')}</code> • <strong>Observed:</strong> {item.get('detected_count', 'N/A')}
                            </div>
                            <div style="font-size: 0.85rem; color: #CBD5E1;">{item.get('observation', '')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No individual PPE items cataloged.")

        with col_hazards:
            st.markdown("#### ⚠️ Identified Site Hazards & Engineering Remedies")
            if hazards:
                for idx, h in enumerate(hazards, 1):
                    sev = h.get("severity", "Medium")
                    badge_html = render_severity_badge(sev)
                    
                    with st.expander(f"Hazard #{idx}: {h.get('hazard', 'Unspecified')} ({sev})", expanded=(sev in ["Critical", "High"])):
                        st.markdown(
                            f"""
                            <div style="margin-bottom: 8px;">
                                <strong>Severity Level:</strong> {badge_html} &nbsp;|&nbsp; 
                                <strong>Code Reference:</strong> <code>{h.get('regulatory_code', 'OSHA / IS 456')}</code>
                            </div>
                            <div style="margin-bottom: 8px;">
                                <strong style="color: #94A3B8;">📍 Location Context:</strong> {h.get('location_context', 'General Site Perimeter')}
                            </div>
                            <div style="background: rgba(30, 41, 59, 0.8); border-left: 3px solid #F59E0B; padding: 10px; border-radius: 4px;">
                                <strong style="color: #F59E0B;">🛠️ Mandatory Corrective Remedy:</strong><br/>
                                <span style="color: #F8FAFC; font-size: 0.9rem;">{h.get('corrective_remedy', 'Implement standard safety mitigation.')}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.success("🎉 Zero safety hazards detected! Field operations are within nominal safety parameters.")

        # Download Report Section
        st.markdown("---")
        st.markdown("#### 📥 Export Audit Report")
        d_col1, d_col2 = st.columns([1, 1])
        with d_col1:
            render_json_download(
                result,
                filename="construction_site_safety_audit.json",
                label="📥 Download Structured JSON Safety Report"
            )
        with d_col2:
            summary_txt = f"""MULTIMODAL CONSTRUCTION INTELLIGENCE PLATFORM
SITE SAFETY & PPE AUDIT DOSSIER
==============================================
Safety Compliance Score: {score}/100
Overall Site Status: {status}
Workers Detected: {workers}
Critical Hazards Detected: {crit_count}
Regulatory Framework: {result.get('regulatory_framework', 'OSHA 1926 / IS 456')}

EXECUTIVE SUMMARY:
{summary_text}

PPE DETECTION BREAKDOWN:
"""
            for p in ppe_list:
                c_str = "COMPLIANT" if p.get('compliant') else "NON-COMPLIANT"
                summary_txt += f"- [{c_str}] {p.get('item')} ({p.get('standard')}): {p.get('observation')}\n"

            summary_txt += "\nHAZARDS & ENGINEERING REMEDIES:\n"
            for h in hazards:
                summary_txt += f"- [{h.get('severity')}] {h.get('hazard')} (Ref: {h.get('regulatory_code')}):\n"
                summary_txt += f"  Location: {h.get('location_context')}\n"
                summary_txt += f"  Remedy: {h.get('corrective_remedy')}\n"

            st.download_button(
                label="📄 Download Formatted TXT Field Report",
                data=summary_txt,
                file_name="site_safety_audit_summary.txt",
                mime="text/plain",
                use_container_width=True
            )
