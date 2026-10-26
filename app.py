"""AgriSmart — Smart Agriculture Decision Support System.

Main application entry point.
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from src.ui.styles import apply_theme
from src.ui.home_page import render_home_page
from src.ui.crop_page import render_crop_page
from src.ui.fertilizer_page import render_fertilizer_page
from src.ui.yield_page import render_yield_page
from src.ui.performance_page import render_performance_page
from src.ui.insights_page import render_insights_page
from src.ui.about_page import render_about_page
from src.utils.constants import MODELS_DIR

st.set_page_config(
    page_title="AgriSmart — Smart Agriculture DSS",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply unified styling
apply_theme()


def main():
    # Sidebar Brand & Navigation
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 0.8rem 0 1.2rem 0; text-align: left;">
                <div style="font-size: 2rem;">🌾 <strong>AgriSmart</strong></div>
                <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.2rem;">
                    Decision Support System
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Navigation")
        pages = {
            "🏠 Home Dashboard": render_home_page,
            "🌾 Crop Recommendation": render_crop_page,
            "🧪 Fertilizer Recommendation": render_fertilizer_page,
            "📈 Crop Yield Prediction": render_yield_page,
            "📊 Model Performance": render_performance_page,
            "🔍 Dataset Insights": render_insights_page,
            "ℹ️ About & Limitations": render_about_page,
        }

        selected_page = st.radio(
            "Select Section",
            options=list(pages.keys()),
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("### System Health")
        
        # Live Model Artifact Check
        crop_ready = (MODELS_DIR / "crop_recommendation.joblib").exists()
        fert_ready = (MODELS_DIR / "fertilizer_recommendation.joblib").exists()
        yield_ready = (MODELS_DIR / "yield_prediction.joblib").exists()

        def status_icon(ready: bool) -> str:
            return "🟢 Ready" if ready else "🔴 Missing"

        st.markdown(
            f"""
            <div style="font-size: 0.82rem; color: #475569; line-height: 1.8;">
                <strong>Crop Model:</strong> {status_icon(crop_ready)}<br>
                <strong>Fertilizer Model:</strong> {status_icon(fert_ready)}<br>
                <strong>Yield Model:</strong> {status_icon(yield_ready)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size: 0.78rem; color: #94a3b8;">
                AgriSmart v1.0.0<br>
                Academic Research Edition<br>
                NIIT University Project
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Route to selected page
    render_func = pages[selected_page]
    render_func()


if __name__ == "__main__":
    main()
