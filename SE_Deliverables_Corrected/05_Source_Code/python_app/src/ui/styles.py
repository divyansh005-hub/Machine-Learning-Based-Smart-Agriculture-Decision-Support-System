"""Custom CSS styles and UI card components for AgriSmart."""

import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, .brand-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
}

/* App Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #1b4d3e 0%, #0d2818 50%, #1a3c40 100%);
    color: #ffffff;
    padding: 2.2rem 2.4rem;
    border-radius: 18px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
    color: #f1faee;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #a8dadc;
    margin-top: 0.6rem;
    line-height: 1.5;
}

.hero-badge {
    display: inline-block;
    background: rgba(46, 204, 113, 0.2);
    border: 1px solid #2ecc71;
    color: #2ecc71;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Glass & Clean Cards */
.agrismart-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.agrismart-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.card-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.4rem;
}

.card-desc {
    color: #64748b;
    font-size: 0.92rem;
    line-height: 1.45;
}

/* Metric Pill */
.metric-pill {
    display: inline-block;
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
    padding: 0.35rem 0.8rem;
    border-radius: 8px;
    font-size: 0.85rem;
    margin-right: 0.5rem;
    margin-top: 0.5rem;
}

/* Prediction Result Box */
.prediction-box {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border: 2px solid #86efac;
    border-radius: 16px;
    padding: 1.8rem;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
}

.prediction-label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #166534;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.prediction-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #14532d;
    margin: 0.4rem 0;
    letter-spacing: -0.5px;
}

.prediction-subtext {
    font-size: 1rem;
    color: #15803d;
    margin-top: 0.4rem;
}

/* Disclaimer Banner */
.disclaimer-banner {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    padding: 1rem 1.2rem;
    border-radius: 8px;
    color: #92400e;
    font-size: 0.88rem;
    line-height: 1.5;
    margin: 1.2rem 0;
}

/* Status Badges */
.badge-active {
    background: #dcfce7;
    color: #15803d;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-info {
    background: #e0f2fe;
    color: #0369a1;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
}
</style>
"""


def apply_theme():
    """Inject custom styles into Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, badge: str = "AgriSmart Decision Platform"):
    """Render modern hero section."""
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-badge">{badge}</div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer(text: str):
    """Render standardized agronomic disclaimer."""
    st.markdown(
        f"""
        <div class="disclaimer-banner">
            <strong>⚠️ Agronomic & Responsible Use Notice:</strong> {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
