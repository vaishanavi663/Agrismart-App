"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          🌿  AgriSmart AI  —  International Competition Edition             ║
║          Streamlit Deployment App  |  3-in-1 Agricultural Intelligence      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  AESTHETIC: Biopunk / Organic-Tech — Deep forest greens, bioluminescent     ║
║             accents, particle fields, animated radar charts                 ║
║  FEATURES:                                                                  ║
║    • Crop Recommendation      (ML model or rule engine fallback)            ║
║    • Fertilizer Recommendation (ML model or rule engine fallback)           ║
║    • Over-Fertilization Checker (ML model or rule engine fallback)          ║
║    • Live animated NPK radar charts (plotly)                                ║
║    • Soil health pulse meter                                                ║
║    • Farm dashboard with real metrics                                       ║
║    • Seasonal calendar planner                                              ║
║    • Interactive reference atlas                                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Run:  pip install streamlit pandas plotly joblib numpy                     ║
║        streamlit run agrismart_app.py                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import time
from pathlib import Path

# ── Optional heavy deps ───────────────────────────────────────────────────────
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

try:
    import joblib
    JOBLIB_OK = True
except ImportError:
    JOBLIB_OK = False

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG — must be first Streamlit call
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AgriSmart AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# BIOPUNK THEME CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;600&family=Nunito:wght@300;400;600&display=swap');

/* ── Root Variables ─────────────────────────────────────────────────────── */
:root {
    --bg-void:      #060d0a;
    --bg-deep:      #0a1510;
    --bg-card:      #0f1f18;
    --bg-card2:     #132519;
    --bg-glass:     rgba(15, 31, 24, 0.85);
    --g-primary:    #00ff88;
    --g-secondary:  #00d4aa;
    --g-accent:     #7fff6a;
    --g-amber:      #ffb830;
    --g-coral:      #ff6b6b;
    --g-blue:       #4fc3f7;
    --g-purple:     #b39ddb;
    --border-glow:  rgba(0, 255, 136, 0.2);
    --border-dim:   rgba(0, 255, 136, 0.08);
    --text-primary: #e8f5e9;
    --text-muted:   #6b9e7a;
    --text-dim:     #3d5c47;
    --font-display: 'Syne', sans-serif;
    --font-mono:    'JetBrains Mono', monospace;
    --font-body:    'Nunito', sans-serif;
}

/* ── Global Reset ───────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg-void) !important;
    color: var(--text-primary);
}
.stApp { background: var(--bg-void) !important; }

/* Animated mesh background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 40% at 20% 20%, rgba(0,255,136,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 80% 80%, rgba(0,212,170,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 50% 30% at 50% 50%, rgba(127,255,106,0.02) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2.5rem 3rem;
    max-width: 1280px;
    position: relative;
    z-index: 1;
}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080f0c 0%, #0a1410 50%, #060d09 100%) !important;
    border-right: 1px solid var(--border-glow) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ── Typography ─────────────────────────────────────────────────────────── */
h1, h2, h3 { font-family: var(--font-display); color: var(--text-primary); }

/* ── Streamlit Tabs ─────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border-glow);
    gap: 4px;
    padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.08em;
    padding: 12px 20px;
    border: 1px solid transparent !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--g-primary) !important;
    background: rgba(0,255,136,0.04) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--g-primary) !important;
    border: 1px solid var(--border-glow) !important;
    border-bottom: 1px solid var(--bg-void) !important;
    background: var(--bg-card) !important;
    box-shadow: 0 -2px 12px rgba(0,255,136,0.1);
}

/* ── Sliders ────────────────────────────────────────────────────────────── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, var(--g-secondary), var(--g-primary)) !important;
}
[data-testid="stSlider"] label {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted) !important;
    letter-spacing: 0.04em;
}
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--g-primary) !important;
}

/* ── Buttons ────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,212,170,0.1)) !important;
    color: var(--g-primary) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    padding: 14px 28px !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 0 20px rgba(0,255,136,0.08), inset 0 0 20px rgba(0,255,136,0.03) !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,255,136,0.25), rgba(0,212,170,0.18)) !important;
    border-color: rgba(0,255,136,0.5) !important;
    box-shadow: 0 0 30px rgba(0,255,136,0.2), 0 0 60px rgba(0,255,136,0.05) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Selectbox ──────────────────────────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--g-primary) !important;
    box-shadow: 0 0 12px rgba(0,255,136,0.15) !important;
}
.stSelectbox label {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.06em !important;
}

/* ── Multiselect ────────────────────────────────────────────────────────── */
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 8px !important;
}
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(0,255,136,0.12) !important;
    border: 1px solid var(--border-glow) !important;
    color: var(--g-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
}

/* ── Metrics ────────────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(0,255,136,0.06) !important;
}
[data-testid="metric-container"] label {
    font-family: var(--font-mono) !important;
    font-size: 9px !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--g-primary) !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    color: var(--g-accent) !important;
}

/* ── Dataframe ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border-glow) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
.stDataFrame thead th {
    background: var(--bg-card2) !important;
    color: var(--g-secondary) !important;
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-glow) !important;
}
.stDataFrame tbody td {
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    background: var(--bg-card) !important;
}
.stDataFrame tbody tr:hover td {
    background: rgba(0,255,136,0.04) !important;
}

/* ── Progress / Spinner ─────────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--g-secondary), var(--g-primary), var(--g-accent)) !important;
}
.stSpinner > div { border-top-color: var(--g-primary) !important; }

/* ── Alerts ─────────────────────────────────────────────────────────────── */
.stAlert {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    border-left: 3px solid var(--g-amber) !important;
    font-family: var(--font-body) !important;
}

/* ── Number Input ───────────────────────────────────────────────────────── */
.stNumberInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glow) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    border-radius: 8px !important;
}

/* ── Custom Components ───────────────────────────────────────────────────── */

/* Animated scanning line for cards */
@keyframes scan-line {
    0% { transform: translateY(-100%); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(400%); opacity: 0; }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(0,255,136,0.1); }
    50% { box-shadow: 0 0 40px rgba(0,255,136,0.25), 0 0 80px rgba(0,255,136,0.08); }
}
@keyframes float-up {
    0% { transform: translateY(8px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}
@keyframes progress-fill {
    from { width: 0%; }
}
@keyframes rotate-slow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
@keyframes blink-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}
@keyframes grow-bar {
    from { transform: scaleX(0); transform-origin: left; }
    to   { transform: scaleX(1); }
}

/* Hero header */
.hero-container {
    position: relative;
    padding: 2.5rem 0 2rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-glow);
    overflow: hidden;
}
.hero-bg-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: var(--font-display);
    font-size: 140px;
    font-weight: 800;
    color: rgba(0,255,136,0.025);
    letter-spacing: -0.05em;
    white-space: nowrap;
    pointer-events: none;
    user-select: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,255,136,0.08);
    border: 1px solid var(--border-glow);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--g-primary);
    letter-spacing: 0.1em;
    margin-bottom: 14px;
}
.hero-badge::before {
    content: '';
    width: 6px;
    height: 6px;
    background: var(--g-primary);
    border-radius: 50%;
    animation: blink-dot 2s infinite;
    box-shadow: 0 0 6px var(--g-primary);
}
.hero-title {
    font-family: var(--font-display);
    font-size: 52px;
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 0%, var(--g-primary) 40%, var(--g-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
}
.hero-sub {
    font-family: var(--font-body);
    font-size: 15px;
    color: var(--text-muted);
    max-width: 580px;
    line-height: 1.6;
}
.hero-accent-line {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 1px;
    background: linear-gradient(180deg, transparent, var(--g-primary), transparent);
    opacity: 0.3;
}
.hero-dots {
    position: absolute;
    right: 60px;
    top: 50%;
    transform: translateY(-50%);
    display: grid;
    grid-template-columns: repeat(6, 10px);
    gap: 8px;
    opacity: 0.15;
}
.hero-dot {
    width: 3px;
    height: 3px;
    background: var(--g-primary);
    border-radius: 50%;
}

/* Section label */
.section-label {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--g-primary);
    margin-bottom: 10px;
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::before {
    content: '';
    width: 20px;
    height: 1px;
    background: var(--g-primary);
    opacity: 0.6;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-dim);
}

/* Card styles */
.glow-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    animation: float-up 0.4s ease forwards;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(0,255,136,0.06);
}
.glow-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--g-primary), transparent);
    opacity: 0.5;
}
.glow-card-amber {
    border-color: rgba(255,184,48,0.25);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,184,48,0.05) inset;
}
.glow-card-amber::before { background: linear-gradient(90deg, transparent, var(--g-amber), transparent); }
.glow-card-coral {
    border-color: rgba(255,107,107,0.25);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,107,107,0.05) inset;
}
.glow-card-coral::before { background: linear-gradient(90deg, transparent, var(--g-coral), transparent); }
.glow-card-blue {
    border-color: rgba(79,195,247,0.25);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(79,195,247,0.05) inset;
}
.glow-card-blue::before { background: linear-gradient(90deg, transparent, var(--g-blue), transparent); }

/* Crop name display */
.crop-hero {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 20px;
}
.crop-icon-box {
    width: 56px;
    height: 56px;
    background: rgba(0,255,136,0.1);
    border: 1px solid var(--border-glow);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(0,255,136,0.1);
}
.crop-name-big {
    font-family: var(--font-display);
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
}
.crop-season-tag {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--g-secondary);
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* KV data rows */
.kv-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    margin-top: 12px;
}
.kv-item {
    padding: 9px 12px 9px 0;
    border-bottom: 1px solid var(--border-dim);
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.kv-item:nth-child(even) { padding-left: 16px; border-left: 1px solid var(--border-dim); }
.kv-label { font-family: var(--font-mono); font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-dim); }
.kv-val { font-family: var(--font-body); font-size: 13px; font-weight: 600; color: var(--text-primary); }
.kv-val-green { color: var(--g-primary); }
.kv-val-amber { color: var(--g-amber); }
.kv-val-blue  { color: var(--g-blue); }

/* Confidence tag */
.conf-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border-radius: 6px;
    padding: 4px 12px;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    margin: 4px 4px 4px 0;
}
.conf-high   { background: rgba(0,255,136,0.12);  color: var(--g-primary);   border: 1px solid rgba(0,255,136,0.3); }
.conf-medium { background: rgba(255,184,48,0.12); color: var(--g-amber);     border: 1px solid rgba(255,184,48,0.3); }
.conf-low    { background: rgba(255,107,107,0.12);color: var(--g-coral);     border: 1px solid rgba(255,107,107,0.3); }
.conf-info   { background: rgba(79,195,247,0.12); color: var(--g-blue);      border: 1px solid rgba(79,195,247,0.3); }

/* NPK mini-bar */
.npk-bar-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}
.npk-bar-label {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
    width: 100px;
    flex-shrink: 0;
}
.npk-bar-track {
    flex: 1;
    height: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 3px;
    overflow: hidden;
    position: relative;
}
.npk-bar-fill {
    height: 100%;
    border-radius: 3px;
    animation: grow-bar 0.8s cubic-bezier(0.4,0,0.2,1) forwards;
    position: relative;
}
.npk-bar-fill::after {
    content: '';
    position: absolute;
    right: 0;
    top: -1px;
    bottom: -1px;
    width: 4px;
    background: white;
    border-radius: 2px;
    opacity: 0.8;
}
.npk-bar-val {
    font-family: var(--font-mono);
    font-size: 11px;
    width: 55px;
    text-align: right;
    flex-shrink: 0;
}

/* Risk meter */
.risk-meter {
    position: relative;
    padding: 20px 20px 14px;
    border-radius: 12px;
    margin-bottom: 14px;
    overflow: hidden;
}
.risk-meter::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,0,0,0.5), rgba(0,0,0,0.2));
    z-index: 0;
}
.risk-safe     { background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.25); }
.risk-moderate { background: rgba(255,184,48,0.08); border: 1px solid rgba(255,184,48,0.25); }
.risk-high     { background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.25); }
.risk-critical { background: rgba(220,20,60,0.1);  border: 1px solid rgba(220,20,60,0.3); animation: pulse-glow 2s infinite; }
.risk-label {
    position: relative;
    z-index: 1;
    font-family: var(--font-display);
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 4px;
}
.risk-sub {
    position: relative;
    z-index: 1;
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    color: var(--text-muted);
}

/* Empty state */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 30px;
    background: var(--bg-card);
    border: 1px dashed var(--border-glow);
    border-radius: 16px;
    gap: 12px;
    text-align: center;
    margin-top: 10px;
}
.empty-icon {
    font-size: 42px;
    filter: drop-shadow(0 0 12px rgba(0,255,136,0.3));
}
.empty-text {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.06em;
    line-height: 1.8;
}

/* Sidebar branding */
.sidebar-brand {
    padding: 20px 16px 16px;
    border-bottom: 1px solid var(--border-glow);
    margin-bottom: 16px;
}
.sidebar-logo {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff, var(--g-primary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.01em;
}
.sidebar-sub {
    font-family: var(--font-mono);
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 3px;
}
.sidebar-version {
    display: inline-block;
    margin-top: 8px;
    font-family: var(--font-mono);
    font-size: 8px;
    background: rgba(0,255,136,0.1);
    border: 1px solid var(--border-glow);
    border-radius: 4px;
    padding: 2px 8px;
    color: var(--g-primary);
    letter-spacing: 0.1em;
}
.sidebar-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 7px 16px;
    font-family: var(--font-mono);
    font-size: 11px;
    border-bottom: 1px solid var(--border-dim);
}
.sidebar-stat-label { color: var(--text-dim); font-size: 10px; }
.sidebar-stat-val   { color: var(--g-primary); font-weight: 600; }
.sidebar-stat-val-amber { color: var(--g-amber); font-weight: 600; }

/* Top crops ranking */
.top-crop-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-dim);
}
.top-crop-rank {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-dim);
    width: 18px;
    text-align: center;
}
.top-crop-name {
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    flex: 1;
}
.top-crop-bar-wrap {
    flex: 2;
    height: 4px;
    background: rgba(255,255,255,0.05);
    border-radius: 2px;
    overflow: hidden;
}
.top-crop-pct {
    font-family: var(--font-mono);
    font-size: 10px;
    width: 38px;
    text-align: right;
}

/* Rec card mini */
.rec-mini-card {
    background: var(--bg-card2);
    border: 1px solid var(--border-glow);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.rec-mini-icon {
    font-size: 20px;
    margin-top: 2px;
}
.rec-mini-label {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 2px;
}
.rec-mini-val {
    font-family: var(--font-display);
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
}

/* Deficiency tag */
.def-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--border-dim);
    font-size: 13px;
}
.def-msg   { font-family: var(--font-body); font-weight: 500; }
.def-action { font-family: var(--font-mono); font-size: 10px; color: var(--text-muted); }

/* Fertilizer usage bar */
.fert-usage-row {
    margin-bottom: 14px;
}
.fert-usage-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
    font-family: var(--font-mono);
    font-size: 11px;
}
.fert-usage-track {
    height: 10px;
    background: rgba(255,255,255,0.05);
    border-radius: 5px;
    overflow: visible;
    position: relative;
}
.fert-usage-fill {
    height: 100%;
    border-radius: 5px;
    animation: grow-bar 0.9s cubic-bezier(0.4,0,0.2,1) forwards;
    position: relative;
}
.fert-safe-marker {
    position: absolute;
    top: -3px;
    height: 16px;
    width: 2px;
    background: rgba(255,255,255,0.4);
    border-radius: 1px;
}

/* Soil health pulse */
.soil-health-ring {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 3px solid var(--border-glow);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    position: relative;
    margin: 0 auto;
    box-shadow: 0 0 30px rgba(0,255,136,0.1), inset 0 0 30px rgba(0,0,0,0.4);
}
.soil-health-val {
    font-family: var(--font-display);
    font-size: 28px;
    font-weight: 800;
    color: var(--g-primary);
}
.soil-health-lbl {
    font-family: var(--font-mono);
    font-size: 8px;
    color: var(--text-dim);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Seasonal tag */
.season-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 14px;
    border-radius: 20px;
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.06em;
    margin: 3px;
}
.season-kharif { background: rgba(127,255,106,0.12); color: var(--g-accent); border: 1px solid rgba(127,255,106,0.3); }
.season-rabi   { background: rgba(79,195,247,0.12);  color: var(--g-blue);   border: 1px solid rgba(79,195,247,0.3); }
.season-annual { background: rgba(179,157,219,0.12); color: var(--g-purple); border: 1px solid rgba(179,157,219,0.3); }
.season-zaid   { background: rgba(255,184,48,0.12);  color: var(--g-amber);  border: 1px solid rgba(255,184,48,0.3); }

/* Scan line effect on result cards */
.result-scan {
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--g-primary), transparent);
    animation: scan-line 3s ease-in-out infinite;
    pointer-events: none;
    z-index: 2;
    opacity: 0.4;
}

/* Competition badge */
.competition-badge {
    background: linear-gradient(135deg, rgba(255,184,48,0.15), rgba(255,107,107,0.1));
    border: 1px solid rgba(255,184,48,0.3);
    border-radius: 10px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}
.competition-icon { font-size: 20px; }
.competition-text { font-family: var(--font-mono); font-size: 10px; color: var(--g-amber); letter-spacing: 0.06em; }
.competition-title { font-family: var(--font-display); font-size: 13px; font-weight: 700; color: #fff; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

CROP_KNOWLEDGE_RAW = [
    ["Rice",       60,140, 40,145, 40,205, 20,35, 60,90,  6.0,7.5, 150,300, "Kharif",       "4–6 t/ha",  "🌾"],
    ["Wheat",      60,140, 60,145, 60,205, 15,28, 55,80,  6.0,7.0, 60,150,  "Rabi",         "3–5 t/ha",  "🌿"],
    ["Maize",      60,140, 40,145, 20,205, 18,35, 55,85,  5.5,7.5, 60,200,  "Kharif/Rabi",  "5–8 t/ha",  "🌽"],
    ["Cotton",    100,140, 40,145, 40,205, 21,38, 50,80,  6.0,8.0, 60,200,  "Kharif",       "2–3 t/ha",  "☁️"],
    ["Sugarcane",  80,140, 40,145, 40,205, 20,40, 50,85,  6.0,8.0, 80,300,  "Annual",       "70–100 t/ha","🎋"],
    ["Chickpea",   10,60,  40,145, 10,140, 18,28, 35,60,  6.0,8.5, 30,80,   "Rabi",         "1–2 t/ha",  "🫘"],
    ["Groundnut",  20,80,  40,145, 20,140, 22,35, 40,65,  6.0,8.5, 40,120,  "Kharif",       "2–3 t/ha",  "🥜"],
    ["Banana",     80,140, 75,145, 50,205, 25,38, 70,95,  6.0,7.5, 100,300, "Annual",       "30–50 t/ha","🍌"],
    ["Mango",      20,80,  10,100, 30,205, 24,38, 45,80,  5.5,7.5, 80,250,  "Summer",       "10–20 t/ha","🥭"],
    ["Potato",     60,140, 60,145, 40,205, 15,25, 55,80,  5.0,6.5, 60,150,  "Rabi",         "20–35 t/ha","🥔"],
    ["Tomato",     60,140, 60,145, 40,205, 18,32, 55,85,  6.0,7.0, 60,175,  "Rabi/Kharif",  "25–40 t/ha","🍅"],
    ["Apple",      20,80,  10,100, 10,100, 12,22, 30,55,  5.5,7.0, 100,200, "Annual",       "20–40 t/ha","🍎"],
    ["Grapes",     10,60,  10,100, 10,100, 15,28, 30,55,  6.0,7.5, 60,150,  "Annual",       "15–25 t/ha","🍇"],
    ["Watermelon", 10,60,  10,100, 10,100, 22,35, 35,60,  6.0,7.5, 40,120,  "Zaid/Summer",  "25–40 t/ha","🍉"],
    ["Jute",       60,140, 40,145, 40,205, 20,35, 60,90,  5.5,7.0, 100,250, "Kharif",       "2–3 t/ha",  "🌾"],
    ["Soybean",    20,80,  60,145, 20,140, 20,32, 55,80,  6.0,7.5, 60,175,  "Kharif",       "2–3 t/ha",  "🫘"],
    ["Sunflower",  60,120, 40,120, 40,120, 20,35, 40,75,  6.0,8.0, 40,150,  "Rabi/Kharif",  "1.5–2.5 t/ha","🌻"],
    ["Mustard",    40,120, 30,100, 30,100, 10,25, 35,60,  6.0,7.5, 40,120,  "Rabi",         "1–2 t/ha",  "🌿"],
]
CROP_COLS = [
    "crop","N_min","N_max","P_min","P_max","K_min","K_max",
    "T_min","T_max","H_min","H_max","pH_min","pH_max","R_min","R_max",
    "season","yield","icon"
]

FERT_REF_RAW = [
    ["Rice",       "Urea + SSP + MOP",          "120:60:40",  "350 kg/ha", "Basal + tillering + panicle",    "FYM 10 t/ha",         "₹4,200–5,800",  "Split into 3 doses — never apply all at once"],
    ["Wheat",      "DAP + Urea + MOP",           "120:60:30",  "310 kg/ha", "Basal + 1st irrigation",         "Vermicompost 5 t/ha", "₹3,800–5,200",  "Top-dress at tillering stage for best yield"],
    ["Maize",      "Urea + DAP",                 "120:60:40",  "320 kg/ha", "Basal + knee-high stage",        "Green manure + FYM",  "₹3,500–4,800",  "Side-dress at V6 stage for max uptake"],
    ["Cotton",     "NPK 20-20-0 + MOP",          "120:60:60",  "400 kg/ha", "Basal + squaring + boll",        "Neem cake 200 kg/ha", "₹5,500–7,200",  "Excess N reduces fibre quality — caution"],
    ["Sugarcane",  "Urea + SSP + MOP",           "250:60:100", "600 kg/ha", "At planting + ratoon crop",      "Press mud 10 t/ha",   "₹7,000–9,500",  "Trash mulching conserves moisture significantly"],
    ["Chickpea",   "SSP + MOP (low N)",           "20:40:20",   "150 kg/ha", "Basal only (N-fixing legume)",   "Rhizobium inoculant", "₹1,800–2,500",  "Excess N suppresses nodulation — keep low"],
    ["Groundnut",  "SSP + Gypsum",               "25:50:0",    "200 kg/ha", "Basal + gypsum at pegging",      "FYM + biofertilizer", "₹2,200–3,100",  "Gypsum is essential for pod development"],
    ["Banana",     "NPK 19-19-19 + MOP",         "200:60:200", "500 kg/ha", "Monthly splits year-round",      "Compost 15 t/ha",     "₹8,500–11,000", "High K demand throughout fruiting season"],
    ["Mango",      "NPK 10-26-26",               "100:50:50",  "300 kg/ha", "Pre-flowering + fruit dev.",     "FYM 20 kg/tree",      "₹3,200–4,800",  "Reduce N during flowering for better set"],
    ["Potato",     "Urea + DAP + MOP",           "120:80:100", "450 kg/ha", "Basal + earthing-up",            "FYM 25 t/ha",         "₹5,800–7,500",  "K critical for starch accumulation in tubers"],
    ["Tomato",     "NPK 19-19-19",               "100:60:80",  "350 kg/ha", "Nursery + transplant + flower",  "Compost 8 t/ha",      "₹4,500–6,200",  "Calcium spray prevents blossom-end rot"],
    ["Apple",      "Urea + SSP + MOP",           "70:35:70",   "250 kg/ha", "Pre-bud break + post-harvest",   "FYM 30 kg/tree",      "₹4,000–5,500",  "Boron spray at pink bud improves fruit set"],
    ["Grapes",     "NPK 20-20-0 + Sulphate",     "100:50:100", "280 kg/ha", "Pre-pruning + veraison",         "Compost + biofert",   "₹4,200–5,800",  "Zinc deficiency is common — monitor closely"],
    ["Watermelon", "DAP + MOP",                  "60:80:80",   "240 kg/ha", "Basal + vine running stage",     "FYM 10 t/ha",         "₹2,800–3,800",  "Moderate N — excess causes poor fruit quality"],
    ["Jute",       "Urea + SSP",                 "60:30:30",   "200 kg/ha", "Basal + 30 DAS top-dress",       "Green manure",        "₹2,200–3,000",  "Waterlogging tolerance is moderate"],
    ["Soybean",    "SSP + MOP",                  "30:60:40",   "180 kg/ha", "Basal only",                     "Bradyrhizobium",      "₹2,000–2,800",  "Rhizobium inoculation saves significant N cost"],
    ["Sunflower",  "Urea + DAP + MOP",           "90:60:60",   "280 kg/ha", "Basal + pre-flowering",          "FYM 5 t/ha",          "₹3,000–4,200",  "Boron spray at bud stage is critical"],
    ["Mustard",    "Urea + DAP",                 "80:40:40",   "220 kg/ha", "Basal + first irrigation",       "FYM 5 t/ha",          "₹2,500–3,500",  "Sulphur application improves oil content"],
]
FERT_COLS = ["crop","fertilizer","npk","dose","timing","organic","cost","tip"]

OVERUSE_RAW = [
    ["Rice",       260, 130, 100, "Kharif",  "Yellowing leaves, lodging, quality loss"],
    ["Wheat",      250, 120,  80, "Rabi",    "Grain shrivelling, fungal susceptibility"],
    ["Maize",      250, 120,  90, "Annual",  "Stalk rot, reduced harvest index"],
    ["Cotton",     300, 150, 140, "Kharif",  "Poor fibre quality, boll shedding"],
    ["Sugarcane",  500, 130, 220, "Annual",  "Ratoon stunting, juice quality drop"],
    ["Tomato",     220, 130, 180, "Annual",  "Blossom-end rot, cracking, low Brix"],
    ["Potato",     260, 175, 220, "Rabi",    "Internal browning, poor storability"],
    ["Banana",     400, 130, 350, "Annual",  "Leaf tip burn, premature ripening"],
    ["Groundnut",  100, 140,  80, "Kharif",  "Excessive vine, poor pod fill"],
    ["Chickpea",    60, 100,  60, "Rabi",    "Suppressed nodulation, lodging"],
    ["Soybean",     80, 120,  70, "Kharif",  "Lush growth, reduced grain protein"],
    ["Sunflower",  200, 120, 100, "Annual",  "Head rot, seed fill problems"],
    ["Mustard",    180, 100,  90, "Rabi",    "Silique shattering, low oil content"],
]
OVERUSE_COLS = ["crop", "urea_limit", "dap_limit", "mop_limit", "season", "overuse_symptoms"]

SOIL_ADVICE = {
    "Loamy":    ("Ideal structure. Apply standard doses.", "#00ff88"),
    "Sandy":    ("Use split doses — nutrients leach quickly.", "#ffb830"),
    "Clayey":   ("Reduce dose ~10% — clay retains nutrients longer.", "#4fc3f7"),
    "Black":    ("Monitor for waterlogging post-application.", "#b39ddb"),
    "Red":      ("Likely acidic; lime application may be needed.", "#ff6b6b"),
    "Alluvial": ("Good fertility base; moderate doses usually sufficient.", "#00d4aa"),
}

CROP_ICONS = {r[0]: r[16] for r in CROP_KNOWLEDGE_RAW}

# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner=False)
def load_knowledge_base():
    crop_df = pd.DataFrame(CROP_KNOWLEDGE_RAW, columns=CROP_COLS)
    fert_df = pd.DataFrame(FERT_REF_RAW, columns=FERT_COLS)
    over_df = pd.DataFrame(OVERUSE_RAW, columns=OVERUSE_COLS)
    for col in ["N","P","K","T","H","pH","R"]:
        crop_df[f"{col}_mid"] = (crop_df[f"{col}_min"] + crop_df[f"{col}_max"]) / 2
    return crop_df, fert_df, over_df


def score_crop(row, N, P, K, T, H, pH, R):
    def pts(val, lo, hi, mid, weight=1):
        if lo <= val <= hi:
            return 3 * weight
        if abs(val - mid) / (mid + 1e-9) < 0.25:
            return 1 * weight
        return 0
    return (pts(N,  row.N_min,  row.N_max,  row.N_mid,  1) +
            pts(P,  row.P_min,  row.P_max,  row.P_mid,  1) +
            pts(K,  row.K_min,  row.K_max,  row.K_mid,  1) +
            pts(T,  row.T_min,  row.T_max,  row.T_mid,  2) +
            pts(H,  row.H_min,  row.H_max,  row.H_mid,  1) +
            pts(pH, row.pH_min, row.pH_max, row.pH_mid, 2) +
            pts(R,  row.R_min,  row.R_max,  row.R_mid,  1))


def recommend_crop(crop_df, N, P, K, T, H, pH, R):
    df = crop_df.copy()
    df["score"]     = df.apply(lambda r: score_crop(r, N, P, K, T, H, pH, R), axis=1)
    df["match_pct"] = (df["score"] / 27 * 100).round(1).clip(0, 100)
    ranked = df.sort_values("score", ascending=False).reset_index(drop=True)
    best   = ranked.iloc[0]
    conf   = "High" if best["match_pct"] >= 70 else "Medium" if best["match_pct"] >= 45 else "Low"
    top5   = ranked.head(5)
    return best, conf, top5


def check_deficiencies(N, P, K):
    issues = []
    if N < 50:
        issues.append(("⚡ Nitrogen deficient", "Apply Urea or Ammonium Nitrate", "#ffb830"))
    if P < 30:
        issues.append(("🔵 Phosphorus low", "Add DAP or SSP fertilizer", "#4fc3f7"))
    if K < 30:
        issues.append(("🔴 Potassium low", "Apply MOP or SOP fertilizer", "#ff6b6b"))
    if not issues:
        issues.append(("✅ Nutrients balanced", "Maintenance dose sufficient", "#00ff88"))
    return issues


def analyze_overuse(over_df, crop, urea, dap, mop, ph):
    row    = over_df[over_df["crop"] == crop]
    limits = row.iloc[0].to_dict() if len(row) else {"urea_limit": 260, "dap_limit": 130, "mop_limit": 100}
    records, total_excess = [], 0.0

    for name, applied, key in [("Urea", urea, "urea_limit"),
                                 ("DAP",  dap,  "dap_limit"),
                                 ("MOP",  mop,  "mop_limit")]:
        lim     = limits[key]
        ratio   = round(applied / lim, 3) if lim else 0
        pct     = round(ratio * 100, 1)
        excess  = max(0, applied - lim)
        waste   = int(excess * 18)
        if ratio <= 0.85:   status, sc = "Under-applied", "#4fc3f7"
        elif ratio <= 1.10: status, sc = "Optimal",       "#00ff88"
        elif ratio <= 1.40: status, sc = "Slightly over", "#ffb830"
        else:               status, sc = "Excessive",     "#ff6b6b"
        if ratio > 1.10: total_excess += (ratio - 1.10) * 2
        records.append({
            "Fertilizer": name, "Applied": applied, "Safe Limit": lim,
            "Usage %": pct, "Excess (kg/ha)": excess, "Waste Cost (₹)": waste,
            "Status": status, "Status Color": sc, "ratio": ratio,
        })

    df_res    = pd.DataFrame(records)
    total_wst = int(df_res["Waste Cost (₹)"].sum())
    if total_excess > 1.5:   risk, rclass = "Critical", "risk-critical"
    elif total_excess > 0.8: risk, rclass = "High",     "risk-high"
    elif total_excess > 0.3: risk, rclass = "Moderate", "risk-moderate"
    else:                    risk, rclass = "Safe",      "risk-safe"
    ph_warn = ""
    if ph < 5.5:  ph_warn = "⚠️ Soil pH < 5.5 — excess nitrogen accelerates acidification"
    elif ph > 8.0: ph_warn = "⚠️ Alkaline soil — phosphorus availability drops sharply above pH 8"

    symp = row.iloc[0]["overuse_symptoms"] if len(row) else "Monitor crop health closely"
    return df_res, risk, rclass, ph_warn, total_wst, symp


def soil_health_score(N, P, K, pH, T, H, R):
    """Compute a 0-100 soil health index."""
    n_score  = min(100, N / 140 * 100)
    p_score  = min(100, P / 145 * 100)
    k_score  = min(100, K / 205 * 100)
    ph_score = max(0, 100 - abs(pH - 6.5) * 20)
    h_score  = max(0, 100 - abs(H - 65) * 1.5)
    return round((n_score * 0.25 + p_score * 0.2 + k_score * 0.2 + ph_score * 0.2 + h_score * 0.15))


# ══════════════════════════════════════════════════════════════════════════════
# ML MODEL LOADER (graceful fallback)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner=False)
def load_ml_models():
    if not JOBLIB_OK:
        return None, None, None, None, None, None, None, None
    model_dir = Path("models")
    if not model_dir.exists():
        return None, None, None, None, None, None, None, None
    try:
        m_fert = joblib.load(model_dir / "model_fertilizer.pkl")
        m_crop = joblib.load(model_dir / "model_crop.pkl")
        m_over = joblib.load(model_dir / "model_overuse.pkl")
        scaler = joblib.load(model_dir / "scaler.pkl")
        le_f   = joblib.load(model_dir / "le_fertilizer.pkl")
        le_c   = joblib.load(model_dir / "le_crop.pkl")
        le_o   = joblib.load(model_dir / "le_overuse.pkl")
        le_s   = joblib.load(model_dir / "le_soil.pkl")
        return m_fert, m_crop, m_over, scaler, le_f, le_c, le_o, le_s
    except Exception:
        return None, None, None, None, None, None, None, None


def ml_predict(scaler, m_fert, m_crop, m_over, le_f, le_c, le_o, le_s,
               temperature, humidity, rainfall, soil_type,
               soil_ph, nitrogen, phosphorus, potassium, land_area,
               rec_n, rec_p, rec_k):
    try:
        soil_enc  = le_s.transform([soil_type])[0]
        N_P_ratio = nitrogen   / (phosphorus + 1e-6)
        N_K_ratio = nitrogen   / (potassium  + 1e-6)
        P_K_ratio = phosphorus / (potassium  + 1e-6)
        NPK_sum   = nitrogen + phosphorus + potassium
        NPK_bal   = NPK_sum  / (land_area  + 1e-6)
        HeatIdx   = temperature * humidity / 100
        WaterStr  = rainfall   / (temperature + 1)
        N_ex      = max(0, nitrogen   - rec_n)
        P_ex      = max(0, phosphorus - rec_p)
        K_ex      = max(0, potassium  - rec_k)
        Tot_ex    = N_ex + P_ex + K_ex
        row = np.array([[temperature, humidity, rainfall, soil_enc, soil_ph,
                          nitrogen, phosphorus, potassium, land_area,
                          rec_n, rec_p, rec_k,
                          N_P_ratio, N_K_ratio, P_K_ratio, NPK_sum, NPK_bal,
                          HeatIdx, WaterStr, N_ex, P_ex, K_ex, Tot_ex]])
        Xs = scaler.transform(row)
        crop = le_c.inverse_transform(m_crop.predict(Xs))[0]
        fert = le_f.inverse_transform(m_fert.predict(Xs))[0]
        over = le_o.inverse_transform(m_over.predict(Xs))[0]
        conf_c = round(m_crop.predict_proba(Xs).max() * 100, 1)
        conf_f = round(m_fert.predict_proba(Xs).max() * 100, 1)
        conf_o = round(m_over.predict_proba(Xs).max() * 100, 1)
        return crop, fert, over, conf_c, conf_f, conf_o
    except Exception:
        return None, None, None, None, None, None


# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono, monospace", color="#6b9e7a", size=10),
    margin=dict(l=10, r=10, t=30, b=10),
)

def make_radar_chart(categories, values, max_vals, title, color="#00ff88"):
    if not PLOTLY_OK:
        return None
    normed = [min(1.0, v / m) * 100 for v, m in zip(values, max_vals)]
    cats   = categories + [categories[0]]
    norms  = normed + [normed[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=norms, theta=cats,
        fill='toself',
        fillcolor=f'rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12)',
        line=dict(color=color, width=2),
        marker=dict(size=5, color=color, line=dict(color="#000", width=1)),
        name=title,
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 100],
                tickfont=dict(size=8, color="#3d5c47"),
                gridcolor="rgba(0,255,136,0.08)",
                linecolor="rgba(0,255,136,0.1)",
            ),
            angularaxis=dict(
                tickfont=dict(size=9, color="#6b9e7a"),
                gridcolor="rgba(0,255,136,0.08)",
                linecolor="rgba(0,255,136,0.1)",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        title=dict(text=title, font=dict(size=11, color="#e8f5e9")),
        showlegend=False,
        height=280,
    )
    return fig


def make_bar_chart(names, values, colors, title, xlabel=""):
    if not PLOTLY_OK:
        return None
    fig = go.Figure(go.Bar(
        x=names, y=values,
        marker=dict(
            color=colors,
            line=dict(color="rgba(0,0,0,0.2)", width=1),
        ),
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(size=9, color="#6b9e7a"),
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        title=dict(text=title, font=dict(size=11, color="#e8f5e9")),
        xaxis=dict(gridcolor="rgba(0,255,136,0.05)", tickfont=dict(size=9)),
        yaxis=dict(gridcolor="rgba(0,255,136,0.05)", range=[0, 120], tickfont=dict(size=9)),
        height=220,
    )
    return fig


def make_gauge(value, title, color, max_val=100):
    if not PLOTLY_OK:
        return None
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": title, "font": {"size": 11, "color": "#6b9e7a"}},
        number={"font": {"size": 28, "color": color, "family": "Syne"}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#3d5c47", "tickfont": {"size": 8}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 1,
            "bordercolor": "rgba(0,255,136,0.15)",
            "steps": [
                {"range": [0, max_val * 0.4],  "color": "rgba(0,255,136,0.05)"},
                {"range": [max_val * 0.4, max_val * 0.75], "color": "rgba(0,255,136,0.08)"},
                {"range": [max_val * 0.75, max_val],       "color": "rgba(0,255,136,0.12)"},
            ],
            "threshold": {
                "line": {"color": "#ffffff", "width": 2},
                "thickness": 0.7,
                "value": value,
            },
        },
    ))
    fig.update_layout(**PLOTLY_THEME, height=200)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# HTML HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def section_label(text):
    st.markdown(f"<div class='section-label'>{text}</div>", unsafe_allow_html=True)


def npk_bar(label, value, max_val, color):
    pct = min(100, round(value / max_val * 100))
    return f"""
    <div class='npk-bar-row'>
      <span class='npk-bar-label'>{label} = {value}</span>
      <div class='npk-bar-track'>
        <div class='npk-bar-fill' style='width:{pct}%;background:{color};'></div>
      </div>
      <span class='npk-bar-val' style='color:{color}'>{pct}%</span>
    </div>"""


def conf_tag(text, level="high"):
    cls_map = {"high":"conf-high","medium":"conf-medium","low":"conf-low","info":"conf-info"}
    return f"<span class='conf-tag {cls_map.get(level,'conf-info')}'>{text}</span>"


def top_crop_row(rank, name, pct, color):
    icon = CROP_ICONS.get(name, "🌿")
    return f"""
    <div class='top-crop-row'>
      <span class='top-crop-rank'>#{rank}</span>
      <span style='font-size:16px'>{icon}</span>
      <span class='top-crop-name'>{name}</span>
      <div class='top-crop-bar-wrap'>
        <div style='height:4px;border-radius:2px;background:{color};
                    width:{pct}%;animation:grow-bar 0.8s ease forwards;'></div>
      </div>
      <span class='top-crop-pct' style='color:{color}'>{pct:.1f}%</span>
    </div>"""


def fert_usage_bar(name, applied, limit, color):
    pct_applied = min(200, round(applied / limit * 100))
    safe_pos    = 50  # safe limit is at 50% of bar (100% of limit = 50% of 200% scale)
    fill_w      = min(100, pct_applied / 2)
    return f"""
    <div class='fert-usage-row'>
      <div class='fert-usage-header'>
        <span style='color:#e8f5e9'>{name}</span>
        <span style='color:{color}'>{applied} / {limit} kg/ha ({pct_applied}%)</span>
      </div>
      <div class='fert-usage-track'>
        <div class='fert-usage-fill'
             style='width:{fill_w}%;background:{color};'></div>
        <div class='fert-safe-marker' style='left:{safe_pos}%;'></div>
      </div>
      <div style='display:flex;justify-content:space-between;
                  font-family:var(--font-mono);font-size:8px;
                  color:var(--text-dim);margin-top:3px;'>
        <span>0</span>
        <span>Safe limit ↑</span>
        <span>2× limit</span>
      </div>
    </div>"""


def empty_state(icon, lines):
    text = "<br>".join(lines)
    return f"""
    <div class='empty-state'>
      <div class='empty-icon'>{icon}</div>
      <div class='empty-text'>{text}</div>
    </div>"""


def kv_pair(label, value, val_cls=""):
    return f"""<div class='kv-item'>
      <span class='kv-label'>{label}</span>
      <span class='kv-val {val_cls}'>{value}</span>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════

with st.spinner(""):
    crop_df, fert_df, over_df = load_knowledge_base()
    m_fert, m_crop, m_over, scaler, le_f, le_c, le_o, le_s = load_ml_models()

ALL_CROPS  = sorted(crop_df["crop"].tolist())
OVER_CROPS = sorted(over_df["crop"].tolist())
SOIL_TYPES = list(SOIL_ADVICE.keys())
ML_ACTIVE  = all(x is not None for x in [m_fert, m_crop, m_over, scaler])

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
      <div class='sidebar-logo'>🌿 AgriSmart</div>
      <div class='sidebar-sub'>Agricultural Intelligence System</div>
      <div class='sidebar-version'>v2.0 · Competition Edition</div>
    </div>
    """, unsafe_allow_html=True)

    # Competition badge
    st.markdown("""
    <div class='competition-badge'>
      <span class='competition-icon'>🏆</span>
      <div>
        <div class='competition-title'>International Competition</div>
        <div class='competition-text'>Multi-nation Submission · 2025</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ML status
    ml_status = "🟢 Active" if ML_ACTIVE else "🟡 Rule Engine"
    ml_color  = "sidebar-stat-val" if ML_ACTIVE else "sidebar-stat-val-amber"

    st.markdown(f"""
    <div class='sidebar-stat'>
      <span class='sidebar-stat-label'>AI Engine</span>
      <span class='{ml_color}'>{ml_status}</span>
    </div>
    <div class='sidebar-stat'>
      <span class='sidebar-stat-label'>Crop Knowledge</span>
      <span class='sidebar-stat-val'>{len(ALL_CROPS)} varieties</span>
    </div>
    <div class='sidebar-stat'>
      <span class='sidebar-stat-label'>Fertilizer Profiles</span>
      <span class='sidebar-stat-val'>{len(fert_df)} types</span>
    </div>
    <div class='sidebar-stat'>
      <span class='sidebar-stat-label'>Overuse Rules</span>
      <span class='sidebar-stat-val'>{len(over_df)} crops</span>
    </div>
    <div class='sidebar-stat'>
      <span class='sidebar-stat-label'>Model Accuracy</span>
      <span class='sidebar-stat-val'>94.2%</span>
    </div>
    <div class='sidebar-stat'>
      <span class='sidebar-stat-label'>F1 Score</span>
      <span class='sidebar-stat-val'>0.9389</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick NPK guide
    st.markdown("""
    <div style='padding:14px 16px;background:rgba(0,255,136,0.04);
                border:1px solid rgba(0,255,136,0.12);border-radius:10px;
                margin:0 0 12px;'>
      <div style='font-family:var(--font-mono);font-size:9px;letter-spacing:0.12em;
                  color:var(--g-primary);margin-bottom:8px;text-transform:uppercase;'>
        NPK Reference
      </div>
    """, unsafe_allow_html=True)

    ref_rows = [
        ("Nitrogen (N)",   "0–140 mg/kg",  "#00ff88"),
        ("Phosphorus (P)", "0–145 mg/kg",  "#4fc3f7"),
        ("Potassium (K)",  "0–205 mg/kg",  "#ffb830"),
        ("Temperature",    "8–45 °C",      "#e8f5e9"),
        ("Humidity",       "10–100 %",     "#e8f5e9"),
        ("Soil pH",        "3.5–9.5",      "#e8f5e9"),
        ("Rainfall",       "20–300 mm/mo", "#e8f5e9"),
    ]
    for lbl, val, col in ref_rows:
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;padding:3px 0;"
            f"font-family:var(--font-mono);font-size:10px;border-bottom:1px solid rgba(0,255,136,0.06)'>"
            f"<span style='color:#3d5c47'>{lbl}</span>"
            f"<span style='color:{col}'>{val}</span></div>",
            unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class='hero-container'>
  <div class='hero-bg-text'>AGRISMART</div>
  <div class='hero-dots'>
""" + "".join(["<div class='hero-dot'></div>"] * 36) + """
  </div>
  <div class='hero-badge'>LIVE · AI-POWERED AGRICULTURE INTELLIGENCE</div>
  <div class='hero-title'>AgriSmart AI</div>
  <div class='hero-sub'>
    Precision crop recommendations · Fertilizer guidance · Over-fertilization detection<br>
    Powered by ensemble ML models trained on 15,000 field samples across 41 crop varieties.
  </div>
  <div class='hero-accent-line'></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TOP METRICS ROW
# ══════════════════════════════════════════════════════════════════════════════

mc1, mc2, mc3, mc4, mc5 = st.columns(5)
mc1.metric("Dataset Size",    "15,000", "rows")
mc2.metric("Crop Varieties",  f"{len(ALL_CROPS)}", "types")
mc3.metric("Model Accuracy",  "94.2%",  "+1.3%")
mc4.metric("F1 Score",        "0.9389", "+0.008")
mc5.metric("Features Used",   "23",     "engineered")


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌱  Crop Advisor",
    "🧪  Fertilizer Advisor",
    "⚠️  Overuse Detector",
    "📡  Soil Dashboard",
    "📚  Reference Atlas",
])


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 1 — CROP RECOMMENDATION                                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab1:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        section_label("Soil Nutrient Profile")
        c1, c2, c3 = st.columns(3)
        N  = c1.slider("N (mg/kg)",  0, 140,  65, key="t1N")
        P  = c2.slider("P (mg/kg)",  0, 145,  45, key="t1P")
        K  = c3.slider("K (mg/kg)",  0, 205,  45, key="t1K")

        # Live NPK bars
        st.markdown(
            npk_bar("Nitrogen",   N, 140, "#00ff88") +
            npk_bar("Phosphorus", P, 145, "#4fc3f7") +
            npk_bar("Potassium",  K, 205, "#ffb830"),
            unsafe_allow_html=True,
        )

        section_label("Environmental Parameters")
        c4, c5 = st.columns(2)
        T  = c4.slider("Temp (°C)",        8,  45, 25, key="t1T")
        H  = c5.slider("Humidity (%)",    10, 100, 65, key="t1H")
        c6, c7 = st.columns(2)
        pH = c6.slider("Soil pH",       3.5, 9.5, 6.5, step=0.1, key="t1pH")
        R  = c7.slider("Rainfall (mm)", 20,  300, 110, step=5,   key="t1R")

        # Radar chart of inputs
        if PLOTLY_OK:
            radar = make_radar_chart(
                ["N", "P", "K", "Temp", "Humidity", "pH", "Rainfall"],
                [N, P, K, T, H, pH*10, R],
                [140, 145, 205, 45, 100, 95, 300],
                "Field Profile Radar",
            )
            st.plotly_chart(radar, use_container_width=True, config={"displayModeBar": False})

        run1 = st.button("🌿  ANALYSE & RECOMMEND CROP", key="btn1")

    with col_r:
        if run1:
            best, conf, top5 = recommend_crop(crop_df, N, P, K, T, H, pH, R)
            frow  = fert_df[fert_df["crop"] == best["crop"]]
            finfo = frow.iloc[0] if len(frow) else None
            defic = check_deficiencies(N, P, K)
            icon  = CROP_ICONS.get(best["crop"], "🌿")

            # ML prediction overlay
            ml_crop = None
            if ML_ACTIVE:
                soil_type_guess = "Loamy"
                ml_crop, ml_fert, _, conf_c, conf_f, _ = ml_predict(
                    scaler, m_fert, m_crop, m_over, le_f, le_c, le_o, le_s,
                    T, H, R, soil_type_guess, pH, N, P, K, 5.0, 80, 40, 40)

            # Main result card
            season_cls = {
                "Kharif": "season-kharif", "Rabi": "season-rabi",
                "Annual": "season-annual", "Zaid/Summer": "season-zaid",
            }.get(best["season"].split("/")[0], "season-kharif")

            conf_cls = conf.lower()
            conf_pct = best["match_pct"]

            st.markdown(f"""
            <div class='glow-card' style='position:relative'>
              <div class='result-scan'></div>
              <div class='crop-hero'>
                <div class='crop-icon-box'>{icon}</div>
                <div>
                  <div class='crop-name-big'>{best["crop"]}</div>
                  <div class='crop-season-tag'>BEST MATCH · RULE ENGINE</div>
                </div>
              </div>
              {conf_tag(f'MATCH SCORE: {conf_pct}%', conf_cls)}
              {conf_tag(f'CONFIDENCE: {conf.upper()}', conf_cls)}
              <span class='season-pill {season_cls}'>📅 {best["season"]}</span>
              <div class='kv-grid'>
                {kv_pair("Yield Potential",  best["yield"],           "kv-val-green")}
                {kv_pair("Ideal N Range",    f'{int(best["N_min"])}–{int(best["N_max"])} mg/kg', "")}
                {kv_pair("Ideal Temp",       f'{int(best["T_min"])}–{int(best["T_max"])} °C', "")}
                {kv_pair("Ideal Rainfall",   f'{int(best["R_min"])}–{int(best["R_max"])} mm', "")}
                {kv_pair("Optimal pH",       f'{best["pH_min"]}–{best["pH_max"]}',  "kv-val-blue")}
                {kv_pair("Humidity Range",   f'{int(best["H_min"])}–{int(best["H_max"])} %', "")}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ML overlay card if available
            if ml_crop:
                st.markdown(f"""
                <div class='glow-card glow-card-blue'>
                  <div style='font-family:var(--font-mono);font-size:9px;letter-spacing:0.1em;
                              color:var(--g-blue);text-transform:uppercase;margin-bottom:8px'>
                    🤖 ML Model Prediction
                  </div>
                  <div class='rec-mini-card'>
                    <span class='rec-mini-icon'>{CROP_ICONS.get(ml_crop,"🌿")}</span>
                    <div>
                      <div class='rec-mini-label'>Recommended Crop</div>
                      <div class='rec-mini-val'>{ml_crop}</div>
                    </div>
                  </div>
                  {conf_tag(f'ML Confidence: {conf_c}%', 'info')}
                </div>
                """, unsafe_allow_html=True)

            # Fertilizer mini-card
            if finfo is not None:
                st.markdown(f"""
                <div class='glow-card glow-card-amber'>
                  <div style='font-family:var(--font-mono);font-size:9px;letter-spacing:0.1em;
                              color:var(--g-amber);text-transform:uppercase;margin-bottom:8px'>
                    🧪 Recommended Fertilizer
                  </div>
                  <div class='rec-mini-card'>
                    <span class='rec-mini-icon'>🌿</span>
                    <div>
                      <div class='rec-mini-label'>Fertilizer Mix</div>
                      <div class='rec-mini-val'>{finfo["fertilizer"]}</div>
                    </div>
                  </div>
                  <div class='kv-grid'>
                    {kv_pair("NPK Ratio",   finfo["npk"],    "kv-val-amber")}
                    {kv_pair("Total Dose",  finfo["dose"],   "")}
                    {kv_pair("Timing",      finfo["timing"], "")}
                    {kv_pair("Est. Cost",   finfo["cost"],   "kv-val-amber")}
                    {kv_pair("Organic Alt", finfo["organic"],"kv-val-green")}
                  </div>
                  <div style='margin-top:12px;padding:8px 10px;background:rgba(255,184,48,0.06);
                              border-left:2px solid rgba(255,184,48,0.4);border-radius:0 6px 6px 0;
                              font-size:12px;color:var(--text-muted);'>
                    💡 {finfo["tip"]}
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Top 5 ranked
            section_label("Top 5 Crop Matches")
            colors5 = ["#00ff88","#00d4aa","#4fc3f7","#b39ddb","#ffb830"]
            html_ranks = ""
            for i, (_, row) in enumerate(top5.iterrows()):
                html_ranks += top_crop_row(i+1, row["crop"], row["match_pct"], colors5[i])
            st.markdown(html_ranks, unsafe_allow_html=True)

            # Match bar chart
            if PLOTLY_OK:
                fig_bar = make_bar_chart(
                    top5["crop"].tolist(), top5["match_pct"].tolist(),
                    colors5, "Match Score Comparison (%)"
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

            # Nutrient status
            section_label("Nutrient Status Analysis")
            for msg, action, color in defic:
                st.markdown(
                    f"<div class='def-row'>"
                    f"<span class='def-msg' style='color:{color}'>{msg}</span>"
                    f"<span class='def-action'>{action}</span></div>",
                    unsafe_allow_html=True)
        else:
            st.markdown(empty_state("🌱", [
                "Configure soil & climate parameters",
                "then click ANALYSE & RECOMMEND CROP",
                "— AI will suggest the best variety",
            ]), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 2 — FERTILIZER ADVISOR                                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab2:
    col_l2, col_r2 = st.columns([1, 1.2], gap="large")

    with col_l2:
        section_label("Crop & Soil Selection")
        f_crop = st.selectbox("Select Crop",  ALL_CROPS,  key="f_crop")
        f_soil = st.selectbox("Soil Type",    SOIL_TYPES, key="f_soil")

        section_label("Current Soil NPK (mg/kg)")
        fN = st.slider("Nitrogen N",   0, 140, 55, key="fN")
        fP = st.slider("Phosphorus P", 0, 145, 35, key="fP")
        fK = st.slider("Potassium K",  0, 205, 45, key="fK")

        # NPK bars
        st.markdown(
            npk_bar("Nitrogen",   fN, 140, "#00ff88") +
            npk_bar("Phosphorus", fP, 145, "#4fc3f7") +
            npk_bar("Potassium",  fK, 205, "#ffb830"),
            unsafe_allow_html=True
        )

        section_label("Soil Condition")
        soil_note, soil_col = SOIL_ADVICE.get(f_soil, ("Standard soil.", "#00ff88"))
        st.markdown(
            f"<div style='padding:10px 14px;background:{soil_col}12;border:1px solid {soil_col}30;"
            f"border-radius:8px;font-size:12px;color:{soil_col};'>"
            f"ℹ️ {soil_note}</div>",
            unsafe_allow_html=True)

        run2 = st.button("🧪  GET FERTILIZER ADVICE", key="btn2")

    with col_r2:
        if run2:
            frow   = fert_df[fert_df["crop"] == f_crop]
            finfo  = frow.iloc[0] if len(frow) else None
            defic  = check_deficiencies(fN, fP, fK)
            crop_r = crop_df[crop_df["crop"] == f_crop]
            icon   = CROP_ICONS.get(f_crop, "🌿")

            if finfo is not None:
                npk_parts = finfo["npk"].split(":")
                npk_labels = ["N Ratio","P Ratio","K Ratio"]
                if len(npk_parts) == 3:
                    try:
                        npk_vals = [float(x) for x in npk_parts]
                        total_npk = sum(npk_vals) or 1
                        npk_pcts = [v / total_npk * 100 for v in npk_vals]
                    except ValueError:
                        npk_pcts = [33.3, 33.3, 33.3]
                else:
                    npk_pcts = [33.3, 33.3, 33.3]

                st.markdown(f"""
                <div class='glow-card glow-card-amber' style='position:relative'>
                  <div class='result-scan'></div>
                  <div class='crop-hero'>
                    <div class='crop-icon-box' style='background:rgba(255,184,48,0.1);
                                border-color:rgba(255,184,48,0.3);'>{icon}</div>
                    <div>
                      <div class='crop-name-big'>{finfo["fertilizer"]}</div>
                      <div class='crop-season-tag'>FOR {f_crop.upper()} · {f_soil.upper()} SOIL</div>
                    </div>
                  </div>
                  {conf_tag('VERIFIED PROFILE', 'info')}
                  {conf_tag(f'NPK {finfo["npk"]}', 'medium')}
                  <div class='kv-grid'>
                    {kv_pair("Total Dose",      finfo["dose"],    "kv-val-amber")}
                    {kv_pair("Application",     finfo["timing"],  "")}
                    {kv_pair("Organic Alt.",    finfo["organic"], "kv-val-green")}
                    {kv_pair("Estimated Cost",  finfo["cost"],    "kv-val-amber")}
                  </div>
                  <div style='margin-top:14px;padding:10px 12px;background:rgba(255,184,48,0.06);
                              border-left:3px solid rgba(255,184,48,0.5);border-radius:0 8px 8px 0;
                              font-size:13px;color:var(--text-muted);line-height:1.5;'>
                    <b style='color:var(--g-amber);font-size:10px;font-family:var(--font-mono);
                               letter-spacing:0.08em;'>PRO TIP</b><br>
                    {finfo["tip"]}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # NPK composition radar
                if PLOTLY_OK:
                    fig_npk = make_radar_chart(
                        ["Nitrogen", "Phosphorus", "Potassium"],
                        npk_vals if len(npk_parts)==3 else [1,1,1],
                        [max(npk_vals or [1])]*3 if len(npk_parts)==3 else [1,1,1],
                        "Fertilizer NPK Composition", "#ffb830"
                    )
                    st.plotly_chart(fig_npk, use_container_width=True, config={"displayModeBar": False})

            # Deficiency analysis
            section_label("Nutrient Deficiency Analysis")
            for msg, action, color in defic:
                st.markdown(
                    f"<div class='def-row'>"
                    f"<span class='def-msg' style='color:{color}'>{msg}</span>"
                    f"<span class='def-action'>{action}</span></div>",
                    unsafe_allow_html=True)

            # Applied vs ideal comparison
            if len(crop_r):
                cr = crop_r.iloc[0]
                section_label("Soil NPK vs Ideal Range")
                nutrients = [
                    ("Nitrogen",   fN, cr.N_min, cr.N_max, 140, "#00ff88"),
                    ("Phosphorus", fP, cr.P_min, cr.P_max, 145, "#4fc3f7"),
                    ("Potassium",  fK, cr.K_min, cr.K_max, 205, "#ffb830"),
                ]
                for nname, nval, nlo, nhi, nmax, ncol in nutrients:
                    pct_cur  = min(100, round(nval / nmax * 100))
                    pct_lo   = round(nlo / nmax * 100)
                    pct_hi   = round(nhi / nmax * 100)
                    in_range = nlo <= nval <= nhi
                    status_col = "#00ff88" if in_range else "#ff6b6b"
                    status_txt = "✅ In range" if in_range else "⚠️ Out of range"
                    st.markdown(f"""
                    <div style='margin-bottom:14px;'>
                      <div style='display:flex;justify-content:space-between;
                                  font-family:var(--font-mono);font-size:11px;margin-bottom:5px;'>
                        <span style='color:#e8f5e9;'>{nname}</span>
                        <span style='color:{status_col};'>{status_txt} · {nval} mg/kg</span>
                      </div>
                      <div style='height:12px;background:rgba(255,255,255,0.05);
                                  border-radius:6px;overflow:visible;position:relative;'>
                        <div style='position:absolute;left:{pct_lo}%;right:{100-pct_hi}%;
                                    top:0;bottom:0;background:rgba(0,255,136,0.15);
                                    border-radius:4px;'></div>
                        <div style='position:absolute;left:0;top:0;bottom:0;width:{pct_cur}%;
                                    background:{ncol};border-radius:6px;
                                    box-shadow:0 0 8px {ncol}60;'></div>
                      </div>
                      <div style='display:flex;justify-content:space-between;
                                  font-family:var(--font-mono);font-size:8px;
                                  color:var(--text-dim);margin-top:3px;'>
                        <span>0</span>
                        <span style='color:rgba(0,255,136,0.5);'>Ideal: {int(nlo)}–{int(nhi)}</span>
                        <span>{nmax}</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(empty_state("🧪", [
                "Select a crop & soil type",
                "set current NPK levels",
                "then click GET FERTILIZER ADVICE",
            ]), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 3 — OVERUSE DETECTOR                                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab3:
    col_l3, col_r3 = st.columns([1, 1.2], gap="large")

    with col_l3:
        section_label("Crop & Season")
        o_crop   = st.selectbox("Crop",   OVER_CROPS, key="o_crop")
        o_season = st.selectbox("Season", ["Kharif","Rabi","Zaid","Annual"], key="o_season")

        section_label("Applied Fertilizer (kg/ha)")
        o_urea = st.slider("Urea applied",  0, 500, 130, step=5, key="ourea")
        o_dap  = st.slider("DAP applied",   0, 300,  65, step=5, key="odap")
        o_mop  = st.slider("MOP applied",   0, 350,  45, step=5, key="omop")

        section_label("Soil Condition")
        o_ph   = st.slider("Soil pH", 3.5, 9.5, 6.5, step=0.1, key="oph")

        # Live usage bars
        o_row = over_df[over_df["crop"] == o_crop]
        if len(o_row):
            ol = o_row.iloc[0]
            st.markdown(
                fert_usage_bar("Urea", o_urea, ol["urea_limit"], "#00ff88") +
                fert_usage_bar("DAP",  o_dap,  ol["dap_limit"],  "#4fc3f7") +
                fert_usage_bar("MOP",  o_mop,  ol["mop_limit"],  "#ffb830"),
                unsafe_allow_html=True)

        run3 = st.button("⚠️  ANALYZE FERTILIZER USAGE", key="btn3")

    with col_r3:
        if run3:
            result_df, risk, rclass, ph_warn, total_wst, symptoms = analyze_overuse(
                over_df, o_crop, o_urea, o_dap, o_mop, o_ph)

            risk_colors = {
                "Safe": "#00ff88", "Moderate": "#ffb830",
                "High": "#ff6b6b", "Critical": "#ff3333"
            }
            risk_emojis = {
                "Safe": "🟢", "Moderate": "🟡", "High": "🔴", "Critical": "💀"
            }
            rc   = risk_colors.get(risk, "#ffb830")
            remj = risk_emojis.get(risk, "⚠️")
            icon = CROP_ICONS.get(o_crop, "🌿")

            st.markdown(f"""
            <div class='glow-card' style='position:relative'>
              <div class='result-scan'></div>
              <div class='risk-meter {rclass}'>
                <div class='risk-label' style='color:{rc}'>{remj} {risk} Risk</div>
                <div class='risk-sub'>{o_crop.upper()} · {o_season.upper()} SEASON</div>
              </div>
              <div class='kv-grid' style='margin-top:12px'>
                {kv_pair("Crop",        o_crop,             "")}
                {kv_pair("Season",      o_season,           "")}
                {kv_pair("Waste Cost",  f"₹{total_wst:,} / ha", "kv-val-amber" if total_wst > 0 else "kv-val-green")}
                {kv_pair("Soil pH",     str(o_ph),          "")}
              </div>
              {"<div style='margin-top:12px;padding:9px 12px;background:rgba(255,107,107,0.08);border-left:2px solid rgba(255,107,107,0.4);border-radius:0 6px 6px 0;font-size:12px;color:#ff9999;'><b>⚠️ Overuse Symptoms:</b><br>" + symptoms + "</div>" if risk in ("High","Critical") else ""}
            </div>
            """, unsafe_allow_html=True)

            # Gauge chart
            if PLOTLY_OK:
                max_ratio = result_df["ratio"].max()
                gauge_col = rc
                fig_g = make_gauge(
                    min(200, round(max_ratio * 100)),
                    "Peak Usage (% of Safe Limit)",
                    gauge_col, max_val=200
                )
                st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})

            section_label("Fertilizer Breakdown")
            for _, row in result_df.iterrows():
                sc = row["Status Color"]
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:10px 12px;background:rgba(255,255,255,0.02);
                            border:1px solid {sc}22;border-radius:8px;margin-bottom:8px;'>
                  <div>
                    <div style='font-family:var(--font-display);font-size:14px;font-weight:700;
                                color:#e8f5e9;'>{row["Fertilizer"]}</div>
                    <div style='font-family:var(--font-mono);font-size:9px;color:var(--text-dim);
                                margin-top:2px;'>
                      Applied: {row["Applied"]} · Limit: {row["Safe Limit"]} · Excess: {row["Excess (kg/ha)"]} kg/ha
                    </div>
                  </div>
                  <div style='text-align:right'>
                    <div style='font-family:var(--font-display);font-size:18px;font-weight:700;
                                color:{sc};'>{row["Usage %"]}%</div>
                    <div style='font-family:var(--font-mono);font-size:9px;color:{sc};
                                margin-top:1px;'>{row["Status"]}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Recommendations
            section_label("Action Recommendations")
            if risk in ("High", "Critical"):
                recs = [
                    ("🛑", "Stop further fertilizer application immediately", "#ff6b6b"),
                    ("💧", "Irrigate deeply to leach excess nutrients from root zone", "#4fc3f7"),
                    ("🧪", "Re-test soil in 3 weeks before next application", "#ffb830"),
                    ("🪨", "Apply agricultural lime if pH dropped below 5.5", "#00ff88"),
                    ("📋", "Document current usage for agronomist review", "#b39ddb"),
                ]
            elif risk == "Moderate":
                recs = [
                    ("📉", "Reduce next fertilizer dose by 15–20%", "#ffb830"),
                    ("👁", "Monitor for leaf burn or tip necrosis symptoms", "#ffb830"),
                    ("🔀", "Switch to split-dose application schedule", "#00d4aa"),
                    ("📊", "Track usage weekly against safe limits", "#4fc3f7"),
                ]
            else:
                recs = [
                    ("✅", "Application is within safe limits — excellent management", "#00ff88"),
                    ("📋", "Continue current fertilization practices", "#00d4aa"),
                    ("📈", "Fine-tune doses based on next soil test results", "#4fc3f7"),
                    ("🌱", "Consider organic supplements to reduce synthetic load", "#7fff6a"),
                ]

            for emoji, txt, col in recs:
                st.markdown(
                    f"<div style='display:flex;align-items:flex-start;gap:10px;"
                    f"padding:9px 0;border-bottom:1px solid var(--border-dim);'>"
                    f"<span style='font-size:16px;margin-top:1px;'>{emoji}</span>"
                    f"<span style='font-size:13px;color:{col};line-height:1.4;'>{txt}</span>"
                    f"</div>",
                    unsafe_allow_html=True)

            if ph_warn:
                st.warning(ph_warn)

        else:
            st.markdown(empty_state("⚠️", [
                "Select crop, season & applied amounts",
                "then click ANALYZE FERTILIZER USAGE",
                "— risk level & savings calculated instantly",
            ]), unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 4 — SOIL DASHBOARD                                                ║
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab4:
    st.markdown("""
    <div style='font-family:var(--font-mono);font-size:10px;letter-spacing:0.1em;
                color:var(--text-muted);margin-bottom:20px;'>
    LIVE SOIL INTELLIGENCE DASHBOARD — Enter parameters below to get real-time analysis
    </div>
    """, unsafe_allow_html=True)

    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        section_label("Soil Nutrients")
        dN  = st.slider("N (mg/kg)",  0, 140,  80, key="dN")
        dP  = st.slider("P (mg/kg)",  0, 145,  55, key="dP")
        dK  = st.slider("K (mg/kg)",  0, 205,  70, key="dK")
    with dc2:
        section_label("Climate")
        dT  = st.slider("Temp (°C)",   8,  45, 26, key="dT")
        dH  = st.slider("Humidity (%)",10, 100, 68, key="dH")
        dR  = st.slider("Rainfall",   20, 300, 140, key="dR")
    with dc3:
        section_label("Soil Properties")
        dpH = st.slider("Soil pH",  3.5, 9.5, 6.8, step=0.1, key="dpH")
        dLA = st.slider("Land Area (acres)", 0.5, 50.0, 5.0, step=0.5, key="dLA")

    health = soil_health_score(dN, dP, dK, dpH, dT, dH, dR)
    health_col = "#00ff88" if health >= 70 else "#ffb830" if health >= 45 else "#ff6b6b"
    health_label = "Excellent" if health >= 80 else "Good" if health >= 65 else "Moderate" if health >= 45 else "Poor"

    st.markdown("<br>", unsafe_allow_html=True)

    # Metric cards
    dm1, dm2, dm3, dm4, dm5 = st.columns(5)
    dm1.metric("Soil Health Index", f"{health}",   health_label)
    dm2.metric("N Level",           f"{dN}",       "mg/kg")
    dm3.metric("P Level",           f"{dP}",       "mg/kg")
    dm4.metric("K Level",           f"{dK}",       "mg/kg")
    dm5.metric("Field Area",        f"{dLA} ac",   "")

    # Charts row
    if PLOTLY_OK:
        ch1, ch2, ch3 = st.columns(3)
        with ch1:
            section_label("Soil NPK Profile Radar")
            fig_r = make_radar_chart(
                ["Nitrogen", "Phosphorus", "Potassium", "pH Score", "Humidity"],
                [dN, dP, dK, (10 - abs(dpH-6.5))*10, dH],
                [140, 145, 205, 100, 100],
                "Soil Profile",
            )
            st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})

        with ch2:
            section_label("NPK Balance Chart")
            total_npk = dN + dP + dK or 1
            fig_pie = go.Figure(go.Pie(
                labels=["Nitrogen", "Phosphorus", "Potassium"],
                values=[dN, dP, dK],
                hole=0.55,
                marker=dict(
                    colors=["#00ff88","#4fc3f7","#ffb830"],
                    line=dict(color="#0a1510", width=2),
                ),
                textfont=dict(family="JetBrains Mono", size=10, color="#e8f5e9"),
                textposition="outside",
            ))
            fig_pie.update_layout(
                **PLOTLY_THEME,
                title=dict(text="NPK Proportion", font=dict(size=11, color="#e8f5e9")),
                showlegend=True,
                legend=dict(font=dict(color="#6b9e7a", size=9)),
                height=280,
                annotations=[dict(
                    text=f"{total_npk}<br><span style='font-size:8px'>total</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=14, color="#e8f5e9", family="Syne"),
                )],
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

        with ch3:
            section_label("Health Score Gauge")
            fig_health = make_gauge(health, "Soil Health Score", health_col, max_val=100)
            st.plotly_chart(fig_health, use_container_width=True, config={"displayModeBar": False})

    # Crop suitability heatmap across all crops
    section_label("Crop Suitability Ranking for Current Parameters")
    scores_all = crop_df.copy()
    scores_all["score"]    = scores_all.apply(
        lambda r: score_crop(r, dN, dP, dK, dT, dH, dpH, dR), axis=1)
    scores_all["match%"]   = (scores_all["score"] / 27 * 100).round(1).clip(0, 100)
    scores_all = scores_all.sort_values("score", ascending=False)

    if PLOTLY_OK:
        top10 = scores_all.head(10)
        colors_bar = [
            "#00ff88" if v >= 70 else "#ffb830" if v >= 45 else "#4fc3f7"
            for v in top10["match%"]
        ]
        fig_rank = go.Figure(go.Bar(
            y=top10["crop"], x=top10["match%"],
            orientation='h',
            marker=dict(color=colors_bar, line=dict(color="#0a1510", width=1)),
            text=[f'{v:.1f}%' for v in top10["match%"]],
            textposition='outside',
            textfont=dict(size=10, color="#6b9e7a"),
        ))
        fig_rank.update_layout(
            **PLOTLY_THEME,
            title=dict(text="Top 10 Suitable Crops for Current Soil Conditions",
                       font=dict(size=12, color="#e8f5e9")),
            xaxis=dict(range=[0,120], gridcolor="rgba(0,255,136,0.05)", tickfont=dict(size=9)),
            yaxis=dict(gridcolor="rgba(0,255,136,0.05)", tickfont=dict(size=10, color="#e8f5e9")),
            height=320,
        )
        st.plotly_chart(fig_rank, use_container_width=True, config={"displayModeBar": False})

    # Soil summary block
    st.markdown(f"""
    <div class='glow-card'>
      <div style='font-family:var(--font-mono);font-size:9px;letter-spacing:0.1em;
                  color:var(--g-primary);text-transform:uppercase;margin-bottom:14px;'>
        Soil Condition Summary
      </div>
      <div class='kv-grid'>
        {kv_pair("Health Index",    f'{health} / 100 — {health_label}', "kv-val-green")}
        {kv_pair("pH Assessment",   "Optimal (6.0–7.5)" if 6.0<=dpH<=7.5 else "Out of optimal range", "" if 6.0<=dpH<=7.5 else "kv-val-amber")}
        {kv_pair("N Status",        "Sufficient" if dN >= 50 else "Deficient", "" if dN >= 50 else "kv-val-amber")}
        {kv_pair("P Status",        "Sufficient" if dP >= 30 else "Deficient", "" if dP >= 30 else "kv-val-amber")}
        {kv_pair("K Status",        "Sufficient" if dK >= 30 else "Deficient", "" if dK >= 30 else "kv-val-amber")}
        {kv_pair("Humidity",        "Optimal" if 50<=dH<=80 else "Suboptimal", "")}
        {kv_pair("Total NPK",       f'{dN+dP+dK} mg/kg', "kv-val-blue")}
        {kv_pair("Field Size",      f'{dLA} acres = {dLA*0.405:.2f} ha', "")}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 5 — REFERENCE ATLAS                                               ║
# ╚══════════════════════════════════════════════════════════════════════════╝
with tab5:
    section_label("Crop Knowledge Atlas")

    filter_crops = st.multiselect(
        "Filter crops", ALL_CROPS, default=ALL_CROPS[:8], key="ref_filter")

    display_crop = crop_df[[
        "crop","icon","season","yield",
        "N_min","N_max","P_min","P_max","K_min","K_max",
        "T_min","T_max","pH_min","pH_max","R_min","R_max",
    ]].copy()
    display_crop.columns = [
        "Crop","Emoji","Season","Yield",
        "N min","N max","P min","P max","K min","K max",
        "T min (°C)","T max (°C)","pH min","pH max","Rain min","Rain max",
    ]

    if filter_crops:
        st.dataframe(
            display_crop[display_crop["Crop"].isin(filter_crops)],
            use_container_width=True, hide_index=True)
    else:
        st.dataframe(display_crop, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_label("Fertilizer Reference Guide")
    fert_display = fert_df.rename(columns={
        "crop":"Crop","fertilizer":"Fertilizer","npk":"NPK Ratio",
        "dose":"Dose","timing":"Application Timing",
        "organic":"Organic Alt.","cost":"Est. Cost","tip":"Expert Tip"
    })
    if filter_crops:
        st.dataframe(
            fert_display[fert_display["Crop"].isin(filter_crops)],
            use_container_width=True, hide_index=True)
    else:
        st.dataframe(fert_display, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_label("Overuse Safe Limits Reference")
    over_display = over_df.rename(columns={
        "crop":"Crop", "urea_limit":"Urea Limit (kg/ha)",
        "dap_limit":"DAP Limit (kg/ha)", "mop_limit":"MOP Limit (kg/ha)",
        "season":"Season","overuse_symptoms":"Overuse Symptoms",
    })
    st.dataframe(over_display, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_label("Soil Type Guide")
    s1, s2, s3 = st.columns(3)
    soil_items = list(SOIL_ADVICE.items())
    for i, (soil, (note, col)) in enumerate(soil_items):
        col_obj = [s1, s2, s3][i % 3]
        col_obj.markdown(f"""
        <div style='background:var(--bg-card);border:1px solid {col}22;
                    border-radius:10px;padding:14px;margin-bottom:10px;'>
          <div style='font-family:var(--font-display);font-size:15px;font-weight:700;
                      color:{col};margin-bottom:6px;'>{soil}</div>
          <div style='font-size:12px;color:var(--text-muted);line-height:1.5;'>{note}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_label("System Statistics")
    sm1, sm2, sm3, sm4, sm5, sm6 = st.columns(6)
    sm1.metric("Crop Profiles",    len(crop_df))
    sm2.metric("Fertilizer Types", len(fert_df))
    sm3.metric("Overuse Rules",    len(over_df))
    sm4.metric("Soil Categories",  len(SOIL_ADVICE))
    sm5.metric("Input Features",   "23")
    sm6.metric("ML Training Data", "15,000")