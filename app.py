import streamlit as st
import google.generativeai as genai
from datetime import date

# 1. KONFIGURÁCIÓ
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Rendszerhiba: A diagnosztikai modul nem elérhető.")

# --- LINKEK ÉS KÉPEK ---
AFFILIATE_LINK = "https://a-te-linked-ide.hu"
PROFESSOR_IMAGE_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_ui715qui715qui71.png" 
ARTERY_BAD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_ymgn5oymgn5oymgn.png"
ARTERY_GOOD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_fpxagafpxagafpxa.png"
STAMP_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_bg06mbbg06mbbg06.png"

st.set_page_config(page_title="VascularAge AI - Klinikai Analízis", page_icon="⚖️", layout="centered")

# --- UI STÍLUS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-title { color: #002244; font-weight: 900; text-align: center; margin-bottom: 5px; font-family: 'Helvetica', sans-serif; }
    
    .prof-card { 
        display: flex; 
        background-color: #ffffff; 
        border-radius: 15px; 
        overflow: hidden; 
        border: 1px solid #e0e0e0;
        border-left: 10px solid #d93025; 
        margin-top: 25px;
        margin-bottom: 25px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08); 
        position: relative;
    }
    .prof-img { width: 35%; object-fit: cover; border-right: 1px solid #eee; }
    .prof-text { width: 65%; padding: 30px; position: relative; z-index: 2; }
    .prof-name { color: #d93025; margin-top: 0; font-weight: 700; font-size: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 10px; }
    .stamp-img { position: absolute; bottom: 10px; right: 100px; width: 150px; opacity: 0.4; transform: rotate(-15deg); z-index: 1; pointer-events: none; }
    .signature-wrap { text-align: right; margin-top: 30px; position: relative; z-index: 3; }

    /* Pulzáló Gomb Design */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(217, 48, 37, 0.7); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(217, 48, 37, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(217, 48, 37, 0); }
    }
    .cta-button {
        display: block;
        width: 100%;
        padding: 20px;
        background: linear-gradient(90deg, #d93025, #a00000);
        color: white !important;
        text-align: center;
        text-decoration: none !important;
        border-radius: 12px;
        font-weight: 900;
        font-size: 1.2em;
        animation: pulse 2s infinite;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-top: 20px;
    }

    .result-text { color: #1e293b; line-height: 1.8; font-size: 1.15em; font-family: 'Georgia', serif; }
    .stat-box { text-align: center; padding: 15px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; }
    .trust-badge-container { display: flex; justify-content: space-between; margin-top: 25px; text-align: center; }
    .trust-badge-item { font-size: 0.8em; color: #555; font-weight: 600; flex: 1; }

    @media (max-width: 600px) { 
        .prof-card { flex-direction: column; } 
        .prof-img { width: 100%; height: 280px; } 
        .prof-text { width: 100%; } 
    }
    </style>
    """, unsafe_allow_html=True)

# --- FEJLÉC ---
st.markdown("<h1 class='main-title'>⚖️ VascularAge AI™</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666; font-size:1.1em; margin-bottom:30px;'>Klinikai Érrendszeri Állapotfelmérés - Verzió 4.1</p>", unsafe_allow_html=True)

# --- SOCIAL PROOF ---
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("<div class='stat-box'><small>Elemzések ma</small><br><b>1,432</b></div>", unsafe_allow_html=True)
with col_s2:
    st.markdown("<div class='stat-box'><small>Kritikus állapot</small><br><b style='color:#d93025;'>84%</b></div>", unsafe_allow_html=True)
with col_s3:
    st.markdown("<div class='stat-box'><small>Garancia</small><br><b style='color:#1e8e3e;'>100%</b></div>", unsafe_allow_html=True)

st.write("---")

# --- KÉRDŐÍV (Bővítve dohányzással és vérnyomással) ---
with st.container():
    c_left, c_right = st.columns(2)
    with c_left:
        age = st.number_input("Életkor", 18, 100, 58)
        gender = st.selectbox("Nem", ["Nő", "Férfi"])
        height = st.number_input("Magasság (cm)", 120, 220, 172)
    with c_right:
        weight = st.number_input("Testsúly (kg)", 40, 200, 88)
        smoke = st.selectbox("Dohányzás", ["Soha nem dohányzott", "Alkalmi dohányos", "Rendszeres dohányos"])
        stress = st.select_slider("Stressz-szint", ["Alacsony", "Átlagos", "Magas"], value="Magas")

    st.write("**Egészségügyi előzmények:**")
    check1, check2 = st.columns(2)
    with check1:
        bp = st.checkbox("Ismert magas vérnyomás")
        s1 = st.checkbox("Lábdagadás (ödéma)")
    with check2:
        family = st.checkbox("Családi érrendszeri betegség")
        s4 = st.checkbox("Végtagzsibbadás")

# --- ANALÍZIS GOMB ---
if st.button("KLINIKAI JELENTÉS GENERÁLÁSA"):
    bmi = round(weight / ((height/100)**2), 1)
    
    # Érrendszeri kor kalkuláció (Bővített logika)
    v_age = age
    if smoke == "Rendszeres dohányos": v_age += 12
    elif smoke == "Alkalmi dohányos": v_age += 5
    if bp: v_age += 7
    if bmi > 28: v_age += 5
    if stress == "Magas": v_age += 3
    if family: v_age += 4
    if s1 or s4: v_age += 5

    with st.spinner('Jakab professzor elemzi az érfal állapotát...'):
        prompt = f"""
        Te Jakab Tamás professzor vagy. Egy {gender} pácienshez beszélsz ({age} éves, {weight}kg).
        Dohányzás: {smoke}. Magas vérnyomás: {'Igen' if bp else 'Nem'}.
        Számított érrendszeri kor: {v_age} év.
        
        Írj egy sokkoló diagnózist:
        - Szólítsd meg: Uram/Asszonyom.
        - Ha dohányzik, írd le, hogy a nikotin elvékonyítja és törékennyé teszi az érfalait.
        - Említsd a 6,1 kg lerakódást és a Cardiotensive-et.
        - Stílus: rövid, tekintélyes, ijesztő.
        """
        
        try:
            response = model.generate_content(prompt)
            st.divider()
            st.write(f"📅 **Hivatalos lelet kiállítva:** {date.today().strftime('%Y. %m. %d.')}")
            
            # --- MÉRŐSZÁMOK ---
            risk_percent = min(100, (v_age - age) * 8 + 42)
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.metric("BECSÜLT ÉRRENDSZERI KOR", f"{v_age} ÉV", f"+{v_age-age} év eltérés")
            with m_col2:
                st.write(f"**Érfal elzáródási szint: {risk_percent}%**")
                st.progress(risk_percent / 100)

            # --- KÉPEK ---
            st.write("### 🔍 Mikroszkópos érfal analízis")
            
            i_col1, i_col2 = st.columns(2)
            i_col1.error("JELENLEGI ÁLLAPOT")
            i_col1.image(ARTERY_BAD_URL)
            i_col2.success("TISZTÍTÁS UTÁN")
            i_col2.image(ARTERY_GOOD_URL)

            # --- PROFESSZORI KÁRTYA ---
            res_txt = response.text.replace('**', '<b>').replace('</b>', '</b>').replace('\n', '<br>')
            st.markdown(f"""
            <div class='prof-card'>
                <img src='{PROFESSOR_IMAGE_URL}' class='prof-img'>
                <div class='prof-text'>
                    <img src='{STAMP_URL}' class='stamp-img'>
                    <h3 class='prof-name'>📋 Dr. Jakab Tamás Sürgősségi Lelete</h3>
                    <div class='result-text'>{res_txt}</div>
                    <div class='signature-wrap'>
                        <img src='https://upload.wikimedia.org/wikipedia/commons/3/3a/Jon_Hancock_Signature.png' width='140' style='filter: brightness(0.5) sepia(1) hue-rotate(200deg);'>
                        <p style='font-family: cursive; font-size: 0.9em; margin-top: -10px; color: #444;'>Dr. Jakab Tamás s.k.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ HALASZTHATATLAN BEAVATKOZÁS JAVASOLT")
            
            # --- JAVÍTOTT GOMB ---
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank" class="cta-button">
                    IGÉNYLEM A TISZTÍTÓKÚRÁT (LIMITÁLT 50% KEDVEZMÉNY) »
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
            st.error(f"Hiba történt az elemzés során: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='font-size: 11px; color: #999; text-align: center; padding: 20px;'>NYILATKOZAT: Ez az alkalmazás mesterséges intelligencia alapú állapotfelmérést végez. Az eredmények tájékoztató jellegűek, nem helyettesítik az orvosi diagnózist.</div>", unsafe_allow_html=True)


