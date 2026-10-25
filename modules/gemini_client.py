"""
Gemini Client Wrapper for Multimodal Construction Intelligence Platform.
Supports Google GenAI SDK (gemini-2.5-flash) with seamless fallback to Demonstration Mode.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List, Union
from PIL import Image
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GeminiClient")

try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-genai SDK not available, will default to Demonstration Mode.")


class ConstructionGeminiClient:
    """Wrapper managing live Gemini vision/chat inference with reliable offline simulation fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or ""
        self.client = None
        self.is_live = False
        self._init_client()

    def _init_client(self):
        """Initialize the GenAI client if valid API key is present."""
        if not self.api_key or not self.api_key.strip():
            self.is_live = False
            return

        if GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key.strip())
                self.is_live = True
                logger.info("GenAI client initialized in LIVE mode.")
            except Exception as e:
                logger.error(f"Failed to initialize GenAI client: {e}")
                self.is_live = False

    def set_api_key(self, api_key: str):
        """Update API key dynamically."""
        self.api_key = api_key.strip()
        self._init_client()

    def analyze_multimodal(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
        system_instruction: str,
        fallback_data: Dict[str, Any],
        is_json: bool = True,
        model_name: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        """
        Analyze image with multimodal Gemini model.
        Returns parsed JSON dict (or formatted text if not JSON).
        Gracefully falls back to fallback_data if key is absent or an error occurs.
        """
        if not self.is_live or not self.client:
            logger.info("Operating in Demonstration Mode: returning calibrated simulation data.")
            return fallback_data

        try:
            image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            contents = [image_part, prompt]

            config_args = {
                "system_instruction": system_instruction,
                "temperature": 0.2,
            }
            if is_json:
                config_args["response_mime_type"] = "application/json"

            config = types.GenerateContentConfig(**config_args)

            response = self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )

            raw_text = response.text
            if is_json:
                # Strip markdown json fences if any
                cleaned = raw_text.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                
                try:
                    return json.loads(cleaned.strip())
                except json.JSONDecodeError as jde:
                    logger.warning(f"JSON decode failed on Gemini output: {jde}. Raw: {raw_text[:200]}")
                    return fallback_data
            else:
                return {"response": raw_text}

        except Exception as err:
            logger.error(f"Live Gemini API call failed: {err}. Switching gracefully to Demonstration mode.")
            st.warning(f"⚠️ Live Gemini API call encountered an error: {str(err)[:120]}... Serving calibrated demonstration simulation data.")
            return fallback_data

    def chat_response(
        self,
        conversation_history: List[Dict[str, str]],
        system_instruction: str,
        weather_context: Optional[str] = None,
        model_name: str = "gemini-2.5-flash"
    ) -> str:
        """
        Multi-turn chat interaction with Gemini or engineering rule-based assistant.
        """
        if not self.is_live or not self.client:
            return self._generate_simulated_chat_reply(conversation_history[-1]["content"], weather_context)

        try:
            # Format messages for Gemini
            contents = []
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            sys_inst = system_instruction
            if weather_context:
                sys_inst += f"\n\nCURRENT ON-SITE WEATHER ADVISORY CONTEXT:\n{weather_context}"

            config = types.GenerateContentConfig(
                system_instruction=sys_inst,
                temperature=0.3,
            )

            response = self.client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )
            return response.text

        except Exception as err:
            logger.error(f"Gemini chat failed: {err}")
            return (
                f"*(Note: Gemini live query encountered {type(err).__name__}. Serving Senior Civil Engineer fallback advisory)*\n\n"
                + self._generate_simulated_chat_reply(conversation_history[-1]["content"], weather_context)
            )

    def _generate_simulated_chat_reply(self, user_query: str, weather_context: Optional[str]) -> str:
        """Generate authoritative domain responses when operating in offline/demo mode."""
        q = user_query.lower()

        if "curing" in q or "is 456" in q or "water" in q:
            return (
                "### 📘 IS 456:2000 Concrete Curing Standards\n\n"
                "According to **IS 456:2000 Clause 13.5**:\n\n"
                "1. **Ordinary Portland Cement (OPC):** Minimum curing period is **7 days** under standard damp conditions.\n"
                "2. **Mineral Admixtures (Fly Ash, Slag, Silica Fume / PPC):** Curing period must be extended to at least **10 days** (and **14 days** under hot/dry weather conditions).\n"
                "3. **Ponding Method:** Mandatory for horizontal slabs and flat pavements to prevent plastic shrinkage cracking.\n"
                "4. **Curing Membranes:** If water ponding is impractical (e.g., vertical columns or high-wind environments), apply an approved resin-based curing compound complying with **ASTM C309** immediately after formwork demoulding."
            )
        elif "wind" in q or "crane" in q or "speed" in q:
            return (
                "### 🏗️ Crane Safety & High Wind Protocols (IS 875 Part 3 & OSHA 1926.1431)\n\n"
                "1. **Wind Speed Thresholds:**\n"
                "   - **> 38 km/h (20 knots / 10.5 m/s):** Exercise extreme caution; ban high surface-area panel lifts (formwork shutters, glazing units).\n"
                "   - **> 45 km/h (24 knots / 12.5 m/s):** **MANDATORY CRANE OPERATIONS SUSPENSION**. Lower all suspended loads to ground.\n"
                "   - **> 72 km/h:** Activate tower crane **weathervaning (free-slewing brake released)** so the jib aligns naturally with wind vectors to prevent overturning moment.\n"
                "2. **Elevation Restrictions:** Scaffolding work above 10m must be halted immediately. Ensure all unsecured cladding and formwork plywood are strapped down."
            )
        elif "shear" in q or "crack" in q or "beam" in q:
            return (
                "### 🔬 Remediation of Structural Shear Cracks (IS 456 & IS 13920)\n\n"
                "Diagonal cracks inclined at ~45° near beam-column joints indicate principal tensile stress failure:\n\n"
                "1. **Immediate Propping:** Install structural Acrow jacks or hydraulic shores within 1 meter of the column face to relieve ongoing gravity dead & live loads.\n"
                "2. **Epoxy Pressure Injection:** For crack widths > 0.3mm, seal the surface with thixotropic epoxy paste and inject low-viscosity structural epoxy (ASTM C881 Type IV) under 0.2–0.4 MPa pressure.\n"
                "3. **CFRP Shear Strengthening:** Wrap Carbon Fiber Reinforced Polymer (CFRP) bidirectional laminates (U-jacket configuration) anchored to the slab flange per **ACI 440.2R** to compensate for internal stirrup yielding."
            )
        elif "stripping" in q or "props" in q or "formwork" in q:
            return (
                "### ⏱️ IS 456 Table 11: Minimum Formwork Striking Periods (OPC)\n\n"
                "- **Walls, columns and vertical faces of beams:** 16 to 24 hours\n"
                "- **Slab soffit (props left under):** 3 days\n"
                "- **Beam soffit (props left under):** 7 days\n"
                "- **Removal of props under slabs:**\n"
                "  - Spanning up to 4.5 m: 7 days\n"
                "  - Spanning over 4.5 m: 14 days\n"
                "- **Removal of props under beams and arches:**\n"
                "  - Spanning up to 6.0 m: 14 days\n"
                "  - Spanning over 6.0 m: **21 days**"
            )
        else:
            weather_alert = f"\n\n*Site Condition Advisory: Active weather status is '{weather_context}'. Ensure field crews abide by prevailing environmental precautions.*" if weather_context else ""
            return (
                f"### 👷 Construction Site Engineering Advisory\n\n"
                f"Regarding your query on: **'{user_query}'**:\n\n"
                "1. **Structural Compliance:** Always benchmark structural verifications against **IS 456:2000** (Plain & Reinforced Concrete) and **IS 1893:2016** (Earthquake Resistant Design).\n"
                "2. **Occupational Safety:** Field execution must strictly comply with **OSHA 1926 Safety & Health Regulations for Construction** and Indian National Building Code (NBC 2016 Part 7 - Construction Practices and Safety).\n"
                "3. **Quality Assurance:** Verify cube compressive strength testing at 7 and 28 days (IS 516), maintaining water-cement ratio <= 0.45 for severe exposure conditions."
                f"{weather_alert}"
            )
