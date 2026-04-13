import streamlit as st

def apply_theme(mode="Light"):
    if mode == "Dark":
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            background: #0f0f13;
            color: #e8e3f0;
            font-family: 'Inter', sans-serif;
        }

        .main .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: #16161d;
            border-right: 1px solid #2a2a3a;
        }

        [data-testid="stSidebar"] * {
            color: #e8e3f0 !important;
        }

        div[data-testid="stMarkdownContainer"] p,
        label, p, span {
            color: #e8e3f0 !important;
            font-family: 'Inter', sans-serif !important;
        }

        h1, h2, h3, h4 {
            color: #f0ecfa !important;
            font-weight: 600 !important;
            letter-spacing: -0.3px;
        }

        .stTextArea textarea {
            background: #1e1e2e !important;
            color: #e8e3f0 !important;
            border: 1px solid #3a3a5c !important;
            border-radius: 14px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 15px !important;
            padding: 14px !important;
        }

        .stTextArea textarea:focus {
            border: 1px solid #7c6af7 !important;
            box-shadow: 0 0 0 3px rgba(124,106,247,0.15) !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #7c6af7, #a78bfa) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.4rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(124,106,247,0.35) !important;
        }

        .card {
            background: #1e1e2e;
            border: 1px solid #2e2e45;
            border-radius: 18px;
            padding: 22px 26px;
            margin-bottom: 18px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        }

        .metric-card {
            background: #1a1a2e;
            border: 1px solid #2e2e45;
            border-radius: 14px;
            padding: 16px;
            text-align: center;
        }

        [data-testid="stMetric"] {
            background: #1e1e2e;
            border: 1px solid #2e2e45;
            border-radius: 14px;
            padding: 16px 20px;
        }

        [data-testid="stMetricValue"] {
            color: #a78bfa !important;
            font-weight: 700 !important;
            font-size: 1.6rem !important;
        }

        [data-testid="stMetricLabel"] {
            color: #9990b0 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stDownloadButton > button {
            background: #1e1e2e !important;
            color: #a78bfa !important;
            border: 1px solid #a78bfa !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }

        .stChatMessage {
            background: #1e1e2e !important;
            border: 1px solid #2e2e45 !important;
            border-radius: 16px !important;
            margin-bottom: 10px !important;
        }

        div[data-testid="stRadio"] label {
            color: #e8e3f0 !important;
        }

        .stSelectbox > div > div {
            background: #1e1e2e !important;
            border: 1px solid #3a3a5c !important;
            border-radius: 10px !important;
            color: #e8e3f0 !important;
        }

        hr {
            border-color: #2a2a3a !important;
        }

        .stDataFrame {
            border-radius: 14px !important;
            overflow: hidden !important;
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            background: #f8f7ff;
            color: #1a1a2e;
            font-family: 'Inter', sans-serif;
        }

        .main .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #ede9fe;
        }

        [data-testid="stSidebar"] * {
            color: #1a1a2e !important;
        }

        div[data-testid="stMarkdownContainer"] p,
        label, p, span {
            color: #1a1a2e !important;
            font-family: 'Inter', sans-serif !important;
        }

        h1, h2, h3, h4 {
            color: #1a1a2e !important;
            font-weight: 600 !important;
            letter-spacing: -0.3px;
        }

        .stTextArea textarea {
            background: #ffffff !important;
            color: #1a1a2e !important;
            border: 1.5px solid #ddd6fe !important;
            border-radius: 14px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 15px !important;
            padding: 14px !important;
        }

        .stTextArea textarea:focus {
            border: 1.5px solid #7c6af7 !important;
            box-shadow: 0 0 0 3px rgba(124,106,247,0.12) !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #7c6af7, #a78bfa) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.4rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(124,106,247,0.3) !important;
        }

        .card {
            background: #ffffff;
            border: 1px solid #ede9fe;
            border-radius: 18px;
            padding: 22px 26px;
            margin-bottom: 18px;
            box-shadow: 0 2px 16px rgba(124,106,247,0.07);
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #ede9fe;
            border-radius: 14px;
            padding: 16px 20px;
            box-shadow: 0 2px 12px rgba(124,106,247,0.06);
        }

        [data-testid="stMetricValue"] {
            color: #7c6af7 !important;
            font-weight: 700 !important;
            font-size: 1.6rem !important;
        }

        [data-testid="stMetricLabel"] {
            color: #6b7280 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stDownloadButton > button {
            background: #ffffff !important;
            color: #7c6af7 !important;
            border: 1.5px solid #7c6af7 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }

        .stChatMessage {
            background: #ffffff !important;
            border: 1px solid #ede9fe !important;
            border-radius: 16px !important;
            margin-bottom: 10px !important;
        }

        .stSelectbox > div > div {
            background: #ffffff !important;
            border: 1.5px solid #ddd6fe !important;
            border-radius: 10px !important;
        }

        hr {
            border-color: #ede9fe !important;
        }

        .stDataFrame {
            border-radius: 14px !important;
            overflow: hidden !important;
        }
        </style>
        """, unsafe_allow_html=True)