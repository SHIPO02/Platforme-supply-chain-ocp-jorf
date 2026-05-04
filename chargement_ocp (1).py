import streamlit as st
import pandas as pd
import re, os, io, pickle, json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import base64

# ── AUTHENTIFICATION ──
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown("""
    <div style="max-width:400px;margin:80px auto;background:white;
    border:1px solid #E0E4EA;border-radius:12px;padding:40px;
    box-shadow:0 8px 32px rgba(0,0,0,0.10);text-align:center">
    <div style="font-family:'Barlow Condensed',sans-serif;font-size:28px;
    font-weight:800;color:#00843D;margin-bottom:6px">OCP Manufacturing</div>
    <div style="font-size:12px;color:#94A3B8;margin-bottom:28px">
    Accès réservé — Supply Chain Jorf Lasfar</div>
    </div>
    """, unsafe_allow_html=True)

    pwd = st.text_input("Mot de passe", type="password", key="pwd_input")
    if st.button("Accéder", type="primary"):
        # Stocker le mot de passe dans Streamlit Secrets (voir ci-dessous)
        if pwd == st.secrets["password"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect.")
    return False

if not check_password():
    st.stop()

# ... reste de votre code ...

st.set_page_config(page_title="OCP Manufacturing", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@500;600;700;800&display=swap');
:root {
  --green:#00843D;--green-dk:#005C2A;--green-lt:#E8F5EE;
  --blue:#1565C0;--blue-lt:#E3EAF8;
  --orange:#C05A00;--orange-lt:#FBF0E6;
  --purple:#6B3FA0;--purple-lt:#F0EBF8;
  --red:#C62828;
  --bg:#F2F4F7;--white:#FFFFFF;
  --border:#E0E4EA;--border2:#EEF0F4;
  --text:#12202E;--text2:#4A5568;--text3:#94A3B8;
  --sh1:0 1px 3px rgba(0,0,0,0.07);
  --sh2:0 4px 16px rgba(0,0,0,0.10);
  --sh3:0 8px 32px rgba(0,0,0,0.12);
}
html,body,[class*="css"]{font-family:'Barlow',sans-serif !important;color:var(--text);}
.stApp{background:var(--bg) !important;}
.main .block-container{padding:0 1.8rem 2rem 1.8rem !important;max-width:100% !important;}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent !important;height:0 !important;}
[data-testid="stDecoration"],.stDeployButton{display:none !important;}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
[data-testid="stSidebar"]{background:var(--white) !important;border-right:1px solid var(--border) !important;box-shadow:2px 0 10px rgba(0,0,0,0.06) !important;}
[data-testid="stSidebar"],[data-testid="stSidebar"]>div{width:220px !important;min-width:220px !important;max-width:220px !important;}
[data-testid="stSidebarContent"]{padding:0 !important;overflow-y:auto !important;}
[data-testid="stSidebarCollapseButton"],button[data-testid="baseButton-headerNoPadding"]{display:none !important;}
[data-testid="stSidebar"] section,[data-testid="stSidebar"] .block-container{padding:0 !important;}
.sbl{padding:16px 14px 14px 14px;border-bottom:1px solid var(--border2);display:flex;align-items:center;gap:10px;background:var(--white);}
.sbl-box{width:38px;height:38px;background:var(--green);border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:'Barlow Condensed',sans-serif;font-size:15px;font-weight:800;color:white;flex-shrink:0;letter-spacing:.3px;}
.sbl-img{width:38px;height:38px;object-fit:contain;flex-shrink:0;}
.sbl-name{font-family:'Barlow Condensed',sans-serif;font-size:18px;font-weight:800;color:var(--green);line-height:1.1;}
.sbl-sub{font-size:8px;color:var(--text3);letter-spacing:1.5px;text-transform:uppercase;margin-top:1px;}
.slbl{font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--text3);padding:14px 14px 4px 14px;}
.shr{height:1px;background:var(--border2);margin:6px 0;}
[data-testid="stSidebar"] .stButton button{width:100% !important;background:transparent !important;border:none !important;border-radius:0 !important;color:var(--text2) !important;font-family:'Barlow',sans-serif !important;font-size:13px !important;font-weight:500 !important;padding:9px 12px 9px 16px !important;text-align:left !important;border-left:3px solid transparent !important;white-space:nowrap !important;box-shadow:none !important;transition:background .15s,color .15s !important;}
[data-testid="stSidebar"] .stButton button:hover{background:var(--green-lt) !important;color:var(--green) !important;border-left-color:rgba(0,132,61,.4) !important;}
[data-testid="stSidebar"] .stButton button[kind="primary"]{background:var(--green-lt) !important;color:var(--green-dk) !important;border-left:3px solid var(--green) !important;font-weight:700 !important;}
.topbar{background:var(--white);border-bottom:1px solid var(--border);padding:12px 1.8rem;margin:0 -1.8rem 20px -1.8rem;display:flex;align-items:center;justify-content:space-between;box-shadow:var(--sh1);}
.tb-title{font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:700;color:var(--text);}
.tb-bread{font-size:11px;color:var(--text3);margin-top:1px;}
.tb-badge{background:var(--green-lt);color:var(--green-dk);border:1px solid rgba(0,132,61,.2);border-radius:20px;padding:4px 14px;font-size:11px;font-weight:600;}
.kcard{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:18px 20px;box-shadow:var(--sh1);transition:transform .18s,box-shadow .18s;position:relative;overflow:hidden;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;}
.kcard:hover{transform:translateY(-2px);box-shadow:var(--sh2);}
.kcard::after{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:10px 10px 0 0;}
.kcard.green::after{background:var(--green);}
.kcard.blue::after{background:var(--blue);}
.kcard.orange::after{background:var(--orange);}
.kcard.purple::after{background:var(--purple);}
.kc-lbl{font-size:9px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--text3);}
.kc-val{font-family:'Barlow Condensed',sans-serif;font-size:34px;font-weight:700;line-height:1;margin:4px 0;}
.kc-val.green{color:var(--green);}.kc-val.blue{color:var(--blue);}
.kc-val.orange{color:var(--orange);}.kc-val.purple{color:var(--purple);}
.kc-unit{font-size:13px;font-weight:500;color:var(--text3);margin-left:2px;}
.kc-sub{font-size:11px;color:var(--text2);}
.kc-detail{margin-top:8px;padding-top:8px;border-top:1px solid var(--border2);display:flex;flex-direction:column;gap:3px;}
.kc-detail-row{display:flex;justify-content:space-between;align-items:center;}
.kc-detail-label{font-size:10px;color:var(--text3);}
.kc-detail-value{font-size:10px;font-weight:700;color:var(--text2);}
.stitle{font-family:'Barlow Condensed',sans-serif;font-size:13px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--text2);margin:20px 0 10px 0;display:flex;align-items:center;gap:8px;}
.stitle::before{content:'';width:3px;height:14px;background:var(--green);border-radius:2px;display:inline-block;}
.stitle.blue::before{background:var(--blue);}
.stitle.orange::before{background:var(--orange);}
.stitle.purple::before{background:var(--purple);}
.card{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:20px;box-shadow:var(--sh1);}
.card-title{font-family:'Barlow Condensed',sans-serif;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text2);margin-bottom:14px;display:flex;align-items:center;gap:6px;}
.decade-wrap{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:18px 20px;box-shadow:var(--sh1);height:100%;box-sizing:border-box;}
.decade-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}
.decade-title{font-family:'Barlow Condensed',sans-serif;font-size:15px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text);}
.decade-badge{font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;padding:2px 8px;border-radius:10px;}
.decade-badge.current{background:var(--green-lt);color:var(--green-dk);}
.decade-badge.past{background:var(--border2);color:var(--text3);}
.decade-badge.future{background:var(--blue-lt);color:var(--blue);}
.decade-grid{display:flex;gap:8px;}
.decade-block{flex:1;background:var(--bg);border:1px solid var(--border2);border-radius:8px;padding:10px 12px;text-align:center;transition:border-color .15s;}
.decade-block:hover{border-color:var(--green);}
.decade-block.active{background:var(--green-lt);border-color:rgba(0,132,61,.3);}
.decade-block-label{font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text3);margin-bottom:4px;}
.decade-block.active .decade-block-label{color:var(--green-dk);}
.decade-block-val{font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:700;line-height:1;color:var(--text);}
.decade-block.active .decade-block-val{color:var(--green);}
.decade-block-unit{font-size:9px;color:var(--text3);margin-top:2px;}
.decade-total-row{margin-top:12px;padding-top:10px;border-top:1px solid var(--border2);display:flex;justify-content:space-between;align-items:center;}
.decade-total-label{font-size:10px;font-weight:700;color:var(--text2);}
.decade-total-val{font-family:'Barlow Condensed',sans-serif;font-size:16px;font-weight:700;color:var(--green);}
.hist-item{display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border-radius:7px;border:1px solid var(--border2);background:var(--bg);margin-bottom:6px;transition:border-color .15s;}
.hist-item:hover{border-color:var(--green);}
.hist-item-name{font-size:12px;font-weight:600;color:var(--text);}
.hist-item-date{font-size:10px;color:var(--text3);margin-top:2px;}
.hist-active{width:7px;height:7px;border-radius:50%;background:var(--green);flex-shrink:0;box-shadow:0 0 5px rgba(0,132,61,.5);}
.hist-inactive{width:7px;height:7px;border-radius:50%;background:var(--border);flex-shrink:0;}
.upload-zone{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:20px;box-shadow:var(--sh1);}
.upload-zone .zone-title{font-family:'Barlow Condensed',sans-serif;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text2);margin-bottom:4px;display:flex;align-items:center;gap:6px;}
.upload-zone .zone-desc{font-size:11px;color:var(--text3);margin-bottom:14px;}
[data-testid="stFileUploader"] label{font-size:11px !important;color:var(--text2) !important;font-weight:600 !important;}
[data-testid="stFileUploaderDropzone"]{background:var(--bg) !important;border:1.5px dashed var(--border) !important;border-radius:8px !important;}
[data-testid="stFileUploaderDropzone"] p{font-size:11px !important;color:var(--text3) !important;}
.filter-panel{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:18px 20px;box-shadow:var(--sh1);margin-bottom:16px;}
.filter-panel-title{font-family:'Barlow Condensed',sans-serif;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text2);margin-bottom:12px;display:flex;align-items:center;gap:6px;}
.filter-panel-title::before{content:'';width:3px;height:12px;background:var(--green);border-radius:2px;display:inline-block;}
.hero{background:linear-gradient(135deg,var(--green) 0%,var(--green-dk) 100%);border-radius:12px;padding:28px 32px;color:white;margin-bottom:20px;position:relative;overflow:hidden;box-shadow:var(--sh2);}
.hero::before{content:'';position:absolute;top:-30px;right:-30px;width:160px;height:160px;border-radius:50%;background:rgba(255,255,255,.08);}
.hero::after{content:'';position:absolute;bottom:-50px;right:80px;width:100px;height:100px;border-radius:50%;background:rgba(255,255,255,.05);}
.hero-title{font-family:'Barlow Condensed',sans-serif;font-size:30px;font-weight:800;line-height:1.1;margin-bottom:6px;}
.hero-sub{font-size:13px;opacity:.85;max-width:480px;line-height:1.5;}
.hero-date{font-size:11px;opacity:.7;margin-top:12px;letter-spacing:.5px;}
.hero-stat-val{font-family:'Barlow Condensed',sans-serif;font-size:38px;font-weight:800;line-height:1;}
.hero-stat-lbl{font-size:10px;opacity:.75;letter-spacing:1px;text-transform:uppercase;margin-top:2px;}
.mcard{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:18px 20px;box-shadow:var(--sh1);transition:transform .18s,box-shadow .18s;cursor:pointer;height:100%;}
.mcard:hover{transform:translateY(-3px);box-shadow:var(--sh2);border-color:var(--green);}
.mcard-title{font-family:'Barlow Condensed',sans-serif;font-size:17px;font-weight:700;color:var(--text);margin-bottom:4px;}
.mcard-desc{font-size:11px;color:var(--text3);line-height:1.5;}
.mcard-badge{display:inline-block;margin-top:10px;padding:3px 10px;border-radius:10px;font-size:9px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;}
.mcard-badge.active{background:var(--green-lt);color:var(--green-dk);}
.mcard-badge.soon{background:#F1F3F5;color:var(--text3);}
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:var(--white) !important;border-bottom:2px solid var(--border) !important;gap:0 !important;}
[data-testid="stTabs"] [data-baseweb="tab"]{background:transparent !important;color:var(--text2) !important;font-family:'Barlow',sans-serif !important;font-size:13px !important;font-weight:500 !important;padding:10px 20px !important;border-bottom:2px solid transparent !important;margin-bottom:-2px !important;}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"]{color:var(--green) !important;border-bottom-color:var(--green) !important;font-weight:700 !important;}
[data-testid="stTabs"] [data-baseweb="tab-panel"]{background:var(--white) !important;border:1px solid var(--border) !important;border-top:none !important;border-radius:0 0 8px 8px !important;padding:20px !important;}
[data-testid="stNumberInput"] input,[data-testid="stTextInput"] input{background:var(--white) !important;border-color:var(--border) !important;color:var(--text) !important;border-radius:6px !important;}
[data-testid="stNumberInput"] label,[data-testid="stTextInput"] label,[data-testid="stSelectbox"] label,[data-testid="stCheckbox"] label{color:var(--text2) !important;font-size:12px !important;font-weight:600 !important;}
.main .stButton button[kind="primary"]{background:var(--green) !important;color:white !important;border:none !important;border-radius:7px !important;font-weight:700 !important;box-shadow:0 2px 8px rgba(0,132,61,.25) !important;}
.main .stButton button[kind="primary"]:hover{background:var(--green-dk) !important;transform:translateY(-1px) !important;}
.main .stButton button[kind="secondary"]{background:var(--white) !important;color:var(--text) !important;border:1px solid var(--border) !important;border-radius:7px !important;}
[data-testid="stMetric"]{background:var(--white) !important;border:1px solid var(--border) !important;border-radius:8px !important;padding:14px 16px !important;box-shadow:var(--sh1) !important;}
[data-testid="stMetricLabel"]{color:var(--text2) !important;font-size:11px !important;font-weight:600 !important;}
[data-testid="stMetricValue"]{color:var(--text) !important;font-family:'Barlow Condensed',sans-serif !important;font-size:24px !important;}
[data-testid="stDataFrame"]{border:1px solid var(--border) !important;border-radius:8px !important;overflow:hidden !important;box-shadow:var(--sh1) !important;}
hr{border-color:var(--border2) !important;}
[data-baseweb="tag"]{background:var(--green-lt) !important;border-color:rgba(0,132,61,.25) !important;}
[data-baseweb="tag"] span{color:var(--green-dk) !important;}
.stAlert{border-radius:8px !important;}
[data-testid="stExpander"]{background:var(--white) !important;border:1px solid var(--border) !important;border-radius:8px !important;}
.ph-card{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:56px 40px;text-align:center;margin-top:20px;box-shadow:var(--sh1);}
.ph-card h2{font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:700;color:var(--text);margin-bottom:8px;}
.ph-card p{font-size:14px;color:var(--text2);max-width:400px;margin:0 auto;line-height:1.6;}
.ph-badge-b{display:inline-block;margin-top:20px;background:var(--blue-lt);color:var(--blue);border:1px solid rgba(21,101,192,.2);border-radius:20px;padding:5px 18px;font-size:10px;font-weight:700;letter-spacing:1px;}
.llm-badge{display:inline-flex;align-items:center;gap:5px;background:var(--purple-lt);color:var(--purple);border:1px solid rgba(107,63,160,.2);border-radius:12px;padding:3px 10px;font-size:10px;font-weight:600;letter-spacing:.3px;margin-bottom:10px;}
.tsp-hero{background:linear-gradient(135deg,#1565C0 0%,#0D47A1 100%);border-radius:12px;padding:22px 28px;color:white;margin-bottom:18px;position:relative;overflow:hidden;box-shadow:var(--sh2);}
.tsp-hero::before{content:'';position:absolute;top:-20px;right:-20px;width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.08);}
.tsp-hero-title{font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:800;letter-spacing:.5px;}
.tsp-hero-sub{font-size:12px;opacity:.8;margin-top:4px;}
.tsp-kcard{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:16px 18px;box-shadow:var(--sh1);border-top:3px solid var(--blue);text-align:center;}
.tsp-kcard-lbl{font-size:9px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--text3);margin-bottom:4px;}
.tsp-kcard-val{font-family:'Barlow Condensed',sans-serif;font-size:30px;font-weight:800;color:var(--blue);line-height:1;}
.tsp-kcard-unit{font-size:12px;color:var(--text3);margin-left:2px;}
img.flag-img{display:inline-block;vertical-align:middle;margin-right:8px;border-radius:3px;border:1px solid rgba(0,0,0,0.12);box-shadow:0 1px 4px rgba(0,0,0,0.18);object-fit:cover;}

/* ── DASHBOARD VENTES styles ── */
.dv-hero{background:linear-gradient(135deg,#12202E 0%,#1E3A5F 60%,#1565C0 100%);border-radius:14px;padding:26px 32px;color:white;margin-bottom:20px;position:relative;overflow:hidden;box-shadow:0 6px 32px rgba(21,101,192,.28);}
.dv-hero::before{content:'';position:absolute;top:-40px;right:-40px;width:220px;height:220px;border-radius:50%;background:rgba(255,255,255,.05);}
.dv-hero::after{content:'';position:absolute;bottom:-60px;right:140px;width:140px;height:140px;border-radius:50%;background:rgba(100,181,246,.07);}
.dv-hero-title{font-family:'Barlow Condensed',sans-serif;font-size:28px;font-weight:800;letter-spacing:.6px;position:relative;}
.dv-hero-sub{font-size:12px;opacity:.75;margin-top:5px;position:relative;}
.dv-stat-pill{display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:10px 18px;backdrop-filter:blur(8px);}
.dv-stat-val{font-family:'Barlow Condensed',sans-serif;font-size:28px;font-weight:800;line-height:1;}
.dv-stat-lbl{font-size:9px;opacity:.7;text-transform:uppercase;letter-spacing:1.2px;margin-top:2px;}
.dv-kpi{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:16px 18px;box-shadow:var(--sh1);position:relative;overflow:hidden;}
.dv-kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;}
.dv-kpi.c-green::before{background:var(--green);}
.dv-kpi.c-blue::before{background:var(--blue);}
.dv-kpi.c-orange::before{background:var(--orange);}
.dv-kpi.c-purple::before{background:var(--purple);}
.dv-kpi-lbl{font-size:9px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:var(--text3);margin-bottom:4px;}
.dv-kpi-val{font-family:'Barlow Condensed',sans-serif;font-size:28px;font-weight:800;line-height:1;}
.dv-kpi-val.c-green{color:var(--green);}
.dv-kpi-val.c-blue{color:var(--blue);}
.dv-kpi-val.c-orange{color:var(--orange);}
.dv-kpi-val.c-purple{color:var(--purple);}
.dv-kpi-sub{font-size:10px;color:var(--text3);margin-top:4px;}
.dv-section{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:20px;box-shadow:var(--sh1);margin-bottom:16px;}
.dv-section-title{font-family:'Barlow Condensed',sans-serif;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text);margin-bottom:16px;display:flex;align-items:center;gap:8px;}
.dv-section-title::before{content:'';width:4px;height:16px;border-radius:2px;display:inline-block;}
.dv-section-title.t-green::before{background:var(--green);}
.dv-section-title.t-blue::before{background:var(--blue);}
.dv-section-title.t-orange::before{background:var(--orange);}
.dv-section-title.t-purple::before{background:var(--purple);}
.dv-rank-item{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:8px;border:1px solid var(--border2);background:var(--bg);margin-bottom:6px;transition:border-color .15s,background .15s;}
.dv-rank-item:hover{border-color:var(--green);background:var(--green-lt);}
.dv-rank-num{font-family:'Barlow Condensed',sans-serif;font-size:18px;font-weight:800;color:var(--text3);min-width:24px;}
.dv-rank-name{font-size:12px;font-weight:600;color:var(--text);flex:1;}
.dv-rank-val{font-family:'Barlow Condensed',sans-serif;font-size:16px;font-weight:700;color:var(--green);}
.dv-rank-pct{font-size:9px;color:var(--text3);margin-left:4px;}
.dv-bar-track{height:4px;background:var(--border2);border-radius:2px;margin-top:3px;}
.dv-bar-fill{height:4px;border-radius:2px;}
.dv-filter-chip{display:inline-flex;align-items:center;gap:4px;background:var(--green-lt);color:var(--green-dk);border:1px solid rgba(0,132,61,.2);border-radius:20px;padding:3px 10px;font-size:10px;font-weight:600;margin:2px;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# PERSISTENCE & UTILS
# ══════════════════════════════════════════════════════
CACHE_DIR=os.path.join("/tmp",".ocp_cache")
JORF_CACHE=os.path.join(CACHE_DIR,"jorf.pkl")
SAFI_CACHE=os.path.join(CACHE_DIR,"safi.pkl")
VENTES_CACHE=os.path.join(CACHE_DIR,"ventes.pkl")
HIST_JORF=os.path.join(CACHE_DIR,"hist_jorf.json")
HIST_SAFI=os.path.join(CACHE_DIR,"hist_safi.json")
HIST_VENTES=os.path.join(CACHE_DIR,"hist_ventes.json")
HIST_FILES=os.path.join(CACHE_DIR,"hist_files")
os.makedirs(CACHE_DIR,exist_ok=True); os.makedirs(HIST_FILES,exist_ok=True)

def save_cache(p,d):
    with open(p,"wb") as f: pickle.dump(d,f)
def load_cache(p):
    if os.path.exists(p):
        try:
            with open(p,"rb") as f: return pickle.load(f)
        except: pass
    return None
def clear_cache(p):
    if os.path.exists(p): os.remove(p)
def load_hist(p):
    if os.path.exists(p):
        try:
            with open(p,"r",encoding="utf-8") as f: return json.load(f)
        except: pass
    return []
def save_hist(p,h):
    with open(p,"w",encoding="utf-8") as f: json.dump(h,f,ensure_ascii=False,indent=2)
def add_hist(p,filename,filebytes,ftype):
    h=load_hist(p); ts=datetime.now().strftime("%Y%m%d_%H%M%S")
    pp=os.path.join(HIST_FILES,f"{ftype}_{ts}_{filename.replace(' ','_')}")
    with open(pp,"wb") as f: f.write(filebytes)
    e={"filename":filename,"date_upload":datetime.now().strftime("%d/%m/%Y %H:%M"),"path":pp,"type":ftype}
    h=[x for x in h if not(x["filename"]==filename and x["date_upload"][:10]==e["date_upload"][:10])]
    h.insert(0,e); save_hist(p,h[:20]); return pp
def get_hist_bytes(e):
    p=e.get("path","")
    if os.path.exists(p):
        with open(p,"rb") as f: return f.read()
    return None

NOMS_MOIS={1:"Jan",2:"Fev",3:"Mar",4:"Avr",5:"Mai",6:"Jun",7:"Jul",8:"Aou",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
ORDRE_MOIS={v:k for k,v in NOMS_MOIS.items()}

def force_n(v):
    if pd.isna(v): return 0.
    if isinstance(v,(int,float)): return 0. if abs(v)<1e-6 else float(v)
    s=str(v).strip()
    if s in("-","","nan"): return 0.
    n=re.sub(r'[^\d]','',s.replace("\xa0","").replace(" ",""))
    if len(n)>12: return 0.
    try: return float(n)
    except: return 0.

def mil(v): return round(v/1000,1)
def fmt(n):
    s=f"{n:,.1f}"; s=s.replace(",","THOUSEP"); s=s.replace(".",","); s=s.replace("THOUSEP","\u00a0")
    return s
def dsort(d):
    try: p=str(d).split("/"); return (int(p[2]),int(p[1]),int(p[0]))
    except: return (9999,99,99)
def msort(m):
    try: p=m.split(); return (int(p[1]),ORDRE_MOIS.get(p[0],99))
    except: return (9999,99)
def filt(df,sel,col="Date"):
    if not sel: return df
    return df[df[col].isin(sel)]
SKIP=["total","recap","recapitulatif","annee","annuel","bilan","synthese","summary"]
def is_sheet(n): return not any(k in n.strip().lower() for k in SKIP)
def detect_eng(raw):
    for e in ['openpyxl','pyxlsb','calamine']:
        try: pd.ExcelFile(io.BytesIO(raw),engine=e); return e
        except: continue
    raise ValueError("Impossible de lire ce fichier.")
def read_bytes(file):
    file.seek(0); raw=file.read(); fn=getattr(file,'name','').lower().strip()
    if fn.endswith('.xlsb'): return raw,'pyxlsb'
    if fn.endswith(('.xlsm','.xlsx')):
        try: pd.ExcelFile(io.BytesIO(raw),engine='openpyxl'); return raw,'openpyxl'
        except: pass
    if fn.endswith('.xls'):
        try: pd.ExcelFile(io.BytesIO(raw),engine='calamine'); return raw,'calamine'
        except: pass
    return raw,detect_eng(raw)
def last_val(df,col,col_d="Date"):
    if df is None or df.empty: return 0.,None
    t=df[df[col]>0].copy()
    if t.empty: return 0.,None
    t["_s"]=t[col_d].apply(dsort); last=t.sort_values("_s").iloc[-1]
    return round(float(last[col]),1),last[col_d]
def get_decade(day):
    if day<=10: return "D1"
    elif day<=20: return "D2"
    else: return "D3"
def compute_decades(df,col_total,date_col="Date"):
    if df is None or df.empty: return []
    results={}
    for _,row in df.iterrows():
        d_str=str(row[date_col])
        try: parts=d_str.split("/"); day,month,year=int(parts[0]),int(parts[1]),int(parts[2])
        except: continue
        key=(year,month)
        if key not in results:
            results[key]={"annee":year,"mois":month,"mois_label":f"{NOMS_MOIS.get(month,'?')} {year}","D1":0.,"D2":0.,"D3":0.}
        dec=get_decade(day); val=float(row[col_total]) if pd.notna(row[col_total]) else 0.
        results[key][dec]+=val
    out=[]
    for key in sorted(results.keys()):
        r=results[key]; r["D1"]=round(r["D1"],1); r["D2"]=round(r["D2"],1); r["D3"]=round(r["D3"],1)
        r["total"]=round(r["D1"]+r["D2"]+r["D3"],1); out.append(r)
    return out
def decade_status(annee,mois,decade):
    now=datetime.now(); cur_day=now.day; cur_mois=now.month; cur_annee=now.year
    if annee<cur_annee or (annee==cur_annee and mois<cur_mois): return "past"
    if annee>cur_annee or (annee==cur_annee and mois>cur_mois): return "future"
    if decade=="D1":
        if cur_day>10: return "past"
        else: return "current"
    elif decade=="D2":
        if cur_day>20: return "past"
        elif cur_day<=10: return "future"
        else: return "current"
    else:
        if cur_day<=20: return "future"
        else: return "current"

PL=dict(
    paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(242,244,247,0.6)',
    font=dict(family='Barlow,sans-serif',color='#4A5568'),
    xaxis=dict(gridcolor='#E0E4EA',linecolor='#E0E4EA',tickfont=dict(color='#4A5568',size=11)),
    yaxis=dict(gridcolor='#E0E4EA',linecolor='#E0E4EA',tickfont=dict(color='#4A5568',size=11)),
    legend=dict(bgcolor='rgba(255,255,255,.9)',bordercolor='#E0E4EA',borderwidth=1,font=dict(color='#12202E',size=11)),
    margin=dict(l=12,r=12,t=36,b=12),height=340,
)

# Palette étendue pour les graphiques du dashboard ventes
DV_PALETTE = [
    "#1565C0","#00843D","#C05A00","#6B3FA0","#C62828",
    "#0097A7","#558B2F","#E65100","#4527A0","#AD1457",
    "#00695C","#F57F17","#283593","#4E342E","#37474F",
    "#1B5E20","#880E4F","#01579B","#FF6F00","#4A148C",
]

def country_flag(pays_name, size=22):
    import unicodedata as _u
    def _n(t):
        t=_u.normalize("NFD",str(t))
        return "".join(c for c in t if _u.category(c)!="Mn").lower().strip()
    PM={
        "brazil":"BR","bresil":"BR","argentina":"AR","argentine":"AR",
        "chile":"CL","chili":"CL","colombia":"CO","colombie":"CO",
        "peru":"PE","perou":"PE","ecuador":"EC","equateur":"EC",
        "bolivia":"BO","bolivie":"BO","paraguay":"PY","uruguay":"UY",
        "venezuela":"VE","cuba":"CU","mexico":"MX","mexique":"MX",
        "usa":"US","united states":"US","etats-unis":"US","etats unis":"US","amerique":"US",
        "canada":"CA","france":"FR","germany":"DE","allemagne":"DE",
        "spain":"ES","espagne":"ES","italy":"IT","italie":"IT",
        "united kingdom":"GB","royaume-uni":"GB","uk":"GB","angleterre":"GB",
        "netherlands":"NL","pays-bas":"NL","hollande":"NL",
        "belgium":"BE","belgique":"BE","portugal":"PT",
        "greece":"GR","grece":"GR","poland":"PL","pologne":"PL",
        "ukraine":"UA","romania":"RO","roumanie":"RO",
        "hungary":"HU","hongrie":"HU","czech republic":"CZ","tcheque":"CZ",
        "sweden":"SE","suede":"SE","norway":"NO","norvege":"NO",
        "denmark":"DK","danemark":"DK","finland":"FI","finlande":"FI",
        "austria":"AT","autriche":"AT","switzerland":"CH","suisse":"CH",
        "russia":"RU","russie":"RU","turkey":"TR","turquie":"TR",
        "serbia":"RS","serbie":"RS","croatia":"HR","croatie":"HR",
        "bulgaria":"BG","bulgarie":"BG","ireland":"IE","irlande":"IE",
        "morocco":"MA","maroc":"MA","algeria":"DZ","algerie":"DZ",
        "tunisia":"TN","tunisie":"TN","egypt":"EG","egypte":"EG",
        "libya":"LY","libye":"LY","nigeria":"NG",
        "south africa":"ZA","afrique du sud":"ZA","kenya":"KE",
        "ethiopia":"ET","ethiopie":"ET","ghana":"GH",
        "tanzania":"TZ","tanzanie":"TZ","senegal":"SN",
        "ivory coast":"CI","cote d'ivoire":"CI","cote divoire":"CI",
        "cameroon":"CM","cameroun":"CM","zambia":"ZM","zambie":"ZM",
        "zimbabwe":"ZW","mozambique":"MZ","angola":"AO","malawi":"MW",
        "uganda":"UG","ouganda":"UG","rwanda":"RW","mali":"ML",
        "burkina faso":"BF","niger":"NE","chad":"TD","tchad":"TD",
        "sudan":"SD","soudan":"SD","madagascar":"MG","guinea":"GN","guinee":"GN",
        "togo":"TG","benin":"BJ","congo":"CG","gabon":"GA",
        "mauritania":"MR","mauritanie":"MR","mauritius":"MU","ile maurice":"MU",
        "saudi arabia":"SA","arabie saoudite":"SA",
        "uae":"AE","united arab emirates":"AE","emirats arabes unis":"AE","emirats":"AE",
        "qatar":"QA","kuwait":"KW","koweit":"KW","iran":"IR","iraq":"IQ",
        "jordan":"JO","jordanie":"JO","lebanon":"LB","liban":"LB",
        "israel":"IL","oman":"OM","bahrain":"BH","bahrein":"BH",
        "yemen":"YE","syria":"SY","syrie":"SY",
        "india":"IN","inde":"IN","china":"CN","chine":"CN",
        "japan":"JP","japon":"JP","south korea":"KR","coree du sud":"KR",
        "pakistan":"PK","bangladesh":"BD","indonesia":"ID","indonesie":"ID",
        "vietnam":"VN","thailand":"TH","thailande":"TH",
        "malaysia":"MY","malaisie":"MY","philippines":"PH",
        "myanmar":"MM","sri lanka":"LK","nepal":"NP",
        "cambodia":"KH","cambodge":"KH","laos":"LA",
        "taiwan":"TW","hong kong":"HK","singapore":"SG","singapour":"SG",
        "australia":"AU","australie":"AU","new zealand":"NZ","nouvelle-zelande":"NZ",
        "new caledonia":"NC","nouvelle-caledonie":"NC",
    }
    key=_n(pays_name.strip())
    iso=PM.get(key)
    if not iso:
        for k,v in PM.items():
            if key in k or k in key: iso=v; break
    h=size; w=int(round(size*4/3))
    if iso and len(iso)==2:
        c=iso.lower()
        url=f"https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.2.3/flags/4x3/{c}.svg"
        return (f'<img src="{url}" width="{w}" height="{h}" class="flag-img" alt="{iso}" '
                f'style="width:{w}px;height:{h}px;border-radius:3px;border:1px solid rgba(0,0,0,0.13);'
                f'box-shadow:0 1px 4px rgba(0,0,0,0.18);vertical-align:middle;margin-right:8px;'
                f'object-fit:cover;display:inline-block;">')
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:{w}px;height:{h}px;background:#E0E4EA;border-radius:3px;'
            f'border:1px solid #CBD5E0;margin-right:8px;vertical-align:middle;'
            f'font-size:8px;color:#94A3B8;font-weight:700;letter-spacing:.5px;">?</span>')


# ══════════════════════════════════════════════════════
# PARSERS
# ══════════════════════════════════════════════════════
def parse_jorf(raw, eng):
    df = pd.read_excel(io.BytesIO(raw), sheet_name='EXPORT', header=None, engine=eng)
    co = {"E": None, "C": None, "V": None}
    for r in range(len(df)):
        # ← Convertir chaque cellule en str avant le join pour éviter float
        l = " ".join(str(v) for v in df.iloc[r, 0:3].values).upper()
        if "EXPORT ENGRAIS" in l: co["E"] = r
        if "EXPORT CAMIONS" in l: co["C"] = r
        if "VL CAMIONS" in l: co["V"] = r

    ld = df.iloc[2, :]
    cd = [j for j in range(3, len(ld)) if pd.notna(ld[j])]
    rows = []
    for j in cd:
        dt = ld[j]
        # ← Gestion robuste de la date (datetime, str, float, int)
        try:
            if hasattr(dt, 'strftime'):
                dl = dt.strftime('%d/%m/%Y')
            elif pd.isna(dt):
                continue  # sauter les colonnes sans date
            else:
                s = str(dt).strip().split(" ")[0]
                if not s or s in ("nan", "None", ""):
                    continue
                dl = s
        except Exception:
            continue

        v1 = mil(force_n(df.iloc[co["E"], j])) if co["E"] is not None else 0.
        v2 = mil(force_n(df.iloc[co["C"], j])) if co["C"] is not None else 0.
        v3 = mil(force_n(df.iloc[co["V"], j])) if co["V"] is not None else 0.
        rows.append({
            "Date": dl,
            "Export Engrais": v1,
            "Export Camions": v2,
            "VL Camions": v3,
            "TOTAL Jorf": round(v1 + v2 + v3, 1)
        })
    return pd.DataFrame(rows)
def parse_rade(raw,eng):
    df=pd.read_excel(io.BytesIO(raw),sheet_name='Sit Navire',header=None,engine=eng)
    rows=[]
    for r in range(len(df)):
        dv=df.iloc[r,1]; val=df.iloc[r,3]
        if pd.isna(dv) or pd.isna(val): continue
        sd=str(dv).strip()
        if sd in("","nan","Date"): continue
        dl=dv.strftime('%d/%m/%Y') if hasattr(dv,'strftime') else sd
        rows.append({"Date":dl,"Engrais en attente":mil(force_n(val))})
    return pd.DataFrame(rows) if rows else None

def parse_safi(raw,eng):
    xl=pd.ExcelFile(io.BytesIO(raw),engine=eng); CJ=1;CE=31;CM=32;SR=6
    def norm(s):
        acc={"é":"e","è":"e","ê":"e","à":"a","â":"a","ù":"u","û":"u","ô":"o","î":"i","ç":"c"}
        s=s.lower()
        for a,b in acc.items(): s=s.replace(a,b)
        return s
    def pm(sn):
        mm={"jan":1,"fev":2,"mar":3,"avr":4,"mai":5,"jun":6,"jui":6,"jul":7,"aou":8,"sep":9,"oct":10,"nov":11,"dec":12}
        ml={"janvier":1,"fevrier":2,"mars":3,"avril":4,"mai":5,"juin":6,"juillet":7,"aout":8,"septembre":9,"octobre":10,"novembre":11,"decembre":12}
        pts=sn.strip().split(); mn=None; an=None
        for p in pts:
            pn=norm(p)
            if pn[:3] in mm: mn=mm[pn[:3]]
            if pn in ml: mn=ml[pn]
            try:
                y=int(p)
                if 2000<=y<=2100: an=y
            except: pass
        return mn,an
    rows=[]
    for sheet in xl.sheet_names:
        if not is_sheet(sheet): continue
        mn,an=pm(sheet)
        if mn is None or an is None: continue
        dfs=pd.read_excel(io.BytesIO(raw),sheet_name=sheet,header=None,engine=eng)
        tec=CE; tml=CM
        if dfs.shape[1]<=CM:
            fe=False
            for hr in range(min(8,len(dfs))):
                rv=[str(v).strip().upper() for v in dfs.iloc[hr]]
                for ci,v in enumerate(rv):
                    if "TSP" in v and "EXPORT" in v: tec=ci; fe=True
                    if "TSP" in v and "ML" in v: tml=ci
            if not fe: continue
        for ri in range(SR,len(dfs)):
            jv=dfs.iloc[ri,CJ]
            if pd.isna(jv): continue
            s=str(jv).strip()
            if s in("","nan") or any(k in s.upper() for k in ["TOTAL","CUMUL","MOYENNE","MOY"]): continue
            try: jn=int(float(s))
            except: continue
            if jn<1 or jn>31: continue
            te=mil(force_n(dfs.iloc[ri,tec])) if tec<dfs.shape[1] else 0.
            tm=mil(force_n(dfs.iloc[ri,tml])) if tml<dfs.shape[1] else 0.
            rows.append({"Mois":sheet,"Jour":jn,"Date":f"{jn:02d}/{mn:02d}/{an}","TSP Export":te,"TSP ML":tm,"TOTAL Safi":round(te+tm,1)})
    return pd.DataFrame(rows) if rows else None

def load_jorf(raw,fname):
    ff=io.BytesIO(raw); ff.name=fname; r,e=read_bytes(ff)
    jd=parse_jorf(r,e); rd=None
    try: rd=parse_rade(r,e)
    except: pass
    st.session_state.update({"jorf_df":jd,"rade_df":rd,"jorf_name":fname})
    save_cache(JORF_CACHE,{"jorf_df":jd,"rade_df":rd,"filename":fname})
    return jd

def load_safi(raw,fname):
    ff=io.BytesIO(raw); ff.name=fname; r,e=read_bytes(ff)
    sd=parse_safi(r,e)
    st.session_state.update({"safi_df":sd,"safi_name":fname})
    save_cache(SAFI_CACHE,{"safi_df":sd,"filename":fname})
    return sd

def load_ventes_hist(raw,fname):
    ff=io.BytesIO(raw); ff.name=fname; r,e=read_bytes(ff)
    xl=pd.ExcelFile(io.BytesIO(r),engine=e); target=xl.sheet_names[0]
    for sn in xl.sheet_names:
        if any(k in sn.lower() for k in ["january","pipeline","ventes","janvier","data"]): target=sn; break
    df=pd.read_excel(io.BytesIO(r),sheet_name=target,engine=e)
    df.columns=[str(c).strip() for c in df.columns]; df=df.dropna(how="all")
    st.session_state.update({"ventes_df":df,"ventes_name":fname})
    save_cache(VENTES_CACHE,{"ventes_df":df,"ventes_map":st.session_state.get("ventes_map",{}),"filename":fname})
    st.session_state["llm_statut_input_key"]=""
    return df


# ══════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════
if "page" not in st.session_state: st.session_state["page"]="accueil"
for key,cache in [("jorf_loaded",JORF_CACHE),("safi_loaded",SAFI_CACHE)]:
    if key not in st.session_state:
        c=load_cache(cache)
        if c:
            if "jorf" in key:
                st.session_state["jorf_df"]=c.get("jorf_df"); st.session_state["rade_df"]=c.get("rade_df"); st.session_state["jorf_name"]=c.get("filename","")
            else:
                st.session_state["safi_df"]=c.get("safi_df"); st.session_state["safi_name"]=c.get("filename","")
        st.session_state[key]=True
if "ventes_loaded" not in st.session_state:
    c=load_cache(VENTES_CACHE)
    if c:
        st.session_state["ventes_df"]=c.get("ventes_df"); st.session_state["ventes_map"]=c.get("ventes_map",{}); st.session_state["ventes_name"]=c.get("filename","")
    st.session_state["ventes_loaded"]=True

EXCEL_T=["xlsx","xls","xlsm","xlsb"]

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    if os.path.exists("logo_ocp.png"):
        b64=base64.b64encode(open("logo_ocp.png","rb").read()).decode()
        logo_html=f'<img src="data:image/png;base64,{b64}" class="sbl-img"/>'
    else:
        logo_html='<div class="sbl-box">OCP</div>'
    st.markdown(f'<div class="sbl">{logo_html}<div><div class="sbl-name">OCP</div><div class="sbl-sub">Manufacturing</div></div></div>',unsafe_allow_html=True)
    st.markdown('<div class="slbl">Navigation</div>',unsafe_allow_html=True)
    NAV=[
        ("accueil","Accueil"),
        ("suivi","Suivi Chargement"),
        ("dashboard_chargement","Dashboard Chargement"),
        ("stock","Simulation Stock"),
        ("ventes","Pipeline des Ventes"),
        ("dashboard_ventes","Dashboard Ventes"),
        ("tsp_zoom","Zoom TSP"),
    ]
    for key,label in NAV:
        t="primary" if st.session_state["page"]==key else "secondary"
        if st.button(label,key=f"nav_{key}",type=t,use_container_width=True):
            st.session_state["page"]=key; st.rerun()
    st.markdown('<div class="shr"></div>',unsafe_allow_html=True)
    st.markdown('<div class="slbl">Données actives</div>',unsafe_allow_html=True)
    jn=st.session_state.get("jorf_name",""); sn=st.session_state.get("safi_name",""); vn=st.session_state.get("ventes_name","")
    dj="●" if jn else "○"; ds="●" if sn else "○"; dv="●" if vn else "○"
    st.markdown(f'<div style="padding:6px 14px 10px 14px;font-size:11px;color:#4A5568;line-height:2">{dj} <b>Jorf :</b> <span style="color:{"#00843D" if jn else "#94A3B8"}">{jn or "Non chargé"}</span><br/>{ds} <b>Safi :</b> <span style="color:{"#00843D" if sn else "#94A3B8"}">{sn or "Non chargé"}</span><br/>{dv} <b>Pipeline :</b> <span style="color:{"#00843D" if vn else "#94A3B8"}">{vn or "Non chargé"}</span></div>',unsafe_allow_html=True)

jorf_df=st.session_state.get("jorf_df"); rade_df=st.session_state.get("rade_df")
safi_df=st.session_state.get("safi_df"); page=st.session_state["page"]

TITLES={
    "accueil":("Tableau de Bord","Vue d'ensemble & historique"),
    "suivi":("Suivi Chargement","Jorf Lasfar & Safi — données par jour"),
    "dashboard_chargement":("Dashboard Chargement","Visualisation journalière — Safi TSP & Jorf"),
    "stock":("Simulation Stock","Projection matières premières"),
    "ventes":("Pipeline des Ventes","Performances commerciales"),
    "dashboard_ventes":("Dashboard Ventes","Volume par Produit • Statut • Pays • Site"),
    "tsp_zoom":("Zoom TSP","Pipeline TSP — filtres & analyse complète"),
}
t_title,t_sub=TITLES[page]
st.markdown(f'<div class="topbar"><div><div class="tb-title">{t_title}</div><div class="tb-bread">OCP Manufacturing &nbsp;›&nbsp; {t_title.split(" ",1)[1] if " " in t_title else t_title}</div></div><div class="tb-badge">{t_sub}</div></div>',unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SHARED VENTES HELPERS
# ══════════════════════════════════════════════════════════════════════════════
import unicodedata as _uc_glob
import re as _re_glob

def _ventes_clean_num(series): return pd.to_numeric(series,errors='coerce').fillna(0)
def _ventes_fmt_kt(val): return f"{val:,.1f}".replace(",","\u202f").replace(".",",")
def _ventes_fuzzy_col(df,*keywords):
    def norm(s):
        s=_uc_glob.normalize('NFD',str(s))
        return ''.join(c for c in s if _uc_glob.category(c)!='Mn').lower().strip()
    for col in df.columns:
        cn=norm(col)
        if all(norm(k) in cn for k in keywords): return col
    return None
def _ventes_auto_map(df):
    mapping={}
    for role,kws in [
        ("bl_month",    ["bl","month"]),
        ("phys_month",  ["physical","month"]),
        ("work_month",  ["working","month"]),
        ("del_month",   ["deliv","month"]),
        ("site",        ["site"]),
        ("status",      ["status","planif"]),
        ("confirmation",["confirm"]),
        ("pays",        ["pays"]),
        ("produit",     ["produit"]),
        ("macro_qualite",["macro"]),
        ("loading_port",["loading","port"]),
        ("region",      ["region"]),
        ("navire",      ["navire"]),
    ]:
        mapping[role]=_ventes_fuzzy_col(df,*kws)
    for role,kws in [("d1",["d1"]),("d2",["d2"]),("d3",["d3"])]:
        c=_ventes_fuzzy_col(df,*kws)
        if c and re.fullmatch(r'[dD]\s*[123]',c.strip()): mapping[role]=c
        elif c:
            exact=[col for col in df.columns if re.fullmatch(r'[dD]\s*'+kws[0][-1],col.strip())]
            mapping[role]=exact[0] if exact else c
    return mapping
def _deaccent(t):
    t=_uc_glob.normalize("NFD",str(t))
    return "".join(c for c in t if _uc_glob.category(c)!="Mn").lower().strip()
def _strip_num(s): return _re_glob.sub(r"^\s*\d+\s*[.\-\):]\s*","",str(s).strip()).strip()
def _norm_key(s): return _deaccent(_strip_num(s))
def _sort_key_statut_global(x): return (_deaccent(x),x)

_LLM_PROMPT_VERSION="v5"
if "llm_statut_map" not in st.session_state: st.session_state["llm_statut_map"]={}
if "llm_statut_input_key" not in st.session_state: st.session_state["llm_statut_input_key"]=""
if st.session_state.get("llm_prompt_version")!=_LLM_PROMPT_VERSION:
    st.session_state["llm_statut_map"]={}; st.session_state["llm_statut_input_key"]=""; st.session_state["llm_prompt_version"]=_LLM_PROMPT_VERSION

if "llm_tsp_statut_map" not in st.session_state: st.session_state["llm_tsp_statut_map"]={}
if "llm_tsp_statut_input_key" not in st.session_state: st.session_state["llm_tsp_statut_input_key"]=""

def _call_llm_clustering(statuts_purs):
    import json as _json
    statuts_str="\n".join(f"- {s}" for s in statuts_purs)
    prompt=f"""Tu es un expert en normalisation de données logistiques pour OCP (Maroc).
LISTE DES STATUTS : {statuts_str}
MISSION : Regrouper les statuts identiques ou sémantiquement équivalents.
RÈGLES : Ignore casse, accents, espaces. Regroupe abréviations.
GROUPES : Chargé/Chargée->Chargé | En cours de chargement | En rade | Nommé | Laycan en discussion | En planif | Recherche navire CFR | Recherche navire FOB | Containers
FORMAT : JSON brut uniquement. Clés=statuts de la liste. Valeurs=label canonique."""
    try:
        import urllib.request as _ur
        payload=_json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":2000,"system":"Réponds UNIQUEMENT avec du JSON valide brut.","messages":[{"role":"user","content":prompt}]}).encode("utf-8")
        req=_ur.Request("https://api.anthropic.com/v1/messages",data=payload,headers={"Content-Type":"application/json"},method="POST")
        with _ur.urlopen(req,timeout=25) as resp:
            data=_json.loads(resp.read().decode("utf-8"))
        raw_text="".join(b.get("text","") for b in data.get("content",[]))
        match=_re_glob.search(r"\{.*\}",raw_text,_re_glob.DOTALL)
        if match:
            mapping=_json.loads(match.group(0)); result={}
            for k,v in mapping.items():
                if k in set(statuts_purs): result[_norm_key(k)]=str(v).strip()
            for s in statuts_purs:
                nk=_norm_key(s)
                if nk not in result: result[nk]=s
            return result
    except Exception: pass
    return {_norm_key(s):s for s in statuts_purs}

def build_num_map(df_col, map_key="llm_statut_map", input_key="llm_statut_input_key"):
    purs=[]; seen=set()
    for v in df_col.dropna().unique():
        p=_strip_num(str(v).strip())
        if p and p not in seen: purs.append(p); seen.add(p)
    cache_key="|".join(sorted(_norm_key(p) for p in purs))
    if cache_key==st.session_state[input_key]: return
    with st.spinner("Analyse IA des statuts en cours..."):
        mapping=_call_llm_clustering(purs)
    st.session_state[map_key]=mapping; st.session_state[input_key]=cache_key

def normalize_statut(s, map_key="llm_statut_map"):
    raw=str(s).strip(); nk=_norm_key(raw)
    llm_map=st.session_state.get(map_key,{})
    return llm_map.get(nk,_strip_num(raw) or raw)

def _build_card_interactive(decade_label, val, col_dec, border_color, val_color, df_f, vmap):
    c_macro=vmap.get("macro_qualite"); c_pays_card=vmap.get("pays"); c_prod=vmap.get("produit"); c_navire=vmap.get("navire")
    st.markdown(f'<div style="background:white;border:1px solid #E0E4EA;border-radius:10px;padding:18px 20px;box-shadow:0 1px 3px rgba(0,0,0,0.07);border-top:3px solid {border_color}">',unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#94A3B8;margin-bottom:4px">{decade_label}</div><div style="font-family:Barlow Condensed,sans-serif;font-size:34px;font-weight:700;line-height:1;color:{val_color};margin-bottom:10px">{_ventes_fmt_kt(val)}<span style="font-size:13px;font-weight:500;color:#94A3B8;margin-left:3px">KT</span></div>',unsafe_allow_html=True)
    has_data=col_dec and col_dec in df_f.columns and not df_f.empty
    if has_data and c_macro and c_macro in df_f.columns:
        macro_grp=(df_f.groupby(df_f[c_macro].astype(str).str.strip())[col_dec].apply(lambda s: pd.to_numeric(s,errors='coerce').fillna(0).sum()).sort_values(ascending=False))
        total_dec=macro_grp.sum(); macro_items=[(m,v) for m,v in macro_grp.items() if v>0]
        if macro_items:
            st.markdown('<div style="border-top:1px solid #EEF0F4;padding-top:8px"><div style="font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#94A3B8;margin-bottom:6px">MACRO QUALITE</div>',unsafe_allow_html=True)
            for macro,mval in macro_items:
                pct=round(mval/total_dec*100) if total_dec>0 else 0; bar_w=max(3,pct)
                with st.expander(f"{macro}  |  {_ventes_fmt_kt(mval)} KT  ({pct}%)"):
                    st.markdown(f'<div style="height:4px;background:#E0E4EA;border-radius:2px;margin-bottom:10px"><div style="width:{bar_w}%;height:4px;background:{border_color};border-radius:2px"></div></div>',unsafe_allow_html=True)
                    df_macro=df_f[df_f[c_macro].astype(str).str.strip()==macro]
                    if c_prod and c_prod in df_f.columns:
                        if c_pays_card and c_pays_card in df_macro.columns:
                            pays_grp=(df_macro.groupby(df_macro[c_pays_card].astype(str).str.strip())[col_dec].apply(lambda s: pd.to_numeric(s,errors='coerce').fillna(0).sum()).sort_values(ascending=False))
                            for pays_name,pays_val in [(p,v) for p,v in pays_grp.items() if v>0]:
                                pays_pct=round(pays_val/mval*100) if mval>0 else 0
                                pays_bar=max(3,pays_pct)
                                flag_html=country_flag(pays_name,20)
                                c_region_card=vmap.get("region")
                                region_badge_card=""
                                if c_region_card and c_region_card in df_macro.columns:
                                    _regs=df_macro[df_macro[c_pays_card].astype(str).str.strip()==pays_name][c_region_card].dropna().astype(str).str.strip().unique().tolist()
                                    if _regs:
                                        region_badge_card=f'<span style="background:#F0EBF8;color:#6B3FA0;border-radius:4px;padding:1px 6px;font-size:8px;font-weight:700;margin-left:6px">{_regs[0]}</span>'
                                st.markdown(
                                    f'<div style="margin:8px 0 2px 0;padding:7px 10px;background:#F8FAFC;border:1px solid #E0E4EA;border-left:3px solid {border_color};border-radius:6px">'
                                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                                    f'<span style="font-size:13px;font-weight:700;color:#12202E;display:flex;align-items:center">{flag_html}{pays_name}{region_badge_card}</span>'
                                    f'<span style="font-size:11px;font-weight:700;color:{val_color}">{_ventes_fmt_kt(pays_val)} KT <span style="font-size:9px;color:#94A3B8;font-weight:400">({pays_pct}%)</span></span>'
                                    f'</div>'
                                    f'<div style="height:3px;background:#E0E4EA;border-radius:2px;margin-top:5px">'
                                    f'<div style="width:{pays_bar}%;height:3px;background:{border_color};border-radius:2px;opacity:.6"></div>'
                                    f'</div></div>',
                                    unsafe_allow_html=True
                                )
                                df_pays_macro=df_macro[df_macro[c_pays_card].astype(str).str.strip()==pays_name]
                                prod_grp=(df_pays_macro.groupby(df_pays_macro[c_prod].astype(str).str.strip())[col_dec].apply(lambda s: pd.to_numeric(s,errors='coerce').fillna(0).sum()).sort_values(ascending=False))
                                for pname,pval in [(p,v) for p,v in prod_grp.items() if v>0]:
                                    ppct=round(pval/pays_val*100) if pays_val>0 else 0
                                    # Récupérer les navires pour ce produit+pays
                                    navire_badge=""
                                    if c_navire and c_navire in df_pays_macro.columns:
                                        navires=df_pays_macro[df_pays_macro[c_prod].astype(str).str.strip()==pname][c_navire].dropna().astype(str).str.strip().unique().tolist()
                                        navires=[n for n in navires if n and n.lower() not in ("nan","none","")]
                                        if navires:
                                            navire_badge="".join(
                                                f'<span style="background:#E3EAF8;color:#1565C0;border-radius:4px;padding:1px 6px;font-size:8px;font-weight:700;margin-left:4px;white-space:nowrap">🚢 {n}</span>'
                                                for n in navires[:3]
                                            )
                                    st.markdown(
                                        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:4px 8px 4px 20px;border-bottom:1px solid #F2F4F7">'
                                        f'<span style="font-size:11px;color:#4A5568;display:flex;align-items:center;flex-wrap:wrap;gap:3px">↳ {pname}{navire_badge}</span>'
                                        f'<div style="text-align:right">'
                                        f'<span style="font-size:12px;font-weight:700;color:{val_color}">{_ventes_fmt_kt(pval)} KT</span>'
                                        f'<span style="display:block;font-size:9px;color:#94A3B8">{ppct}%</span>'
                                        f'</div></div>',
                                        unsafe_allow_html=True
                                    )
                        else:
                            prod_grp=(df_macro.groupby(df_macro[c_prod].astype(str).str.strip())[col_dec].apply(lambda s: pd.to_numeric(s,errors='coerce').fillna(0).sum()).sort_values(ascending=False))
                            for pname,pval in [(p,v) for p,v in prod_grp.items() if v>0]:
                                ppct=round(pval/mval*100) if mval>0 else 0
                                st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid #F2F4F7"><span style="font-size:11px;color:#4A5568">{pname}</span><div style="text-align:right"><span style="font-size:12px;font-weight:700;color:{val_color}">{_ventes_fmt_kt(pval)} KT</span><span style="display:block;font-size:9px;color:#94A3B8">{ppct}%</span></div></div>',unsafe_allow_html=True)
                    else:
                        st.caption("Mappez la colonne Produit pour voir le détail.")
            st.markdown('</div>',unsafe_allow_html=True)
    elif has_data and c_prod and c_prod in df_f.columns:
        prod_grp=(df_f.groupby(df_f[c_prod].astype(str).str.strip())[col_dec].apply(lambda s: pd.to_numeric(s,errors='coerce').fillna(0).sum()).sort_values(ascending=False))
        total_dec=prod_grp.sum(); items=[(p,v) for p,v in prod_grp.items() if v>0]
        if items:
            st.markdown('<div style="border-top:1px solid #EEF0F4;padding-top:8px"><div style="font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#94A3B8;margin-bottom:6px">PRODUITS</div>',unsafe_allow_html=True)
            for prod,pval in items:
                pct=round(pval/total_dec*100) if total_dec>0 else 0; bar_w=max(3,pct)
                with st.expander(f"{prod}  |  {_ventes_fmt_kt(pval)} KT  ({pct}%)"):
                    st.markdown(f'<div style="height:4px;background:#E0E4EA;border-radius:2px"><div style="width:{bar_w}%;height:4px;background:{border_color};border-radius:2px"></div></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)
def _normalize_site(s):
    """Normalise les noms de sites : SAFI* -> SAFI, JORF* -> JORF"""
    v = str(s).strip().upper()
    if v.startswith("SAFI"): return "SAFI"
    if v.startswith("JORF"): return "JORF"
    return str(s).strip()  # garde la casse originale pour les autres


# ══════════════════════════════════════════════════════════════════════════════
# PAGE ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
if page=="accueil":
    jorf_kpi=jorf_df; safi_kpi=safi_df
    cj=round(float(jorf_kpi["TOTAL Jorf"].sum()),1) if jorf_kpi is not None else 0.
    cs=round(float(safi_kpi["TOTAL Safi"].sum()),1) if safi_kpi is not None else 0.
    ct=round(cj+cs,1); today=datetime.now().strftime("%A %d %B %Y")
    cj_eng=round(float(jorf_kpi["Export Engrais"].sum()),1) if jorf_kpi is not None else 0.
    cj_cam=round(float(jorf_kpi["Export Camions"].sum()),1) if jorf_kpi is not None else 0.
    cj_vl=round(float(jorf_kpi["VL Camions"].sum()),1) if jorf_kpi is not None else 0.
    cs_exp=round(float(safi_kpi["TSP Export"].sum()),1) if safi_kpi is not None else 0.
    cs_ml=round(float(safi_kpi["TSP ML"].sum()),1) if safi_kpi is not None else 0.
    st.markdown(f'<div style="display:flex;gap:16px;margin-bottom:20px;align-items:stretch"><div class="hero" style="flex:2;margin-bottom:0"><div class="hero-title">OCP Manufacturing Dashboard</div><div class="hero-sub">Suivi consolidé des chargements, simulation de stock et pilotage des opérations — Jorf Lasfar & Safi.</div><div class="hero-date">{today}</div></div><div class="hero" style="flex:1;margin-bottom:0;display:flex;flex-direction:column;justify-content:center;text-align:center"><div class="hero-stat-val">{fmt(ct)}</div><div class="hero-stat-lbl">KT — Production Totale Cumulée — Jorf + Safi</div><div style="margin-top:14px;opacity:.75;font-size:11px">Jorf Lasfar : {fmt(cj)} KT &nbsp;|&nbsp; Safi : {fmt(cs)} KT</div></div></div>',unsafe_allow_html=True)
    st.markdown('<div class="stitle">Synthèse cumulée — toutes données</div>',unsafe_allow_html=True)
    k1,k2,k3=st.columns(3)
    with k1:
        if jorf_kpi is not None:
            st.markdown(f'<div class="kcard green"><div><div class="kc-lbl">Total Jorf Lasfar</div><div class="kc-val green">{fmt(cj)}<span class="kc-unit">KT</span></div></div><div class="kc-detail"><div class="kc-detail-row"><span class="kc-detail-label">Export Engrais</span><span class="kc-detail-value">{fmt(cj_eng)} KT</span></div><div class="kc-detail-row"><span class="kc-detail-label">Export Camions</span><span class="kc-detail-value">{fmt(cj_cam)} KT</span></div><div class="kc-detail-row"><span class="kc-detail-label">VL Camions</span><span class="kc-detail-value">{fmt(cj_vl)} KT</span></div></div></div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="kcard green"><div class="kc-lbl">Total Jorf Lasfar</div><div class="kc-val green">—</div><div class="kc-sub" style="color:#94A3B8">Fichier non chargé</div></div>',unsafe_allow_html=True)
    with k2:
        if safi_kpi is not None:
            st.markdown(f'<div class="kcard blue"><div><div class="kc-lbl">Total Safi</div><div class="kc-val blue">{fmt(cs)}<span class="kc-unit">KT</span></div></div><div class="kc-detail"><div class="kc-detail-row"><span class="kc-detail-label">TSP Export</span><span class="kc-detail-value">{fmt(cs_exp)} KT</span></div><div class="kc-detail-row"><span class="kc-detail-label">TSP ML</span><span class="kc-detail-value">{fmt(cs_ml)} KT</span></div></div></div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="kcard blue"><div class="kc-lbl">Total Safi</div><div class="kc-val blue">—</div><div class="kc-sub" style="color:#94A3B8">Fichier non chargé</div></div>',unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kcard orange"><div><div class="kc-lbl">Jorf + Safi — Consolidé</div><div class="kc-val orange">{fmt(ct)}<span class="kc-unit">KT</span></div></div><div class="kc-detail"><div class="kc-detail-row"><span class="kc-detail-label">Jorf Lasfar</span><span class="kc-detail-value">{fmt(cj)} KT</span></div><div class="kc-detail-row"><span class="kc-detail-label">Safi</span><span class="kc-detail-value">{fmt(cs)} KT</span></div></div></div>',unsafe_allow_html=True)

    st.markdown('<div class="stitle orange">Chargements par décade — D1 • D2 • D3</div>',unsafe_allow_html=True)
    dec_jorf=compute_decades(jorf_df,"TOTAL Jorf") if jorf_df is not None else []
    dec_safi=compute_decades(safi_df,"TOTAL Safi") if safi_df is not None else []
    def render_decades(dec_list):
        if not dec_list:
            st.markdown('<div style="background:#F2F4F7;border:1px dashed #E0E4EA;border-radius:10px;padding:20px;text-align:center;color:#94A3B8;font-size:12px;margin-bottom:12px">Aucune donnée — chargez un fichier pour voir les décades</div>',unsafe_allow_html=True); return
        for i in range(0,len(dec_list),3):
            cols=st.columns(min(3,len(dec_list)-i))
            for ci,r in enumerate(dec_list[i:i+3]):
                with cols[ci]:
                    d1s=decade_status(r["annee"],r["mois"],"D1"); d2s=decade_status(r["annee"],r["mois"],"D2"); d3s=decade_status(r["annee"],r["mois"],"D3")
                    b1="current" if d1s=="current" else ("past" if d1s=="past" else "future")
                    b2="current" if d2s=="current" else ("past" if d2s=="past" else "future")
                    b3="current" if d3s=="current" else ("past" if d3s=="past" else "future")
                    a1="active" if d1s=="current" else ""; a2="active" if d2s=="current" else ""; a3="active" if d3s=="current" else ""
                    lbl={"past":"Passé","current":"En cours","future":"À venir"}
                    st.markdown(f'<div class="decade-wrap"><div class="decade-header"><div class="decade-title">{r["mois_label"]}</div></div><div class="decade-grid"><div class="decade-block {a1}"><div class="decade-block-label">D1 <span class="decade-badge {b1}">{lbl[d1s]}</span></div><div class="decade-block-val">{fmt(r["D1"])}</div><div class="decade-block-unit">KT • J1–10</div></div><div class="decade-block {a2}"><div class="decade-block-label">D2 <span class="decade-badge {b2}">{lbl[d2s]}</span></div><div class="decade-block-val">{fmt(r["D2"])}</div><div class="decade-block-unit">KT • J11–20</div></div><div class="decade-block {a3}"><div class="decade-block-label">D3 <span class="decade-badge {b3}">{lbl[d3s]}</span></div><div class="decade-block-val">{fmt(r["D3"])}</div><div class="decade-block-unit">KT • J21–fin</div></div></div><div class="decade-total-row"><span class="decade-total-label">Total mensuel</span><span class="decade-total-val">{fmt(r["total"])} KT</span></div></div>',unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#00843D;margin-bottom:8px">▶ Jorf Lasfar</div>',unsafe_allow_html=True)
    render_decades(dec_jorf)
    st.markdown('<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#1565C0;margin:14px 0 8px 0">▶ Safi</div>',unsafe_allow_html=True)
    render_decades(dec_safi)

    st.markdown('<div class="stitle">Modules disponibles</div>',unsafe_allow_html=True)
    m1,m2,m3,m4,m5,m6=st.columns(6)
    modules=[
        (m1,"Suivi Chargement","Tableau consolidé des chargements journaliers par site.","active","suivi"),
        (m2,"Dashboard Chargement","Courbes journalières TSP Safi & Jorf avec histogrammes.","active","dashboard_chargement"),
        (m3,"Simulation Stock","Projection du stock matières premières avec arrivées navires.","active","stock"),
        (m4,"Pipeline des Ventes","Suivi des ventes par décade avec analyse IA des statuts.","active","ventes"),
        (m5,"Dashboard Ventes","Visualisation volume par Produit, Statut, Pays & Site.","active","dashboard_ventes"),
        (m6,"Zoom TSP","Pipeline TSP filtré automatiquement — analyse complète.","active","tsp_zoom"),
    ]
    for col,title,desc,status,nav_key in modules:
        with col:
            badge="Disponible" if status=="active" else "Prochainement"
            st.markdown(f'<div class="mcard"><div class="mcard-title">{title}</div><div class="mcard-desc">{desc}</div><div class="mcard-badge {status}">{badge}</div></div>',unsafe_allow_html=True)
            if status=="active":
                if st.button(f"Ouvrir →",key=f"open_{nav_key}",use_container_width=True):
                    st.session_state["page"]=nav_key; st.rerun()

    st.markdown('<div class="stitle">Historique des fichiers chargés</div>',unsafe_allow_html=True)
    hj=load_hist(HIST_JORF); hs=load_hist(HIST_SAFI); hv=load_hist(HIST_VENTES)
    col_hj,col_hs,col_hv=st.columns(3)
    def _render_hist_col(col,hist,label,color,loader_fn,name_key):
        clr_map={"jorf":"#00843D","safi":"#1565C0","ventes":"#6B3FA0"}
        bg_map={"jorf":"#E8F5EE","safi":"#E3EAF8","ventes":"#F0EBF8"}
        h_clr=clr_map.get(color,"#94A3B8"); h_bg=bg_map.get(color,"#F2F4F7")
        with col:
            st.markdown(f'<div class="card"><div class="card-title" style="color:{h_clr}">Historique — {label}</div>',unsafe_allow_html=True)
            if hist:
                active_name=st.session_state.get(name_key,"")
                for i,e in enumerate(hist[:8]):
                    is_act=e["filename"]==active_name
                    dot_cls="hist-active" if is_act else "hist-inactive"
                    act_html=f' — <b style="color:{h_clr}">Actif</b>' if is_act else ""
                    st.markdown(f'<div class="hist-item"><div><div style="display:flex;align-items:center;gap:8px"><span class="{dot_cls}"></span><span class="hist-item-name">{e["filename"]}</span><span style="background:{h_bg};color:{h_clr};border-radius:10px;padding:2px 8px;font-size:9px;font-weight:700;text-transform:uppercase">{color.upper()}</span></div><div class="hist-item-date" style="margin-left:15px">{e["date_upload"]}{act_html}</div></div></div>',unsafe_allow_html=True)
                    if not is_act:
                        if st.button("Recharger",key=f"rl_{color}_{i}",use_container_width=True):
                            raw=get_hist_bytes(e)
                            if raw:
                                try: loader_fn(raw,e["filename"]); st.rerun()
                                except Exception as ex: st.error(str(ex))
                            else: st.error("Fichier introuvable.")
            else:
                st.markdown(f'<div style="color:#94A3B8;font-size:12px;padding:12px 0">Aucun fichier {label} dans l\'historique.</div>',unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)
    _render_hist_col(col_hj,hj,"Jorf Lasfar","jorf",load_jorf,"jorf_name")
    _render_hist_col(col_hs,hs,"Safi","safi",load_safi,"safi_name")
    _render_hist_col(col_hv,hv,"Pipeline","ventes",load_ventes_hist,"ventes_name")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE SUIVI CHARGEMENT
# ══════════════════════════════════════════════════════════════════════════════
elif page=="suivi":
    st.markdown('<div class="stitle">Chargement des fichiers</div>',unsafe_allow_html=True)
    uc1,uc2=st.columns(2)
    with uc1:
        st.markdown('<div class="upload-zone"><div class="zone-title">Fichier Jorf Lasfar</div><div class="zone-desc">Fichier Excel avec feuille EXPORT et Sit Navire</div>',unsafe_allow_html=True)
        file_jorf=st.file_uploader("Choisir fichier Jorf",type=EXCEL_T,key="jorf_up",label_visibility="collapsed")
        jn=st.session_state.get("jorf_name","")
        if jn: st.success(f"Actif : {jn}")
        if file_jorf:
            try:
                jb,eng=read_bytes(file_jorf); jd=parse_jorf(jb,eng); rd=None
                try: rd=parse_rade(jb,eng)
                except: pass
                clear_cache(JORF_CACHE)
                st.session_state.update({"jorf_df":jd,"rade_df":rd,"jorf_name":file_jorf.name})
                save_cache(JORF_CACHE,{"jorf_df":jd,"rade_df":rd,"filename":file_jorf.name})
                file_jorf.seek(0); add_hist(HIST_JORF,file_jorf.name,file_jorf.read(),"jorf")
                jorf_df=jd; rade_df=rd; st.success("Jorf chargé avec succès")
            except Exception as e: st.error(f"Erreur : {e}")
        st.markdown("</div>",unsafe_allow_html=True)
    with uc2:
        st.markdown('<div class="upload-zone"><div class="zone-title">Fichier Safi</div><div class="zone-desc">Fichier Excel avec feuilles mensuelles TSP Export / ML</div>',unsafe_allow_html=True)
        file_safi=st.file_uploader("Choisir fichier Safi",type=EXCEL_T,key="safi_up",label_visibility="collapsed")
        sn=st.session_state.get("safi_name","")
        if sn: st.success(f"Actif : {sn}")
        if file_safi:
            try:
                sb,eng=read_bytes(file_safi); sd=parse_safi(sb,eng)
                clear_cache(SAFI_CACHE)
                st.session_state.update({"safi_df":sd,"safi_name":file_safi.name})
                save_cache(SAFI_CACHE,{"safi_df":sd,"filename":file_safi.name})
                file_safi.seek(0); add_hist(HIST_SAFI,file_safi.name,file_safi.read(),"safi")
                safi_df=sd
                if sd is not None: st.success("Safi chargé avec succès")
                else: st.warning("Aucune feuille mensuelle détectée.")
            except Exception as e: st.error(f"Erreur : {e}")
        st.markdown("</div>",unsafe_allow_html=True)

    jorf_df=st.session_state.get("jorf_df"); rade_df=st.session_state.get("rade_df"); safi_df=st.session_state.get("safi_df")
    st.markdown('<div class="stitle">Filtrage des données</div>',unsafe_allow_html=True)
    def filtre_widget(df,label,key):
        mois_map={}; annees=set()
        for d in df["Date"].unique():
            try: p=str(d).split("/"); annees.add(int(p[2])); ml=f"{NOMS_MOIS.get(int(p[1]),'?')} {p[2]}"
            except: ml="Autre"
            mois_map.setdefault(ml,[]).append(d)
        for an in annees:
            for num,nom in NOMS_MOIS.items():
                ml=f"{nom} {an}"
                if ml not in mois_map: mois_map[ml]=[]
        mois_tries=sorted(mois_map.keys(),key=msort)
        opts=[m if mois_map[m] else f"{m} —" for m in mois_tries]
        mode=st.radio(f"Filtrer **{label}** par",["Tout","Mois","Dates"],horizontal=True,key=f"{key}_mode")
        if mode=="Tout": return [],"Toute la période"
        elif mode=="Mois":
            choix=st.multiselect("Sélectionner les mois",options=opts,default=[],key=f"{key}_mois")
            if not choix: return [],"Toute la période"
            ds=[]; lb=[]
            for m in choix:
                cl=m.rstrip(" —"); ds+=mois_map.get(cl,[]); lb.append(cl)
            return ds,", ".join(lb)
        else:
            all_d=sorted(df["Date"].unique().tolist(),key=lambda x:tuple(int(v) for v in str(x).split("/"))[::-1])
            choix=st.multiselect("Sélectionner les dates",all_d,key=f"{key}_dates")
            if not choix: return [],"Toute la période"
            return choix,f"{len(choix)} date(s)"

    fc1,fc2=st.columns(2)
    with fc1:
        st.markdown('<div class="filter-panel"><div class="filter-panel-title">Jorf Lasfar</div>',unsafe_allow_html=True)
        if jorf_df is not None: sel_jorf,lbl_jorf=filtre_widget(jorf_df,"Jorf","jorf")
        else: st.info("Chargez le fichier Jorf pour activer les filtres."); sel_jorf,lbl_jorf=[],"Toute la période"
        st.markdown('</div>',unsafe_allow_html=True)
    with fc2:
        st.markdown('<div class="filter-panel"><div class="filter-panel-title">Safi</div>',unsafe_allow_html=True)
        if safi_df is not None: sel_safi,lbl_safi=filtre_widget(safi_df,"Safi","safi")
        else: st.info("Chargez le fichier Safi pour activer les filtres."); sel_safi,lbl_safi=[],"Toute la période"
        st.markdown('</div>',unsafe_allow_html=True)

    jorf_k=filt(jorf_df,sel_jorf) if jorf_df is not None else None
    safi_k=filt(safi_df,sel_safi) if safi_df is not None else None
    rade_k=filt(rade_df,sel_jorf) if rade_df is not None else None
    cj=round(float(jorf_k["TOTAL Jorf"].sum()),1) if jorf_k is not None else 0.
    cs=round(float(safi_k["TOTAL Safi"].sum()),1) if safi_k is not None else 0.
    ct=round(cj+cs,1)
    rv,rd_=last_val(rade_k,"Engrais en attente") if rade_k is not None else (0.,None)
    periode=f"Filtre : {lbl_jorf} / {lbl_safi}" if (sel_jorf or sel_safi) else "Toute la période"
    st.markdown(f'<div class="stitle">Cumul à date — {periode}</div>',unsafe_allow_html=True)
    k1,k2,k3,k4=st.columns(4)
    def kpi(col,color,lbl,val,sub,extra=""):
        with col:
            extra_html=f'<div style="font-size:10px;color:#94A3B8;margin-top:3px">{extra}</div>' if extra else ""
            st.markdown(f'<div class="kcard {color}"><div class="kc-lbl">{lbl}</div><div class="kc-val {color}">{fmt(val)}<span class="kc-unit">KT</span></div><div class="kc-sub">{sub}</div>{extra_html}</div>',unsafe_allow_html=True)
    kpi(k1,"green","Total Jorf",cj,"Export Engrais • Camions • VL" if jorf_df is not None else "Non chargé")
    with k2:
        if rade_df is not None and rd_:
            st.markdown(f'<div class="kcard purple"><div class="kc-lbl">Rade Jorf</div><div class="kc-val purple">{fmt(rv)}<span class="kc-unit">KT</span></div><div class="kc-sub">Engrais en attente</div><div style="font-size:10px;color:#94A3B8;margin-top:3px">{rd_}</div></div>',unsafe_allow_html=True)
        else: kpi(k2,"purple","Rade Jorf",0.,"Non chargé")
    kpi(k3,"blue","Total Safi",cs,"TSP Export • TSP ML" if safi_df is not None else "Non chargé")
    kpi(k4,"orange","Jorf + Safi",ct,"Consolidé toutes unités")

    st.markdown('<div class="stitle">Tableau consolidé — par jour (KT)</div>',unsafe_allow_html=True)
    any_data=jorf_df is not None or safi_df is not None or rade_df is not None
    if any_data:
        jf=filt(jorf_df,sel_jorf) if jorf_df is not None else None
        rf=filt(rade_df,sel_jorf) if rade_df is not None else None
        sf=filt(safi_df,sel_safi) if safi_df is not None else None
        all_d=set()
        if jf is not None: all_d|=set(jf["Date"].unique())
        if rf is not None: all_d|=set(rf["Date"].unique())
        if sf is not None: all_d|=set(sf["Date"].unique())
        all_d=sorted(all_d,key=dsort); rows=[]
        for d in all_d:
            row={"Date":d}
            if jf is not None:
                r=jf[jf["Date"]==d]
                row["J_Eng"]=round(r["Export Engrais"].sum(),1) if not r.empty else 0.
                row["J_Cam"]=round(r["Export Camions"].sum(),1) if not r.empty else 0.
                row["J_VL"]=round(r["VL Camions"].sum(),1) if not r.empty else 0.
            if sf is not None:
                r=sf[sf["Date"]==d]
                row["S_Eng"]=round(r["TSP Export"].sum(),1) if not r.empty else 0.
                row["S_VL"]=round(r["TSP ML"].sum(),1) if not r.empty else 0.
            jt=round(row.get("J_Eng",0)+row.get("J_Cam",0)+row.get("J_VL",0),1) if jf is not None else 0.
            st_=round(row.get("S_Eng",0)+row.get("S_VL",0),1) if sf is not None else 0.
            if jf is not None: row["J_TOT"]=jt
            if sf is not None: row["S_TOT"]=st_
            row["TOTAL"]=round(jt+st_,1)
            if rf is not None:
                r=rf[rf["Date"]==d]; row["RADE"]=round(r["Engrais en attente"].sum(),1) if not r.empty else 0.
            rows.append(row)
        udf=pd.DataFrame(rows)
        co=["Date"]
        if jf is not None: co+=["J_Eng","J_Cam","J_VL","J_TOT"]
        if sf is not None: co+=["S_Eng","S_VL","S_TOT"]
        co+=["TOTAL"]
        if rf is not None: co+=["RADE"]
        co=[c for c in co if c in udf.columns]; udf=udf[co]
        tr={"Date":"TOTAL GÉNÉRAL"}
        for c in udf.columns:
            if c=="Date": continue
            elif c=="RADE": tr[c]=None
            else: tr[c]=round(udf[c].sum(),1)
        disp=pd.concat([udf,pd.DataFrame([tr])],ignore_index=True)
        nm={"J_Eng":"Engrais","J_Cam":"Camions","J_VL":"VL","J_TOT":"▶ Total Jorf","S_Eng":"TSP Export","S_VL":"TSP ML","S_TOT":"▶ Total Safi","TOTAL":"▶ Total Cumulé","RADE":"Rade Jorf"}
        cfg={"Date":st.column_config.TextColumn("Date",width=90)}
        for c,n in nm.items():
            if c in disp.columns: cfg[c]=st.column_config.NumberColumn(n,format="%.1f")
        st.dataframe(disp,use_container_width=True,hide_index=True,height=min(660,45+35*len(disp)),column_config=cfg)
        cb1,cb2,cb3,cb4,_=st.columns([1,1,1,1,1])
        def copy_btn(container,df,col,lbl,key):
            vals=df[df["Date"]!="TOTAL GÉNÉRAL"][col].dropna().tolist()
            txt="\t".join(str(round(float(v),1)) for v in vals)
            bid=f"cb_{key}"
            with container:
                st.components.v1.html(f'<button id="{bid}" onclick="navigator.clipboard.writeText(\'{txt}\').then(()=>{{this.innerHTML=\'✓ Copié !\';this.style.background=\'#E8F5EE\';this.style.color=\'#005C2A\';setTimeout(()=>{{this.innerHTML=\'{lbl}\';this.style.background=\'\';this.style.color=\'\';}},2000)}})"> {lbl}</button><style>#{bid}{{background:#F2F4F7;color:#4A5568;border:1px solid #E0E4EA;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600;font-family:Barlow,sans-serif;width:100%}}</style>',height=40)
        if jf is not None and "J_TOT" in udf.columns: copy_btn(cb1,udf,"J_TOT","Copier Jorf","j")
        if sf is not None and "S_TOT" in udf.columns: copy_btn(cb2,udf,"S_TOT","Copier Safi","s")
        if "TOTAL" in udf.columns: copy_btn(cb3,udf,"TOTAL","Copier Total","t")
        if rf is not None and "RADE" in udf.columns: copy_btn(cb4,udf,"RADE","Copier Rade","r")
        g1,g2=st.columns(2)
        with g1:
            st.markdown('<div class="stitle purple">Rade Jorf — Engrais en attente</div>',unsafe_allow_html=True)
            if rf is not None and "RADE" in udf.columns:
                rc=udf[udf["RADE"]>0].copy()
                if len(rc)>0:
                    fig=go.Figure()
                    fig.add_trace(go.Bar(x=rc["Date"],y=rc["RADE"],name="Rade",marker=dict(color="#6B3FA0",opacity=.85),hovertemplate='<b>%{x}</b><br>%{y:.1f} KT<extra></extra>'))
                    fig.update_layout(**PL,title=dict(text="Rade Jorf (KT)",font=dict(size=13,color="#4A5568")))
                    st.plotly_chart(fig,use_container_width=True)
                else: st.info("Pas de données Rade.")
            else: st.info("Chargez le fichier Jorf.")
        with g2:
            st.markdown('<div class="stitle">Jorf vs Safi — production journalière</div>',unsafe_allow_html=True)
            djs=[c for c in ["J_TOT","S_TOT"] if c in udf.columns]; nm2={"J_TOT":"Jorf","S_TOT":"Safi"}
            if djs and len(udf)>1:
                fig=go.Figure()
                for c in djs:
                    clr="#00843D" if c=="J_TOT" else "#1565C0"; fc2="rgba(0,132,61,0.07)" if c=="J_TOT" else "rgba(21,101,192,0.07)"
                    fig.add_trace(go.Scatter(x=udf["Date"],y=udf[c],mode='lines',name=nm2[c],line=dict(color=clr,width=2),fill='tozeroy',fillcolor=fc2))
                fig.update_layout(**PL,title=dict(text="Total Jorf & Safi (KT/jour)",font=dict(size=13,color="#4A5568")))
                st.plotly_chart(fig,use_container_width=True)
            else: st.info("Chargez les fichiers pour voir les graphiques.")
    else:
        st.info("Chargez au moins un fichier Excel ci-dessus pour afficher les données.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE DASHBOARD CHARGEMENT
# ══════════════════════════════════════════════════════════════════════════════
elif page=="dashboard_chargement":
    MOIS_FR_D=["Tous","Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    dc_safi=st.session_state.get("safi_df")
    dc_jorf=st.session_state.get("jorf_df")

    def _render_chargement_bloc(df_raw_dc, label, couleur_principal, couleur_secondaire,
                                 col1_key, col2_key, total_key,
                                 lbl1, lbl2, lbl_total,
                                 section_key, col3_key=None, lbl3=None,
                                 couleur_tertiaire="#00843D", mois_num_filtre=None):
        if df_raw_dc is None or df_raw_dc.empty:
            st.markdown(f'<div style="background:#F2F4F7;border:1px dashed #E0E4EA;border-radius:10px;padding:24px;text-align:center;color:#94A3B8;font-size:13px">Fichier {label} non chargé — chargez-le depuis la page <b>Suivi Chargement</b></div>',unsafe_allow_html=True)
            return
        df_dc=df_raw_dc.copy()
        if mois_num_filtre:
            df_dc=df_dc[df_dc["Date"].apply(lambda d: int(str(d).split("/")[1])==mois_num_filtre if len(str(d).split("/"))>=2 else False)]
        df_dc=df_dc.sort_values("Date",key=lambda s: s.apply(dsort))
        if df_dc.empty:
            st.info(f"Aucune donnée {label} pour la période sélectionnée."); return
        v1=round(float(df_dc[col1_key].sum()),1) if col1_key in df_dc.columns else 0.
        v2=round(float(df_dc[col2_key].sum()),1) if col2_key in df_dc.columns else 0.
        v3=round(float(df_dc[col3_key].sum()),1) if col3_key and col3_key in df_dc.columns else None
        vt=round(float(df_dc[total_key].sum()),1) if total_key in df_dc.columns else 0.
        nj=len(df_dc)
        if col3_key and lbl3:
            _k1,_k2,_k3,_k4=st.columns(4)
            with _k1: st.markdown(f'<div class="tsp-kcard" style="border-top-color:{couleur_principal}"><div class="tsp-kcard-lbl">{lbl1}</div><div class="tsp-kcard-val" style="color:{couleur_principal}">{fmt(v1)}<span class="tsp-kcard-unit">KT</span></div></div>',unsafe_allow_html=True)
            with _k2: st.markdown(f'<div class="tsp-kcard" style="border-top-color:{couleur_secondaire}"><div class="tsp-kcard-lbl">{lbl2}</div><div class="tsp-kcard-val" style="color:{couleur_secondaire}">{fmt(v2)}<span class="tsp-kcard-unit">KT</span></div></div>',unsafe_allow_html=True)
            with _k3: st.markdown(f'<div class="tsp-kcard" style="border-top-color:{couleur_tertiaire}"><div class="tsp-kcard-lbl">{lbl3}</div><div class="tsp-kcard-val" style="color:{couleur_tertiaire}">{fmt(v3)}<span class="tsp-kcard-unit">KT</span></div></div>',unsafe_allow_html=True)
            with _k4: st.markdown(f'<div class="tsp-kcard" style="border-top-color:#94A3B8"><div class="tsp-kcard-lbl">NB JOURS</div><div class="tsp-kcard-val" style="color:#94A3B8">{nj}<span class="tsp-kcard-unit">j</span></div></div>',unsafe_allow_html=True)
        else:
            _k1,_k2,_k3=st.columns(3)
            with _k1: st.markdown(f'<div class="tsp-kcard" style="border-top-color:{couleur_principal}"><div class="tsp-kcard-lbl">{lbl1}</div><div class="tsp-kcard-val" style="color:{couleur_principal}">{fmt(v1)}<span class="tsp-kcard-unit">KT</span></div></div>',unsafe_allow_html=True)
            with _k2: st.markdown(f'<div class="tsp-kcard" style="border-top-color:{couleur_secondaire}"><div class="tsp-kcard-lbl">{lbl2}</div><div class="tsp-kcard-val" style="color:{couleur_secondaire}">{fmt(v2)}<span class="tsp-kcard-unit">KT</span></div></div>',unsafe_allow_html=True)
            with _k3: st.markdown(f'<div class="tsp-kcard" style="border-top-color:#94A3B8"><div class="tsp-kcard-lbl">NB JOURS</div><div class="tsp-kcard-val" style="color:#94A3B8">{nj}<span class="tsp-kcard-unit">j</span></div></div>',unsafe_allow_html=True)
        tab_hist,tab_line,tab_cum,tab_comp=st.tabs(["Histogramme","Courbe journalière","Cumul",f"{lbl1} vs {lbl2}"])
        with tab_hist:
            fig=go.Figure()
            fig.add_trace(go.Bar(x=df_dc["Date"],y=df_dc[col1_key] if col1_key in df_dc.columns else [],name=lbl1,marker=dict(color=couleur_principal,opacity=.85),hovertemplate=f'<b>%{{x}}</b><br>{lbl1} : %{{y:.1f}} KT<extra></extra>'))
            fig.add_trace(go.Bar(x=df_dc["Date"],y=df_dc[col2_key] if col2_key in df_dc.columns else [],name=lbl2,marker=dict(color=couleur_secondaire,opacity=.85),hovertemplate=f'<b>%{{x}}</b><br>{lbl2} : %{{y:.1f}} KT<extra></extra>'))
            if col3_key and lbl3 and col3_key in df_dc.columns:
                fig.add_trace(go.Bar(x=df_dc["Date"],y=df_dc[col3_key],name=lbl3,marker=dict(color=couleur_tertiaire,opacity=.85),hovertemplate=f'<b>%{{x}}</b><br>{lbl3} : %{{y:.1f}} KT<extra></extra>'))
            lyt=dict(**PL); lyt['height']=420; lyt['title']=dict(text=f"{label} par jour — Histogramme (KT)",font=dict(size=13,color="#12202E")); lyt['barmode']='stack'
            fig.update_layout(**lyt); st.plotly_chart(fig,use_container_width=True)
        with tab_line:
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=df_dc["Date"],y=df_dc[col1_key] if col1_key in df_dc.columns else [],mode='lines+markers',name=lbl1,line=dict(color=couleur_principal,width=2.5),marker=dict(size=4),fill='tozeroy',fillcolor=f'rgba({int(couleur_principal[1:3],16)},{int(couleur_principal[3:5],16)},{int(couleur_principal[5:7],16)},0.07)'))
            fig.add_trace(go.Scatter(x=df_dc["Date"],y=df_dc[col2_key] if col2_key in df_dc.columns else [],mode='lines+markers',name=lbl2,line=dict(color=couleur_secondaire,width=2.5),marker=dict(size=4),fill='tozeroy',fillcolor=f'rgba({int(couleur_secondaire[1:3],16)},{int(couleur_secondaire[3:5],16)},{int(couleur_secondaire[5:7],16)},0.07)'))
            if col3_key and lbl3 and col3_key in df_dc.columns:
                fig.add_trace(go.Scatter(x=df_dc["Date"],y=df_dc[col3_key],mode='lines+markers',name=lbl3,line=dict(color=couleur_tertiaire,width=2),marker=dict(size=4)))
            fig.add_trace(go.Scatter(x=df_dc["Date"],y=df_dc[total_key] if total_key in df_dc.columns else [],mode='lines',name=lbl_total,line=dict(color="#12202E",width=1.5,dash='dot')))
            lyt=dict(**PL); lyt['height']=420; lyt['title']=dict(text=f"{label} — Courbe journalière (KT)",font=dict(size=13,color="#12202E"))
            fig.update_layout(**lyt); st.plotly_chart(fig,use_container_width=True)
        with tab_cum:
            df_c=df_dc.copy()
            if col1_key in df_c.columns: df_c[f"Cum_{col1_key}"]=df_c[col1_key].cumsum()
            if col2_key in df_c.columns: df_c[f"Cum_{col2_key}"]=df_c[col2_key].cumsum()
            if col3_key and col3_key in df_c.columns: df_c[f"Cum_{col3_key}"]=df_c[col3_key].cumsum()
            if total_key in df_c.columns: df_c[f"Cum_{total_key}"]=df_c[total_key].cumsum()
            fig=go.Figure()
            if f"Cum_{col1_key}" in df_c.columns: fig.add_trace(go.Scatter(x=df_c["Date"],y=df_c[f"Cum_{col1_key}"],mode='lines',name=f"Cumul {lbl1}",line=dict(color=couleur_principal,width=2.5),fill='tozeroy',fillcolor=f'rgba({int(couleur_principal[1:3],16)},{int(couleur_principal[3:5],16)},{int(couleur_principal[5:7],16)},0.07)'))
            if f"Cum_{col2_key}" in df_c.columns: fig.add_trace(go.Scatter(x=df_c["Date"],y=df_c[f"Cum_{col2_key}"],mode='lines',name=f"Cumul {lbl2}",line=dict(color=couleur_secondaire,width=2.5),fill='tozeroy',fillcolor=f'rgba({int(couleur_secondaire[1:3],16)},{int(couleur_secondaire[3:5],16)},{int(couleur_secondaire[5:7],16)},0.07)'))
            if col3_key and lbl3 and f"Cum_{col3_key}" in df_c.columns: fig.add_trace(go.Scatter(x=df_c["Date"],y=df_c[f"Cum_{col3_key}"],mode='lines',name=f"Cumul {lbl3}",line=dict(color=couleur_tertiaire,width=2)))
            if f"Cum_{total_key}" in df_c.columns: fig.add_trace(go.Scatter(x=df_c["Date"],y=df_c[f"Cum_{total_key}"],mode='lines',name=f"Cumul {lbl_total}",line=dict(color="#12202E",width=1.5,dash='dot')))
            lyt=dict(**PL); lyt['height']=420; lyt['title']=dict(text=f"{label} — Cumul progressif (KT)",font=dict(size=13,color="#12202E"))
            fig.update_layout(**lyt); st.plotly_chart(fig,use_container_width=True)
        with tab_comp:
            if "Mois" in df_dc.columns:
                grp_cols=[c for c in [col1_key,col2_key,col3_key,total_key] if c and c in df_dc.columns]
                grp_cols=list(dict.fromkeys(grp_cols))
                mois_g=df_dc.groupby("Mois")[grp_cols].sum().reset_index()
                fig_cmp=go.Figure()
                fig_cmp.add_trace(go.Bar(x=mois_g["Mois"],y=mois_g[col1_key] if col1_key in mois_g.columns else [],name=lbl1,marker=dict(color=couleur_principal,opacity=.85)))
                fig_cmp.add_trace(go.Bar(x=mois_g["Mois"],y=mois_g[col2_key] if col2_key in mois_g.columns else [],name=lbl2,marker=dict(color=couleur_secondaire,opacity=.85)))
                if col3_key and lbl3 and col3_key in mois_g.columns: fig_cmp.add_trace(go.Bar(x=mois_g["Mois"],y=mois_g[col3_key],name=lbl3,marker=dict(color=couleur_tertiaire,opacity=.85)))
                fig_cmp.update_layout(barmode='group',**{**PL,'height':400,'title':dict(text=f"Comparaison {label} par mois (KT)",font=dict(size=13,color="#12202E"))})
                st.plotly_chart(fig_cmp,use_container_width=True)
            _p1,_p2=st.columns(2)
            with _p1:
                pie_lbls=[lbl1,lbl2]; pie_vals=[v1,v2]; pie_clrs=[couleur_principal,couleur_secondaire]
                if col3_key and lbl3 and v3 is not None and v3>0:
                    pie_lbls.append(lbl3); pie_vals.append(v3); pie_clrs.append(couleur_tertiaire)
                if any(v>0 for v in pie_vals):
                    fig_pie=go.Figure(go.Pie(labels=pie_lbls,values=pie_vals,marker=dict(colors=pie_clrs),hole=.45,textinfo='label+percent',hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
                    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='Barlow,sans-serif'),legend=dict(bgcolor='rgba(255,255,255,.9)',bordercolor='#E0E4EA',borderwidth=1),margin=dict(l=12,r=12,t=36,b=12),height=300,title=dict(text=f"Répartition {label}",font=dict(size=13,color="#12202E")))
                    st.plotly_chart(fig_pie,use_container_width=True)
            with _p2:
                _dec=compute_decades(df_dc,total_key)
                if _dec:
                    _dv=[r["D1"] for r in _dec],[r["D2"] for r in _dec],[r["D3"] for r in _dec]
                    fig_dec=go.Figure(go.Bar(x=["D1 (J1-10)","D2 (J11-20)","D3 (J21+)"],y=[sum(_dv[0]),sum(_dv[1]),sum(_dv[2])],marker=dict(color=[couleur_principal,couleur_secondaire,couleur_tertiaire],opacity=.85)))
                    fig_dec.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(242,244,247,0.6)',font=dict(family='Barlow,sans-serif',color='#4A5568'),xaxis=dict(gridcolor='#E0E4EA'),yaxis=dict(gridcolor='#E0E4EA'),margin=dict(l=12,r=12,t=36,b=12),height=300,title=dict(text=f"Total {label} par décade",font=dict(size=13,color="#12202E")))
                    st.plotly_chart(fig_dec,use_container_width=True)

    st.markdown('<div class="filter-panel"><div class="filter-panel-title">Filtre mois</div>',unsafe_allow_html=True)
    _df_filt=st.columns(2)
    with _df_filt[0]:
        dc_sel_mois=st.selectbox("Filtrer par mois",MOIS_FR_D,key="dc_mois")
    with _df_filt[1]:
        _dc_info_parts=[]
        if st.session_state.get("safi_name"): _dc_info_parts.append(f'<span style="background:#E3EAF8;color:#1565C0;border-radius:6px;padding:3px 10px;font-size:10px;font-weight:700">Safi : {st.session_state["safi_name"]}</span>')
        if st.session_state.get("jorf_name"): _dc_info_parts.append(f'<span style="background:#E8F5EE;color:#005C2A;border-radius:6px;padding:3px 10px;font-size:10px;font-weight:700">Jorf : {st.session_state["jorf_name"]}</span>')
        if _dc_info_parts: st.markdown(f'<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;height:100%;padding-top:22px">{"".join(_dc_info_parts)}</div>',unsafe_allow_html=True)
        else: st.markdown('<div style="padding-top:22px;font-size:11px;color:#94A3B8">Chargez les fichiers depuis Suivi Chargement</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)
    dc_mois_num=MOIS_FR_D.index(dc_sel_mois) if dc_sel_mois!="Tous" else None
    st.markdown('<div style="background:linear-gradient(135deg,#1565C0,#0D47A1);color:white;padding:14px 22px;border-radius:10px;margin:0 0 16px 0;box-shadow:0 4px 16px rgba(21,101,192,.2)"><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:20px;font-weight:800;letter-spacing:.5px">▶ SAFI — TSP Export & ML</div><div style="font-size:11px;opacity:.75;margin-top:3px">Données journalières chargement TSP — Export et Marché Local</div></div>',unsafe_allow_html=True)
    _render_chargement_bloc(dc_safi,"Safi TSP","#1565C0","#C05A00","TSP Export","TSP ML","TOTAL Safi","TSP EXPORT","TSP ML","Total Safi","safi",mois_num_filtre=dc_mois_num)
    st.markdown('<div style="height:24px"></div>',unsafe_allow_html=True)
    st.markdown('<div style="background:linear-gradient(135deg,#00843D,#005C2A);color:white;padding:14px 22px;border-radius:10px;margin:0 0 16px 0;box-shadow:0 4px 16px rgba(0,132,61,.2)"><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:20px;font-weight:800;letter-spacing:.5px">▶ JORF LASFAR — Export Engrais, Camions & VL</div><div style="font-size:11px;opacity:.75;margin-top:3px">Données journalières chargement — Engrais export, Camions export, VL camions</div></div>',unsafe_allow_html=True)
    _render_chargement_bloc(dc_jorf,"Jorf Lasfar","#00843D","#C05A00","Export Engrais","Export Camions","TOTAL Jorf","EXPORT ENGRAIS","EXPORT CAMIONS","Total Jorf","jorf",col3_key="VL Camions",lbl3="VL CAMIONS",couleur_tertiaire="#1565C0",mois_num_filtre=dc_mois_num)
    # ══════════════════════════════════════════════════════
    # GRAPHE CONSOLIDÉ — Total Jorf / Total Safi / Cumul / Rade
    # ══════════════════════════════════════════════════════
    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="background:linear-gradient(135deg,#12202E,#1E3A5F);color:white;padding:14px 22px;'
        'border-radius:10px;margin:0 0 16px 0;box-shadow:0 4px 16px rgba(0,0,0,.2)">'
        '<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:20px;font-weight:800;letter-spacing:.5px">'
        '▶ VUE CONSOLIDÉE — Jorf + Safi + Rade</div>'
        '<div style="font-size:11px;opacity:.75;margin-top:3px">'
        'Total Jorf · Total Safi · Cumul Consolidé · Rade Jorf — sur la même période</div>'
        '</div>', unsafe_allow_html=True)

    _rade_df_dc = st.session_state.get("rade_df")

    def _apply_mois_filter(df, mois_num):
        if df is None or df.empty or mois_num is None:
            return df
        return df[df["Date"].apply(
            lambda d: int(str(d).split("/")[1]) == mois_num
            if len(str(d).split("/")) >= 2 else False
        )]

    _jorf_c = _apply_mois_filter(dc_jorf, dc_mois_num)
    _safi_c = _apply_mois_filter(dc_safi, dc_mois_num)
    _rade_c = _apply_mois_filter(_rade_df_dc, dc_mois_num)

    _all_dates = set()
    if _jorf_c is not None:
        _all_dates |= set(_jorf_c["Date"].unique())
    if _safi_c is not None:
        _all_dates |= set(_safi_c["Date"].unique())
    if _rade_c is not None:
        _all_dates |= set(_rade_c["Date"].unique())
    _all_dates = sorted(_all_dates, key=dsort)

    if _all_dates:
        _cons_rows = []
        for _d in _all_dates:
            _row = {"Date": _d}
            if _jorf_c is not None:
                _r = _jorf_c[_jorf_c["Date"] == _d]
                _row["Total Jorf"] = round(_r["TOTAL Jorf"].sum(), 1) if not _r.empty else 0.
            else:
                _row["Total Jorf"] = 0.
            if _safi_c is not None:
                _r = _safi_c[_safi_c["Date"] == _d]
                _row["Total Safi"] = round(_r["TOTAL Safi"].sum(), 1) if not _r.empty else 0.
            else:
                _row["Total Safi"] = 0.
            _row["Cumul Total"] = round(_row["Total Jorf"] + _row["Total Safi"], 1)
            if _rade_c is not None:
                _r = _rade_c[_rade_c["Date"] == _d]
                _row["Rade Jorf"] = round(_r["Engrais en attente"].sum(), 1) if not _r.empty else None
            else:
                _row["Rade Jorf"] = None
            _cons_rows.append(_row)

        _df_cons = pd.DataFrame(_cons_rows)

        # KPIs
        _kc1, _kc2, _kc3, _kc4 = st.columns(4)
        _kc1.markdown(
            f'<div class="tsp-kcard" style="border-top-color:#00843D">'
            f'<div class="tsp-kcard-lbl">Total Jorf</div>'
            f'<div class="tsp-kcard-val" style="color:#00843D">{fmt(round(_df_cons["Total Jorf"].sum(),1))}'
            f'<span class="tsp-kcard-unit">KT</span></div></div>', unsafe_allow_html=True)
        _kc2.markdown(
            f'<div class="tsp-kcard" style="border-top-color:#1565C0">'
            f'<div class="tsp-kcard-lbl">Total Safi</div>'
            f'<div class="tsp-kcard-val" style="color:#1565C0">{fmt(round(_df_cons["Total Safi"].sum(),1))}'
            f'<span class="tsp-kcard-unit">KT</span></div></div>', unsafe_allow_html=True)
        _kc3.markdown(
            f'<div class="tsp-kcard" style="border-top-color:#C05A00">'
            f'<div class="tsp-kcard-lbl">Cumul Total</div>'
            f'<div class="tsp-kcard-val" style="color:#C05A00">{fmt(round(_df_cons["Cumul Total"].sum(),1))}'
            f'<span class="tsp-kcard-unit">KT</span></div></div>', unsafe_allow_html=True)
        _rade_last = _df_cons["Rade Jorf"].dropna()
        _rade_val = round(float(_rade_last.iloc[-1]), 1) if not _rade_last.empty else 0.
        _kc4.markdown(
            f'<div class="tsp-kcard" style="border-top-color:#6B3FA0">'
            f'<div class="tsp-kcard-lbl">Rade Jorf (dernière)</div>'
            f'<div class="tsp-kcard-val" style="color:#6B3FA0">{fmt(_rade_val)}'
            f'<span class="tsp-kcard-unit">KT</span></div></div>', unsafe_allow_html=True)

        # Graphiques
        _tab_line, _tab_bar = st.tabs(["Courbes journalières", "Histogramme journalier"])

        with _tab_line:
            fig_cons = go.Figure()
            fig_cons.add_trace(go.Scatter(
                x=_df_cons["Date"], y=_df_cons["Total Jorf"],
                mode='lines+markers', name='Total Jorf',
                line=dict(color='#00843D', width=2.5), marker=dict(size=4),
                fill='tozeroy', fillcolor='rgba(0,132,61,0.05)',
                hovertemplate='<b>%{x}</b><br>Total Jorf : %{y:.1f} KT<extra></extra>'))
            fig_cons.add_trace(go.Scatter(
                x=_df_cons["Date"], y=_df_cons["Total Safi"],
                mode='lines+markers', name='Total Safi',
                line=dict(color='#1565C0', width=2.5), marker=dict(size=4),
                fill='tozeroy', fillcolor='rgba(21,101,192,0.05)',
                hovertemplate='<b>%{x}</b><br>Total Safi : %{y:.1f} KT<extra></extra>'))
            fig_cons.add_trace(go.Scatter(
                x=_df_cons["Date"], y=_df_cons["Cumul Total"],
                mode='lines', name='Cumul Total (Jorf + Safi)',
                line=dict(color='#C05A00', width=3),
                hovertemplate='<b>%{x}</b><br>Cumul Total : %{y:.1f} KT<extra></extra>'))
            _rade_non_null = _df_cons[_df_cons["Rade Jorf"].notna()]
            if not _rade_non_null.empty:
                fig_cons.add_trace(go.Scatter(
                    x=_rade_non_null["Date"], y=_rade_non_null["Rade Jorf"],
                    mode='lines+markers', name='Rade Jorf',
                    line=dict(color='#6B3FA0', width=2, dash='dot'),
                    marker=dict(size=4, symbol='diamond'),
                    yaxis='y2',
                    hovertemplate='<b>%{x}</b><br>Rade Jorf : %{y:.1f} KT<extra></extra>'))
            fig_cons.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(242,244,247,0.6)',
                font=dict(family='Barlow,sans-serif', color='#4A5568'),
                margin=dict(l=12, r=12, t=60, b=12),
                height=460,
                title=dict(text='Vue Consolidée — Total Jorf · Total Safi · Cumul · Rade (KT/jour)', font=dict(size=13, color='#12202E')),
                xaxis=dict(gridcolor='#E0E4EA', linecolor='#E0E4EA', tickfont=dict(color='#4A5568', size=11)),
                yaxis=dict(title='KT/jour', gridcolor='#E0E4EA', linecolor='#E0E4EA', tickfont=dict(color='#4A5568', size=11)),
                yaxis2=dict(
                    title=dict(text='Rade Jorf (KT)', font=dict(color='#6B3FA0')),
                    overlaying='y', side='right', showgrid=False,
                    tickfont=dict(color='#6B3FA0', size=11)),
                legend=dict(bgcolor='rgba(255,255,255,.9)', bordercolor='#E0E4EA', borderwidth=1,
                            font=dict(color='#12202E', size=11), orientation='h',
                            yanchor='bottom', y=1.02, xanchor='left', x=0))
            st.plotly_chart(fig_cons, use_container_width=True)

        with _tab_bar:
            fig_bar_cons = go.Figure()
            fig_bar_cons.add_trace(go.Bar(
                x=_df_cons["Date"], y=_df_cons["Total Jorf"],
                name='Total Jorf', marker=dict(color='#00843D', opacity=.85),
                hovertemplate='<b>%{x}</b><br>Total Jorf : %{y:.1f} KT<extra></extra>'))
            fig_bar_cons.add_trace(go.Bar(
                x=_df_cons["Date"], y=_df_cons["Total Safi"],
                name='Total Safi', marker=dict(color='#1565C0', opacity=.85),
                hovertemplate='<b>%{x}</b><br>Total Safi : %{y:.1f} KT<extra></extra>'))
            _rade_non_null = _df_cons[_df_cons["Rade Jorf"].notna()]
            if not _rade_non_null.empty:
                fig_bar_cons.add_trace(go.Scatter(
                    x=_rade_non_null["Date"], y=_rade_non_null["Rade Jorf"],
                    mode='lines', name='Rade Jorf',
                    line=dict(color='#6B3FA0', width=2, dash='dot'),
                    yaxis='y2',
                    hovertemplate='<b>%{x}</b><br>Rade Jorf : %{y:.1f} KT<extra></extra>'))
            fig_bar_cons.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(242,244,247,0.6)',
                font=dict(family='Barlow,sans-serif', color='#4A5568'),
                margin=dict(l=12, r=12, t=60, b=12),
                height=460,
                barmode='group',
                title=dict(text='Histogramme Consolidé — Jorf vs Safi (KT/jour)', font=dict(size=13, color='#12202E')),
                xaxis=dict(gridcolor='#E0E4EA', linecolor='#E0E4EA', tickfont=dict(color='#4A5568', size=11)),
                yaxis=dict(gridcolor='#E0E4EA', linecolor='#E0E4EA', tickfont=dict(color='#4A5568', size=11)),
                yaxis2=dict(
                    title=dict(text='Rade Jorf (KT)', font=dict(color='#6B3FA0')),
                    overlaying='y', side='right', showgrid=False,
                    tickfont=dict(color='#6B3FA0', size=11)),
                legend=dict(bgcolor='rgba(255,255,255,.9)', bordercolor='#E0E4EA', borderwidth=1,
                            font=dict(color='#12202E', size=11), orientation='h',
                            yanchor='bottom', y=1.02, xanchor='left', x=0))
            st.plotly_chart(fig_bar_cons, use_container_width=True)

    else:
        st.markdown(
            '<div style="background:#F2F4F7;border:1px dashed #E0E4EA;border-radius:10px;'
            'padding:24px;text-align:center;color:#94A3B8;font-size:13px">'
            'Chargez les fichiers Jorf et/ou Safi pour afficher la vue consolidée.</div>',
            unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# PAGE SIMULATION STOCK
# ══════════════════════════════════════════════════════════════════════════════
elif page=="stock":
    def sim_stock(si,cj,navires,retards,cr=None):
        navires=sorted(navires,key=lambda x:x[0]); t=pd.Timestamp.today(); debut=pd.Timestamp(t.year,t.month,1)
        cal=pd.date_range(start=debut,end=debut+pd.DateOffset(days=60),freq='D')
        stock=si; sv=[]; dates=[]; na=[]; nq=[]
        for j in cal:
            for (dp,qty) in navires:
                de=dp+pd.Timedelta(days=retards.get(dp,0))
                if j==de: stock+=qty; na.append(j); nq.append(qty)
            c=cr.get(j.date(),cj) if cr else cj
            stock-=c; sv.append(stock); dates.append(j)
        return dates,sv,na,nq
    def show_sim(dates,sv,na,nq,titre,seuil=36000):
        fig=go.Figure()
        fig.add_hrect(y0=0,y1=seuil,fillcolor="rgba(198,40,40,0.05)",line_width=0)
        fig.add_trace(go.Scatter(x=dates,y=sv,mode='lines',name='Stock',line=dict(color='#00843D',width=2.5),fill='tozeroy',fillcolor='rgba(0,132,61,0.07)',hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Stock : %{y:,.0f} T<extra></extra>'))
        fig.add_trace(go.Scatter(x=dates,y=[seuil]*len(dates),mode='lines',name=f'Seuil ({seuil:,} T)',line=dict(dash='dash',color='#C62828',width=1.5)))
        for i,d in enumerate(na):
            idx=dates.index(d)
            fig.add_trace(go.Scatter(x=[d],y=[sv[idx]],mode='markers+text',name=f'Navire {i+1}',marker=dict(symbol='triangle-up',color='#1565C0',size=13,line=dict(color='white',width=1.5)),text=[f"+{nq[i]:,} T"],textposition='top center',textfont=dict(size=11,color='#1565C0'),showlegend=True))
        lyt=dict(**PL); lyt['height']=400; lyt['title']=dict(text=titre,font=dict(size=14,color='#12202E'))
        fig.update_layout(**lyt); st.plotly_chart(fig,use_container_width=True)
        m1,m2,m3=st.columns(3)
        mn=min(sv); mn_d=dates[sv.index(mn)]; jc=sum(1 for v in sv if v<seuil)
        m1.metric("Stock minimum",f"{mn:,.0f} T",f"le {mn_d.strftime('%d/%m/%Y')}")
        m2.metric("Stock final",f"{sv[-1]:,.0f} T")
        m3.metric("Jours critiques",f"{jc} j",delta="Risque" if jc>0 else "OK")
    tab_sa,tab_jo=st.tabs(["Site de Safi","Site de Jorf"])
    with tab_sa:
        ms=st.selectbox("Matière première",["Soufre"],key="ss_mat"); ps=f"ss_{ms.lower()}"
        c1,c2=st.columns(2)
        with c1: si_s=st.number_input("Stock initial (T)",key=f"{ps}_si",min_value=0,value=40000,step=1000)
        with c2: cj_s=st.number_input("Conso journalière (T)",key=f"{ps}_cj",min_value=0,value=3600,step=100)
        ucr=st.checkbox("Consommations réelles par jour ?",key=f"{ps}_ucr"); cr={}
        if ucr:
            dm=pd.Timestamp.today().replace(day=1); jours=pd.date_range(dm,dm+pd.offsets.MonthEnd(1),freq='D'); cols=st.columns(4)
            for i,j in enumerate(jours):
                with cols[i%4]: cr[j.date()]=st.number_input(j.strftime('%d/%m'),min_value=0,value=int(cj_s),step=100,key=f"{ps}_cr{j.strftime('%Y%m%d')}")
        st.markdown('<div class="stitle blue">Navires prévus</div>',unsafe_allow_html=True)
        nav,ret=[],{}; nn=st.number_input("Nombre de navires",key=f"{ps}_n",min_value=0,value=3)
        for i in range(int(nn)):
            cd,cq,cr2=st.columns(3)
            with cd: da=st.date_input(f"Date navire {i+1}",pd.Timestamp.today(),key=f"{ps}_d{i}")
            with cq: qty=st.number_input(f"Quantité {i+1} (T)",0,500000,30000,1000,key=f"{ps}_q{i}")
            with cr2: r=st.number_input(f"Retard (j) {i+1}",0,30,0,1,key=f"{ps}_r{i}")
            nav.append((pd.Timestamp(da),qty))
            if r>0: ret[pd.Timestamp(da)]=r
        if st.button(f"Lancer la simulation — Safi / {ms}",key=f"{ps}_btn",type="primary"):
            d,sv,na,nq=sim_stock(si_s,cj_s,nav,ret,cr if ucr else None); show_sim(d,sv,na,nq,f"Stock — Safi / {ms}")
    with tab_jo:
        mj=st.selectbox("Matière première",["Soufre","NH3","KCL","ACS"],key="sj_mat"); pj=f"sj_{mj.lower()}"
        if mj=="ACS":
            st.markdown('<div class="stitle">Paramètres ACS</div>',unsafe_allow_html=True)
            c1,c2,c3,c4=st.columns(4)
            with c1: ce=st.number_input("Conso engrais (T)",key=f"{pj}_ce",min_value=0,value=12000)
            with c2: si_a=st.number_input("Stock initial (T)",key=f"{pj}_si",min_value=0,value=300000)
            with c3: rv2=st.number_input("Rade (T)",key=f"{pj}_rv",min_value=0,value=60000)
            with c4: dc=st.number_input("Déchargement (T)",key=f"{pj}_dc",min_value=0,value=300000)
            dm=pd.Timestamp.today().replace(day=1); cal=pd.date_range(start=dm,end=dm+pd.DateOffset(days=60),freq='D')
            pjj={d.normalize():0 for d in cal}
            def rl(lignes,pfx,cad_def):
                tot=0
                for i,t in enumerate(st.tabs([f"{l}" for l in lignes])):
                    with t:
                        la=lignes[i]; jar_str=st.text_input(f"Arrêts (ex: 1-3,15)",key=f"{pfx}_{la}_a"); jar=[]
                        if jar_str:
                            for pt in jar_str.split(","):
                                pt=pt.strip()
                                if "-" in pt: a_,b_=pt.split("-"); jar.extend(range(int(a_),int(b_)+1))
                                else: jar.append(int(pt))
                            jar=sorted(set(jar))
                        nb=st.number_input("Périodes",min_value=1,value=1,key=f"{pfx}_{la}_nb"); pl=0
                        for p2 in range(int(nb)):
                            ca,cb,cc=st.columns(3)
                            with ca: dd=st.date_input(f"Début {p2+1}",dm,key=f"{pfx}_{la}_dd{p2}")
                            with cb: df2=st.date_input(f"Fin {p2+1}",dm+pd.Timedelta(days=5),key=f"{pfx}_{la}_df{p2}")
                            with cc: cad=st.number_input(f"Cadence T/j",min_value=0,value=cad_def,key=f"{pfx}_{la}_cd{p2}")
                            for d in pd.date_range(pd.Timestamp(dd),pd.Timestamp(df2),freq='D'):
                                if d.day not in jar: pjj[d.normalize()]=pjj.get(d.normalize(),0)+cad; pl+=cad
                        tot+=pl; st.info(f"**{la}** : {pl:,.0f} T")
                return tot
            st.markdown('<div class="stitle">Lignes ACS</div>',unsafe_allow_html=True)
            la_acs=["01A","01B","01C","01X","01Y","01Z","101D","101E","101U","JFC1","JFC2","JFC3","JFC4","JFC5","IMACID","PMP"]
            pa=rl(la_acs,f"{pj}_a",2600)
            st.markdown('<div class="stitle blue">Lignes ACP29</div>',unsafe_allow_html=True)
            la_acp=["JFC1_ACP29","JFC2_ACP29","JFC3_ACP29","JFC4_ACP29","JFC5_ACP29","JLN_03AB","JLN_03CD","JLN_03XY","JLN_03ZU","JLN_03E","JLN_03F","PMP_ACP29","IMACID_ACP29"]
            pp=rl(la_acp,f"{pj}_p",1000)
            st.markdown('<div class="stitle orange">Résultats</div>',unsafe_allow_html=True)
            c29=3.14*pp; sf2=si_a+dc+rv2+pa-c29-ce
            r1,r2,r3,r4=st.columns(4)
            r1.metric("Production ACS",f"{pa:,.0f} T"); r2.metric("Production ACP29",f"{pp:,.0f} T")
            r3.metric("Conso ACP29 (x3.14)",f"{c29:,.0f} T"); r4.metric("Stock final",f"{sf2:,.0f} T",delta="Excédent" if sf2>0 else "Déficit")
            nb2=len(cal); pjr=pa/nb2 if nb2>0 else 0; cjr=(c29+ce)/nb2 if nb2>0 else 0
            stk2=si_a; svacs=[]
            for i_d,d in enumerate(cal):
                if i_d==0: stk2+=rv2+dc
                stk2+=pjr; stk2-=cjr; svacs.append(stk2)
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=cal,y=svacs,mode='lines',name='Stock ACS',line=dict(color='#00843D',width=2.5),fill='tozeroy',fillcolor='rgba(0,132,61,0.07)'))
            fig.add_trace(go.Scatter(x=cal,y=[0]*len(cal),mode='lines',name='Zéro',line=dict(dash='dash',color='#C62828',width=1.5)))
            lyt2=dict(**PL); lyt2['height']=380; lyt2['title']=dict(text="Évolution stock ACS",font=dict(size=13,color='#12202E'))
            fig.update_layout(**lyt2); st.plotly_chart(fig,use_container_width=True)
        else:
            SEUILS={"Soufre":36000,"NH3":5000,"KCL":10000}; seuil=SEUILS.get(mj,36000)
            c1,c2=st.columns(2)
            with c1: si_j=st.number_input("Stock initial (T)",key=f"{pj}_si",min_value=0,value=100000,step=1000)
            with c2: cj_j=st.number_input("Conso journalière (T)",key=f"{pj}_cj",min_value=0,value=17500,step=100)
            ucr2=st.checkbox("Consommations réelles ?",key=f"{pj}_ucr"); cr2={}
            if ucr2:
                dm=pd.Timestamp.today().replace(day=1); jours=pd.date_range(dm,dm+pd.offsets.MonthEnd(1),freq='D'); cols=st.columns(4)
                for i,j in enumerate(jours):
                    with cols[i%4]: cr2[j.date()]=st.number_input(j.strftime('%d/%m'),min_value=0,value=int(cj_j),step=100,key=f"{pj}_cr{j.strftime('%Y%m%d')}")
            st.markdown('<div class="stitle blue">Navires prévus</div>',unsafe_allow_html=True)
            nav2,ret2=[],{}; nn2=st.number_input(f"Navires ({mj})",key=f"{pj}_n",min_value=0,value=3)
            for i in range(int(nn2)):
                cd,cq,cr3=st.columns(3)
                with cd: da=st.date_input(f"Date {i+1}",pd.Timestamp.today(),key=f"{pj}_d{i}")
                with cq: qty=st.number_input(f"Qté {i+1} (T)",0,500000,30000,1000,key=f"{pj}_q{i}")
                with cr3: r=st.number_input(f"Retard {i+1}j",0,30,0,1,key=f"{pj}_r{i}")
                nav2.append((pd.Timestamp(da),qty))
                if r>0: ret2[pd.Timestamp(da)]=r
            if st.button(f"Lancer la simulation — Jorf / {mj}",key=f"{pj}_btn",type="primary"):
                d,sv,na,nq=sim_stock(si_j,cj_j,nav2,ret2,cr2 if ucr2 else None); show_sim(d,sv,na,nq,f"Stock — Jorf / {mj}",seuil=seuil)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE PIPELINE DES VENTES
# ══════════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
# PATCH — PAGE PIPELINE DES VENTES
# Remplace le bloc "elif page=='ventes':" dans ton app.py
#
# NOUVEAUTÉS :
#   1. 🔍 Barre de recherche par mots-clés (multicol)
#   2. 🌍 Filtre Région
#   3. ⚙️  Sélecteur de périmètre : l'utilisateur choisit quels filtres afficher
# ══════════════════════════════════════════════════════════════════════════════

elif page == "ventes":
    if "ventes_df" not in st.session_state:
        st.session_state["ventes_df"] = None
    if "ventes_map" not in st.session_state:
        st.session_state["ventes_map"] = {}

    # ── Clé de persistance du périmètre choisi ──
    if "ventes_perimetre" not in st.session_state:
        st.session_state["ventes_perimetre"] = [
            "mois", "confirmation", "site", "pays", "produit", "region", "statut", "recherche"
        ]

    st.markdown('<div class="stitle">Pipeline des Ventes — Pilotage par Décades</div>', unsafe_allow_html=True)
    vn = st.session_state.get("ventes_name", "")
    _actif_html = f'<br><b style="color:#00843D">✓ Fichier actif : {vn}</b>' if vn else ""
    st.markdown(
        f'<div class="upload-zone"><div class="zone-title">Charger le fichier Pipeline</div>'
        f'<div class="zone-desc">Fichier Excel : BL Month, Physical Month, Working Month, Delivery Month, '
        f'Confirmation, Pays, Produit, D1, D2, D3, Status Planif, Loading Port, Région{_actif_html}</div>',
        unsafe_allow_html=True)
    file_v = st.file_uploader("Pipeline Excel", type=EXCEL_T, key="v_upload", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if file_v:
        try:
            raw_v, eng_v = read_bytes(file_v)
            xl = pd.ExcelFile(io.BytesIO(raw_v), engine=eng_v)
            target = xl.sheet_names[0]
            for sn in xl.sheet_names:
                if any(k in sn.lower() for k in ["january", "pipeline", "ventes", "janvier", "data"]):
                    target = sn
                    break
            df_full = pd.read_excel(io.BytesIO(raw_v), sheet_name=target, engine=eng_v)
            df_full.columns = [str(c).strip() for c in df_full.columns]
            df_full = df_full.dropna(how='all')
            detected_map = _ventes_auto_map(df_full)
            st.session_state.update({"ventes_df": df_full, "ventes_map": detected_map, "ventes_name": file_v.name})
            save_cache(VENTES_CACHE, {"ventes_df": df_full, "ventes_map": detected_map, "filename": file_v.name})
            file_v.seek(0)
            add_hist(HIST_VENTES, file_v.name, file_v.read(), "ventes")
            st.session_state["llm_statut_input_key"] = ""
            st.success(f"Fichier importé — feuille « {target} » — {len(df_full)} lignes")
        except Exception as e:
            st.error(f"Erreur : {e}")

    df_raw = st.session_state.get("ventes_df")
    vmap = st.session_state.get("ventes_map", {})

    if df_raw is None:
        st.info("Chargez un fichier Excel Pipeline pour commencer.")
        if st.button("Effacer le cache Pipeline", key="clear_ventes_cache"):
            clear_cache(VENTES_CACHE)
            st.session_state.update({"ventes_df": None, "ventes_map": {}, "ventes_name": ""})
            st.rerun()
        st.stop()

    # ── Mapping des colonnes ──
    with st.expander("Vérifier / Ajuster le mapping des colonnes"):
        ROLES = {
            "bl_month":       "BL Month",
            "phys_month":     "Physical Month",
            "work_month":     "Working Month",
            "del_month":      "Delivery Month",
            "site":           "Site",
            "status":         "Status Planif",
            "confirmation":   "Confirmation",
            "pays":           "Pays",
            "produit":        "Produit",
            "macro_qualite":  "Macro Qualité",
            "d1":             "D1",
            "d2":             "D2",
            "d3":             "D3",
            "loading_port":   "Loading Port",
            "region":         "Region",
            "navire":         "Navire",
        }
        new_map = {}
        opts = ["(non mappé)"] + df_raw.columns.tolist()
        cols_map = st.columns(4)
        for i, (rk, rl) in enumerate(ROLES.items()):
            cur = vmap.get(rk)
            idx = opts.index(cur) if cur in opts else 0
            sel = cols_map[i % 4].selectbox(rl, opts, index=idx, key=f"vm_{rk}")
            new_map[rk] = sel if sel != "(non mappé)" else None
        if st.button("Enregistrer le mapping", type="primary"):
            st.session_state["ventes_map"] = new_map
            save_cache(VENTES_CACHE, {"ventes_df": df_raw, "ventes_map": new_map,
                                       "filename": st.session_state.get("ventes_name", "")})
            vmap = new_map
            st.rerun()

    with st.expander("Changer / Effacer le fichier Pipeline"):
        if st.button("Effacer le fichier Pipeline actuel", key="clear_ventes", type="secondary"):
            clear_cache(VENTES_CACHE)
            st.session_state.update({"ventes_df": None, "ventes_map": {}, "ventes_name": ""})
            st.rerun()

    # ══════════════════════════════════════════════════════
    # ⚙️  SÉLECTEUR DE PÉRIMÈTRE DE FILTRES
    # L'utilisateur choisit quels filtres sont visibles
    # ══════════════════════════════════════════════════════
    FILTRE_OPTIONS = {
        "mois":         "📅 Filtres Mois (BL / Physical / Working / Delivery)",
        "confirmation": "✅ Confirmation (CONF / Res.CAPA)",
        "site":         "🏭 Site / Port de chargement",
        "pays":         "🌍 Pays",
        "produit":      "📦 Produit",
        "region":       "🗺️  Région",
        "statut":       "🏷️  Status Planif (IA)",       
    }

    with st.expander("⚙️  Périmètre des filtres — choisissez quels filtres afficher", expanded=False):
        st.markdown(
            '<div style="font-size:11px;color:#4A5568;margin-bottom:10px">'
            'Cochez uniquement les dimensions sur lesquelles vous souhaitez filtrer. '
            'Les filtres non sélectionnés seront masqués pour simplifier l\'interface.'
            '</div>', unsafe_allow_html=True)
        perim_cols = st.columns(2)
        new_perim = []
        for i, (key, label) in enumerate(FILTRE_OPTIONS.items()):
            checked = key in st.session_state["ventes_perimetre"]
            if perim_cols[i % 2].checkbox(label, value=checked, key=f"perim_{key}"):
                new_perim.append(key)
        if st.button("Appliquer le périmètre", type="primary", key="apply_perim"):
            st.session_state["ventes_perimetre"] = new_perim
            st.rerun()

    perim = st.session_state["ventes_perimetre"]

    # ══════════════════════════════════════════════════════
    # PANEL FILTRES — uniquement les dimensions activées
    # ══════════════════════════════════════════════════════
    st.markdown('<div class="filter-panel"><div class="filter-panel-title">Filtres</div>', unsafe_allow_html=True)

    MOIS_FR = ["Tous", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
               "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    MOIS_EN = ["All", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

    c_stat_col = vmap.get("status")
    c_region_col = vmap.get("region")

    # ── Ligne mois (si périmètre activé) ──
    sel_m_bl = sel_m_phys = sel_m_work = sel_m_del = "Tous"
    if "mois" in perim:
        frow0 = st.columns(4)
        sel_m_bl   = frow0[0].selectbox("BL Month",       MOIS_FR, key="v_mois_bl")
        sel_m_phys = frow0[1].selectbox("Physical Month", MOIS_FR, key="v_mois_phys")
        sel_m_work = frow0[2].selectbox("Working Month",  MOIS_FR, key="v_mois_work")
        sel_m_del  = frow0[3].selectbox("Delivery Month", MOIS_FR, key="v_mois_del")

    # Pré-filtrage mois pour peupler les listes des autres filtres dynamiquement
    df_prefilt = df_raw.copy()
    for sel_mx, role_key in [(sel_m_bl, "bl_month"), (sel_m_phys, "phys_month"),
                              (sel_m_work, "work_month"), (sel_m_del, "del_month")]:
        if sel_mx != "Tous":
            col_mx = vmap.get(role_key)
            if col_mx and col_mx in df_prefilt.columns:
                mois_en_x = MOIS_EN[MOIS_FR.index(sel_mx)]
                df_prefilt = df_prefilt[
                    df_prefilt[col_mx].astype(str).str.contains(f"{sel_mx}|{mois_en_x}", case=False, na=False)
                ]

    # ── Ligne 2 : Site, Confirmation, Pays, Produit ──
    _active_row2 = [k for k in ["site", "confirmation", "pays", "produit"] if k in perim]
    sel_s = sel_co = sel_pays = sel_prod = "Tous"

    if _active_row2:
        frow1 = st.columns(len(_active_row2))
        col_idx = 0

        if "site" in perim:
            _col_site_dyn = (
                vmap.get("loading_port") if vmap.get("loading_port") and vmap.get("loading_port") in df_prefilt.columns
                else vmap.get("site") if vmap.get("site") and vmap.get("site") in df_prefilt.columns else None
            )
            if _col_site_dyn:
                sites_dyn = sorted(df_prefilt[_col_site_dyn].dropna().astype(str).apply(_normalize_site).unique())
                sel_s = frow1[col_idx].selectbox("Site / Port", ["Tous"] + sites_dyn, key="v_site")
            else:
                sel_s = frow1[col_idx].selectbox("Site / Port", ["Tous"], key="v_site")
            col_idx += 1

        if "confirmation" in perim:
            sel_co = frow1[col_idx].selectbox("Confirmation", ["Tous", "CONF", "Res.CAPA"], key="v_conf")
            col_idx += 1

        if "pays" in perim:
            sel_pays_opts = (
                ["Tous"] + sorted(df_prefilt[vmap["pays"]].dropna().astype(str).str.strip().unique().tolist())
            ) if vmap.get("pays") and vmap["pays"] in df_prefilt.columns else ["Tous"]
            sel_pays = frow1[col_idx].selectbox("Pays", sel_pays_opts, key="v_pays")
            col_idx += 1

        if "produit" in perim:
            sel_prod_opts = (
                ["Tous"] + sorted(df_prefilt[vmap["produit"]].dropna().astype(str).str.strip().unique().tolist())
            ) if vmap.get("produit") and vmap["produit"] in df_prefilt.columns else ["Tous"]
            sel_prod = frow1[col_idx].selectbox("Produit", sel_prod_opts, key="v_produit")

    # ── Région (si périmètre activé) ──
    sel_region = "Tous"
    if "region" in perim and c_region_col and c_region_col in df_prefilt.columns:
        regions_dyn = sorted(df_prefilt[c_region_col].dropna().astype(str).str.strip().unique().tolist())
        if regions_dyn:
            sel_region = st.selectbox(
                "🗺️  Région",
                ["Tous"] + regions_dyn,
                key="v_region"
            )
        else:
            st.caption("Aucune région disponible pour les filtres sélectionnés.")
    elif "region" in perim and not c_region_col:
        st.caption("⚠️ Colonne Région non mappée — allez dans « Vérifier le mapping ».")

    # ── Statuts IA ──
    if "statut" in perim and c_stat_col and c_stat_col in df_prefilt.columns:
        build_num_map(df_prefilt[c_stat_col])
        statuts_norm = sorted(
            set(normalize_statut(s) for s in df_prefilt[c_stat_col].dropna().unique()),
            key=_sort_key_statut_global
        )
    else:
        statuts_norm = []

    llm_map = st.session_state.get("llm_statut_map", {})
    regroupes = {k: v for k, v in llm_map.items() if _deaccent(v) != k}
    if "statut" in perim and llm_map:
        if regroupes:
            details = " | ".join(f"{v}" for v in sorted(set(llm_map.values()))[:6])
            st.markdown(
                f'<div class="llm-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" '
                f'stroke="currentColor" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 '
                f'10-5M2 12l10 5 10-5"/></svg>IA — {len(regroupes)} regroupement(s) • Groupes : {details}</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="llm-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" '
                f'stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>'
                f'IA — {len(llm_map)} statut(s) analysé(s), aucun regroupement nécessaire</div>',
                unsafe_allow_html=True)

    sel_statuts = []
    if "statut" in perim and statuts_norm:
        sel_statuts = st.multiselect("Status Planif", options=statuts_norm, default=[], key="v_statuts")
    elif "statut" in perim and c_stat_col:
        st.caption("Aucun statut disponible pour les filtres sélectionnés.")

    if "statut" in perim and llm_map:
        with st.expander("Voir le mapping IA complet"):
            if c_stat_col and c_stat_col in df_raw.columns:
                bruts = sorted(df_raw[c_stat_col].dropna().astype(str).str.strip().unique())
                rows_html = "".join(
                    f'<div style="display:flex;justify-content:space-between;padding:4px 0;'
                    f'border-bottom:1px solid #F2F4F7;font-size:11px;">'
                    f'<span style="color:#4A5568">{b}</span>'
                    f'<span style="font-weight:700;color:{"#6B3FA0" if normalize_statut(b) != _strip_num(b) else "#94A3B8"}">'
                    f'→ {normalize_statut(b)}</span></div>'
                    for b in bruts
                )
                st.markdown(f'<div style="max-height:220px;overflow-y:auto">{rows_html}</div>', unsafe_allow_html=True)
            if st.button("Réanalyser avec l'IA", key="reanalyze_llm", type="secondary"):
                st.session_state["llm_statut_input_key"] = ""
                st.rerun()


    # ══════════════════════════════════════════════════════
    # APPLICATION DE TOUS LES FILTRES
    # ══════════════════════════════════════════════════════
    df_f = df_raw.copy()

    # Filtres mois
    for sel_mx, role_key in [(sel_m_bl, "bl_month"), (sel_m_phys, "phys_month"),
                              (sel_m_work, "work_month"), (sel_m_del, "del_month")]:
        if sel_mx != "Tous":
            col_mx = vmap.get(role_key)
            if col_mx and col_mx in df_f.columns:
                mois_en_x = MOIS_EN[MOIS_FR.index(sel_mx)]
                df_f = df_f[df_f[col_mx].astype(str).str.contains(f"{sel_mx}|{mois_en_x}", case=False, na=False)]

    # Site
    _col_site_filtre = (
        vmap.get("loading_port") if vmap.get("loading_port") and vmap.get("loading_port") in df_f.columns
        else vmap.get("site") if vmap.get("site") and vmap.get("site") in df_f.columns else None
    )
    if sel_s != "Tous" and _col_site_filtre:
        df_f = df_f[df_f[_col_site_filtre].astype(str).apply(_normalize_site) == sel_s]

    # Confirmation
    if sel_co != "Tous" and vmap.get("confirmation") and vmap["confirmation"] in df_f.columns:
        df_f = df_f[df_f[vmap["confirmation"]].astype(str).str.strip() == sel_co]

    # Pays
    if sel_pays != "Tous" and vmap.get("pays") and vmap["pays"] in df_f.columns:
        df_f = df_f[df_f[vmap["pays"]].astype(str).str.strip().str.lower() == sel_pays.strip().lower()]

    # Produit
    if sel_prod != "Tous" and vmap.get("produit") and vmap["produit"] in df_f.columns:
        df_f = df_f[df_f[vmap["produit"]].astype(str).str.strip() == sel_prod]

    # ── Région ──
    if sel_region != "Tous" and c_region_col and c_region_col in df_f.columns:
        df_f = df_f[df_f[c_region_col].astype(str).str.strip() == sel_region]

    # Statuts IA
    if sel_statuts and c_stat_col and c_stat_col in df_f.columns:
        df_f = df_f[df_f[c_stat_col].apply(lambda x: normalize_statut(x) in sel_statuts)]

# ── Barre de recherche + colonnes à fouiller ──
    src_col1, src_col2 = st.columns([3, 2])
    with src_col1:
        search_query = st.text_input(
            "🔍 Recherche par mots-clés",
            value="",
            placeholder="Ex: India, TSP, CONF, Chargé...",
            key="v_search"
        )
    with src_col2:
        search_cols_sel = st.multiselect(
            "Colonnes à fouiller",
            options=list(df_f.columns),
            default=[],
            key="v_search_cols",
            placeholder="Toutes les colonnes"
        )

    # ── Appliquer la recherche sur une COPIE ──
    df_display = df_f.copy()

    if search_query.strip():
        cols_to_search = search_cols_sel if search_cols_sel else list(df_display.columns)
        mask = pd.Series(False, index=df_display.index)
        for col in cols_to_search:
            mask |= df_display[col].astype(str).str.contains(
                search_query.strip(), case=False, na=False, regex=False
            )
        df_display = df_display[mask]
        st.markdown(
            f'<div style="background:#E8F5EE;border:1px solid rgba(0,132,61,.2);'
            f'border-radius:6px;padding:6px 14px;font-size:11px;color:#005C2A;margin-bottom:8px">'
            f'🔍 <b>{len(df_display)}</b> résultat(s) pour "<b>{search_query}</b>"'
            f'</div>',
            unsafe_allow_html=True
        )
    # ── Totaux décades ──
    v_d1 = vmap.get("d1")
    v_d2 = vmap.get("d2")
    v_d3 = vmap.get("d3")
    val_d1 = pd.to_numeric(df_f[v_d1], errors='coerce').fillna(0).sum() if v_d1 and v_d1 in df_f.columns else 0
    val_d2 = pd.to_numeric(df_f[v_d2], errors='coerce').fillna(0).sum() if v_d2 and v_d2 in df_f.columns else 0
    val_d3 = pd.to_numeric(df_f[v_d3], errors='coerce').fillna(0).sum() if v_d3 and v_d3 in df_f.columns else 0
    total_m = val_d1 + val_d2 + val_d3

    mois_labels = []
    for sel_mx, lbl_mx in [(sel_m_bl, "BL"), (sel_m_phys, "Phys"),
                            (sel_m_work, "Work"), (sel_m_del, "Del")]:
        if sel_mx != "Tous":
            mois_labels.append(f"{lbl_mx}: {sel_mx}")
    filtre_label = " • ".join(mois_labels) if mois_labels else "TOUS MOIS"

    # Bandeau total
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#12202E,#1E3A5F);color:white;padding:12px 22px;'
        f'border-radius:8px;margin:0 0 14px 0;display:flex;justify-content:space-between;align-items:center">'
        f'<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:14px;font-weight:700;'
        f'letter-spacing:.5px;opacity:.85">TOTAL PIPELINE — {filtre_label} '
        f'{"• 🗺️ " + sel_region if sel_region != "Tous" else ""}</span>'
        f'<div style="display:flex;gap:20px;align-items:center">'
        f'<div style="text-align:center"><div style="font-size:9px;opacity:.6;text-transform:uppercase">D1</div>'
        f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:20px;font-weight:800;color:#64B5F6">'
        f'{_ventes_fmt_kt(val_d1)} KT</div></div>'
        f'<div style="text-align:center"><div style="font-size:9px;opacity:.6;text-transform:uppercase">D2</div>'
        f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:20px;font-weight:800;color:#FFB74D">'
        f'{_ventes_fmt_kt(val_d2)} KT</div></div>'
        f'<div style="text-align:center"><div style="font-size:9px;opacity:.6;text-transform:uppercase">D3</div>'
        f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:20px;font-weight:800;color:#81C784">'
        f'{_ventes_fmt_kt(val_d3)} KT</div></div>'
        f'<div style="border-left:1px solid rgba(255,255,255,.25);padding-left:18px">'
        f'<div style="font-size:9px;opacity:.6;text-transform:uppercase">TOTAL</div>'
        f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:26px;font-weight:900">'
        f'{_ventes_fmt_kt(total_m)} KT</div></div></div></div>',
        unsafe_allow_html=True)

    # ── Cartes D1 / D2 / D3 ──
    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        _build_card_interactive("D1 — Jours 1–10",  val_d1, v_d1, "#1565C0", "#1565C0", df_f, vmap)
    with dc2:
        _build_card_interactive("D2 — Jours 11–20", val_d2, v_d2, "#C05A00", "#C05A00", df_f, vmap)
    with dc3:
        _build_card_interactive("D3 — Jours 21+",   val_d3, v_d3, "#00843D", "#00843D", df_f, vmap)
     # ── Tableau complet — toutes colonnes ──
    st.markdown('<div class="stitle">Tableau complet — toutes colonnes</div>', unsafe_allow_html=True)

    role_order = ["bl_month","phys_month","work_month","del_month","confirmation",
                  "pays","macro_qualite","produit","d1","d2","d3","status","loading_port","site"]
    cols_display = []
    seen = set()
    for rk in role_order:
        c = vmap.get(rk)
        if c and c in df_display.columns and c not in seen:
            cols_display.append(c); seen.add(c)
    for c in df_display.columns:
        if c not in seen:
            cols_display.append(c); seen.add(c)
    if not cols_display:
        cols_display = list(df_display.columns)

    df_disp = df_display[cols_display].copy()
    cfg_cols = {}
    for rk in ["d1", "d2", "d3"]:
        c = vmap.get(rk)
        if c and c in df_disp.columns:
            cfg_cols[c] = st.column_config.NumberColumn(c, format="%.1f")

    if df_disp.empty:
        st.warning("⚠️ Aucune ligne ne correspond aux filtres appliqués.")
    else:
        st.dataframe(
            df_disp,
            use_container_width=True,
            hide_index=True,
            height=min(700, 48 + 35 * len(df_disp)),
            column_config=cfg_cols if cfg_cols else None
        )
        st.caption(f"{len(df_disp)} ligne(s) affichée(s) sur {len(df_raw)} total")
    st.markdown("---")
    st.markdown('<div class="stitle purple">Générer un Rapport Automatique</div>',unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">',unsafe_allow_html=True)
        rc1,rc2,rc3=st.columns([2,1,1])
        with rc1: mois_rapport=st.selectbox("Mois du rapport",MOIS_FR[1:],key="rpt_mois")
        with rc2:
            col_mois_opts=[c for c in [vmap.get("bl_month"),vmap.get("del_month"),vmap.get("work_month"),vmap.get("phys_month")] if c and c in df_raw.columns]
            col_mois_rpt=st.selectbox("Colonne mois de référence",col_mois_opts if col_mois_opts else ["(aucune)"],key="rpt_col_mois")
        with rc3:
            st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
            gen_btn=st.button("Générer le Rapport",type="primary",key="gen_rpt",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

    if gen_btn and col_mois_rpt and col_mois_rpt!="(aucune)":
        mois_en_rpt=MOIS_EN[MOIS_FR.index(mois_rapport)]
        df_rpt=df_raw[df_raw[col_mois_rpt].astype(str).str.contains(f"{mois_rapport}|{mois_en_rpt}",case=False,na=False)].copy()
        if df_rpt.empty:
            st.warning(f"Aucune donnée pour {mois_rapport}.")
        else:
            if c_stat_col and c_stat_col in df_rpt.columns:
                build_num_map(df_rpt[c_stat_col])
                df_rpt["__statut_norm__"]=df_rpt[c_stat_col].apply(normalize_statut)
            else:
                df_rpt["__statut_norm__"]="Inconnu"
            c_port_site=vmap.get("loading_port") or vmap.get("site")
            def norm_site(s):
                val=str(s).upper().strip()
                if "JORF" in val: return "JORF"
                if "SAFI" in val: return "SAFI"
                return val
            st.markdown(f'<div style="background:linear-gradient(135deg,#00843D,#005C2A);color:white;padding:20px 28px;border-radius:12px;margin:16px 0 20px 0;box-shadow:0 4px 16px rgba(0,132,61,.25)"><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:26px;font-weight:800;letter-spacing:.5px">RAPPORT PIPELINE — {mois_rapport.upper()} {datetime.now().year}</div><div style="font-size:12px;opacity:.8;margin-top:4px">Généré le {datetime.now().strftime("%d/%m/%Y à %H:%M")} • {len(df_rpt)} lignes analysées</div></div>',unsafe_allow_html=True)
            statuts_rapport=sorted(df_rpt["__statut_norm__"].dropna().unique().tolist(),key=_sort_key_statut_global)
            for statut_norm in statuts_rapport:
                df_stat=df_rpt[df_rpt["__statut_norm__"]==statut_norm]
                if df_stat.empty: continue
                if c_stat_col and c_stat_col in df_stat.columns:
                    raw_vals=df_stat[c_stat_col].dropna().astype(str).str.strip().unique().tolist()
                    raw_vals_sorted=sorted(raw_vals,key=lambda v:(int(_re_glob.match(r"^(\d+)",v).group(1)) if _re_glob.match(r"^\d+",v) else 999,v))
                    sous_label="" if len(raw_vals_sorted)<=1 else f" <span style='font-size:11px;opacity:.7;font-weight:400'>({', '.join(raw_vals_sorted)})</span>"
                else: sous_label=""
                ts_d1=pd.to_numeric(df_stat[v_d1],errors='coerce').fillna(0).sum() if v_d1 and v_d1 in df_stat.columns else 0
                ts_d2=pd.to_numeric(df_stat[v_d2],errors='coerce').fillna(0).sum() if v_d2 and v_d2 in df_stat.columns else 0
                ts_d3=pd.to_numeric(df_stat[v_d3],errors='coerce').fillna(0).sum() if v_d3 and v_d3 in df_stat.columns else 0
                ts_tot=ts_d1+ts_d2+ts_d3
                h_color,bg_color="#12202E","#F2F4F7"
                _sn=statut_norm.lower()
                if "cours" in _sn and "charg" in _sn: h_color,bg_color="#C05A00","#FBF0E6"
                elif "laycan" in _sn: h_color,bg_color="#6B3FA0","#F0EBF8"
                elif "planif" in _sn: h_color,bg_color="#1565C0","#E3EAF8"
                elif "cfr" in _sn: h_color,bg_color="#00843D","#E8F5EE"
                elif "fob" in _sn: h_color,bg_color="#B71C1C","#FFEBEE"
                elif "charg" in _sn: h_color,bg_color="#C05A00","#FBF0E6"
                elif "rade" in _sn: h_color,bg_color="#6B3FA0","#F0EBF8"
                elif "nomm" in _sn: h_color,bg_color="#1565C0","#E3EAF8"
                st.markdown(f'<div style="background:{bg_color};border:1px solid {h_color}33;border-left:4px solid {h_color};border-radius:10px;padding:14px 18px;margin:14px 0 6px 0"><div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px"><div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:18px;font-weight:800;color:{h_color};text-transform:uppercase;letter-spacing:.5px">{statut_norm}{sous_label}</div></div><div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap"><div style="text-align:center;background:rgba(255,255,255,.6);border-radius:8px;padding:6px 12px"><div style="font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{h_color};opacity:.7">D1</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:18px;font-weight:800;color:{h_color}">{_ventes_fmt_kt(ts_d1)} KT</div></div><div style="text-align:center;background:rgba(255,255,255,.6);border-radius:8px;padding:6px 12px"><div style="font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{h_color};opacity:.7">D2</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:18px;font-weight:800;color:{h_color}">{_ventes_fmt_kt(ts_d2)} KT</div></div><div style="text-align:center;background:rgba(255,255,255,.6);border-radius:8px;padding:6px 12px"><div style="font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{h_color};opacity:.7">D3</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:18px;font-weight:800;color:{h_color}">{_ventes_fmt_kt(ts_d3)} KT</div></div><div style="text-align:center;background:{h_color};border-radius:8px;padding:6px 14px"><div style="font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,.75)">TOTAL</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:22px;font-weight:800;color:white">{_ventes_fmt_kt(ts_tot)} KT</div></div></div></div></div>',unsafe_allow_html=True)
                if c_port_site and c_port_site in df_stat.columns:
                    for port_val in sorted(df_stat[c_port_site].dropna().unique()):
                        df_port=df_stat[df_stat[c_port_site].astype(str).str.strip()==str(port_val)]
                        if df_port.empty: continue
                        p_d1=pd.to_numeric(df_port[v_d1],errors='coerce').fillna(0).sum() if v_d1 and v_d1 in df_port.columns else 0
                        p_d2=pd.to_numeric(df_port[v_d2],errors='coerce').fillna(0).sum() if v_d2 and v_d2 in df_port.columns else 0
                        p_d3=pd.to_numeric(df_port[v_d3],errors='coerce').fillna(0).sum() if v_d3 and v_d3 in df_port.columns else 0
                        p_tot=p_d1+p_d2+p_d3
                        st.markdown(f'<div style="margin:6px 0 4px 20px;padding:10px 16px;background:white;border:1px solid #E0E4EA;border-left:3px solid {h_color};border-radius:8px"><div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px"><span style="font-size:14px;font-weight:700;color:#12202E">PORT : {norm_site(port_val)}</span><div style="display:flex;gap:12px;align-items:center"><span style="font-size:11px;color:#94A3B8">D1: <b style="color:#1565C0">{_ventes_fmt_kt(p_d1)}</b></span><span style="font-size:11px;color:#94A3B8">D2: <b style="color:#C05A00">{_ventes_fmt_kt(p_d2)}</b></span><span style="font-size:11px;color:#94A3B8">D3: <b style="color:#00843D">{_ventes_fmt_kt(p_d3)}</b></span><span style="font-family:\'Barlow Condensed\',sans-serif;font-size:18px;font-weight:800;color:{h_color}">{_ventes_fmt_kt(p_tot)} KT</span></div></div></div>',unsafe_allow_html=True)
                        c_pays=vmap.get("pays")
                        if c_pays and c_pays in df_port.columns:
                            for pays_val in sorted(df_port[c_pays].dropna().unique()):
                                df_pays=df_port[df_port[c_pays].astype(str).str.strip()==str(pays_val)]
                                if df_pays.empty: continue
                                py_d1=pd.to_numeric(df_pays[v_d1],errors='coerce').fillna(0).sum() if v_d1 and v_d1 in df_pays.columns else 0
                                py_d2=pd.to_numeric(df_pays[v_d2],errors='coerce').fillna(0).sum() if v_d2 and v_d2 in df_pays.columns else 0
                                py_d3=pd.to_numeric(df_pays[v_d3],errors='coerce').fillna(0).sum() if v_d3 and v_d3 in df_pays.columns else 0
                                py_tot=py_d1+py_d2+py_d3
                                flag_rpt=country_flag(str(pays_val),20)
                                st.markdown(f'<div style="margin:3px 0 3px 44px;padding:8px 14px;background:#F8FAFC;border:1px solid #EEF0F4;border-radius:6px"><div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px"><span style="font-size:13px;font-weight:600;color:#4A5568;display:flex;align-items:center">{flag_rpt}{pays_val}</span><div style="display:flex;gap:10px;align-items:center"><span style="font-size:10px;color:#94A3B8">D1:<b style="color:#1565C0"> {_ventes_fmt_kt(py_d1)}</b></span><span style="font-size:10px;color:#94A3B8">D2:<b style="color:#C05A00"> {_ventes_fmt_kt(py_d2)}</b></span><span style="font-size:10px;color:#94A3B8">D3:<b style="color:#00843D"> {_ventes_fmt_kt(py_d3)}</b></span><span style="font-size:13px;font-weight:700;color:#12202E">{_ventes_fmt_kt(py_tot)} KT</span></div></div>',unsafe_allow_html=True)
                                c_prod_col=vmap.get("produit")
                                if c_prod_col and c_prod_col in df_pays.columns:
                                    prod_lines=""
                                    for p_name in sorted(df_pays[c_prod_col].dropna().unique()):
                                        df_pr=df_pays[df_pays[c_prod_col].astype(str).str.strip()==str(p_name)]
                                        pr_d1=pd.to_numeric(df_pr[v_d1],errors='coerce').fillna(0).sum() if v_d1 and v_d1 in df_pr.columns else 0
                                        pr_d2=pd.to_numeric(df_pr[v_d2],errors='coerce').fillna(0).sum() if v_d2 and v_d2 in df_pr.columns else 0
                                        pr_d3=pd.to_numeric(df_pr[v_d3],errors='coerce').fillna(0).sum() if v_d3 and v_d3 in df_pr.columns else 0
                                        pr_tot=pr_d1+pr_d2+pr_d3
                                        prod_lines+=f'<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #F2F4F7"><span style="font-size:11px;color:#4A5568">{p_name}</span><div style="display:flex;gap:10px;align-items:center"><span style="font-size:10px;color:#94A3B8">D1:<b style="color:#1565C0"> {_ventes_fmt_kt(pr_d1)}</b></span><span style="font-size:10px;color:#94A3B8">D2:<b style="color:#C05A00"> {_ventes_fmt_kt(pr_d2)}</b></span><span style="font-size:10px;color:#94A3B8">D3:<b style="color:#00843D"> {_ventes_fmt_kt(pr_d3)}</b></span><span style="font-size:11px;font-weight:700;color:#12202E">{_ventes_fmt_kt(pr_tot)} KT</span></div></div>'
                                    if prod_lines: st.markdown(f'<div style="margin-top:6px;padding:0 6px">{prod_lines}</div>',unsafe_allow_html=True)
                                st.markdown('</div>',unsafe_allow_html=True)
            tot_d1=pd.to_numeric(df_rpt[v_d1],errors='coerce').fillna(0).sum() if v_d1 and v_d1 in df_rpt.columns else 0
            tot_d2=pd.to_numeric(df_rpt[v_d2],errors='coerce').fillna(0).sum() if v_d2 and v_d2 in df_rpt.columns else 0
            tot_d3=pd.to_numeric(df_rpt[v_d3],errors='coerce').fillna(0).sum() if v_d3 and v_d3 in df_rpt.columns else 0
            tot_all=tot_d1+tot_d2+tot_d3
            st.markdown(f'<div style="margin-top:24px;background:linear-gradient(135deg,#12202E,#1E3A5F);color:white;padding:20px 28px;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,.2)"><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:20px;font-weight:800;margin-bottom:12px;letter-spacing:.5px;opacity:.9;text-align:center">TOTAL GÉNÉRAL — {mois_rapport.upper()}</div><div style="display:flex;justify-content:space-around;align-items:center"><div style="text-align:center"><div style="font-size:10px;opacity:.6;text-transform:uppercase">D1 (J1–10)</div><div style="font-size:24px;font-weight:800;color:#64B5F6">{_ventes_fmt_kt(tot_d1)} KT</div></div><div style="text-align:center"><div style="font-size:10px;opacity:.6;text-transform:uppercase">D2 (J11–20)</div><div style="font-size:24px;font-weight:800;color:#FFB74D">{_ventes_fmt_kt(tot_d2)} KT</div></div><div style="text-align:center"><div style="font-size:10px;opacity:.6;text-transform:uppercase">D3 (J21+)</div><div style="font-size:24px;font-weight:800;color:#81C784">{_ventes_fmt_kt(tot_d3)} KT</div></div><div style="border-left:1px solid rgba(255,255,255,0.2);padding-left:20px;text-align:right"><div style="font-size:10px;opacity:.6;text-transform:uppercase">TOTAL</div><div style="font-size:36px;font-weight:900">{_ventes_fmt_kt(tot_all)} KT</div></div></div></div>',unsafe_allow_html=True)
    elif gen_btn:
        st.warning("Veuillez sélectionner une colonne de référence pour le mois.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE DASHBOARD VENTES  ← NOUVELLE PAGE
# Volume par Produit / Statut / Pays / Site
# ══════════════════════════════════════════════════════════════════════════════
elif page=="dashboard_ventes":

    df_raw_dv = st.session_state.get("ventes_df")
    vmap_dv   = st.session_state.get("ventes_map", {})

    # ── Pas de fichier : invite + upload rapide ──
    if df_raw_dv is None:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#12202E,#1E3A5F);color:white;'
            'border-radius:14px;padding:32px 36px;text-align:center;box-shadow:0 6px 32px rgba(21,101,192,.28)">'
            '<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:26px;font-weight:800;margin-bottom:8px">Dashboard Ventes</div>'
            '<div style="font-size:13px;opacity:.75">Aucun fichier Pipeline chargé. Chargez-le ci-dessous ou depuis la page Pipeline des Ventes.</div>'
            '</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="upload-zone"><div class="zone-title">Charger le fichier Pipeline</div><div class="zone-desc">Fichier Excel Pipeline des Ventes (D1, D2, D3, Produit, Statut, Pays, Site)</div>', unsafe_allow_html=True)
        _fv = st.file_uploader("Pipeline Excel", type=EXCEL_T, key="dv_upload", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        if _fv:
            try:
                _rv, _ev = read_bytes(_fv)
                _xl = pd.ExcelFile(io.BytesIO(_rv), engine=_ev); _tgt = _xl.sheet_names[0]
                for _sn in _xl.sheet_names:
                    if any(k in _sn.lower() for k in ["january","pipeline","ventes","janvier","data"]): _tgt=_sn; break
                _df = pd.read_excel(io.BytesIO(_rv), sheet_name=_tgt, engine=_ev)
                _df.columns = [str(c).strip() for c in _df.columns]; _df = _df.dropna(how='all')
                _dm = _ventes_auto_map(_df)
                st.session_state.update({"ventes_df":_df,"ventes_map":_dm,"ventes_name":_fv.name})
                save_cache(VENTES_CACHE,{"ventes_df":_df,"ventes_map":_dm,"filename":_fv.name})
                _fv.seek(0); add_hist(HIST_VENTES,_fv.name,_fv.read(),"ventes")
                st.session_state["llm_statut_input_key"] = ""
                st.success(f"Fichier importé — {len(_df)} lignes"); st.rerun()
            except Exception as _e: st.error(f"Erreur : {_e}")
        st.stop()

    # ── Colonnes utiles ──
    c_prod  = vmap_dv.get("produit")
    c_stat  = vmap_dv.get("status")
    c_pays  = vmap_dv.get("pays")
    c_site  = vmap_dv.get("loading_port") or vmap_dv.get("site")
    c_conf  = vmap_dv.get("confirmation")
    c_macro = vmap_dv.get("macro_qualite")
    v_d1    = vmap_dv.get("d1")
    v_d2    = vmap_dv.get("d2")
    v_d3    = vmap_dv.get("d3")

    MOIS_FR_DV=["Tous","Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    MOIS_EN_DV=["All","January","February","March","April","May","June","July","August","September","October","November","December"]

    def _sum_dec(df):
        d1 = pd.to_numeric(df[v_d1],errors='coerce').fillna(0).sum() if v_d1 and v_d1 in df.columns else 0
        d2 = pd.to_numeric(df[v_d2],errors='coerce').fillna(0).sum() if v_d2 and v_d2 in df.columns else 0
        d3 = pd.to_numeric(df[v_d3],errors='coerce').fillna(0).sum() if v_d3 and v_d3 in df.columns else 0
        return d1, d2, d3, d1+d2+d3

    # ── Hero ──
    vn_dv = st.session_state.get("ventes_name","")
    d1_all,d2_all,d3_all,tot_all = _sum_dec(df_raw_dv)
    st.markdown(
        f'<div class="dv-hero">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;position:relative">'
        f'<div><div class="dv-hero-title">📊 Dashboard Ventes</div>'
        f'<div class="dv-hero-sub">Volume par Produit • Statut Planif • Pays • Site — {vn_dv or "Pipeline non nommé"}</div></div>'
        f'<div style="display:flex;gap:10px;flex-wrap:wrap">'
        f'<div class="dv-stat-pill"><div><div class="dv-stat-val">{_ventes_fmt_kt(d1_all)}</div><div class="dv-stat-lbl">KT D1</div></div></div>'
        f'<div class="dv-stat-pill"><div><div class="dv-stat-val">{_ventes_fmt_kt(d2_all)}</div><div class="dv-stat-lbl">KT D2</div></div></div>'
        f'<div class="dv-stat-pill"><div><div class="dv-stat-val">{_ventes_fmt_kt(d3_all)}</div><div class="dv-stat-lbl">KT D3</div></div></div>'
        f'<div class="dv-stat-pill" style="background:rgba(100,181,246,.18);border-color:rgba(100,181,246,.4)">'
        f'<div><div class="dv-stat-val" style="font-size:32px">{_ventes_fmt_kt(tot_all)}</div><div class="dv-stat-lbl">TOTAL KT</div></div></div>'
        f'</div></div></div>', unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # FILTRES GLOBAUX
    # ════════════════════════════════════════════════════
    st.markdown('<div class="filter-panel"><div class="filter-panel-title">Filtres globaux</div>', unsafe_allow_html=True)
    fr0 = st.columns(4)
    dv_m_bl   = fr0[0].selectbox("BL Month",   MOIS_FR_DV, key="dv_bl")
    dv_m_phys = fr0[1].selectbox("Physical",   MOIS_FR_DV, key="dv_phys")
    dv_m_work = fr0[2].selectbox("Working",    MOIS_FR_DV, key="dv_work")
    dv_m_del  = fr0[3].selectbox("Delivery",   MOIS_FR_DV, key="dv_del")

    df_dv = df_raw_dv.copy()
    for _sel, _role in [(dv_m_bl,"bl_month"),(dv_m_phys,"phys_month"),(dv_m_work,"work_month"),(dv_m_del,"del_month")]:
        if _sel != "Tous":
            _col = vmap_dv.get(_role)
            if _col and _col in df_dv.columns:
                _en = MOIS_EN_DV[MOIS_FR_DV.index(_sel)]
                df_dv = df_dv[df_dv[_col].astype(str).str.contains(f"{_sel}|{_en}", case=False, na=False)]

    fr1 = st.columns(4)
    # Confirmation
    dv_conf = fr1[0].selectbox("Confirmation", ["Tous","CONF","Res.CAPA"], key="dv_conf")
    if dv_conf != "Tous" and c_conf and c_conf in df_dv.columns:
        df_dv = df_dv[df_dv[c_conf].astype(str).str.strip() == dv_conf]

    # Site
    _sites_dv = sorted(df_dv[c_site].dropna().astype(str).str.strip().unique()) if c_site and c_site in df_dv.columns else []
    dv_site = fr1[1].selectbox("Site / Port", ["Tous"] + _sites_dv, key="dv_site")
    if dv_site != "Tous" and c_site and c_site in df_dv.columns:
        df_dv = df_dv[df_dv[c_site].astype(str).str.strip() == dv_site]

    # Produit
    _prods_dv = sorted(df_dv[c_prod].dropna().astype(str).str.strip().unique()) if c_prod and c_prod in df_dv.columns else []
    dv_prod = fr1[2].selectbox("Produit", ["Tous"] + _prods_dv, key="dv_prod")
    if dv_prod != "Tous" and c_prod and c_prod in df_dv.columns:
        df_dv = df_dv[df_dv[c_prod].astype(str).str.strip() == dv_prod]

    # Pays
    _pays_dv = sorted(df_dv[c_pays].dropna().astype(str).str.strip().unique()) if c_pays and c_pays in df_dv.columns else []
    dv_pays = fr1[3].selectbox("Pays", ["Tous"] + _pays_dv, key="dv_pays")
    if dv_pays != "Tous" and c_pays and c_pays in df_dv.columns:
        df_dv = df_dv[df_dv[c_pays].astype(str).str.strip().str.lower() == dv_pays.strip().lower()]

    st.markdown('</div>', unsafe_allow_html=True)

    # Stats du dataset filtré
    d1f, d2f, d3f, totf = _sum_dec(df_dv)
    n_lignes = len(df_dv)
    n_pays_u  = df_dv[c_pays].nunique() if c_pays and c_pays in df_dv.columns else 0
    n_prod_u  = df_dv[c_prod].nunique() if c_prod and c_prod in df_dv.columns else 0
    n_stat_u  = df_dv[c_stat].nunique() if c_stat and c_stat in df_dv.columns else 0

    # KPIs
    kc1, kc2, kc3, kc4, kc5 = st.columns(5)
    kc1.markdown(f'<div class="dv-kpi c-blue"><div class="dv-kpi-lbl">Total pipeline</div><div class="dv-kpi-val c-blue">{_ventes_fmt_kt(totf)}<span style="font-size:12px;color:#94A3B8;margin-left:3px">KT</span></div><div class="dv-kpi-sub">{n_lignes} ligne(s)</div></div>', unsafe_allow_html=True)
    kc2.markdown(f'<div class="dv-kpi c-green"><div class="dv-kpi-lbl">D1 (J1–10)</div><div class="dv-kpi-val c-green">{_ventes_fmt_kt(d1f)}<span style="font-size:12px;color:#94A3B8;margin-left:3px">KT</span></div><div class="dv-kpi-sub">{round(d1f/totf*100,1) if totf else 0}% du total</div></div>', unsafe_allow_html=True)
    kc3.markdown(f'<div class="dv-kpi c-orange"><div class="dv-kpi-lbl">D2 (J11–20)</div><div class="dv-kpi-val c-orange">{_ventes_fmt_kt(d2f)}<span style="font-size:12px;color:#94A3B8;margin-left:3px">KT</span></div><div class="dv-kpi-sub">{round(d2f/totf*100,1) if totf else 0}% du total</div></div>', unsafe_allow_html=True)
    kc4.markdown(f'<div class="dv-kpi c-purple"><div class="dv-kpi-lbl">D3 (J21+)</div><div class="dv-kpi-val c-purple">{_ventes_fmt_kt(d3f)}<span style="font-size:12px;color:#94A3B8;margin-left:3px">KT</span></div><div class="dv-kpi-sub">{round(d3f/totf*100,1) if totf else 0}% du total</div></div>', unsafe_allow_html=True)
    kc5.markdown(f'<div class="dv-kpi c-blue"><div class="dv-kpi-lbl">Diversité</div><div class="dv-kpi-val c-blue" style="font-size:20px">{n_pays_u} pays<br><span style="font-size:14px">{n_prod_u} produits</span></div><div class="dv-kpi-sub">{n_stat_u} statuts</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # ── Helper agrégation ──
    def _agg_by(df, col):
        if not col or col not in df.columns: return pd.DataFrame()
        grp = df.groupby(df[col].astype(str).str.strip()).agg(
            D1=(v_d1, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if v_d1 else (col, lambda x:0),
            D2=(v_d2, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if v_d2 else (col, lambda x:0),
            D3=(v_d3, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if v_d3 else (col, lambda x:0),
        ).reset_index()
        grp.columns = [col, "D1", "D2", "D3"]
        grp["TOTAL"] = grp["D1"] + grp["D2"] + grp["D3"]
        return grp[grp["TOTAL"] > 0].sort_values("TOTAL", ascending=False)

    def _bar_stacked(grp, col, title, height=420):
        fig = go.Figure()
        for dec, clr in zip(["D1","D2","D3"], ["#1565C0","#C05A00","#00843D"]):
            fig.add_trace(go.Bar(
                y=grp[col], x=grp[dec], name=dec, orientation='h',
                marker=dict(color=clr, opacity=.88),
                hovertemplate=f'<b>%{{y}}</b><br>{dec} : %{{x:.1f}} KT<extra></extra>'))
        lyt = dict(**PL)
        lyt['height'] = height; lyt['barmode'] = 'stack'
        lyt['title'] = dict(text=title, font=dict(size=13,color="#12202E"))
        lyt['margin'] = dict(l=160, r=16, t=44, b=16)
        lyt['yaxis'] = dict(gridcolor='#E0E4EA', linecolor='#E0E4EA',
                            tickfont=dict(color='#4A5568',size=11), autorange='reversed')
        fig.update_layout(**lyt)
        return fig

    def _donut(grp, col, title, height=360):
        labels = grp[col].tolist(); values = grp["TOTAL"].tolist()
        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            marker=dict(colors=DV_PALETTE[:len(labels)]),
            hole=.48, textinfo='percent', textfont=dict(size=11),
            hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Barlow,sans-serif',color='#4A5568'),
            legend=dict(bgcolor='rgba(255,255,255,.9)', bordercolor='#E0E4EA', borderwidth=1,
                        font=dict(size=10,color='#12202E'), orientation='v'),
            margin=dict(l=8,r=8,t=44,b=8), height=height,
            title=dict(text=title, font=dict(size=13,color="#12202E")))
        return fig

    def _rank_list(grp, col, color="#1565C0", max_items=10, df_source=None, c_region_col=None, c_pays_col=None):
        total = grp["TOTAL"].sum()
        items = grp.head(max_items).to_dict('records')
        html  = ""
        for i, row in enumerate(items):
            name = str(row[col])
            val  = row["TOTAL"]
            pct  = round(val / total * 100) if total > 0 else 0
            flag = country_flag(name, 16) if col == c_pays_col else ""
            region_badge = ""
            if col == c_pays_col and df_source is not None and c_region_col and c_region_col in df_source.columns and c_pays_col in df_source.columns:
                regions = (df_source[df_source[c_pays_col].astype(str).str.strip() == name][c_region_col]
                           .dropna().astype(str).str.strip().unique().tolist())
                if regions:
                    region_badge = (
                        f'<span style="background:#F0EBF8;color:#6B3FA0;border-radius:4px;'
                        f'padding:1px 6px;font-size:8px;font-weight:700;margin-left:5px;'
                        f'vertical-align:middle">{regions[0]}</span>'
                    )
            html += (
                f'<div class="dv-rank-item">'
                f'  <div class="dv-rank-num">#{i+1}</div>'
                f'  <div style="flex:1">'
                f'    <div style="display:flex;align-items:center;flex-wrap:wrap">'
                f'      {flag}<span class="dv-rank-name">{name}</span>{region_badge}'
                f'    </div>'
                f'    <div class="dv-bar-track">'
                f'      <div class="dv-bar-fill" style="width:{max(3,pct)}%;background:{color}"></div>'
                f'    </div>'
                f'  </div>'
                f'  <div style="text-align:right">'
                f'    <div class="dv-rank-val" style="color:{color}">{_ventes_fmt_kt(val)}</div>'
                f'    <div class="dv-rank-pct">{pct}%</div>'
                f'  </div>'
                f'</div>'
            )
        return html or '<div style="color:#94A3B8;font-size:12px;padding:12px">Aucune donnée</div>'

    # ════════════════════════════════════════════════════
    # ONGLETS — switch par clic (comme TSP)
    # ════════════════════════════════════════════════════
    tab_pays_dv, tab_stat_dv, tab_prod_dv, tab_port_dv, tab_dist_dv = st.tabs([
        "Par Pays", "Par Statut", "Par Produit", "Par Port", "Répartition D1/D2/D3"
    ])

    # ── PAR PAYS ──
    with tab_pays_dv:
        grp_pays = _agg_by(df_dv, c_pays)
        if not grp_pays.empty:
            _g3a, _g3b = st.columns([3, 2])
            with _g3a:
                h_pays = max(380, len(grp_pays) * 28 + 80)
                st.plotly_chart(_bar_stacked(grp_pays, c_pays, "Volume par Pays — D1/D2/D3 (KT)", h_pays), use_container_width=True)
            with _g3b:
                st.plotly_chart(_donut(grp_pays, c_pays, "Top pays par volume"), use_container_width=True)
                c_region_dv = vmap_dv.get("region")
                st.markdown(
                    _rank_list(grp_pays, c_pays, "#1565C0", 10,
                               df_source=df_dv,
                               c_region_col=c_region_dv,
                               c_pays_col=c_pays),
                    unsafe_allow_html=True)
        else:
            st.info("Colonne Pays non mappée ou aucune donnée.")

    # ── PAR STATUT ──
    with tab_stat_dv:
        if c_stat and c_stat in df_dv.columns:
            df_dv_stat = df_dv.copy()
            llm_m = st.session_state.get("llm_statut_map", {})
            if llm_m:
                df_dv_stat["__sn__"] = df_dv_stat[c_stat].apply(normalize_statut)
                grp_stat = _agg_by(df_dv_stat, "__sn__")
                grp_stat = grp_stat.rename(columns={"__sn__": c_stat})
            else:
                grp_stat = _agg_by(df_dv, c_stat)

            STAT_CLR_MAP = {
                "charg":"#C05A00","cours":"#C05A00","laycan":"#6B3FA0",
                "planif":"#1565C0","cfr":"#00843D","fob":"#C62828",
                "rade":"#6B3FA0","nomm":"#1565C0","container":"#37474F","recherche":"#C62828",
            }
            def _stat_color_list(labels):
                res = []
                for l in labels:
                    sl = _deaccent(str(l)); c = "#94A3B8"
                    for k, v in STAT_CLR_MAP.items():
                        if k in sl: c = v; break
                    res.append(c)
                return res

            if not grp_stat.empty:
                _g2a, _g2b = st.columns([3, 2])
                with _g2a:
                    h_stat = max(380, len(grp_stat) * 32 + 80)
                    fig_stat = go.Figure()
                    for dec, clr in zip(["D1","D2","D3"], ["#1565C0","#C05A00","#00843D"]):
                        fig_stat.add_trace(go.Bar(
                            y=grp_stat[c_stat], x=grp_stat[dec], name=dec, orientation='h',
                            marker=dict(color=clr, opacity=.88),
                            hovertemplate=f'<b>%{{y}}</b><br>{dec} : %{{x:.1f}} KT<extra></extra>'))
                    ls = dict(**PL); ls['height'] = h_stat; ls['barmode'] = 'stack'
                    ls['title'] = dict(text="Volume par Statut — D1/D2/D3 (KT)", font=dict(size=13,color="#12202E"))
                    ls['margin'] = dict(l=200,r=16,t=44,b=16)
                    ls['yaxis'] = dict(gridcolor='#E0E4EA', linecolor='#E0E4EA',
                                       tickfont=dict(color='#4A5568',size=11), autorange='reversed')
                    fig_stat.update_layout(**ls)
                    st.plotly_chart(fig_stat, use_container_width=True)
                with _g2b:
                    fig_pie_s = go.Figure(go.Pie(
                        labels=grp_stat[c_stat].tolist(), values=grp_stat["TOTAL"].tolist(),
                        marker=dict(colors=_stat_color_list(grp_stat[c_stat].tolist())),
                        hole=.48, textinfo='percent', textfont=dict(size=11),
                        hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
                    fig_pie_s.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Barlow,sans-serif',color='#4A5568'),
                        legend=dict(bgcolor='rgba(255,255,255,.9)', bordercolor='#E0E4EA', borderwidth=1, font=dict(size=10)),
                        margin=dict(l=8,r=8,t=44,b=8), height=360,
                        title=dict(text="Répartition par Statut", font=dict(size=13,color="#12202E")))
                    st.plotly_chart(fig_pie_s, use_container_width=True)
                    st.markdown(_rank_list(grp_stat, c_stat, "#C05A00", 8), unsafe_allow_html=True)
        else:
            st.info("Colonne Statut Planif non mappée ou aucune donnée.")

    # ── PAR PRODUIT ──
    with tab_prod_dv:
        grp_prod = _agg_by(df_dv, c_prod)
        if not grp_prod.empty:
            _g1a, _g1b = st.columns([3, 2])
            with _g1a:
                h_prod = max(380, len(grp_prod) * 32 + 80)
                st.plotly_chart(_bar_stacked(grp_prod, c_prod, "Volume par Produit — D1/D2/D3 (KT)", h_prod), use_container_width=True)
            with _g1b:
                st.plotly_chart(_donut(grp_prod, c_prod, "Répartition par Produit"), use_container_width=True)
                st.markdown(_rank_list(grp_prod, c_prod, "#00843D", 8), unsafe_allow_html=True)
        else:
            st.info("Colonne Produit non mappée ou aucune donnée.")

    # ── PAR PORT ──
    with tab_port_dv:
        grp_site = _agg_by(df_dv, c_site)
        if not grp_site.empty:
            _g4a, _g4b, _g4c = st.columns([2, 2, 1])
            with _g4a:
                fig_site_bar = go.Figure()
                fig_site_bar.add_trace(go.Bar(x=grp_site[c_site], y=grp_site["D1"], name="D1", marker=dict(color="#1565C0",opacity=.88)))
                fig_site_bar.add_trace(go.Bar(x=grp_site[c_site], y=grp_site["D2"], name="D2", marker=dict(color="#C05A00",opacity=.88)))
                fig_site_bar.add_trace(go.Bar(x=grp_site[c_site], y=grp_site["D3"], name="D3", marker=dict(color="#00843D",opacity=.88)))
                ls4 = dict(**PL); ls4['height'] = 380; ls4['barmode'] = 'group'
                ls4['title'] = dict(text="D1/D2/D3 par Site (KT)", font=dict(size=13,color="#12202E"))
                fig_site_bar.update_layout(**ls4)
                st.plotly_chart(fig_site_bar, use_container_width=True)
            with _g4b:
                st.plotly_chart(_donut(grp_site, c_site, "Répartition par Site", 380), use_container_width=True)
            with _g4c:
                st.markdown(_rank_list(grp_site, c_site, "#6B3FA0", 10), unsafe_allow_html=True)
        else:
            st.info("Colonne Site / Port non mappée ou aucune donnée.")

    # ── RÉPARTITION D1/D2/D3 ──
    with tab_dist_dv:
        _dv1, _dv2, _dv3 = st.columns(3)
        with _dv1:
            fig_wf = go.Figure(go.Bar(
                x=["D1 (J1-10)","D2 (J11-20)","D3 (J21+)"],
                y=[d1f, d2f, d3f],
                marker=dict(color=["#1565C0","#C05A00","#00843D"], opacity=.9),
                text=[f"{_ventes_fmt_kt(v)} KT" for v in [d1f, d2f, d3f]],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>%{y:.1f} KT<extra></extra>'))
            lwf = dict(**PL); lwf['height'] = 360
            lwf['title'] = dict(text="Volumes D1 / D2 / D3 (KT)", font=dict(size=13,color="#12202E"))
            fig_wf.update_layout(**lwf)
            st.plotly_chart(fig_wf, use_container_width=True)
        with _dv2:
            if totf > 0:
                fig_d3 = go.Figure(go.Pie(
                    labels=["D1","D2","D3"], values=[d1f, d2f, d3f],
                    marker=dict(colors=["#1565C0","#C05A00","#00843D"]),
                    hole=.52, textinfo='label+percent',
                    hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
                fig_d3.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Barlow,sans-serif'),
                    annotations=[dict(text=f"{_ventes_fmt_kt(totf)}<br>KT", x=.5, y=.5,
                                      font_size=14, showarrow=False,
                                      font=dict(color="#12202E",family="Barlow Condensed"))],
                    legend=dict(bgcolor='rgba(255,255,255,.9)', bordercolor='#E0E4EA', borderwidth=1),
                    margin=dict(l=8,r=8,t=36,b=8), height=360,
                    title=dict(text="Répartition D1/D2/D3", font=dict(size=12,color="#12202E")))
                st.plotly_chart(fig_d3, use_container_width=True)
        with _dv3:
            d1_pct = round(d1f/totf*100,1) if totf>0 else 0
            d2_pct = round(d2f/totf*100,1) if totf>0 else 0
            d3_pct = round(d3f/totf*100,1) if totf>0 else 0
            st.markdown(f'''<div style="background:#F8FAFC;border:1px solid #E0E4EA;border-radius:10px;padding:20px">
<div style="font-size:9px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#94A3B8;margin-bottom:16px">RÉCAP DÉCADES</div>
<div style="margin-bottom:14px"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#1565C0">D1 — Jours 1–10</span><span style="font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;color:#1565C0">{_ventes_fmt_kt(d1f)} KT</span></div><div style="height:6px;background:#E0E4EA;border-radius:3px;margin-top:4px"><div style="width:{max(3,int(d1_pct))}%;height:6px;background:#1565C0;border-radius:3px"></div></div><div style="font-size:9px;color:#94A3B8;margin-top:2px">{d1_pct}% du total</div></div>
<div style="margin-bottom:14px"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#C05A00">D2 — Jours 11–20</span><span style="font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;color:#C05A00">{_ventes_fmt_kt(d2f)} KT</span></div><div style="height:6px;background:#E0E4EA;border-radius:3px;margin-top:4px"><div style="width:{max(3,int(d2_pct))}%;height:6px;background:#C05A00;border-radius:3px"></div></div><div style="font-size:9px;color:#94A3B8;margin-top:2px">{d2_pct}% du total</div></div>
<div style="margin-bottom:14px"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#00843D">D3 — Jours 21+</span><span style="font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;color:#00843D">{_ventes_fmt_kt(d3f)} KT</span></div><div style="height:6px;background:#E0E4EA;border-radius:3px;margin-top:4px"><div style="width:{max(3,int(d3_pct))}%;height:6px;background:#00843D;border-radius:3px"></div></div><div style="font-size:9px;color:#94A3B8;margin-top:2px">{d3_pct}% du total</div></div>
<div style="border-top:1px solid #E0E4EA;padding-top:12px;display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#12202E">TOTAL</span><span style="font-family:'Barlow Condensed',sans-serif;font-size:24px;font-weight:900;color:#12202E">{_ventes_fmt_kt(totf)} KT</span></div>
</div>''', unsafe_allow_html=True)

    # ── Bouton vers Pipeline ──
    st.markdown(
        '<div style="background:#E3EAF8;border:1px solid rgba(21,101,192,.2);border-radius:10px;'
        'padding:14px 20px;display:flex;align-items:center;justify-content:space-between;margin-top:8px">'
        '<div><div style="font-size:13px;font-weight:700;color:#1565C0;margin-bottom:3px">📋 Pipeline des Ventes</div>'
        '<div style="font-size:11px;color:#4A5568">Pour le détail par décade, statuts IA, rapports et tableau complet</div></div>'
        '</div>', unsafe_allow_html=True)
    if st.button("→ Ouvrir Pipeline des Ventes", key="dv_goto_ventes", type="primary"):
        st.session_state["page"] = "ventes"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE ZOOM TSP — mêmes filtres que Pipeline, produits TSP uniquement
# Ordre : 1. Total  2. Décades  3. Tableau
# ══════════════════════════════════════════════════════════════════════════════
elif page=="tsp_zoom":

    # ── Hero ──
    st.markdown('<div class="tsp-hero"><div class="tsp-hero-title">🔬 Zoom TSP — Pipeline des Ventes</div><div class="tsp-hero-sub">Analyse complète du pipeline TSP — mêmes filtres que Pipeline des Ventes, produits TSP uniquement</div></div>',unsafe_allow_html=True)

    df_raw_tsp=st.session_state.get("ventes_df")
    vmap_tsp=st.session_state.get("ventes_map",{})
    safi_df_tsp=st.session_state.get("safi_df")

    # ── Upload si pas de fichier pipeline ──
    if df_raw_tsp is None:
        st.markdown('<div class="upload-zone"><div class="zone-title">Fichier Pipeline des Ventes</div><div class="zone-desc">Nécessaire pour les filtres et les décades TSP</div>',unsafe_allow_html=True)
        file_vtsp=st.file_uploader("Pipeline Excel",type=EXCEL_T,key="tsp_v_upload",label_visibility="collapsed")
        st.markdown('</div>',unsafe_allow_html=True)
        if file_vtsp:
            try:
                raw_v,eng_v=read_bytes(file_vtsp)
                xl=pd.ExcelFile(io.BytesIO(raw_v),engine=eng_v); target=xl.sheet_names[0]
                for sn in xl.sheet_names:
                    if any(k in sn.lower() for k in ["january","pipeline","ventes","janvier","data"]): target=sn; break
                df_full=pd.read_excel(io.BytesIO(raw_v),sheet_name=target,engine=eng_v)
                df_full.columns=[str(c).strip() for c in df_full.columns]; df_full=df_full.dropna(how='all')
                detected_map=_ventes_auto_map(df_full)
                st.session_state.update({"ventes_df":df_full,"ventes_map":detected_map,"ventes_name":file_vtsp.name})
                save_cache(VENTES_CACHE,{"ventes_df":df_full,"ventes_map":detected_map,"filename":file_vtsp.name})
                file_vtsp.seek(0); add_hist(HIST_VENTES,file_vtsp.name,file_vtsp.read(),"ventes")
                st.session_state["llm_tsp_statut_input_key"]=""
                st.success(f"Fichier importé — {len(df_full)} lignes"); st.rerun()
            except Exception as e: st.error(f"Erreur : {e}")
        st.info("Chargez le fichier Pipeline des Ventes pour accéder au Zoom TSP.")
        st.stop()

    df_raw_tsp=st.session_state.get("ventes_df")
    vmap_tsp=st.session_state.get("ventes_map",{})
    safi_df_tsp=st.session_state.get("safi_df")

    # ── Détecter la colonne produit et les produits TSP ──
    c_prod_tsp=vmap_tsp.get("produit")

    # Construire la base TSP : on filtre uniquement les lignes dont le produit contient "tsp"
    df_base_tsp=df_raw_tsp.copy()
    _tsp_real_products=[]
    if c_prod_tsp and c_prod_tsp in df_base_tsp.columns:
        all_prods=df_base_tsp[c_prod_tsp].dropna().astype(str).str.strip().unique().tolist()
        _tsp_real_products=sorted([p for p in all_prods if "tsp" in p.lower()])
        if _tsp_real_products:
            df_base_tsp=df_base_tsp[df_base_tsp[c_prod_tsp].astype(str).str.strip().str.lower().str.contains("tsp",na=False)]

    # Badge fichiers actifs
    _vn_tsp=st.session_state.get("ventes_name","")
    _info_parts=[]
    if _vn_tsp: _info_parts.append(f'<span style="background:#E3EAF8;color:#1565C0;border-radius:6px;padding:3px 10px;font-size:10px;font-weight:700">Pipeline : {_vn_tsp}</span>')
    if _tsp_real_products:
        _info_parts.append(f'<span style="background:#FBF0E6;color:#C05A00;border-radius:6px;padding:3px 10px;font-size:10px;font-weight:700">{len(_tsp_real_products)} produit(s) TSP détecté(s)</span>')
    if _info_parts:
        st.markdown(f'<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px">{"".join(_info_parts)}</div>',unsafe_allow_html=True)

    with st.expander("Changer le fichier Pipeline"):
        file_vtsp2=st.file_uploader("Nouveau fichier Pipeline",type=EXCEL_T,key="tsp_v_upload2",label_visibility="visible")
        if file_vtsp2:
            try:
                raw_v2,eng_v2=read_bytes(file_vtsp2)
                xl2=pd.ExcelFile(io.BytesIO(raw_v2),engine=eng_v2); tgt2=xl2.sheet_names[0]
                for sn in xl2.sheet_names:
                    if any(k in sn.lower() for k in ["january","pipeline","ventes","janvier","data"]): tgt2=sn; break
                df_f2=pd.read_excel(io.BytesIO(raw_v2),sheet_name=tgt2,engine=eng_v2)
                df_f2.columns=[str(c).strip() for c in df_f2.columns]; df_f2=df_f2.dropna(how='all')
                dm2=_ventes_auto_map(df_f2)
                st.session_state.update({"ventes_df":df_f2,"ventes_map":dm2,"ventes_name":file_vtsp2.name})
                save_cache(VENTES_CACHE,{"ventes_df":df_f2,"ventes_map":dm2,"filename":file_vtsp2.name})
                file_vtsp2.seek(0); add_hist(HIST_VENTES,file_vtsp2.name,file_vtsp2.read(),"ventes")
                st.session_state["llm_tsp_statut_input_key"]=""; st.rerun()
            except Exception as e: st.error(f"Erreur : {e}")

    # ════════════════════════════════════════════════════
    # FILTRES — identiques à Pipeline des Ventes
    # mais filtre Produit = TSP uniquement
    # ════════════════════════════════════════════════════
    st.markdown('<div class="filter-panel"><div class="filter-panel-title">Filtres TSP</div>',unsafe_allow_html=True)

    MOIS_FR_T=["Tous","Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    MOIS_EN_T=["All","January","February","March","April","May","June","July","August","September","October","November","December"]
    c_stat_col_tsp=vmap_tsp.get("status")

    # Ligne 1 : filtres mois
    tfrow0=st.columns(4)
    tsel_m_bl=tfrow0[0].selectbox("BL Month",MOIS_FR_T,key="tsp_mois_bl")
    tsel_m_phys=tfrow0[1].selectbox("Physical Month",MOIS_FR_T,key="tsp_mois_phys")
    tsel_m_work=tfrow0[2].selectbox("Working Month",MOIS_FR_T,key="tsp_mois_work")
    tsel_m_del=tfrow0[3].selectbox("Delivery Month",MOIS_FR_T,key="tsp_mois_del")

    # Pré-filtre mois sur la base TSP uniquement
    df_tsp_prefilt=df_base_tsp.copy()
    for tsel_mx,trole_key in [(tsel_m_bl,"bl_month"),(tsel_m_phys,"phys_month"),(tsel_m_work,"work_month"),(tsel_m_del,"del_month")]:
        if tsel_mx!="Tous":
            col_mx_t=vmap_tsp.get(trole_key)
            if col_mx_t and col_mx_t in df_tsp_prefilt.columns:
                mois_en_t=MOIS_EN_T[MOIS_FR_T.index(tsel_mx)]
                df_tsp_prefilt=df_tsp_prefilt[df_tsp_prefilt[col_mx_t].astype(str).str.contains(f"{tsel_mx}|{mois_en_t}",case=False,na=False)]

    # Ligne 2 : Site, Confirmation, Pays, Produit TSP
    tfrow1=st.columns(4)

    _tcol_site_dyn=(vmap_tsp.get("loading_port") if vmap_tsp.get("loading_port") and vmap_tsp.get("loading_port") in df_tsp_prefilt.columns
                    else vmap_tsp.get("site") if vmap_tsp.get("site") and vmap_tsp.get("site") in df_tsp_prefilt.columns else None)
    if _tcol_site_dyn:
        # ✅ FIX : normalisation majuscules + regroupement par préfixe/contenu
        # Ex: "SAFI", "SAFI 1ST", "SAFI 2ND" → tous affichés comme "SAFI"
        # Ex: "JORF", "JORF LASFAR" → tous affichés comme "JORF"
        _sites_raw = df_tsp_prefilt[_tcol_site_dyn].dropna().astype(str).str.strip().str.upper().unique().tolist()
        _sites_base = sorted(set(
            next((base for base in ["JORF","SAFI","LAAYOUNE","KHOURIBGA"] if s.startswith(base)), s)
            for s in _sites_raw
        ))
        tsites_dyn = _sites_base
        tsel_s=tfrow1[0].selectbox("Site / Port",["Tous"]+tsites_dyn,key="tsp_site")
    else:
        tsel_s=tfrow1[0].selectbox("Site / Port",["Tous"],key="tsp_site")

    tsel_co=tfrow1[1].selectbox("Confirmation",["Tous","CONF","Res.CAPA"],key="tsp_conf")

    tsel_pays_opts=(["Tous"]+sorted(df_tsp_prefilt[vmap_tsp["pays"]].dropna().astype(str).str.strip().unique().tolist())) if vmap_tsp.get("pays") and vmap_tsp["pays"] in df_tsp_prefilt.columns else ["Tous"]
    tsel_pays=tfrow1[2].selectbox("Pays",tsel_pays_opts,key="tsp_pays")

    # ★ Produit : UNIQUEMENT les produits TSP détectés dans le fichier
    if c_prod_tsp and c_prod_tsp in df_tsp_prefilt.columns:
        _tsp_prods_dyn=sorted(df_tsp_prefilt[c_prod_tsp].dropna().astype(str).str.strip().unique().tolist())
    elif _tsp_real_products:
        _tsp_prods_dyn=_tsp_real_products
    else:
        _tsp_prods_dyn=[]
    tsel_prod=tfrow1[3].selectbox("Produit TSP",["Tous"]+_tsp_prods_dyn,key="tsp_produit")

    # Statuts IA (sur la base TSP pré-filtrée)
    if c_stat_col_tsp and c_stat_col_tsp in df_tsp_prefilt.columns:
        build_num_map(df_tsp_prefilt[c_stat_col_tsp], map_key="llm_tsp_statut_map", input_key="llm_tsp_statut_input_key")
        tstatuts_norm=sorted(set(normalize_statut(s,map_key="llm_tsp_statut_map") for s in df_tsp_prefilt[c_stat_col_tsp].dropna().unique()),key=_sort_key_statut_global)
    else:
        tstatuts_norm=[]
    tllm_map=st.session_state.get("llm_tsp_statut_map",{})
    tregroupes={k:v for k,v in tllm_map.items() if _deaccent(v)!=k}
    if tllm_map:
        if tregroupes:
            tdetails=" | ".join(f"{v}" for v in sorted(set(tllm_map.values()))[:6])
            st.markdown(f'<div class="llm-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>IA — {len(tregroupes)} regroupement(s) • Groupes : {tdetails}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="llm-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>IA — {len(tllm_map)} statut(s) analysé(s)</div>',unsafe_allow_html=True)
    if tstatuts_norm:
        tsel_statuts=st.multiselect("Status Planif",options=tstatuts_norm,default=[],key="tsp_statuts")
    else:
        tsel_statuts=[]

    st.markdown('</div>',unsafe_allow_html=True)

    # ── Application de tous les filtres sur la base TSP ──
    df_tf=df_base_tsp.copy()
    for tsel_mx,trole_key in [(tsel_m_bl,"bl_month"),(tsel_m_phys,"phys_month"),(tsel_m_work,"work_month"),(tsel_m_del,"del_month")]:
        if tsel_mx!="Tous":
            col_mx_t=vmap_tsp.get(trole_key)
            if col_mx_t and col_mx_t in df_tf.columns:
                mois_en_t=MOIS_EN_T[MOIS_FR_T.index(tsel_mx)]
                df_tf=df_tf[df_tf[col_mx_t].astype(str).str.contains(f"{tsel_mx}|{mois_en_t}",case=False,na=False)]
    _tcol_site_f=(vmap_tsp.get("loading_port") if vmap_tsp.get("loading_port") and vmap_tsp.get("loading_port") in df_tf.columns
                  else vmap_tsp.get("site") if vmap_tsp.get("site") and vmap_tsp.get("site") in df_tf.columns else None)
    # ✅ FIX : indentation corrigée + filtre case-insensitive via .str.upper()
    if tsel_s!="Tous" and _tcol_site_f:
        tsel_s_upper=tsel_s.upper().strip()
        df_tf=df_tf[df_tf[_tcol_site_f].astype(str).str.upper().str.contains(tsel_s_upper,na=False)]
    if tsel_co!="Tous" and vmap_tsp.get("confirmation") and vmap_tsp["confirmation"] in df_tf.columns:
        df_tf=df_tf[df_tf[vmap_tsp["confirmation"]].astype(str).str.strip()==tsel_co]
    if tsel_pays!="Tous" and vmap_tsp.get("pays") and vmap_tsp["pays"] in df_tf.columns:
        df_tf=df_tf[df_tf[vmap_tsp["pays"]].astype(str).str.strip().str.lower()==tsel_pays.strip().lower()]
    if tsel_prod!="Tous" and c_prod_tsp and c_prod_tsp in df_tf.columns:
        df_tf=df_tf[df_tf[c_prod_tsp].astype(str).str.strip()==tsel_prod]
    if tsel_statuts and c_stat_col_tsp and c_stat_col_tsp in df_tf.columns:
        df_tf=df_tf[df_tf[c_stat_col_tsp].apply(lambda x: normalize_statut(x,map_key="llm_tsp_statut_map") in tsel_statuts)]

    # Valeurs décades
    tv_d1=vmap_tsp.get("d1"); tv_d2=vmap_tsp.get("d2"); tv_d3=vmap_tsp.get("d3")
    tval_d1=pd.to_numeric(df_tf[tv_d1],errors='coerce').fillna(0).sum() if tv_d1 and tv_d1 in df_tf.columns else 0
    tval_d2=pd.to_numeric(df_tf[tv_d2],errors='coerce').fillna(0).sum() if tv_d2 and tv_d2 in df_tf.columns else 0
    tval_d3=pd.to_numeric(df_tf[tv_d3],errors='coerce').fillna(0).sum() if tv_d3 and tv_d3 in df_tf.columns else 0
    ttotal_m=tval_d1+tval_d2+tval_d3

    # Badges filtres actifs
    tactive_filters=[]
    for tsel_mx,tlbl_mx in [(tsel_m_bl,"BL"),(tsel_m_phys,"Physical"),(tsel_m_work,"Working"),(tsel_m_del,"Delivery")]:
        if tsel_mx!="Tous": tactive_filters.append(f'<span style="background:#E3EAF8;color:#1565C0;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600">{tlbl_mx}: {tsel_mx}</span>')
    for ts in tsel_statuts: tactive_filters.append(f'<span style="background:#E8F5EE;color:#005C2A;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600">{ts}</span>')
    if tsel_s!="Tous": tactive_filters.append(f'<span style="background:#FBF0E6;color:#C05A00;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600">Site: {tsel_s}</span>')
    if tsel_pays!="Tous": tactive_filters.append(f'<span style="background:#F0EBF8;color:#6B3FA0;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600">Pays: {tsel_pays}</span>')
    if tsel_prod!="Tous": tactive_filters.append(f'<span style="background:#E3EAF8;color:#1565C0;border-radius:4px;padding:2px 8px;font-size:10px;font-weight:600">Produit: {tsel_prod}</span>')
    if tactive_filters: st.markdown(f'<div style="margin:4px 0 14px 0;display:flex;flex-wrap:wrap;gap:4px;align-items:center"><span style="font-size:10px;color:#94A3B8;margin-right:4px">Filtres actifs :</span>{"".join(tactive_filters)}</div>',unsafe_allow_html=True)

    tmois_labels=[]
    for tsel_mx,tlbl_mx in [(tsel_m_bl,"BL"),(tsel_m_phys,"Phys"),(tsel_m_work,"Work"),(tsel_m_del,"Del")]:
        if tsel_mx!="Tous": tmois_labels.append(f"{tlbl_mx}: {tsel_mx}")
    tfiltre_label=" • ".join(tmois_labels) if tmois_labels else "TOUS MOIS"

    # ════════════════════════════════════════════════════
    # 1. TOTAL PIPELINE TSP
    # ════════════════════════════════════════════════════
    st.markdown(f'<div style="background:linear-gradient(135deg,#0D47A1,#1565C0);color:white;padding:16px 24px;border-radius:10px;margin:0 0 20px 0;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 16px rgba(21,101,192,.25)"><div><span style="font-family:\'Barlow Condensed\',sans-serif;font-size:17px;font-weight:800;letter-spacing:.5px;opacity:.9">TOTAL PIPELINE TSP — {tfiltre_label}</span><div style="font-size:10px;opacity:.6;margin-top:3px">{len(df_tf)} ligne(s) TSP affichée(s) sur {len(df_base_tsp)} total TSP ({len(df_raw_tsp)} lignes dans le fichier)</div></div><div style="display:flex;gap:20px;align-items:center"><div style="text-align:center"><div style="font-size:9px;opacity:.6;text-transform:uppercase;letter-spacing:1px">D1</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:24px;font-weight:800;color:#90CAF9">{_ventes_fmt_kt(tval_d1)} KT</div></div><div style="text-align:center"><div style="font-size:9px;opacity:.6;text-transform:uppercase;letter-spacing:1px">D2</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:24px;font-weight:800;color:#FFB74D">{_ventes_fmt_kt(tval_d2)} KT</div></div><div style="text-align:center"><div style="font-size:9px;opacity:.6;text-transform:uppercase;letter-spacing:1px">D3</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:24px;font-weight:800;color:#81C784">{_ventes_fmt_kt(tval_d3)} KT</div></div><div style="border-left:1px solid rgba(255,255,255,.3);padding-left:20px"><div style="font-size:9px;opacity:.6;text-transform:uppercase;letter-spacing:1px">TOTAL</div><div style="font-family:\'Barlow Condensed\',sans-serif;font-size:30px;font-weight:900">{_ventes_fmt_kt(ttotal_m)} KT</div></div></div></div>',unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # 2. DÉCADES — cartes D1 / D2 / D3
    # ════════════════════════════════════════════════════
    st.markdown('<div class="stitle blue">Décades Pipeline TSP — D1 • D2 • D3</div>',unsafe_allow_html=True)
    tdc1,tdc2,tdc3=st.columns(3)
    with tdc1: _build_card_interactive("D1 — Jours 1–10",tval_d1,tv_d1,"#1565C0","#1565C0",df_tf,vmap_tsp)
    with tdc2: _build_card_interactive("D2 — Jours 11–20",tval_d2,tv_d2,"#C05A00","#C05A00",df_tf,vmap_tsp)
    with tdc3: _build_card_interactive("D3 — Jours 21+",tval_d3,tv_d3,"#00843D","#00843D",df_tf,vmap_tsp)

    # ════════════════════════════════════════════════════
    # 3. VISUALISATION TSP — Graphiques analytiques
    # ════════════════════════════════════════════════════
    st.markdown('<div class="stitle orange">Visualisation TSP — Analyse graphique</div>',unsafe_allow_html=True)

    if not df_tf.empty and tv_d1 and tv_d1 in df_tf.columns:
        # Préparer les colonnes utiles
        c_pays_viz=vmap_tsp.get("pays"); c_stat_viz=vmap_tsp.get("status"); c_prod_viz=vmap_tsp.get("produit")
        c_port_viz=vmap_tsp.get("loading_port") or vmap_tsp.get("site")

        def _sum_dec(df,col): return pd.to_numeric(df[col],errors='coerce').fillna(0).sum() if col and col in df.columns else 0

        tab_pays_v,tab_stat_v,tab_prod_v,tab_port_v,tab_dist_v=st.tabs(["Par Pays","Par Statut","Par Produit","Par Port","Répartition D1/D2/D3"])

        # ── PAR PAYS ──
        with tab_pays_v:
            if c_pays_viz and c_pays_viz in df_tf.columns:
                pays_grp=df_tf.groupby(df_tf[c_pays_viz].astype(str).str.strip()).agg(
                    D1=(tv_d1, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()),
                    D2=(tv_d2, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if tv_d2 else ("D1", lambda x:0),
                    D3=(tv_d3, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if tv_d3 else ("D1", lambda x:0),
                ).reset_index()
                pays_grp.columns=[c_pays_viz,"D1","D2","D3"]
                pays_grp["TOTAL"]=pays_grp["D1"]+pays_grp["D2"]+pays_grp["D3"]
                pays_grp=pays_grp[pays_grp["TOTAL"]>0].sort_values("TOTAL",ascending=True)
                if not pays_grp.empty:
                    _gv1,_gv2=st.columns([3,1])
                    with _gv1:
                        fig_p=go.Figure()
                        fig_p.add_trace(go.Bar(y=pays_grp[c_pays_viz],x=pays_grp["D1"],name="D1",orientation='h',marker=dict(color="#1565C0",opacity=.85),hovertemplate='<b>%{y}</b><br>D1 : %{x:.1f} KT<extra></extra>'))
                        if tv_d2: fig_p.add_trace(go.Bar(y=pays_grp[c_pays_viz],x=pays_grp["D2"],name="D2",orientation='h',marker=dict(color="#C05A00",opacity=.85),hovertemplate='<b>%{y}</b><br>D2 : %{x:.1f} KT<extra></extra>'))
                        if tv_d3: fig_p.add_trace(go.Bar(y=pays_grp[c_pays_viz],x=pays_grp["D3"],name="D3",orientation='h',marker=dict(color="#00843D",opacity=.85),hovertemplate='<b>%{y}</b><br>D3 : %{x:.1f} KT<extra></extra>'))
                        lp=dict(**PL); lp['height']=max(350,len(pays_grp)*28+80); lp['barmode']='stack'; lp['title']=dict(text="TSP par Pays — D1/D2/D3 (KT)",font=dict(size=13,color="#12202E")); lp['margin']=dict(l=140,r=12,t=40,b=12)
                        fig_p.update_layout(**lp); st.plotly_chart(fig_p,use_container_width=True)
                    with _gv2:
                        top5=pays_grp.sort_values("TOTAL",ascending=False).head(5)
                        total_all=pays_grp["TOTAL"].sum()
                        st.markdown('<div style="background:#F8FAFC;border:1px solid #E0E4EA;border-radius:8px;padding:14px 16px">',unsafe_allow_html=True)
                        st.markdown('<div style="font-size:9px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#94A3B8;margin-bottom:10px">TOP 5 PAYS</div>',unsafe_allow_html=True)
                        for _,row in top5.iterrows():
                            pct=round(row["TOTAL"]/total_all*100) if total_all>0 else 0
                            flag=country_flag(str(row[c_pays_viz]),16)
                            st.markdown(f'<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px"><span style="font-size:12px;font-weight:600;color:#12202E;display:flex;align-items:center">{flag}{row[c_pays_viz]}</span><span style="font-size:11px;font-weight:700;color:#1565C0">{_ventes_fmt_kt(row["TOTAL"])} KT</span></div><div style="height:4px;background:#E0E4EA;border-radius:2px"><div style="width:{max(3,pct)}%;height:4px;background:#1565C0;border-radius:2px"></div></div><div style="font-size:9px;color:#94A3B8;margin-top:2px">{pct}% du total</div></div>',unsafe_allow_html=True)
                        st.markdown('</div>',unsafe_allow_html=True)
            else:
                st.info("Mappez la colonne Pays pour voir cette visualisation.")

        # ── PAR STATUT ──
        with tab_stat_v:
            if c_stat_viz and c_stat_viz in df_tf.columns:
                df_stat_v=df_tf.copy()
                df_stat_v["__sn__"]=df_stat_v[c_stat_viz].apply(lambda x: normalize_statut(x,map_key="llm_tsp_statut_map"))
                stat_grp=df_stat_v.groupby("__sn__").agg(
                    D1=(tv_d1, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()),
                    D2=(tv_d2, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if tv_d2 else ("D1", lambda x:0),
                    D3=(tv_d3, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if tv_d3 else ("D1", lambda x:0),
                ).reset_index()
                stat_grp.columns=["Statut","D1","D2","D3"]
                stat_grp["TOTAL"]=stat_grp["D1"]+stat_grp["D2"]+stat_grp["D3"]
                stat_grp=stat_grp[stat_grp["TOTAL"]>0].sort_values("TOTAL",ascending=False)
                if not stat_grp.empty:
                    STAT_COLORS={"charg":"#C05A00","cours":"#C05A00","laycan":"#6B3FA0","planif":"#1565C0","cfr":"#00843D","fob":"#C62828","rade":"#6B3FA0","nomm":"#1565C0","container":"#94A3B8","recherche":"#C62828"}
                    def _stat_color(s):
                        sl=_deaccent(s)
                        for k,c in STAT_COLORS.items():
                            if k in sl: return c
                        return "#94A3B8"
                    _sv1,_sv2=st.columns([2,1])
                    with _sv1:
                        fig_s=go.Figure()
                        fig_s.add_trace(go.Bar(x=stat_grp["Statut"],y=stat_grp["D1"],name="D1",marker=dict(color="#1565C0",opacity=.85)))
                        if tv_d2: fig_s.add_trace(go.Bar(x=stat_grp["Statut"],y=stat_grp["D2"],name="D2",marker=dict(color="#C05A00",opacity=.85)))
                        if tv_d3: fig_s.add_trace(go.Bar(x=stat_grp["Statut"],y=stat_grp["D3"],name="D3",marker=dict(color="#00843D",opacity=.85)))
                        ls=dict(**PL); ls['height']=420; ls['barmode']='stack'; ls['title']=dict(text="TSP par Statut — D1/D2/D3 (KT)",font=dict(size=13,color="#12202E"))
                        fig_s.update_layout(**ls); st.plotly_chart(fig_s,use_container_width=True)
                    with _sv2:
                        total_stat=stat_grp["TOTAL"].sum()
                        fig_pie_s=go.Figure(go.Pie(
                            labels=stat_grp["Statut"],values=stat_grp["TOTAL"],
                            hole=.45,textinfo='percent',
                            hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
                        fig_pie_s.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='Barlow,sans-serif'),
                            legend=dict(bgcolor='rgba(255,255,255,.9)',bordercolor='#E0E4EA',borderwidth=1,font=dict(size=10)),
                            margin=dict(l=8,r=8,t=36,b=8),height=400,
                            title=dict(text="Répartition par statut",font=dict(size=12,color="#12202E")))
                        st.plotly_chart(fig_pie_s,use_container_width=True)
            else:
                st.info("Mappez la colonne Statut pour voir cette visualisation.")

        # ── PAR PRODUIT ──
        with tab_prod_v:
            if c_prod_viz and c_prod_viz in df_tf.columns:
                prod_grp=df_tf.groupby(df_tf[c_prod_viz].astype(str).str.strip()).agg(
                    D1=(tv_d1, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()),
                    D2=(tv_d2, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if tv_d2 else ("D1", lambda x:0),
                    D3=(tv_d3, lambda x: pd.to_numeric(x,errors='coerce').fillna(0).sum()) if tv_d3 else ("D1", lambda x:0),
                ).reset_index()
                prod_grp.columns=[c_prod_viz,"D1","D2","D3"]
                prod_grp["TOTAL"]=prod_grp["D1"]+prod_grp["D2"]+prod_grp["D3"]
                prod_grp=prod_grp[prod_grp["TOTAL"]>0].sort_values("TOTAL",ascending=False)
                if not prod_grp.empty:
                    _pv1,_pv2=st.columns([1,1])
                    with _pv1:
                        fig_pr=go.Figure()
                        fig_pr.add_trace(go.Bar(x=prod_grp[c_prod_viz],y=prod_grp["D1"],name="D1",marker=dict(color="#1565C0",opacity=.85)))
                        if tv_d2: fig_pr.add_trace(go.Bar(x=prod_grp[c_prod_viz],y=prod_grp["D2"],name="D2",marker=dict(color="#C05A00",opacity=.85)))
                        if tv_d3: fig_pr.add_trace(go.Bar(x=prod_grp[c_prod_viz],y=prod_grp["D3"],name="D3",marker=dict(color="#00843D",opacity=.85)))
                        lpr=dict(**PL); lpr['height']=380; lpr['barmode']='stack'; lpr['title']=dict(text="TSP par Produit — D1/D2/D3 (KT)",font=dict(size=13,color="#12202E"))
                        fig_pr.update_layout(**lpr); st.plotly_chart(fig_pr,use_container_width=True)
                    with _pv2:
                        fig_pie_pr=go.Figure(go.Pie(
                            labels=prod_grp[c_prod_viz],values=prod_grp["TOTAL"],
                            hole=.45,textinfo='label+percent',
                            hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
                        fig_pie_pr.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='Barlow,sans-serif'),
                            legend=dict(bgcolor='rgba(255,255,255,.9)',bordercolor='#E0E4EA',borderwidth=1,font=dict(size=10)),
                            margin=dict(l=8,r=8,t=36,b=8),height=380,
                            title=dict(text="Répartition par produit TSP",font=dict(size=12,color="#12202E")))
                        st.plotly_chart(fig_pie_pr,use_container_width=True)
            else:
                st.info("Mappez la colonne Produit pour voir cette visualisation.")

        # ── PAR PORT ──
        with tab_port_v:
            if c_port_viz and c_port_viz in df_tf.columns:
                # ✅ FIX : normalisation majuscules + regroupement par préfixe site connu
                _SITES_BASE = ["JORF", "SAFI", "LAAYOUNE", "KHOURIBGA"]

                def _normalize_port(val):
                    v = str(val).strip().upper()
                    for base in _SITES_BASE:
                        if v.startswith(base):
                            return base
                    return v

                df_tf_port = df_tf.copy()
                df_tf_port["_port_norm"] = df_tf_port[c_port_viz].astype(str).apply(_normalize_port)

                port_grp = df_tf_port.groupby("_port_norm").agg(
                    D1=(tv_d1, lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum()),
                    D2=(tv_d2, lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum()) if tv_d2 else ("D1", lambda x: 0),
                    D3=(tv_d3, lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum()) if tv_d3 else ("D1", lambda x: 0),
                ).reset_index()
                port_grp.columns = ["Port", "D1", "D2", "D3"]
                port_grp["TOTAL"] = port_grp["D1"] + port_grp["D2"] + port_grp["D3"]
                port_grp = port_grp[port_grp["TOTAL"] > 0].sort_values("TOTAL", ascending=False)

                if not port_grp.empty:
                    _ptv1, _ptv2 = st.columns([1, 1])
                    with _ptv1:
                        fig_pt = go.Figure()
                        fig_pt.add_trace(go.Bar(x=port_grp["Port"], y=port_grp["D1"], name="D1", marker=dict(color="#1565C0", opacity=.85)))
                        if tv_d2: fig_pt.add_trace(go.Bar(x=port_grp["Port"], y=port_grp["D2"], name="D2", marker=dict(color="#C05A00", opacity=.85)))
                        if tv_d3: fig_pt.add_trace(go.Bar(x=port_grp["Port"], y=port_grp["D3"], name="D3", marker=dict(color="#00843D", opacity=.85)))
                        lpt = dict(**PL); lpt['height'] = 380; lpt['barmode'] = 'group'
                        lpt['title'] = dict(text="TSP par Port de chargement — D1/D2/D3 (KT)", font=dict(size=13, color="#12202E"))
                        fig_pt.update_layout(**lpt); st.plotly_chart(fig_pt, use_container_width=True)
                    with _ptv2:
                        fig_pie_pt = go.Figure(go.Pie(
                            labels=port_grp["Port"], values=port_grp["TOTAL"],
                            hole=.45, textinfo='label+percent',
                            marker=dict(colors=["#1565C0", "#00843D", "#C05A00", "#6B3FA0", "#C62828"]),
                            hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
                        fig_pie_pt.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Barlow,sans-serif'),
                            legend=dict(bgcolor='rgba(255,255,255,.9)', bordercolor='#E0E4EA', borderwidth=1, font=dict(size=10)),
                            margin=dict(l=8, r=8, t=36, b=8), height=380,
                            title=dict(text="Répartition par port", font=dict(size=12, color="#12202E")))
                        st.plotly_chart(fig_pie_pt, use_container_width=True)
            else:
                st.info("Mappez la colonne Loading Port ou Site pour voir cette visualisation.")

        # ── RÉPARTITION D1/D2/D3 ──
        with tab_dist_v:
            _dv1,_dv2,_dv3=st.columns(3)
            # Waterfall D1/D2/D3
            with _dv1:
                fig_wf=go.Figure(go.Bar(
                    x=["D1 (J1-10)","D2 (J11-20)","D3 (J21+)"],
                    y=[tval_d1,tval_d2,tval_d3],
                    marker=dict(color=["#1565C0","#C05A00","#00843D"],opacity=.9),
                    text=[f"{_ventes_fmt_kt(v)} KT" for v in [tval_d1,tval_d2,tval_d3]],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>%{y:.1f} KT<extra></extra>'
                ))
                lwf=dict(**PL); lwf['height']=360; lwf['title']=dict(text="Volumes D1 / D2 / D3 (KT)",font=dict(size=13,color="#12202E"))
                fig_wf.update_layout(**lwf); st.plotly_chart(fig_wf,use_container_width=True)
            # Donut D1/D2/D3
            with _dv2:
                if ttotal_m>0:
                    fig_d3=go.Figure(go.Pie(
                        labels=["D1","D2","D3"],values=[tval_d1,tval_d2,tval_d3],
                        marker=dict(colors=["#1565C0","#C05A00","#00843D"]),
                        hole=.52,textinfo='label+percent',
                        hovertemplate='<b>%{label}</b><br>%{value:.1f} KT (%{percent})<extra></extra>'))
                    fig_d3.update_layout(paper_bgcolor='rgba(0,0,0,0)',font=dict(family='Barlow,sans-serif'),
                        annotations=[dict(text=f"{_ventes_fmt_kt(ttotal_m)}<br>KT",x=.5,y=.5,font_size=14,showarrow=False,font=dict(color="#12202E",family="Barlow Condensed"))],
                        legend=dict(bgcolor='rgba(255,255,255,.9)',bordercolor='#E0E4EA',borderwidth=1),
                        margin=dict(l=8,r=8,t=36,b=8),height=360,
                        title=dict(text="Répartition D1/D2/D3",font=dict(size=12,color="#12202E")))
                    st.plotly_chart(fig_d3,use_container_width=True)
            # KPIs récap
            with _dv3:
                d1_pct=round(tval_d1/ttotal_m*100,1) if ttotal_m>0 else 0
                d2_pct=round(tval_d2/ttotal_m*100,1) if ttotal_m>0 else 0
                d3_pct=round(tval_d3/ttotal_m*100,1) if ttotal_m>0 else 0
                st.markdown(f'''<div style="background:#F8FAFC;border:1px solid #E0E4EA;border-radius:10px;padding:20px;height:100%">
<div style="font-size:9px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#94A3B8;margin-bottom:16px">RÉCAP DÉCADES</div>
<div style="margin-bottom:14px"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#1565C0">D1 — Jours 1–10</span><span style="font-family:Barlow Condensed,sans-serif;font-size:20px;font-weight:800;color:#1565C0">{_ventes_fmt_kt(tval_d1)} KT</span></div><div style="height:6px;background:#E0E4EA;border-radius:3px;margin-top:4px"><div style="width:{max(3,int(d1_pct))}%;height:6px;background:#1565C0;border-radius:3px"></div></div><div style="font-size:9px;color:#94A3B8;margin-top:2px">{d1_pct}% du total</div></div>
<div style="margin-bottom:14px"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#C05A00">D2 — Jours 11–20</span><span style="font-family:Barlow Condensed,sans-serif;font-size:20px;font-weight:800;color:#C05A00">{_ventes_fmt_kt(tval_d2)} KT</span></div><div style="height:6px;background:#E0E4EA;border-radius:3px;margin-top:4px"><div style="width:{max(3,int(d2_pct))}%;height:6px;background:#C05A00;border-radius:3px"></div></div><div style="font-size:9px;color:#94A3B8;margin-top:2px">{d2_pct}% du total</div></div>
<div style="margin-bottom:14px"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#00843D">D3 — Jours 21+</span><span style="font-family:Barlow Condensed,sans-serif;font-size:20px;font-weight:800;color:#00843D">{_ventes_fmt_kt(tval_d3)} KT</span></div><div style="height:6px;background:#E0E4EA;border-radius:3px;margin-top:4px"><div style="width:{max(3,int(d3_pct))}%;height:6px;background:#00843D;border-radius:3px"></div></div><div style="font-size:9px;color:#94A3B8;margin-top:2px">{d3_pct}% du total</div></div>
<div style="border-top:1px solid #E0E4EA;padding-top:12px;display:flex;justify-content:space-between;align-items:center"><span style="font-size:12px;font-weight:700;color:#12202E">TOTAL</span><span style="font-family:Barlow Condensed,sans-serif;font-size:24px;font-weight:900;color:#12202E">{_ventes_fmt_kt(ttotal_m)} KT</span></div>
</div>''',unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#F2F4F7;border:1px dashed #E0E4EA;border-radius:10px;padding:20px;text-align:center;color:#94A3B8;font-size:12px">Appliquez des filtres pour voir les visualisations TSP</div>',unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # 4. TABLEAU — Pipeline TSP filtré (uniquement produits TSP)
    # ════════════════════════════════════════════════════
    st.markdown('<div class="stitle">Tableau Pipeline TSP — données filtrées</div>',unsafe_allow_html=True)
    trole_order=["bl_month","phys_month","work_month","del_month","confirmation","pays","macro_qualite","produit","d1","d2","d3","status","loading_port","site"]
    tcols_display=[]; tseen=set()
    for trk in trole_order:
        tc=vmap_tsp.get(trk)
        if tc and tc in df_tf.columns and tc not in tseen: tcols_display.append(tc); tseen.add(tc)
    for tc in df_tf.columns:
        if tc not in tseen: tcols_display.append(tc); tseen.add(tc)
    df_tdisp=df_tf[tcols_display].copy()
    tcfg_cols={}
    for trk in ["d1","d2","d3"]:
        tc=vmap_tsp.get(trk)
        if tc and tc in df_tdisp.columns: tcfg_cols[tc]=st.column_config.NumberColumn(tc,format="%.1f")
    st.dataframe(df_tdisp, use_container_width=True, hide_index=True, height=min(700, 48+35*len(df_tdisp)), column_config=tcfg_cols)
    st.caption(f"{len(df_tf)} ligne(s) TSP affichée(s) — {len(df_base_tsp)} total TSP dans le fichier")
  

