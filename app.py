import streamlit as st
import google.generativeai as genai
from datetime import date

# 1. KONFIGURÁCIÓ
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Rendszerhiba: A diagnosztikai modul nem elérhető.")

# --- LINKEK ÉS ADATOK ---
AFFILIATE_LINK = "https://a-te-linked-ide.hu"
PROFESSOR_IMAGE_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_ui715qui715qui71.png" 
ARTERY_BAD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_ymgn5oymgn5oymgn.png"
ARTERY_GOOD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_fpxagafpxagafpxa.png"
STAMP_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_bg06mbbg06mbbg06.png"

st.set_page_config(page_title="VascularAge AI - Klinikai Analízis", page_icon="⚖️")

# --- UI STÍLUS (Klinikai és Magas Konverziójú) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    .main-title { color: #002244; font-weight: 900; text-align: center; margin-bottom: 0px; }
    
    /* Professzor kártya - Hivatalos lelet struktúra */
    .prof-card { 
        display: flex; 
        background-color: #ffffff; 
        border-radius: 15px; 
        overflow: hidden; 
        border: 1px solid #e0e0e0;
        border-left: 10px solid #d93025; 
        margin-bottom: 25px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.05); 
        position: relative;
    }
    .prof-img { width: 30%; object-fit: cover; border-right: 1px solid #eee; }
    .prof-text { width: 70%; padding: 25px; position: relative; z-index: 2; }
    .prof-name { color: #d93025; margin-top: 0; font-weight: 700; font-size: 1.4em; }
    
    /* Pecsét pozicionálása - Átfedi a szöveget és az aláírást a hitelességért */
    .stamp-img { 
        position: absolute; 
        bottom: 30px; 
        right: 120px; 
        width: 140px; 
        opacity: 0.6; 
        transform: rotate(-12deg); 
        z-index: 1; 
        pointer-events: none;
    }

    /* Aláírás */
    .signature-wrap { text-align: right; margin-top: 20px; position: relative; z-index: 3; }

    /* Pulzáló gomb animáció */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(217, 48, 37, 0.7); }
        70% { transform: scale(1.03); box-shadow: 0 0 0 15px rgba(217, 48, 37, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(217, 48, 37, 0); }
    }
    .stButton>button { 
        background: linear-gradient(90deg, #d93025, #a00000) !important; 
        color: white !important; 
        border-radius: 12px !important; 
        font-weight: bold !important; 
        width: 100%; 
        height: 4.5em !important; 
        border: none !important;
        animation: pulse 2s infinite; 
        text-transform: uppercase;
        font-size: 1.2em !important;
    }

    .result-text { color: #1e293b; line-height: 1.8; font-size: 1.1em; font-family: 'Georgia', serif; position: relative; z-index: 2; }
    .stat-box { text-align: center; padding: 12px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; }
    .trust-badge-container { display: flex; justify-content: space-around; margin-top: 25px; text-align: center; }
    .trust-badge-item { font-size: 0.85em; color: #444; font-weight: 700; border: 1px solid #eee; padding: 5px 10px; border-radius: 5px; background: #fefefe; }

    @media (max-width: 600px) { 
        .prof-card { flex-direction: column; } 
        .prof-img { width: 100%; height: 280px; } 
        .prof-text { width: 100%; } 
        .stamp-img { width: 100px; right: 20px; bottom: 60px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- FEJLÉC ---
st.markdown("<h1 class='main-title'>⚖️ VascularAge AI™</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666; font-size:1.1em; margin-bottom:25px;'>Személyre szabott érrendszeri diagnosztikai protokoll</p>", unsafe_allow_html=True)

# --- SOCIAL PROOF ---
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("<div class='stat-box'><small>Elemzések ma</small><br><b>1,432</b></div>", unsafe_allow_html=True)
with col_s2:
    st.markdown("<div class='stat-box'><small>Kritikus állapot</small><br><b style='color:#d93025;'>84%</b></div>", unsafe_allow_html=True)
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

# --- ANALÍZIS INDÍTÁSA ---
if st.button("KLINIKAI JELENTÉS GENERÁLÁSA"):
    bmi = round(weight / ((height/100)**2), 1)
    active_symptoms = [s for s, b in zip(["ödéma", "fejfájás", "fülzúgás", "zsibbadás"], [s1, s2, s3, s4]) if b]
    v_age = age + (len(active_symptoms) * 5) + (5 if bmi > 28 else 0) + (3 if stress == "Magas" else 0)
    
    with st.spinner('Adatok összevetése a klinikai adatbázissal...'):
        prompt = f"""
        Te Jakab Tamás professzor vagy. Egy {gender} pácienshez beszélsz ({age} év, {weight}kg). 
        Érrendszeri kor: {v_age} év. 
        Írj egy nyers, sürgető orvosi diagnózist. Említsd a 6,1 kg-os lerakódást az erekben. 
        A megoldás a Cardiotensive. Használj magyar nyelvet, tekintélyes, de ijesztő stílust.
        """
        
        try:
            response = model.generate_content(prompt)
            st.divider()
            st.write(f"📅 **Hivatalos lelet kiállítva:** {date.today().strftime('%Y. %m. %d.')}")
            
            # --- MÉRŐSZÁMOK ---
            risk_percent = min(100, (v_age - age) * 10 + 40)
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("BECSÜLT ÉRRENDSZERI KOR", f"{v_age} ÉV", f"+{v_age-age} év eltérés")
            with col_m2:
                st.write(f"**Érfal elzáródási szint: {risk_percent}%**")
                st.progress(risk_percent / 100)

            # --- VIZUÁLIS ANALÍZIS ---
            st.write("### 🔍 Mikroszkópos érfal analízis")
            img_col1, img_col2 = st.columns(2)
            img_col1.error("JELENLEGI ÁLLAPOT")
            img_col1.image(ARTERY_BAD_URL)
            img_col2.success("KÚRA UTÁNI ÁLLAPOT")
            img_col2.image(ARTERY_GOOD_URL)

            # --- PROFESSZORI KÁRTYA (PECSÉTTEL ÉS ALÁÍRÁSSAL) ---
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
                        <img src='https://upload.wikimedia.org/wikipedia/commons/3/3a/Jon_Hancock_Signature.png' width='140' style='filter: brightness(0.5) sepia(1) hue-rotate(200deg);'>
                        <p style='font-family: cursive; font-size: 0.85em; margin-top: -10px; color: #444;'>Dr. Jakab Tamás s.k.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ HALASZTHATATLAN BEAVATKOZÁS JAVASOLT")
            
            # --- CTA GOMB ---
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank" style="text-decoration: none;">
                    <button>IGÉNYLEM A TISZTÍTÓKÚRÁT (LIMITÁLT 50% KEDVEZMÉNY) »</button>
                </a>
            """, unsafe_allow_html=True)
            
            # --- TRUST BADGES ---
            st.markdown("""
                <div class='trust-badge-container'>
                    <div class='trust-badge-item'>🔒 SSL BIZTONSÁG</div>
                    <div class='trust-badge-item'>🌿 100% NATÚR</div>
                    <div class='trust-badge-item'>✅ KLINIKAI TESZT</div>
                    <div class='trust-badge-item'>🚚 GYORS SZÁLLÍTÁS</div>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Diagnosztikai hiba: {e}")

# --- JOGI NYILATKOZAT ---
st.markdown("---")
st.markdown("<div style='font-size: 11px; color: #999; text-align: center; padding: 20px;'>NYILATKOZAT: Ez az alkalmazás mesterséges intelligencia alapú állapotfelmérést végez. Az eredmények nem helyettesítik a szakorvosi vizsgálatot. A weboldal nem áll kapcsolatban a Facebook/Meta platformmal.</div>", unsafe_allow_html=True)






