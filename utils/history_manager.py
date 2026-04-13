import os
import pandas as pd
from datetime import datetime

HISTORY_PATH = "data/history.csv"
COLUMNS = ["datetime", "text", "sentiment", "emotion", "wellbeing_score"]

def ensure_history_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(HISTORY_PATH) or os.path.getsize(HISTORY_PATH) == 0:
        pd.DataFrame(columns=COLUMNS).to_csv(HISTORY_PATH, index=False, encoding="utf-8")

def load_history():
    ensure_history_file()
    try:
        df = pd.read_csv(HISTORY_PATH)
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    except Exception:
        pd.DataFrame(columns=COLUMNS).to_csv(HISTORY_PATH, index=False, encoding="utf-8")
        return pd.DataFrame(columns=COLUMNS)

def save_analysis(text, sentiment, emotion, wellbeing_score):
    ensure_history_file()
    df = load_history()
    new_row = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
        "sentiment": sentiment,
        "emotion": emotion,
        "wellbeing_score": wellbeing_score
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(HISTORY_PATH, index=False, encoding="utf-8")

def clear_history():
    pd.DataFrame(columns=COLUMNS).to_csv(HISTORY_PATH, index=False, encoding="utf-8")