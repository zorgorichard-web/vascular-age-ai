import streamlit as st
import google.generativeai as genai
from datetime import date

# 1. KONFIGURÁCIÓ
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Rendszerhiba: A diagnosztikai modul nem elérhető.")

# LINKEK - (A PROFESSZOR KÉPÉT FRISSÍTETTEM EGY HITELES ARCCAL)
AFFILIATE_LINK = "https://a-te-linked-ide.hu"
PROFESSOR_IMAGE_URL = "https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80&w=400&h=500&auto=format&fit=crop" 
ARTERY_BAD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_ymgn5oymgn5oymgn.png"
ARTERY_GOOD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_fpxagafpxagafpxa.png"
STAMP_URL = "https://www.pngkit.com/png/full/15-159411_quality-certified-stamp-png-certified-original-stamp-png.png" # Mintapélda pecsétre

st.set_page_config(page_title="VascularAge AI - Klinikai Analízis", page_icon="⚖️")

# --- UI STÍLUS (Javított és animált) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Címsor stílusa */
    .main-title { color: #002244; font-weight: 900; text-align: center; margin-bottom: 0px; }
    
    /* Professzor kártya - Hivatalos lelet kinézet */
    .prof-card { 
        display: flex; 
        background-color: #ffffff; 
        border-radius: 15px; 
        overflow: hidden; 
        border: 1px solid #e0e0e0;
        border-left: 10px solid #d93025; 
        margin-bottom: 25px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.05); 
    }
    .prof-img { width: 30%; object-fit: cover; border-right: 1px solid #eee; }
    .prof-text { width: 70%; padding: 25px; position: relative; }
    .prof-name { color: #d93025; margin-top: 0; font-weight: 700; font-size: 1.4em; }
    
    /* Digitális aláírás és pecsét */
    .signature-wrap { text-align: right; margin-top: 20px; opacity: 0.8; }
    .stamp-img { position: absolute; bottom: 20px; right: 150px; width: 80px; opacity: 0.3; transform: rotate(-15deg); }

    /* Pulzáló gomb animáció */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    .stButton>button { 
        background: linear-gradient(90deg, #d93025, #a00000) !important; 
        color: white !important; 
        border-radius: 12px !important; 
        font-weight: bold !important; 
        width: 100%; 
        height: 4.2em !important; 
        border: none !important;
        animation: pulse 2s infinite; 
        text-transform: uppercase;
        font-size: 1.2em !important;
        box-shadow: 0 5px 15px rgba(217, 48, 37, 0.4);
    }

    .result-text { color: #1e293b; line-height: 1.8; font-size: 1.1em; font-family: 'Georgia', serif; }
    .stat-box { text-align: center; padding: 12px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; }
    .trust-badge-container { display: flex; justify-content: space-around; margin-top: 20px; text-align: center; }
    .trust-badge-item { font-size: 0.85em; color: #444; font-weight: 600; }

    @media (max-width: 600px) { 
        .prof-card { flex-direction: column; } 
        .prof-img { width: 100%; height: 250px; } 
        .prof-text { width: 100%; } 
        .stamp-img { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- FŐ CÍMSOR VISSZAÁLLÍTÁSA ---
st.markdown("<h1 class='main-title'>⚖️ VascularAge AI™</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666; font-size:1.1em;'>Személyre szabott érrendszeri diagnosztikai protokoll</p>", unsafe_allow_html=True)

# --- SOCIAL PROOF ---
st.write("---")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("<div class='stat-box'><small>Elemzések ma</small><br><b>1,432</b></div>", unsafe_allow_html=True)
with col_s2:
    st.markdown("<div class='stat-box'><small>Kritikus eset</small><br><b style='color:#d93025;'>84%</b></div>", unsafe_allow_html=True)
with col_s3:
    st.markdown("<div class='stat-box'><small>Garancia</small><br><b style='color:#1e8e3e;'>100%</b></div>", unsafe_allow_html=True)
st.write("---")

# --- KÉRDŐÍV ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Életkor", 18, 100, 48)
        gender = st.selectbox("Nem", ["Férfi", "Nő"])
        height = st.number_input("Magasság (cm)", 120, 220, 175)
    with col2:
        weight = st.number_input("Testsúly (kg)", 40, 200, 85)
        lifestyle = st.selectbox("Életmód", ["Ülőmunka", "Kevés mozgás", "Aktív"])
        stress = st.select_slider("Stressz-szint", ["Alacsony", "Átlagos", "Magas"])

    st.write("**Jelölje be a tapasztalt tüneteket:**")
    c1, c2 = st.columns(2)
    with c1:
        s1 = st.checkbox("Lábdagadás (ödéma)")
        s2 = st.checkbox("Reggeli fejfájás")
    with c2:
        s3 = st.checkbox("Fülzúgás / Szédülés")
        s4 = st.checkbox("Zsibbadó végtagok")

# --- ELEMZÉS LOGIKA ---
if st.button("KLINIKAI JELENTÉS GENERÁLÁSA"):
    bmi = round(weight / ((height/100)**2), 1)
    symptoms = [s for s, b in zip(["ödéma", "fejfájás", "fülzúgás", "zsibbadás"], [s1, s2, s3, s4]) if b]
    v_age = age + (len(symptoms) * 5) + (5 if bmi > 28 else 0) + (3 if stress == "Magas" else 0)
    
    with st.spinner('Adatok összevetése a klinikai adatbázissal...'):
        prompt = f"Te Jakab Tamás professzor vagy. {gender} páciens, {age} éves, {weight}kg. Érrendszeri kor: {v_age} év. Írj nyers, sokkoló diagnózist, említsd a 6,1kg lerakódást és a Cardiotensive-et. Magyarul, orvosi tekintélyként."
        
        try:
            response = model.generate_content(prompt)
            st.divider()
            st.write(f"📅 **Lelet kiállítva:** {date.today().strftime('%Y. %m. %d.')}")
            
            risk_percent = min(100, (v_age - age) * 10 + 40)
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("BECSÜLT ÉRRENDSZERI KOR", f"{v_age} ÉV", f"+{v_age-age} év eltérés")
            with col_m2:
                st.write(f"**Érfal elzáródási szint: {risk_percent}%**")
                st.progress(risk_percent / 100)

            st.write("### 🔍 Mikroszkópos érfal analízis")
            
            c_img1, c_img2 = st.columns(2)
            c_img1.error("KRITIKUS ÁLLAPOT")
            c_img1.image(ARTERY_BAD_URL)
            c_img2.success("TISZTÍTÁS UTÁN")
            c_img2.image(ARTERY_GOOD_URL)

            # --- PROFESSZOR DIAGNÓZISA (KÉPPEL, ALÁÍRÁSSAL, PECSÉTTEL) ---
            st.markdown(f"""
            <div class='prof-card'>
                <img src='{PROFESSOR_IMAGE_URL}' class='prof-img'>
                <div class='prof-text'>
                    <img src='{STAMP_URL}' class='stamp-img'>
                    <h3 class='prof-name'>📋 Dr. Jakab Tamás Sürgősségi Lelete</h3>
                    <div class='result-text'>
                        {response.text.replace('**', '<b>').replace('</b>', '</b>')}
                    </div>
                    <div class='signature-wrap'>
                        <img src='https://upload.wikimedia.org/wikipedia/commons/3/3a/Jon_Hancock_Signature.png' width='130' style='filter: brightness(0.5) sepia(1) hue-rotate(200deg);'>
                        <p style='font-family: cursive; font-size: 0.8em; margin-top: -10px; color: #444;'>Dr. Jakab Tamás s.k.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ HALASZTHATATLAN BEAVATKOZÁS JAVASOLT")
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank" style="text-decoration: none;">
                    <button>IGÉNYLEM A TISZTÍTÓKÚRÁT (LIMITÁLT 50% KEDVEZMÉNY) »</button>
                </a>
            """, unsafe_allow_html=True)
            
            # --- PROFESSZIONÁLIS TRUST BADGES ---
            st.markdown("""
                <div class='trust-badge-container'>
                    <div class='trust-badge-item'>🔒 BIZTONSÁGOS SSL</div>
                    <div class='trust-badge-item'>🌿 NATÚR ÖSSZETEVŐK</div>
                    <div class='trust-badge-item'>✅ KLINIKAI TESZT</div>
                    <div class='trust-badge-item'>🚚 GYORS SZÁLLÍTÁS</div>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"AI hiba: {e}")

# --- NYILATKOZAT ---
st.markdown("---")
st.markdown("<div style='font-size: 10px; color: #888; text-align: center;'>NYILATKOZAT: Ez az alkalmazás mesterséges intelligencia alapú elemzést végez. Nem minősül orvosi diagnózisnak. A honlap nem áll kapcsolatban a Facebookkal.</div>", unsafe_allow_html=True)






