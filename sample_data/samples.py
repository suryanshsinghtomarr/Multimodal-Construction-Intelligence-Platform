"""
Sample Data and Synthetic Visual Generators for Multimodal Construction Intelligence Platform.
Generates realistic sample images for PPE and Concrete Crack testing so users can test immediately.
"""

import io
from PIL import Image, ImageDraw, ImageFont

def generate_sample_ppe_image(scenario: str = "violation") -> bytes:
    """Generate a stylized visual representation of a construction site for PPE testing."""
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color="#1E293B")
    draw = ImageDraw.Draw(img)

    # Background: Construction site sky and building structure
    draw.rectangle([(0, 0), (width, 300)], fill="#334155")
    # Concrete high-rise framework
    for x in range(50, width, 180):
        draw.rectangle([(x, 80), (x + 30, 550)], fill="#475569")  # Columns
    for y in range(120, 550, 100):
        draw.rectangle([(20, y), (width - 20, y + 20)], fill="#64748B")  # Beams
    
    # Scaffolding / Crane boom in background
    draw.line([(100, 150), (450, 40)], fill="#F59E0B", width=8)
    draw.line([(450, 40), (750, 150)], fill="#F59E0B", width=6)
    draw.line([(450, 40), (450, 220)], fill="#E2E8F0", width=3)  # Hoist cable

    # Site Ground
    draw.rectangle([(0, 520), (width, height)], fill="#78350F")  # Mud/gravel earth

    if scenario == "violation":
        # Worker 1: Standing on beam at height WITHOUT harness & WITHOUT helmet
        # Body
        draw.rectangle([(280, 240), (330, 340)], fill="#3B82F6")  # Blue jacket (NO HIGH-VIS VEST)
        # Head (NO HARD HAT - brown hair)
        draw.ellipse([(285, 205), (325, 240)], fill="#FCD34D")
        draw.ellipse([(285, 205), (325, 220)], fill="#451A03")  # Hair
        # Legs
        draw.rectangle([(285, 340), (305, 420)], fill="#1E293B")  # Pants
        draw.rectangle([(310, 340), (330, 420)], fill="#1E293B")
        # Boots (regular sneakers, not steel toe)
        draw.rectangle([(280, 420), (305, 435)], fill="#DC2626")  # Red sneakers

        # Worker 2: On ground with helmet but NO vest
        draw.rectangle([(550, 380), (600, 470)], fill="#6B7280")  # Grey shirt
        draw.ellipse([(555, 345), (595, 380)], fill="#FCD34D")  # Face
        # Yellow Hard Hat
        draw.arc([(550, 335), (600, 365)], 180, 360, fill="#FBBF24", width=12)
        # Legs
        draw.rectangle([(555, 470), (575, 540)], fill="#1E3A8A")
        draw.rectangle([(580, 470), (600, 540)], fill="#1E3A8A")

        # Warning Overlay Badge
        draw.rectangle([(40, 30), (440, 75)], fill="#DC2626")
        draw.text((55, 42), "SAMPLE 1: ELEVATED WORKING VIOLATIONS", fill="#FFFFFF")

    else:
        # Compliant Crew: 2 workers fully equipped
        # Worker 1: Full PPE
        draw.rectangle([(280, 240), (330, 340)], fill="#F97316")  # High-vis orange vest
        # Reflective stripes
        draw.line([(280, 270), (330, 270)], fill="#F8FAFC", width=5)
        draw.line([(280, 300), (330, 300)], fill="#F8FAFC", width=5)
        # Face & Hard Hat
        draw.ellipse([(285, 205), (325, 240)], fill="#FCD34D")
        draw.chord([(280, 195), (330, 230)], 180, 360, fill="#EAB308", outline="#CA8A04")  # Yellow Hard Hat
        # Safety harness strap
        draw.line([(288, 240), (322, 340)], fill="#047857", width=4)
        draw.line([(322, 240), (288, 340)], fill="#047857", width=4)
        # Legs & Steel toe boots
        draw.rectangle([(285, 340), (305, 420)], fill="#1E293B")
        draw.rectangle([(310, 340), (330, 420)], fill="#1E293B")
        draw.rectangle([(280, 420), (305, 435)], fill="#78350F")  # Heavy steel-toe work boot
        draw.rectangle([(310, 420), (335, 435)], fill="#78350F")

        # Compliant Badge
        draw.rectangle([(40, 30), (430, 75)], fill="#059669")
        draw.text((55, 42), "SAMPLE 2: FULLY COMPLIANT SITE CREW", fill="#FFFFFF")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def generate_sample_crack_image(crack_type: str = "shear") -> bytes:
    """Generate a stylized visual representation of concrete surface defects for crack diagnostics."""
    width, height = 800, 600
    # Concrete texture background (greyish slate with slight speckles)
    img = Image.new("RGB", (width, height), color="#64748B")
    draw = ImageDraw.Draw(img)

    # Concrete panel formwork joints
    draw.line([(0, 300), (width, 300)], fill="#475569", width=3)
    draw.line([(400, 0), (400, height)], fill="#475569", width=3)

    if crack_type == "shear":
        # 45-degree Structural Shear Crack near Beam Support
        # Main jagged diagonal fracture
        crack_points = [
            (220, 120), (260, 160), (280, 180), (310, 220), 
            (350, 270), (390, 310), (420, 360), (460, 410),
            (500, 470), (540, 520)
        ]
        # Crack shadow and primary fissure
        draw.line(crack_points, fill="#0F172A", width=8)
        # Secondary branching micro-cracks
        draw.line([(310, 220), (340, 230), (370, 225)], fill="#1E293B", width=4)
        draw.line([(420, 360), (450, 380), (470, 430)], fill="#1E293B", width=4)
        draw.line([(260, 160), (280, 140)], fill="#1E293B", width=3)

        # Dimension annotation overlay
        draw.line([(425, 340), (445, 375)], fill="#EF4444", width=3)
        draw.rectangle([(40, 30), (450, 75)], fill="#B91C1C")
        draw.text((55, 42), "SAMPLE: 45 DEG STRUCTURAL SHEAR CRACK", fill="#FFFFFF")

    elif crack_type == "spalling":
        # Concrete Spalling with exposed corroded reinforcement bars
        # Delaminated irregular spall crater
        draw.ellipse([(260, 180), (560, 440)], fill="#334155", outline="#1E293B", width=4)
        draw.ellipse([(290, 210), (530, 410)], fill="#1E293B")
        
        # Corroded Rebar exposed inside crater
        draw.rectangle([(240, 270), (580, 295)], fill="#B45309")  # Rust rebar horizontal
        draw.rectangle([(380, 160), (405, 460)], fill="#9A3412")  # Rust rebar vertical
        # Rust stain runoffs
        draw.line([(350, 440), (340, 550)], fill="#78350F", width=8)
        draw.line([(420, 440), (430, 570)], fill="#78350F", width=12)

        draw.rectangle([(40, 30), (450, 75)], fill="#C2410C")
        draw.text((55, 42), "SAMPLE: CONCRETE SPALLING & REBAR RUST", fill="#FFFFFF")

    else:
        # Hairline drying shrinkage network
        hairline_pts1 = [(150, 200), (230, 220), (310, 215), (390, 240), (470, 235), (550, 250), (620, 245)]
        hairline_pts2 = [(310, 215), (330, 300), (360, 360), (390, 440)]
        draw.line(hairline_pts1, fill="#1E293B", width=2)
        draw.line(hairline_pts2, fill="#1E293B", width=2)

        draw.rectangle([(40, 30), (450, 75)], fill="#D97706")
        draw.text((55, 42), "SAMPLE: HAIRLINE DRYING SHRINKAGE", fill="#FFFFFF")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


# Pre-computed realistic mock simulation outputs for demonstration mode fallback
DEMO_PPE_AUDIT_DATA = {
    "safety_score": 62,
    "overall_status": "Needs Corrective Action",
    "workers_detected": 4,
    "regulatory_framework": "OSHA 1926 Safety & Health Regulations for Construction / IS 456 & IS 2925",
    "ppe_compliance": [
        {
            "item": "Industrial Safety Helmets (Hard Hats)",
            "standard": "OSHA 1926.100 / IS 2925:1984",
            "detected_count": "2 of 4 compliant",
            "compliant": False,
            "observation": "2 elevated workers observed without mandatory high-density polyethylene (HDPE) hard hats near crane lifting zone."
        },
        {
            "item": "High-Visibility Retroreflective Vests",
            "standard": "OSHA 1926.201 / IS 15809:2017 Class 2",
            "detected_count": "1 of 4 compliant",
            "compliant": False,
            "observation": "3 ground crew personnel wearing standard non-reflective civil clothing in active transit vehicle perimeter."
        },
        {
            "item": "Fall Arrest Harness & Lanyard Anchorage",
            "standard": "OSHA 1926.501 / IS 3521:1999 (Full Body Harness)",
            "detected_count": "0 of 2 elevated workers attached",
            "compliant": False,
            "observation": "Elevated workers on beam level (+8.5m) lack dual-lanyard shock-absorbing tie-offs to structural lifelines."
        },
        {
            "item": "Steel-Toe Protective Safety Footwear",
            "standard": "OSHA 1926.96 / IS 15298:2016 Part 2",
            "detected_count": "3 of 4 compliant",
            "compliant": True,
            "observation": "Adequate puncture-resistant steel toe footwear observed on majority of ground handling personnel."
        }
    ],
    "hazards": [
        {
            "hazard": "Fall from Height Hazard without Fall Protection (>6ft / 1.8m)",
            "severity": "Critical",
            "location_context": "Upper floor edge beam perimeter without guardrails or static lifeline.",
            "corrective_remedy": "Immediately halt work at height. Install OSHA-compliant perimeter toe-boards and static safety lifelines (IS 3521). Enforce 100% tie-off policy before resuming.",
            "regulatory_code": "OSHA 1926.501(b)(1) & IS 456 Cl. 40"
        },
        {
            "hazard": "Overhead Suspended Load Impact Risk",
            "severity": "High",
            "location_context": "Tower crane hook boom radius intersecting active worker ground walkway.",
            "corrective_remedy": "Demarcate crane swing radius with hazard caution tape. Appoint a dedicated certified rigger/banksman and prohibit ground personnel from standing under suspended loads.",
            "regulatory_code": "OSHA 1926.1424 / IS 13367"
        },
        {
            "hazard": "Lack of High-Visibility Garments in Mobile Machinery Zone",
            "severity": "Medium",
            "location_context": "Excavation earthmover maneuvering within 5 meters of ground team.",
            "corrective_remedy": "Issue fluorescent EN471/IS 15809 Class 2 vests with reflective tape to all personnel prior to site ingress.",
            "regulatory_code": "IS 15809 & OSHA 1926.200"
        },
        {
            "hazard": "Housekeeping & Trip Hazards from Discarded Binding Wire & Shuttering Boards",
            "severity": "Low",
            "location_context": "Ground level accessway adjacent to rebar bending yard.",
            "corrective_remedy": "Implement mandatory end-of-shift housekeeping protocol. Clear protruding nails and binding wire coils into designated scrap bins.",
            "regulatory_code": "OSHA 1926.25"
        }
    ],
    "executive_summary": "Site safety audit indicates substantial non-compliance regarding elevated fall protection and hard hat enforcement. 1 Critical hazard and 1 High severity hazard detected. Immediate administrative stop-work order is advised for upper level perimeter shuttering activities until lifelines and PPE compliance are rectified."
}

DEMO_CRACK_DATA = {
    "defect_type": "Structural Shear Crack",
    "defect_category": "Diagonal Tension Shear Failure near RCC Beam-Column Junction",
    "estimated_crack_width_mm": "3.2 mm (Critical width > 0.3 mm permissible limit)",
    "structural_risk_level": "High",
    "urgency": "Urgent Action (48-72 Hours)",
    "applicable_codes": ["IS 456:2000 Cl. 35.3.2 (Crack Width Criteria)", "ACI 224R-01", "IS 13920:2016 (Ductile Detailing)"],
    "root_causes": [
        "Excessive diagonal tension shear stresses exceeding concrete shear capacity (tau_c) at junction zone.",
        "Inadequate or improperly spaced shear stirrups / link ties near support face (non-compliance with IS 13920 Cl. 6).",
        "Overloading of upper floor slab or differential settlement causing diagonal flexure-shear propagation.",
        "Micro-cracking accelerated by poor aggregate interlock and high water-cement ratio during placement."
    ],
    "recommended_repairs": [
        {
            "method": "Structural Propping & Load Relief",
            "material_spec": "Heavy-duty Acrow props / hydraulic shores rated for 150 kN",
            "procedure": "Install adjustable structural shores beneath beam at 1.0m intervals to relieve live and dead load stresses prior to intervention.",
            "standard_reference": "IS 456 Cl. 40.2"
        },
        {
            "method": "Low-Viscosity Epoxy Resin Pressure Injection",
            "material_spec": "ASTM C881 Type I/IV Grade 1 low-viscosity structural epoxy (viscosity < 200 cps)",
            "procedure": "Drill entry ports at 150mm intervals along crack line. Seal surface with epoxy paste, perform water/air pressure test, and inject resin at 0.2-0.4 MPa until refusal to restore monolithic shear transfer.",
            "standard_reference": "IS 15809 / ACI 503.7"
        },
        {
            "method": "External Shear Reinforcement via CFRP Laminates",
            "material_spec": "High-tensile unidirectional Carbon Fiber Reinforced Polymer (CFRP) fabric (300 gsm, tensile strength > 3800 MPa)",
            "procedure": "Mechanically profile concrete surface, apply epoxy primer, and bond U-jacket CFRP wraps around beam cross-section anchored to top slab to compensate for internal stirrup deficiency.",
            "standard_reference": "ACI 440.2R-17 / Fib Bulletin 14"
        }
    ],
    "structural_impact": "Severe reduction in ultimate shear capacity. If left untreated, cyclic dynamic loads will propagate crack through beam web into compression zone, inducing brittle shear failure without prior warning.",
    "monitoring_protocol": "Install tell-tale crack width gauges or vibrating wire displacement sensors to monitor active movement over 14-day observation period."
}
