import streamlit as st
import google.generativeai as genai

# 1. KONFIGURÁCIÓ
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Rendszerhiba: A diagnosztikai modul nem elérhető.")

# Ide jön a végleges AdCombo linked
AFFILIATE_LINK = "https://a-te-linked-ide.hu" 

st.set_page_config(page_title="VascularAge AI - Klinikai Analízis", page_icon="⚖️")

# --- UI STÍLUS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-card { background-color: #fcfcfc; padding: 30px; border-radius: 15px; border: 1px solid #e0e0e0; border-left: 10px solid #d93025; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .stButton>button { background: linear-gradient(90deg, #002244, #004488); color: white; border-radius: 8px; font-weight: bold; width: 100%; height: 3.5em; border: none; font-size: 1.1em; }
    .result-text { color: #1e293b; line-height: 1.8; font-size: 1.15em; font-family: 'Georgia', serif; }
    .stat-box { text-align: center; padding: 10px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ VascularAge AI™")
st.write("#### Személyre szabott érrendszeri diagnosztikai protokoll")

# --- SOCIAL PROOF (Bizalomépítő adatok) ---
st.write("---")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("<div class='stat-box'><small>Ma elvégzett elemzés</small><br><b>1,432</b></div>", unsafe_allow_html=True)
with col_s2:
    st.markdown("<div class='stat-box'><small>Kritikus állapot</small><br><b style='color:#d93025;'>84%</b></div>", unsafe_allow_html=True)
with col_s3:
    st.markdown("<div class='stat-box'><small>Aktív kedvezmény</small><br><b style='color:#1e8e3e;'>50%</b></div>", unsafe_allow_html=True)
st.write("---")

# --- KÉRDŐÍV ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Életkor", 18, 100, 48)
        lifestyle = st.selectbox("Életmód", ["Ülőmunka", "Kevés mozgás", "Aktív"])
    with col2:
        weight_status = st.selectbox("Testsúly", ["Normál", "Túlsúly"])
        stress = st.select_slider("Stressz-szint", ["Alacsony", "Átlagos", "Magas"])

    st.write("**Jelölje be, ha az alábbiakat tapasztalja:**")
    c1, c2 = st.columns(2)
    with c1:
        s1 = st.checkbox("Lábdagadás (ödéma)")
        s2 = st.checkbox("Reggeli fejfájás")
    with c2:
        s3 = st.checkbox("Fülzúgás / Szédülés")
        s4 = st.checkbox("Zsibbadó végtagok")

# --- ELEMZÉS ---
if st.button("KLINIKAI JELENTÉS GENERÁLÁSA"):
    symptoms = []
    if s1: symptoms.append("ödéma")
    if s2: symptoms.append("reggeli fejfájás")
    if s3: symptoms.append("fülzúgás")
    if s4: symptoms.append("zsibbadás")
    
    v_age = age + (len(symptoms) * 5) + (3 if weight_status == "Túlsúly" else 0)
    
    # PSZICHOLÓGIAI SPINNER
    with st.spinner('Jakab professzor éppen elemzi az Ön biológiai markereit... Ez aggasztónak tűnik.'):
        
        prompt = f"""
        Te Jakab Tamás professzor vagy, érrendszeri specialista. Egy 50+ éves emberhez beszélsz, aki fél.
        Adatok: Kor: {age}, Tünetek: {', '.join(symptoms)}. Érrendszeri kor: {v_age} év.

        Írj egy nyers, drasztikus, de segítőkész elemzést:
        - Mondd ki: amit érez, az a SZERVEZETE SEGÉLYKIÁLTÁSA.
        - Használd: "6,1 kg lerakódás az erekben", "időzített bomba a véráramban".
        - Ne kertelj: ha nem tisztítja ki az ereit, a következő állomás a rohammentő.
        - A Cardiotensive az EGYETLEN esélye, hogy "kibelezze" ezt a koszt a rendszeréből.
        - Stílus: rövid, ütős mondatok, orvosi tekintély, nulla AI sallang.
        """
        
        try:
            response = model.generate_content(prompt)
            
            st.divider()

            # --- MÉRŐSZÁMOK ---
            risk_percent = min(100, (v_age - age) * 10 + 40)
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("BECSÜLT ÉRRENDSZERI KOR", f"{v_age} ÉV", f"+{v_age-age} év eltérés")
            with col_m2:
                st.write(f"**Érfal elzáródási szint: {risk_percent}%**")
                st.progress(risk_percent / 100)

            # --- VIZUÁLIS SOKK ---
            st.write("### 🔍 Mikroszkópos érfal analízis")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.error("KRITIKUS ÁLLAPOT")
                st.image("https://img.freepik.com/free-photo/clogged-artery-with-cholesterol-plaque_1048-12444.jpg", caption="Jelenlegi lerakódások")
            with col_img2:
                st.success("TISZTÍTÁS UTÁN")
                st.image("https://img.freepik.com/free-photo/healthy-artery-without-plaque_1048-12445.jpg", caption="Optimális keringés")

            # --- PROFESSZORI LELET ---
            st.markdown(f"""
            <div class='main-card'>
                <h3 style="color: #d93025; margin-top:0;">📋 Jakab Professzor Sürgősségi Diagnózisa</h3>
                <div class='result-text'>
                    {response.text.replace('**', '<b>').replace('</b>', '</b>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ HALASZTHATATLAN BEAVATKOZÁS JAVASOLT")
            
            # CALL TO ACTION GOMB
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank" style="text-decoration: none;">
                    <button style="width:100%; padding:25px; background: linear-gradient(90deg, #d93025, #a00000); color:white; font-size:22px; font-weight:bold; border:none; border-radius:12px; cursor:pointer; box-shadow: 0 10px 25px rgba(217, 48, 37, 0.4);">
                        IGÉNYLEM A TISZTÍTÓKÚRÁT (LIMITÁLT 50% KEDVEZMÉNY) »
                    </button>
                </a>
            """, unsafe_allow_html=True)
            st.caption("<center>Kattintson a fenti gombra a kedvezményes program megnyitásához.</center>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error("A szerver túlterhelt. Kérjük, várjon 10 másodpercet.")
