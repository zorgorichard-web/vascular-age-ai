import streamlit as st
import google.generativeai as genai

# 1. KONFIGURÁCIÓ
API_KEY = "AIzaSyA0mRb_Ance9eUvUGpVKHfUIoIC-wXnL24" # A fizetős kulcsod
AFFILIATE_LINK = "https://a-te-link-helye.hu" # IDE ÍRD A VÉGLEGES LINKET

# HASZNÁLD EZT:
import streamlit as st

# A kulcsot a Streamlit "titkos" beállításaiból olvassuk ki
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# --- OLDAL BEÁLLÍTÁSA ---
st.set_page_config(page_title="VascularAge AI - Klinikai Elemző", page_icon="⚖️", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #ffffff; }
    .stButton>button { 
        background: linear-gradient(135deg, #003366 0%, #004080 100%); 
        color: white; border-radius: 8px; padding: 1rem; font-weight: bold; border: none; width: 100%;
    }
    .report-card { 
        background-color: #f0f7ff; padding: 25px; border-radius: 15px; 
        border: 1px solid #cce3ff; color: #002244; line-height: 1.7;
    }
    .metric-box { text-align: center; padding: 15px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- FEJLÉC ---
st.title("⚖️ VascularAge AI™")
st.write("#### Precíziós érrendszeri állapotfelmérés és kockázati analízis")
st.divider()

# --- ADATBEVITEL ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Életkor", 18, 100, 48)
        gender = st.selectbox("Nem", ["Férfi", "Nő"])
        weight_status = st.select_slider("Testsúly index", options=["Optimális", "Enyhe túlsúly", "Kifejezett túlsúly"])
    with col2:
        lifestyle = st.selectbox("Életmód", ["Ülőmunka", "Kevés mozgás", "Aktív életmód"])
        stress = st.selectbox("Stressz-szint", ["Alacsony", "Átlagos", "Kritikus"])
        blood_pressure = st.selectbox("Ismert vérnyomás profil", ["Normál", "Ingadozó", "Diagnosztizált hipertónia"])

    st.write("---")
    st.write("**Klinikai tünetek monitorozása (Jelölje be):**")
    c1, c2 = st.columns(2)
    with c1:
        s1 = st.checkbox("Alsó végtagi ödéma (lábdagadás)")
        s2 = st.checkbox("Reggeli fejfájás / Nyaki merevség")
    with c2:
        s3 = st.checkbox("Fülzúgás / Szédüléses epizódok")
        s4 = st.checkbox("Végtagzsibbadás / Hideg végtagok")

# --- ANALÍZIS LOGIKA ---
if st.button("KLINIKAI JELENTÉS GENERÁLÁSA"):
    symptoms = []
    if s1: symptoms.append("alsó végtagi ödéma")
    if s2: symptoms.append("reggeli hipertóniás fejfájás")
    if s3: symptoms_list = "tinnitus és vestibuláris zavarok"
    if s4: symptoms.append("perifériás keringési zavar (zsibbadás)")

    # Biológiai kor becslés
    v_age = age + (len(symptoms) * 4) + (5 if blood_pressure == "Diagnosztizált hipertónia" else 0)
    
    with st.spinner('AI Diagnosztikai protokoll futtatása...'):
        system_prompt = f"""
        Te egy vezető kardiológus professzor vagy. Elemezd a pácienst: 
        Kor: {age}, Nem: {gender}, Életmód: {lifestyle}, Súly: {weight_status}, Stressz: {stress}, Vérnyomás: {blood_pressure}, Tünetek: {', '.join(symptoms)}.
        
        A feladatod:
        1. Érrendszeri életkor: {v_age} év.
        2. Tudományos magyarázat: Miért okoznak ezek a tünetek érfal-károsodást (koleszterin plakkok, kalcium sók).
        3. Megoldás: Miért kulcsfontosságú az erek tisztítása olajfalevéllel és galagonyával.
        4. Sürgősség: Miért nem szabad halogatni a kezelést.
        
        Stílus: Orvosi tekintélyt sugárzó, de érthető és meggyőző. Ne használj listákat, folyószöveget írj.
        """

        try:
            response = model.generate_content(system_prompt)
            
            # --- EREDMÉNYEK ---
            st.success("Analízis kész.")
            
            st.divider()
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"""
                <div class="metric-box">
                    <p style="font-size: 14px; color: #666;">Becsült érrendszeri kor</p>
                    <h1 style="color: #d93025; margin: 0;">{v_age} év</h1>
                    <p style="color: {'#d93025' if v_age > age else '#1e8e3e'}">{v_age - age} év eltérés</p>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)

            # --- CALL TO ACTION ---
            st.markdown(f"""
                <div style="background: #fff3f3; padding: 30px; border-radius: 15px; margin-top: 30px; border: 2px solid #d93025; text-align: center;">
                    <h3 style="color: #d93025; margin-top: 0;">⚠️ Halaszthatatlan beavatkozás javasolt</h3>
                    <p>Az Ön profilja alapján az érfalak megtisztítása és a koleszterin-lerakódások feloldása elsődleges fontosságú.</p>
                    <a href="{AFFILIATE_LINK}" target="_blank" style="text-decoration: none;">
                        <button style="background: #d93025; color: white; padding: 20px 40px; border-radius: 10px; font-size: 20px; font-weight: bold; border: none; cursor: pointer; width: 100%;">
                            KÉREM A JAVASOLT KÚRÁT (50% KEDVEZMÉNY) >>
                        </button>
                    </a>
                    <p style="font-size: 12px; margin-top: 10px; color: #666;">*A kedvezményes program 2026. 01. 07-ig érvényes.</p>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Hiba az elemzés során: {e}")