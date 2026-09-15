import os
from datetime import datetime

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from main import app, llm


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="AeroPlan AI — Intelligent Travel",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# SESSION STATE
# =============================================================================
if "trip_query" not in st.session_state:
    st.session_state.trip_query = ""

if "last_plan" not in st.session_state:
    st.session_state.last_plan = None

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "last_thread" not in st.session_state:
    st.session_state.last_thread = "Sai Rohit"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# =============================================================================
# PREMIUM UI
# =============================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --bg: #070b12;
    --panel: #0c121c;
    --panel-2: #101925;
    --panel-3: #131e2d;
    --line: rgba(148, 163, 184, 0.14);
    --line-strong: rgba(96, 165, 250, 0.28);
    --text: #f8fafc;
    --muted: #91a1b5;
    --muted-2: #63748a;
    --blue: #60a5fa;
    --blue-2: #3b82f6;
    --cyan: #22d3ee;
    --green: #34d399;
    --purple: #a78bfa;
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 72% -5%, rgba(59,130,246,.12), transparent 27rem),
        radial-gradient(circle at 12% 18%, rgba(34,211,238,.055), transparent 23rem),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding: 1.35rem 2.2rem 4rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #080d15 0%, #090f18 55%, #070b12 100%) !important;
    border-right: 1px solid var(--line) !important;
}

section[data-testid="stSidebar"] > div {
    padding: 1.1rem .95rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: .75rem;
    margin: .25rem .25rem 1.5rem;
}

.brand-mark {
    width: 42px;
    height: 42px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    font-size: 1.25rem;
    background: linear-gradient(145deg, rgba(59,130,246,.28), rgba(34,211,238,.10));
    border: 1px solid rgba(96,165,250,.25);
    box-shadow: 0 10px 30px rgba(37,99,235,.12);
}

.brand-name {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -.02em;
    font-size: 1.02rem;
}

.brand-sub {
    color: #718198;
    font-size: .7rem;
    margin-top: .12rem;
}

.sidebar-label {
    color: #65758a;
    font-size: .67rem;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin: 1.25rem .35rem .55rem;
}

.sidebar-item {
    display: flex;
    align-items: center;
    gap: .65rem;
    padding: .72rem .78rem;
    margin: .28rem 0;
    border-radius: 11px;
    border: 1px solid rgba(148,163,184,.08);
    background: rgba(15,23,42,.56);
    color: #aebdd0;
    font-size: .82rem;
    transition: .2s ease;
}

.sidebar-item:hover {
    border-color: rgba(96,165,250,.22);
    background: rgba(30,41,59,.72);
    color: #e8f1fb;
}

.pipeline-item {
    position: relative;
}

.pipeline-num {
    width: 23px;
    height: 23px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: rgba(59,130,246,.12);
    border: 1px solid rgba(96,165,250,.25);
    color: #7db9fa;
    font-size: .68rem;
    font-weight: 700;
}

.sidebar-foot {
    margin-top: 1.4rem;
    padding: .85rem;
    border-radius: 12px;
    background: linear-gradient(145deg, rgba(16,29,46,.9), rgba(10,18,29,.9));
    border: 1px solid var(--line);
    color: #7d8da1;
    font-size: .72rem;
    line-height: 1.55;
}

/* ---------- Top mini nav ---------- */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.topbar-left {
    color: #728196;
    font-size: .78rem;
}

.topbar-left strong {
    color: #dbeafe;
    font-weight: 600;
}

.live-pill {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    padding: .35rem .65rem;
    border-radius: 999px;
    background: rgba(52,211,153,.07);
    border: 1px solid rgba(52,211,153,.18);
    color: #78e7bd;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .05em;
    text-transform: uppercase;
}

.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 10px rgba(52,211,153,.9);
}

/* ---------- Hero ---------- */
.hero {
    min-height: 405px;
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    border: 1px solid rgba(148,163,184,.15);
    background:
        linear-gradient(90deg, rgba(5,10,17,.97) 0%, rgba(5,10,17,.76) 42%, rgba(5,10,17,.28) 100%),
        linear-gradient(180deg, rgba(5,10,17,.05), rgba(5,10,17,.68)),
        url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1800&q=90') center/cover;
    box-shadow: 0 28px 80px rgba(0,0,0,.34);
    display: flex;
    align-items: center;
    padding: 3.3rem 4rem;
    margin-bottom: 1.15rem;
}

.hero::after {
    content: "";
    position: absolute;
    width: 430px;
    height: 430px;
    right: -130px;
    bottom: -250px;
    border-radius: 50%;
    background: rgba(59,130,246,.16);
    filter: blur(35px);
}

.hero-copy {
    position: relative;
    z-index: 2;
    max-width: 710px;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .4rem .72rem;
    border-radius: 999px;
    background: rgba(59,130,246,.12);
    border: 1px solid rgba(96,165,250,.25);
    color: #8ec5ff;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .13em;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
}

.hero h1 {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.8rem, 5vw, 4.65rem);
    line-height: .98;
    letter-spacing: -.065em;
    margin: 0;
    color: #fff;
    font-weight: 800;
}

.hero h1 span {
    color: #79b8ff;
}

.hero p {
    color: #aebdce;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 630px;
    margin: 1.25rem 0 0;
}

.hero-stats {
    display: flex;
    gap: .7rem;
    margin-top: 1.6rem;
    flex-wrap: wrap;
}

.hero-stat {
    padding: .58rem .8rem;
    border-radius: 10px;
    background: rgba(8,15,24,.55);
    border: 1px solid rgba(148,163,184,.12);
    backdrop-filter: blur(10px);
    color: #b9c7d8;
    font-size: .72rem;
}

.hero-stat strong {
    color: #eef6ff;
    font-size: .8rem;
}

/* ---------- Destination cards ---------- */
.section-kicker {
    color: #65758a;
    font-size: .67rem;
    font-weight: 800;
    letter-spacing: .15em;
    text-transform: uppercase;
    margin: 1.55rem 0 .7rem;
}

.destination-card {
    position: relative;
    height: 132px;
    border-radius: 17px;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,.13);
    background: #111827;
    box-shadow: 0 10px 25px rgba(0,0,0,.16);
}

.destination-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: saturate(.82) brightness(.63);
    transition: transform .35s ease, filter .35s ease;
}

.destination-card:hover img {
    transform: scale(1.06);
    filter: saturate(1) brightness(.78);
}

.destination-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: flex-end;
    padding: .75rem;
    background: linear-gradient(transparent 25%, rgba(4,8,14,.88));
}

.destination-name {
    color: #fff;
    font-weight: 700;
    font-size: .84rem;
}

.destination-tag {
    color: #a7b7c9;
    font-size: .65rem;
    margin-top: .13rem;
}

/* ---------- Trip builder ---------- */
.builder {
    margin-top: 1.55rem;
    border-radius: 22px;
    border: 1px solid rgba(96,165,250,.18);
    background:
        linear-gradient(145deg, rgba(17,29,45,.88), rgba(10,16,26,.94));
    padding: 1.35rem;
    box-shadow: 0 20px 50px rgba(0,0,0,.18);
}

.builder-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: .95rem;
}

.builder-title {
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
    font-size: 1.15rem;
    color: #f1f7ff;
}

.builder-sub {
    color: #718198;
    font-size: .76rem;
    margin-top: .2rem;
}

.builder-badge {
    padding: .36rem .62rem;
    border-radius: 8px;
    background: rgba(167,139,250,.08);
    border: 1px solid rgba(167,139,250,.18);
    color: #bcaaf9;
    font-size: .65rem;
    font-weight: 700;
    white-space: nowrap;
}

.quick-label {
    color: #75869a;
    font-size: .67rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin: .65rem 0 .5rem;
}

/* ---------- Streamlit controls ---------- */
.stTextArea textarea,
.stTextInput input {
    background: #080f19 !important;
    color: #eaf3fd !important;
    border: 1px solid rgba(148,163,184,.16) !important;
    border-radius: 13px !important;
    font-size: .92rem !important;
}

.stTextArea textarea {
    min-height: 126px !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: rgba(96,165,250,.55) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.10) !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #4e6075 !important;
}

.stTextInput label,
.stTextArea label {
    color: #8ea1b7 !important;
}

div[data-testid="stButton"] > button {
    border-radius: 11px !important;
    border: 1px solid rgba(96,165,250,.15) !important;
    background: #101b2a !important;
    color: #b9c9da !important;
    font-weight: 600 !important;
    transition: all .2s ease !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: rgba(96,165,250,.45) !important;
    color: #fff !important;
    background: #15263a !important;
    transform: translateY(-1px);
}

.generate-btn div[data-testid="stButton"] > button {
    min-height: 54px !important;
    border: 0 !important;
    border-radius: 13px !important;
    background: linear-gradient(135deg, #2563eb, #1686d9 55%, #16a8c8) !important;
    color: #fff !important;
    font-size: .98rem !important;
    font-weight: 800 !important;
    box-shadow: 0 13px 34px rgba(37,99,235,.25) !important;
}

.generate-btn div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #3475f2, #2297e6 55%, #20b8d8) !important;
    box-shadow: 0 17px 42px rgba(37,99,235,.34) !important;
    transform: translateY(-2px);
}

.generate-btn div[data-testid="stButton"] > button:active {
    transform: translateY(0);
}

/* ---------- Agent live section ---------- */
.pipeline-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 2rem 0 .8rem;
}

.pipeline-title {
    font-family: 'Manrope', sans-serif;
    color: #eef6ff;
    font-size: 1.12rem;
    font-weight: 800;
}

.pipeline-sub {
    color: #6f8196;
    font-size: .72rem;
}

[data-testid="stStatusWidget"] {
    background: linear-gradient(145deg, #0d1725, #0a111b) !important;
    border: 1px solid rgba(96,165,250,.16) !important;
    border-radius: 14px !important;
    margin-bottom: .55rem !important;
}

[data-testid="stStatusWidget"] * {
    color: #dce9f6 !important;
}

[data-testid="stStatusWidget"] details > div {
    background: #080f18 !important;
    border-top: 1px solid rgba(148,163,184,.08) !important;
}

[data-testid="stStatusWidget"] a {
    color: #69b3ff !important;
}

/* ---------- Results ---------- */
.result-head {
    margin: 2rem 0 .7rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.result-title {
    font-family: 'Manrope', sans-serif;
    color: #f3f8ff;
    font-size: 1.18rem;
    font-weight: 800;
}

.result-caption {
    color: #718198;
    font-size: .7rem;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .75rem;
    margin: 1rem 0 1.25rem;
}

.metric-box {
    padding: 1rem 1.1rem;
    border-radius: 14px;
    background: linear-gradient(145deg, #0e1826, #0a111a);
    border: 1px solid rgba(148,163,184,.12);
}

.metric-icon {
    font-size: .85rem;
    opacity: .85;
}

.metric-val {
    color: #f4f9ff;
    font-family: 'Manrope', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: .25rem;
}

.metric-lbl {
    color: #6f8197;
    font-size: .66rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-top: .1rem;
}

.final-card {
    border-radius: 18px;
    border: 1px solid rgba(96,165,250,.19);
    border-left: 3px solid #4d9bf3;
    background:
        radial-gradient(circle at 100% 0%, rgba(59,130,246,.10), transparent 22rem),
        linear-gradient(145deg, #0e1a2a, #090f18);
    padding: 1.5rem 1.65rem;
    color: #cbd9e8;
    line-height: 1.82;
    font-size: .92rem;
    box-shadow: 0 20px 55px rgba(0,0,0,.2);
}

.final-card h1, .final-card h2, .final-card h3 {
    color: #f3f8ff !important;
}

/* ---------- Trip chat ---------- */
.chat-shell {
    margin-top: 1.8rem;
    padding: 1.35rem 1.45rem 1rem;
    border: 1px solid rgba(96,165,250,.22);
    border-radius: 20px;
    background:
        radial-gradient(circle at 92% 0%, rgba(34,211,238,.12), transparent 16rem),
        linear-gradient(145deg, rgba(16,31,49,.98), rgba(8,15,24,.98));
    box-shadow: 0 20px 55px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.035);
}

.chat-title {
    font-family: 'Manrope', sans-serif;
    color: #f3f8ff;
    font-size: 1.22rem;
    font-weight: 800;
    letter-spacing: -.02em;
}

.chat-caption {
    color: #91a8bf;
    font-size: .76rem;
    line-height: 1.5;
    margin-top: .28rem;
}

[data-testid="stChatMessage"] {
    background: rgba(15, 28, 43, .72) !important;
    border: 1px solid rgba(148,163,184,.1);
    border-radius: 13px !important;
    margin: .55rem 0 !important;
}

[data-testid="stChatInput"] {
    padding: .4rem .45rem .6rem;
    border: 1px solid rgba(96,165,250,.23);
    border-radius: 16px;
    background: linear-gradient(145deg, #111f31, #0b1522);
    box-shadow: 0 12px 32px rgba(0,0,0,.2), 0 0 0 4px rgba(34,211,238,.035);
}

[data-testid="stChatInput"] > div {
    border: 0 !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea {
    min-height: 48px !important;
    padding: .82rem 1rem !important;
    border: 1px solid rgba(148,163,184,.14) !important;
    border-radius: 11px !important;
    background: #080f19 !important;
    color: #eaf3fd !important;
    font-size: .9rem !important;
    transition: border-color .2s ease, box-shadow .2s ease !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(34,211,238,.58) !important;
    box-shadow: 0 0 0 3px rgba(34,211,238,.1) !important;
}

[data-testid="stChatInput"] button {
    width: 46px !important;
    height: 46px !important;
    margin-left: .45rem !important;
    border: 1px solid rgba(125,211,252,.3) !important;
    border-radius: 11px !important;
    background: linear-gradient(145deg, #1686d9, #2563eb) !important;
    color: #fff !important;
    box-shadow: 0 8px 20px rgba(37,99,235,.24) !important;
}

[data-testid="stChatInput"] button:hover {
    border-color: rgba(165,243,252,.7) !important;
    background: linear-gradient(145deg, #22a4df, #3475f2) !important;
    transform: translateY(-1px);
}

.save-bar {
    border: 1px solid rgba(148,163,184,.12);
    border-radius: 11px;
    padding: .75rem 1rem;
    color: #8092a7;
    font-size: .72rem;
    background: #0b131e;
}

.save-bar code {
    color: #75baff !important;
    background: transparent !important;
}

div[data-testid="stDownloadButton"] > button {
    min-height: 42px;
    border-radius: 11px !important;
    background: #122239 !important;
    border: 1px solid rgba(96,165,250,.25) !important;
    color: #d8eaff !important;
    font-weight: 700 !important;
}

/* ---------- Alerts / markdown ---------- */
.stAlert {
    background: #0d1724 !important;
    border: 1px solid rgba(148,163,184,.12) !important;
    border-radius: 12px !important;
}

.stAlert p, .stAlert div {
    color: #d9e6f4 !important;
}

.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
    color: #c5d3e2 !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #f1f7ff !important;
}

/* ---------- Responsive ---------- */
@media (max-width: 900px) {
    .block-container {
        padding: 1rem 1rem 3rem;
    }

    .hero {
        min-height: 360px;
        padding: 2rem;
    }

    .hero h1 {
        font-size: 2.65rem;
    }

    .metric-row {
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">✈️</div>
            <div>
                <div class="brand-name">AeroPlan AI</div>
                <div class="brand-sub">Multi-agent travel intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">Traveler</div>', unsafe_allow_html=True)

    thread_id = st.text_input(
        "User ID",
        value=st.session_state.last_thread,
        key="thread_id",
        label_visibility="collapsed",
        placeholder="Enter your traveler ID",
        help="Your session ID keeps travel history connected across queries.",
    )
    st.session_state.last_thread = thread_id

    st.markdown('<div class="sidebar-label">Technology</div>', unsafe_allow_html=True)

    for icon, tech in [
        ("◈", "LangGraph"),
        ("✦", "Groq · GPT-OSS-120B"),
        ("◆", "PostgreSQL"),
        ("⌕", "Tavily Search"),
        ("✈", "AviationStack"),
    ]:
        st.markdown(
            f'<div class="sidebar-item"><span>{icon}</span><span>{tech}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-label">Agent pipeline</div>', unsafe_allow_html=True)

    for num, label in [
        ("01", "Flight intelligence"),
        ("02", "Hotel discovery"),
        ("03", "Itinerary builder"),
        ("04", "Final trip planner"),
    ]:
        st.markdown(
            f"""
            <div class="sidebar-item pipeline-item">
                <span class="pipeline-num">{num}</span>
                <span>{label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="sidebar-foot">
            <strong style="color:#bcd0e5;">How it works</strong><br>
            Describe the trip you have in mind. Four specialized agents
            collaborate behind the scenes to turn it into a practical travel plan.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# TOP BAR
# =============================================================================
st.markdown(
    """
    <div class="topbar">
        <div class="topbar-left">
            <strong>AeroPlan AI</strong> &nbsp;/&nbsp; Intelligent trip workspace
        </div>
        <div class="live-pill">
            <span class="live-dot"></span>
            AI system online
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# HERO
# =============================================================================
st.markdown(
    """
    <section class="hero">
        <div class="hero-copy">
            <div class="eyebrow">✦ Your intelligent travel co-pilot</div>
            <h1>Travel planning,<br><span>reimagined.</span></h1>
            <p>
                Tell us where you want to go, what you want to experience,
                and what you want to spend. Our multi-agent AI turns that idea
                into a complete trip plan.
            </p>
            <div class="hero-stats">
                <div class="hero-stat">✈ <strong>Flights</strong> searched</div>
                <div class="hero-stat">⌂ <strong>Hotels</strong> discovered</div>
                <div class="hero-stat">◷ <strong>Itinerary</strong> optimized</div>
                <div class="hero-stat">✦ <strong>One</strong> final plan</div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# DESTINATIONS
# =============================================================================
st.markdown('<div class="section-kicker">Explore inspiration</div>', unsafe_allow_html=True)

DESTINATIONS = [
    (
        "🇯🇵 Tokyo",
        "Neon nights · culture",
        "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=500&q=85",
        "7-day Japan trip with Tokyo, Kyoto and Osaka",
    ),
    (
        "🇫🇷 Paris",
        "Art · food · romance",
        "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=500&q=85",
        "5-day Paris trip with hotels and sightseeing",
    ),
    (
        "🇹🇭 Bangkok",
        "Street food · energy",
        "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=500&q=85",
        "4-day Bangkok trip with food and city experiences",
    ),
    (
        "🇮🇹 Rome",
        "History · architecture",
        "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=500&q=85",
        "5-day Rome and Vatican sightseeing trip",
    ),
    (
        "🇦🇪 Dubai",
        "Luxury · adventure",
        "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=500&q=85",
        "3-day Dubai weekend with premium experiences",
    ),
]

dest_cols = st.columns(5, gap="small")

for col, (name, tag, image, prompt) in zip(dest_cols, DESTINATIONS):
    with col:
        st.markdown(
            f"""
            <div class="destination-card">
                <img src="{image}" alt="{name}">
                <div class="destination-overlay">
                    <div>
                        <div class="destination-name">{name}</div>
                        <div class="destination-tag">{tag}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Plan this trip", key=f"dest_{name}", use_container_width=True):
            st.session_state.trip_query = prompt
            st.rerun()


# =============================================================================
# TRIP BUILDER
# =============================================================================
st.markdown(
    """
    <div class="builder">
        <div class="builder-head">
            <div>
                <div class="builder-title">Build your trip</div>
                <div class="builder-sub">
                    Give the agents enough context and they'll handle the research.
                </div>
            </div>
            <div class="builder-badge">4 AI AGENTS</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="quick-label">Start with a template</div>', unsafe_allow_html=True)

QUICK = [
    ("🇯🇵", "Japan · 7 days · ₹2L", "Plan a 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs"),
    ("🇫🇷", "Paris · 5 days", "Plan a 5-day Paris trip including flights, hotels, food and major sightseeing"),
    ("🇦🇪", "Dubai · weekend", "Plan a Dubai weekend trip including flights, a good hotel and top experiences"),
    ("🏝️", "Bali · backpacking", "Plan a 10-day Bali backpacking trip with affordable stays and experiences"),
]

quick_cols = st.columns(4, gap="small")

for i, (icon, label, prompt) in enumerate(QUICK):
    with quick_cols[i]:
        if st.button(f"{icon}  {label}", key=f"quick_{i}", use_container_width=True):
            st.session_state.trip_query = prompt
            st.rerun()

user_query = st.text_area(
    "Trip brief",
    value=st.session_state.trip_query,
    key="trip_brief",
    placeholder=(
        "Example: Plan a complete 15-day US trip from Hyderabad including "
        "flights, hotels, sightseeing and an overall budget under ₹8 lakhs..."
    ),
    height=128,
    label_visibility="collapsed",
)

st.session_state.trip_query = user_query

st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
generate = st.button(
    "✦  Create my intelligent travel plan",
    use_container_width=True,
    type="primary",
)
st.markdown("</div>", unsafe_allow_html=True)


# =============================================================================
# AGENT PIPELINE
# =============================================================================
AGENT_META = {
    "flight_agent": ("✈️", "Flight Intelligence", "Searching and comparing flight options"),
    "hotel_agent": ("🏨", "Hotel Discovery", "Finding stays that fit the trip"),
    "itinerary_agent": ("🗓️", "Itinerary Builder", "Structuring the days and experiences"),
    "final_agent": ("✦", "Final Travel Planner", "Combining everything into one plan"),
}


def answer_trip_question(question: str) -> str:
    """Answer a follow-up using the active plan as the travel context."""
    plan = st.session_state.last_plan or {}

    def excerpt(value: str, limit: int) -> str:
        text = str(value or "")
        if len(text) <= limit:
            return text
        return text[:limit] + "\n[Additional details omitted for this follow-up]"

    context = f"""
Original trip request:
{excerpt(st.session_state.last_query, 1200)}

Flight research:
{excerpt(plan.get('flight_results', ''), 1800)}

Hotel research:
{excerpt(plan.get('hotel_results', ''), 1800)}

Itinerary:
{excerpt(plan.get('itinerary', ''), 4500)}

Final plan:
{excerpt(plan.get('final_response', ''), 6500)}
"""

    conversation = []
    for message in st.session_state.chat_messages[-6:]:
        message_type = HumanMessage if message["role"] == "user" else AIMessage
        conversation.append(
            message_type(content=excerpt(message["content"], 900))
        )

    try:
        response = llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are a helpful travel co-pilot. Answer the user's "
                        "follow-up using the active trip context below. Be concise, "
                        "practical, and honest when the plan does not contain "
                        "enough information. Do not invent bookings or prices.\n\n"
                        + context
                    )
                ),
                *conversation,
                HumanMessage(content=excerpt(question, 1200)),
            ],
            max_tokens=700,
        )
        return response.content
    except Exception as error:
        if getattr(error, "status_code", None) == 413 or "Request too large" in str(error):
            return (
                "This trip plan is too detailed for a single follow-up request. "
                "Try asking about one day, destination, booking, or budget item "
                "at a time."
            )
        return (
            "I couldn't answer that right now. Please try the question again in "
            "a moment."
        )


if generate:
    if not user_query.strip():
        st.warning("Tell me a little about your trip first — destination, duration, budget, or anything you care about.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        st.session_state.chat_messages = []

        collected = {
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0,
        }

        st.markdown(
            """
            <div class="pipeline-header">
                <div>
                    <div class="pipeline-title">AI agents at work</div>
                    <div class="pipeline-sub">Live orchestration · research → planning → synthesis</div>
                </div>
                <div class="live-pill"><span class="live-dot"></span> Running</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for chunk in app.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label, description = AGENT_META.get(
                    node_name,
                    ("🔧", node_name, "Processing your request"),
                )

                with st.status(
                    f"{icon}  {label}",
                    state="complete",
                    expanded=True,
                ):
                    st.caption(description)

                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")

                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")

                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")

                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")

                    collected["llm_calls"] = state_update.get(
                        "llm_calls",
                        collected["llm_calls"],
                    )

        st.session_state.last_plan = collected
        st.session_state.last_query = user_query

        # ---------------------------------------------------------------------
        # Metrics
        # ---------------------------------------------------------------------
        st.markdown(
            f"""
            <div class="result-head">
                <div>
                    <div class="result-title">Your trip is ready</div>
                    <div class="result-caption">Generated just now · powered by your multi-agent workflow</div>
                </div>
            </div>

            <div class="metric-row">
                <div class="metric-box">
                    <div class="metric-icon">◈</div>
                    <div class="metric-val">4</div>
                    <div class="metric-lbl">Agents completed</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon">✦</div>
                    <div class="metric-val">{collected['llm_calls']}</div>
                    <div class="metric-lbl">LLM calls</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon">✓</div>
                    <div class="metric-val">Ready</div>
                    <div class="metric-lbl">Plan status</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------------------------------------------------------------
        # Final plan
        # ---------------------------------------------------------------------
        if collected["final_response"]:
            st.markdown(
                """
                <div class="result-head">
                    <div>
                        <div class="result-title">✦ Final travel plan</div>
                        <div class="result-caption">Flights · stays · itinerary · recommendations</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Markdown is rendered normally so headings, lists and tables in the
            # LLM response remain useful and readable.
            st.markdown(
                f'<div class="final-card">{collected["final_response"]}</div>',
                unsafe_allow_html=True,
            )

        # ---------------------------------------------------------------------
        # Save
        # ---------------------------------------------------------------------
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan

**Query:** {user_query}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**User ID:** {thread_id}

---

## ✈️ Flight Information

{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information

{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary

{collected['itinerary'] or 'N/A'}

---

## ✦ Final Travel Plan

{collected['final_response'] or 'N/A'}

---

*LLM Calls: {collected['llm_calls']}*
"""

        with open(
            os.path.join(save_dir, filename),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(file_content)

        dl_col, info_col = st.columns([1, 3])

        with dl_col:
            st.download_button(
                "⬇️  Download plan",
                data=file_content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )

        with info_col:
            st.markdown(
                f"""
                <div class="save-bar">
                    ✓ Saved locally &nbsp;·&nbsp;
                    <code>travel_plans/{filename}</code>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =============================================================================
# FOLLOW-UP TRIP CHAT
# =============================================================================
if st.session_state.last_plan:
    if not generate and st.session_state.last_plan.get("final_response"):
        st.markdown(
            """
            <div class="result-head">
                <div>
                    <div class="result-title">✦ Your active travel plan</div>
                    <div class="result-caption">Ask follow-up questions about this plan below</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="final-card">{st.session_state.last_plan["final_response"]}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="chat-shell">
            <div class="chat-title">Ask about your trip</div>
            <div class="chat-caption">
                Your co-pilot can clarify the itinerary, suggest alternatives,
                or help you adjust the plan without starting over.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.chat_messages:
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    chat_question = st.chat_input(
        "Ask a follow-up about this trip...",
        key="trip_chat_input",
    )

    if chat_question:
        st.session_state.chat_messages.append(
            {"role": "user", "content": chat_question}
        )
        with st.chat_message("user"):
            st.markdown(chat_question)

        with st.chat_message("assistant"):
            with st.spinner("Reviewing your trip plan..."):
                answer = answer_trip_question(chat_question)
            st.markdown(answer)

        st.session_state.chat_messages.append(
            {"role": "assistant", "content": answer}
        )

    if st.session_state.chat_messages and st.button(
        "Clear conversation",
        key="clear_trip_chat",
    ):
        st.session_state.chat_messages = []
        st.rerun()