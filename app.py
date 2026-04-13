import streamlit as st
from utils.translations import t
from views import analyzer, chat, dashboard

if "lang" not in st.session_state:
    st.session_state.lang = "FR"
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "chat"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "theme_colors" not in st.session_state:
    st.session_state.theme_colors = {}

st.set_page_config(
    page_title="EmotionCare AI",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

if st.session_state.theme == "light":
    BG       = "#f5efe6"
    BG2      = "#ede4d8"
    BG3      = "#d9cfc4"
    BORDER   = "#c8b89a"
    TEXT     = "#2c2010"
    TEXT2    = "#7a6a55"
    ACCENT   = "#8a6a3a"
    CARD     = "#faf6f0"
    BTN_BG   = "#8a6a3a"
    BTN_TEXT = "#f5efe6"
else:
    BG       = "#1e1810"
    BG2      = "#2c2416"
    BG3      = "#3d3020"
    BORDER   = "#4a3c28"
    TEXT     = "#f5efe6"
    TEXT2    = "#8a7a65"
    ACCENT   = "#c9a96e"
    CARD     = "#252015"
    BTN_BG   = "#3d3020"
    BTN_TEXT = "#f5efe6"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"] {{
    background: {BG} !important;
    font-family: 'Inter', sans-serif;
    color: {TEXT};
}}

.main .block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

[data-testid="stSidebar"] {{
    background: {BG2} !important;
    border-right: 1px solid {BORDER} !important;
    min-width: 260px !important;
    max-width: 260px !important;
    transform: none !important;
    display: flex !important;
    visibility: visible !important;
}}

[data-testid="stSidebar"] > div {{
    padding: 0 !important;
    width: 100% !important;
}}

header[data-testid="stHeader"] {{
    display: none !important;
    height: 0 !important;
}}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}

/* ── Tous les boutons sidebar ── */
.stButton > button {{
    background: transparent !important;
    color: {TEXT} !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
    text-align: left !important;
    padding: 9px 14px !important;
    height: 38px !important;
    min-height: 38px !important;
    max-height: 38px !important;
    line-height: 38px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
}}

.stButton > button:hover {{
    background: {BG3} !important;
    color: {TEXT} !important;
    transform: none !important;
    opacity: 1 !important;
}}

.stButton > button p,
.stButton > button span,
.stButton > button div,
.stButton > button * {{
    color: {TEXT} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: ellipsis !important;
    text-align: left !important;
    line-height: 1 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: inline !important;
    visibility: visible !important;
    opacity: 1 !important;
}}python -m streamlit run app.py

/* Bouton nouvelle conversation — style spécial */
[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    justify-content: center !important;
    text-align: center !important;
}}

[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button p,
[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button span {{
    color: {TEXT} !important;
    text-align: center !important;
}}

[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover {{
    background: {ACCENT} !important;
    border-color: {ACCENT} !important;
    color: {BTN_TEXT} !important;
}}

[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover p,
[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type button:hover span {{
    color: {BTN_TEXT} !important;
}}

/* Boutons langue — petits et côte à côte */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 8px !important;
}}

/* Form buttons */
.stFormSubmitButton > button {{
    background: {BTN_BG} !important;
    color: {BTN_TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    height: 42px !important;
    white-space: nowrap !important;
}}

.stFormSubmitButton > button p,
.stFormSubmitButton > button span {{
    color: {BTN_TEXT} !important;
    white-space: nowrap !important;
}}

.stTextArea textarea {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    color: {TEXT} !important;
    font-size: 0.95rem !important;
}}

.stTextInput > div > div > input {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 14px 18px !important;
}}

.stTextInput > div > div > input::placeholder {{
    color: {TEXT2} !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 2px {ACCENT}22 !important;
}}

div[data-testid="stMarkdownContainer"] p,
label, p, span {{
    font-family: 'Inter', sans-serif !important;
    color: {TEXT} !important;
}}

h1, h2, h3, h4 {{
    color: {TEXT} !important;
    font-family: 'Inter', sans-serif !important;
}}

.stDownloadButton > button {{
    background: {CARD} !important;
    color: {ACCENT} !important;
    border: 1px solid {ACCENT} !important;
}}

.stDownloadButton > button p {{
    color: {ACCENT} !important;
}}

hr {{ border-color: {BORDER} !important; }}

[data-testid="stFileUploaderDropzone"] {{
    background: {CARD} !important;
    border: 1px dashed {BORDER} !important;
    border-radius: 10px !important;
}}

.stSelectbox > div > div {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}
</style>
""", unsafe_allow_html=True)

lang = st.session_state.lang

with st.sidebar:
    # Logo + thème
    col_logo, col_theme = st.columns([3, 1])
    with col_logo:
        st.markdown(f"""
            <div style='padding:24px 0 18px 20px;'>
                <div style='font-size:1.05rem; font-weight:700;
                    color:{ACCENT}; letter-spacing:0.5px;'>
                    ✦ EmotionCare AI
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_theme:
        st.markdown(
            "<div style='padding-top:18px;'>",
            unsafe_allow_html=True
        )
        icon = "☀️" if st.session_state.theme == "dark" else "🌙"
        if st.button(icon, key="theme_toggle"):
            st.session_state.theme = (
                "light" if st.session_state.theme == "dark" else "dark"
            )
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"<hr style='border-color:{BORDER}; margin:0 0 14px 0;'/>",
        unsafe_allow_html=True
    )

    # Nouvelle conversation
    st.markdown(
        "<div style='padding:0 12px 14px 12px;'>",
        unsafe_allow_html=True
    )
    if st.button("＋  " + t(lang, "new_conv"),
                 use_container_width=True, key="new_conv"):
        st.session_state.chat_messages = []
        st.session_state.current_mode = "chat"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Historique
    if st.session_state.chat_history:
        st.markdown(f"""
            <div style='padding:4px 20px 8px 20px;
                font-size:0.65rem; font-weight:600; color:{TEXT2};
                text-transform:uppercase; letter-spacing:2px;'>
                {t(lang, "hist_label")}
            </div>
        """, unsafe_allow_html=True)

        icons_map = {
            "joy":"😊","sadness":"😢","anger":"😠",
            "fear":"😨","stress":"😰"
        }
        colors_map = {
            "joy":ACCENT,"sadness":"#e07070",
            "anger":"#e07070","fear":"#a07aba","stress":"#e09060"
        }

        for conv in reversed(st.session_state.chat_history[-8:]):
            ei  = icons_map.get(conv.get("emotion",""), "✦")
            ec  = colors_map.get(conv.get("emotion",""), TEXT2)
            txt = conv.get("text","")[:28]
            st.markdown(f"""
                <div style='margin:0 10px 6px 10px;
                    padding:10px 14px; background:{BG3};
                    border-radius:10px;
                    border:1px solid {BORDER};
                    cursor:pointer;'>
                    <div style='font-size:0.83rem; color:{TEXT};
                        white-space:nowrap; overflow:hidden;
                        text-overflow:ellipsis; margin-bottom:4px;
                        font-weight:500;'>
                        {ei} {txt}...
                    </div>
                    <div style='display:flex;
                        justify-content:space-between;
                        align-items:center;'>
                        <span style='font-size:0.7rem; color:{ec};
                            font-weight:600;'>
                            {conv.get("emotion","").capitalize()}
                        </span>
                        <span style='font-size:0.68rem; color:{TEXT2};'>
                            {conv.get("time","")}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Navigation
    st.markdown(f"""
        <div style='padding:14px 20px 8px 20px;
            font-size:0.65rem; font-weight:600; color:{TEXT2};
            text-transform:uppercase; letter-spacing:2px;'>
            {t(lang, "nav_label")}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:0 8px;'>", unsafe_allow_html=True)
    for mode, key in [
        ("chat",      "chat_mode"),
        ("analyzer",  "analyzer_mode"),
        ("dashboard", "dashboard_mode"),
    ]:
        is_active = st.session_state.current_mode == mode
        active_style = f"background:{BG3} !important; font-weight:600 !important;" if is_active else ""
        if st.button(
            t(lang, key),
            use_container_width=True,
            key=f"nav_{mode}"
        ):
            st.session_state.current_mode = mode
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Langue
    st.markdown(
        f"<hr style='border-color:{BORDER}; margin:14px 0 12px 0;'/>",
        unsafe_allow_html=True
    )
    st.markdown(f"""
        <div style='padding:0 20px 8px 20px;
            font-size:0.65rem; font-weight:600; color:{TEXT2};
            text-transform:uppercase; letter-spacing:2px;'>
            {t(lang, "lang_label")}
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='padding:0 8px 20px 8px;'>",
        unsafe_allow_html=True
    )
    col_fr, col_en = st.columns(2)
    with col_fr:
        if st.button("🇫🇷  FR",
                     use_container_width=True, key="btn_fr"):
            st.session_state.lang = "FR"
            st.rerun()
    with col_en:
        if st.button("🇬🇧  EN",
                     use_container_width=True, key="btn_en"):
            st.session_state.lang = "EN"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.session_state.theme_colors = {
    "BG": BG, "BG2": BG2, "BG3": BG3,
    "BORDER": BORDER, "TEXT": TEXT,
    "TEXT2": TEXT2, "ACCENT": ACCENT, "CARD": CARD,
    "BTN_BG": BTN_BG, "BTN_TEXT": BTN_TEXT
}

if st.session_state.current_mode == "chat":
    chat.render()
elif st.session_state.current_mode == "analyzer":
    analyzer.render()
else:
    dashboard.render()