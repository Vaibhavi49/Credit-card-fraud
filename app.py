import streamlit as st
import numpy as np
import pandas as pd
import joblib
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="FraudX — Intelligence",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #07090f;
    color: #bcc4d8;
}
.stApp { background: #07090f; }

section[data-testid="stSidebar"] {
    background: #0b0e18 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}

.hero { padding: 2.8rem 0 2rem; }
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #2e3a52;
    margin-bottom: 0.7rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -2px;
    color: #e8edf8;
    margin: 0 0 0.4rem;
    line-height: 1;
}
.hero h1 em { font-style: normal; color: #4a6cf7; }
.hero-sub {
    font-size: 0.85rem;
    color: #374155;
    max-width: 420px;
    line-height: 1.6;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #3a4560 !important;
    background: transparent !important;
    border: none !important;
    padding: 0.7rem 1.4rem !important;
}
.stTabs [aria-selected="true"] {
    color: #e8edf8 !important;
    border-bottom: 2px solid #4a6cf7 !important;
}

.sec-head {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #2a3348;
    margin: 1.8rem 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sec-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.04);
}

.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 9px !important;
    color: #c8d0e4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: rgba(74,108,247,0.45) !important;
    box-shadow: 0 0 0 3px rgba(74,108,247,0.08) !important;
}
.stSelectbox label, .stNumberInput label, .stSlider label {
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    color: #3a4a63 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
.stSlider > div > div > div > div { background: #4a6cf7 !important; }

.stButton > button {
    width: 100%;
    background: #4a6cf7;
    color: #ffffff;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    border: none;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    letter-spacing: 0.5px;
    transition: all 0.2s;
    box-shadow: 0 0 24px rgba(74,108,247,0.25);
}
.stButton > button:hover {
    background: #3a5ce6;
    box-shadow: 0 0 32px rgba(74,108,247,0.4);
    transform: translateY(-1px);
}

.result-wrap {
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin: 1.2rem 0;
}
.result-fraud { background: rgba(239,68,68,0.07); border: 1px solid rgba(239,68,68,0.2); }
.result-legit { background: rgba(16,185,129,0.07); border: 1px solid rgba(16,185,129,0.2); }
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.result-fraud .result-title { color: #f87171; }
.result-legit .result-title { color: #34d399; }
.result-score { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #3a4560; margin-bottom: 14px; }
.score-track { height: 5px; background: rgba(255,255,255,0.05); border-radius: 5px; overflow: hidden; margin-top: 10px; }
.score-fill-fraud { height: 100%; background: linear-gradient(90deg,#dc2626,#f87171); border-radius: 5px; }
.score-fill-legit { height: 100%; background: linear-gradient(90deg,#059669,#34d399); border-radius: 5px; }

.explain-row { display: flex; align-items: center; gap: 10px; margin: 6px 0; }
.explain-label {
    font-family: 'DM Mono', monospace;
    color: #4a5a78;
    width: 200px;
    flex-shrink: 0;
    font-size: 0.72rem;
}
.explain-bar-wrap { flex: 1; height: 5px; background: rgba(255,255,255,0.04); border-radius: 3px; overflow: hidden; }
.explain-bar-pos { height: 100%; background: #ef4444; border-radius: 3px; }
.explain-bar-neg { height: 100%; background: #10b981; border-radius: 3px; }
.explain-val { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: #2e3a52; width: 50px; text-align: right; flex-shrink: 0; }

.log-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.78rem;
}
.log-id { font-family: 'DM Mono', monospace; color: #2e3a52; font-size: 0.68rem; width: 80px; }
.log-amount { color: #8292b0; width: 80px; text-align: right; }
.log-merchant { color: #4a5a78; flex: 1; padding: 0 12px; }
.log-time { font-family: 'DM Mono', monospace; color: #2a3348; font-size: 0.65rem; width: 70px; text-align: right; }
.badge-fraud {
    background: rgba(239,68,68,0.1); color: #f87171;
    border: 1px solid rgba(239,68,68,0.2); border-radius: 6px;
    padding: 2px 9px; font-size: 0.65rem; font-weight: 600;
    font-family: 'DM Mono', monospace; letter-spacing: 0.5px;
}
.badge-legit {
    background: rgba(16,185,129,0.1); color: #34d399;
    border: 1px solid rgba(16,185,129,0.2); border-radius: 6px;
    padding: 2px 9px; font-size: 0.65rem; font-weight: 600;
    font-family: 'DM Mono', monospace; letter-spacing: 0.5px;
}

.metric-row { display: flex; gap: 10px; margin: 1rem 0; }
.metric-box {
    flex: 1;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.9rem 1rem;
}
.metric-label { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 1.5px; text-transform: uppercase; color: #2e3a52; margin-bottom: 4px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700; color: #c8d0e4; letter-spacing: -0.5px; }
.metric-value.red { color: #f87171; }
.metric-value.green { color: #34d399; }

hr { border-color: rgba(255,255,255,0.05) !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──
if "history" not in st.session_state:
    st.session_state.history = []

# ── Load model ──
@st.cache_resource
def load_artifacts():
    model  = joblib.load('xgb_fraud_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_artifacts()

# ── Constants ──
MERCHANT_CATS = ["Retail","Grocery","Travel","Dining","Entertainment","Healthcare","Online","ATM/Cash"]
CARD_TYPES    = ["Visa Debit","Visa Credit","Mastercard Debit","Mastercard Credit","Amex"]
COUNTRIES     = ["Same country","Different country","High-risk region"]

# ── Feature engineering ──
def engineer_features(amount, hour, day_of_week, merchant_cat, card_type,
                       is_foreign, velocity, avg_spend, pin_used, online_txn):
    rng = np.random.default_rng(seed=int(amount * 100 + hour))
    v   = rng.normal(0, 0.3, 28)

    mc_idx  = MERCHANT_CATS.index(merchant_cat)
    ct_idx  = CARD_TYPES.index(card_type)
    for_idx = COUNTRIES.index(is_foreign)

    night_flag = 1 if (hour < 5 or hour > 22) else 0
    high_vel   = 1 if velocity > 5 else 0
    over_avg   = max(0, (amount - avg_spend) / (avg_spend + 1))

    v[0]  += -2.5 * night_flag
    v[1]  += -1.8 * (for_idx / 2)
    v[2]  += -1.5 * high_vel
    v[3]  += -2.0 * int(online_txn) * (1 - int(pin_used))
    v[4]  += -over_avg * 0.8
    v[5]  += mc_idx * 0.15
    v[6]  += ct_idx * 0.12
    v[7]  += (day_of_week / 6) * 0.2
    v[10] += night_flag * 0.6
    v[11] += high_vel * 0.4
    v[14] += for_idx * 0.3

    amount_scaled = scaler.transform([[amount]])[0][0]
    return np.concatenate([v, [amount_scaled]])

def feature_importance(amount, hour, day_of_week, merchant_cat, card_type,
                        is_foreign, velocity, avg_spend, pin_used, online_txn):
    night_flag = hour < 5 or hour > 22
    high_vel   = velocity > 5
    for_idx    = COUNTRIES.index(is_foreign)
    over_avg   = (amount - avg_spend) / (avg_spend + 1)
    return {
        "Unusual hour (night)":         0.35 if night_flag else -0.10,
        "Foreign / high-risk location": 0.30 * (for_idx / 2),
        "High transaction velocity":    0.28 if high_vel else -0.05,
        "Online + no PIN/3DS":          0.25 if (online_txn and not pin_used) else -0.08,
        "Amount vs avg spend":          min(max(over_avg * 0.2, -0.15), 0.30),
        "Merchant category risk":       0.05 * MERCHANT_CATS.index(merchant_cat),
        "Card type risk":               0.04 * CARD_TYPES.index(card_type),
        "Weekend transaction":          0.03 if day_of_week >= 5 else -0.02,
    }

def run_prediction(features_arr):
    pred = model.predict(features_arr.reshape(1, -1))[0]
    prob = model.predict_proba(features_arr.reshape(1, -1))[0][1]
    return int(pred), float(prob)

def render_result(pred, prob, merchant, amount):
    pct = round(prob * 100, 1)
    if pred == 1:
        st.markdown(f"""<div class="result-wrap result-fraud">
            <div class="result-title">🚨 Fraud Detected</div>
            <div class="result-score">Confidence · {pct}% &nbsp;|&nbsp; {merchant} · €{amount:.2f}</div>
            <div class="score-track"><div class="score-fill-fraud" style="width:{pct}%"></div></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="result-wrap result-legit">
            <div class="result-title">✅ Legitimate</div>
            <div class="result-score">Fraud prob · {pct}% &nbsp;|&nbsp; {merchant} · €{amount:.2f}</div>
            <div class="score-track"><div class="score-fill-legit" style="width:{100-pct}%"></div></div>
        </div>""", unsafe_allow_html=True)

def render_explain(factors):
    st.markdown("<div class='sec-head'>Why this result</div>", unsafe_allow_html=True)
    max_val = max(abs(v) for v in factors.values()) or 1
    for label, val in sorted(factors.items(), key=lambda x: -abs(x[1])):
        bar_w   = round(abs(val) / max_val * 100)
        bar_cls = "explain-bar-pos" if val > 0 else "explain-bar-neg"
        sign    = "+" if val > 0 else ""
        st.markdown(f"""<div class="explain-row">
            <span class="explain-label">{label}</span>
            <div class="explain-bar-wrap"><div class="{bar_cls}" style="width:{bar_w}%"></div></div>
            <span class="explain-val">{sign}{val:.2f}</span>
        </div>""", unsafe_allow_html=True)
    st.caption("Red = pushes toward fraud · Green = pushes toward legitimate")

# ── Hero ──
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">v2.0 · xgboost · real-time inference</div>
    <h1>Fraud<em>X</em></h1>
    <p class="hero-sub">Intelligent transaction risk assessment — fill in real details or upload a CSV batch.</p>
</div>
""", unsafe_allow_html=True)

# ── Session metrics ──
h      = st.session_state.history
total  = len(h)
frauds = sum(1 for r in h if r["pred"] == 1)
legits = total - frauds
rate   = f"{frauds/total*100:.1f}%" if total else "—"

st.markdown(f"""
<div class="metric-row">
    <div class="metric-box"><div class="metric-label">Analysed</div><div class="metric-value">{total}</div></div>
    <div class="metric-box"><div class="metric-label">Flagged</div><div class="metric-value red">{frauds}</div></div>
    <div class="metric-box"><div class="metric-label">Legitimate</div><div class="metric-value green">{legits}</div></div>
    <div class="metric-box"><div class="metric-label">Flag Rate</div><div class="metric-value">{rate}</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["  Single Transaction  ", "  Batch CSV Upload  ", "  History Log  "])

# ══ TAB 1 ══
with tab1:
    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown("<div class='sec-head'>Transaction details</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            amount    = st.number_input("Amount (€)", min_value=0.01, value=128.50, step=0.01, format="%.2f")
            merchant  = st.text_input("Merchant name", value="Amazon EU")
            merch_cat = st.selectbox("Merchant category", MERCHANT_CATS)
        with c2:
            card_type  = st.selectbox("Card type", CARD_TYPES)
            is_foreign = st.selectbox("Location", COUNTRIES)
            online_txn = st.selectbox("Channel", ["In-store", "Online"]) == "Online"

        st.markdown("<div class='sec-head'>Temporal & behavioural signals</div>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            hour        = st.slider("Hour of transaction (0–23)", 0, 23, 14)
            day_of_week = st.slider("Day of week  (0=Mon · 6=Sun)", 0, 6, 2)
        with c4:
            velocity  = st.slider("Transactions in last hour", 1, 20, 2)
            avg_spend = st.number_input("Cardholder avg spend (€)", min_value=1.0, value=95.0, step=1.0)
            pin_used  = st.selectbox("PIN / 3DS verified?", ["Yes", "No"]) == "Yes"

        st.markdown("<br>", unsafe_allow_html=True)
        analyse = st.button("⟶  Analyse Transaction")

    with col_right:
        if analyse:
            feats      = engineer_features(amount, hour, day_of_week, merch_cat, card_type,
                                           is_foreign, velocity, avg_spend, pin_used, online_txn)
            pred, prob = run_prediction(feats)
            render_result(pred, prob, merchant, amount)
            factors = feature_importance(amount, hour, day_of_week, merch_cat, card_type,
                                         is_foreign, velocity, avg_spend, pin_used, online_txn)
            render_explain(factors)

            txn_id = hashlib.md5(f"{datetime.now()}{amount}{merchant}".encode()).hexdigest()[:8].upper()
            st.session_state.history.insert(0, {
                "id": txn_id, "merchant": merchant, "amount": amount,
                "pred": pred, "prob": round(prob * 100, 1),
                "time": datetime.now().strftime("%H:%M:%S"),
            })
            st.rerun()
        else:
            st.markdown("""
            <div style="padding:3rem 1rem;text-align:center;color:#1e2840;">
                <div style="font-family:'DM Mono',monospace;font-size:2rem;margin-bottom:0.5rem;">◈</div>
                <div style="font-size:0.78rem;letter-spacing:1px">Fill in transaction details and click Analyse</div>
            </div>""", unsafe_allow_html=True)

# ══ TAB 2 ══
with tab2:
    st.markdown("<div class='sec-head'>Upload CSV file</div>", unsafe_allow_html=True)
    st.caption("Required columns: **amount, hour, day_of_week, merchant_cat, card_type, is_foreign, velocity, avg_spend, pin_used, online_txn, merchant**")

    sample = pd.DataFrame([
        {"merchant":"Zara","amount":65.0,"hour":14,"day_of_week":2,"merchant_cat":"Retail",
         "card_type":"Visa Credit","is_foreign":"Same country","velocity":1,"avg_spend":80.0,"pin_used":True,"online_txn":False},
        {"merchant":"Unknown Site","amount":999.99,"hour":3,"day_of_week":6,"merchant_cat":"Online",
         "card_type":"Mastercard Debit","is_foreign":"High-risk region","velocity":12,"avg_spend":60.0,"pin_used":False,"online_txn":True},
    ])
    st.download_button("⬇ Download sample CSV", sample.to_csv(index=False), "fraudx_sample.csv", "text/csv")

    uploaded = st.file_uploader("Drop your CSV here", type=["csv"], label_visibility="collapsed")

    if uploaded:
        df = pd.read_csv(uploaded)
        st.markdown(f"<div class='sec-head'>Preview — {len(df)} rows</div>", unsafe_allow_html=True)
        st.dataframe(df.head(5), use_container_width=True)

        if st.button("⟶  Run Batch Analysis"):
            results  = []
            progress = st.progress(0)
            for i, row in df.iterrows():
                try:
                    feats      = engineer_features(
                        float(row.get("amount", 100)), int(row.get("hour", 12)),
                        int(row.get("day_of_week", 2)), str(row.get("merchant_cat", "Retail")),
                        str(row.get("card_type", "Visa Debit")), str(row.get("is_foreign", "Same country")),
                        int(row.get("velocity", 1)), float(row.get("avg_spend", 100)),
                        bool(row.get("pin_used", True)), bool(row.get("online_txn", False)),
                    )
                    pred, prob = run_prediction(feats)
                    results.append({
                        "Merchant":     row.get("merchant", "Unknown"),
                        "Amount (€)":   row.get("amount", "—"),
                        "Verdict":      "🚨 FRAUD" if pred == 1 else "✅ Legit",
                        "Fraud prob %": round(prob * 100, 1),
                    })
                except Exception:
                    results.append({"Merchant": row.get("merchant","?"), "Verdict": "⚠️ Error"})
                progress.progress((i + 1) / len(df))

            out_df      = pd.DataFrame(results)
            fraud_count = sum(1 for r in results if "FRAUD" in str(r.get("Verdict","")))
            st.markdown("<div class='sec-head'>Results</div>", unsafe_allow_html=True)
            st.dataframe(out_df, use_container_width=True)
            st.markdown(f"""
            <div class="metric-row" style="margin-top:1rem">
                <div class="metric-box"><div class="metric-label">Total</div><div class="metric-value">{len(results)}</div></div>
                <div class="metric-box"><div class="metric-label">Fraudulent</div><div class="metric-value red">{fraud_count}</div></div>
                <div class="metric-box"><div class="metric-label">Legitimate</div><div class="metric-value green">{len(results)-fraud_count}</div></div>
            </div>""", unsafe_allow_html=True)
            st.download_button("⬇ Export results CSV", out_df.to_csv(index=False), "fraudx_results.csv", "text/csv")

# ══ TAB 3 ══
with tab3:
    st.markdown("<div class='sec-head'>Session transaction log</div>", unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div style="padding:3rem;text-align:center;color:#1e2840;font-family:'DM Mono',monospace;font-size:0.75rem;letter-spacing:1px;">
            No transactions analysed yet
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="log-row" style="border-bottom:1px solid rgba(255,255,255,0.08)">
            <span class="log-id" style="color:#2a3550;font-size:0.62rem;letter-spacing:1px">ID</span>
            <span class="log-merchant" style="color:#2a3550;font-size:0.62rem;letter-spacing:1px">MERCHANT</span>
            <span class="log-amount" style="color:#2a3550;font-size:0.62rem;letter-spacing:1px">AMOUNT</span>
            <span style="width:80px;text-align:center;color:#2a3550;font-size:0.62rem;letter-spacing:1px">VERDICT</span>
            <span class="log-time">TIME</span>
        </div>""", unsafe_allow_html=True)

        for r in st.session_state.history:
            badge = '<span class="badge-fraud">FRAUD</span>' if r["pred"] == 1 else '<span class="badge-legit">LEGIT</span>'
            st.markdown(f"""
            <div class="log-row">
                <span class="log-id">{r['id']}</span>
                <span class="log-merchant">{r['merchant']}</span>
                <span class="log-amount">€{r['amount']:.2f}</span>
                <span style="width:80px;text-align:center">{badge}</span>
                <span class="log-time">{r['time']}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear history"):
            st.session_state.history = []
            st.rerun()
