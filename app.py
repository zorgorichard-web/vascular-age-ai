import streamlit as st
import google.generativeai as genai
from datetime import date

# 1. KONFIGURÁCIÓ
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Rendszerhiba: A diagnosztikai modul nem elérhető.")

# LINKEK (A professzor képének helye és az affiliate link)
AFFILIATE_LINK = "https://a-te-linked-ide.hu"
PROFESSOR_IMAGE_URL = "https://via.placeholder.com/300x400.png?text=Prof+Jakab+Foto" 
ARTERY_BAD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_ymgn5oymgn5oymgn.png"
ARTERY_GOOD_URL = "https://raw.githubusercontent.com/zorgorichard-web/vascular-age-ai/refs/heads/main/Gemini_Generated_Image_fpxagafpxagafpxa.png"

st.set_page_config(page_title="VascularAge AI - Klinikai Analízis", page_icon="⚖️")

# --- UI STÍLUS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .prof-card { display: flex; background-color: #f8f9fa; border-radius: 15px; overflow: hidden; border-left: 8px solid #d93025; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
    .prof-img { width: 30%; object-fit: cover; }
    .prof-text { width: 70%; padding: 25px; }
    .prof-name { color: #d93025; margin-top: 0; font-weight: 700; }
    .stButton>button { background: linear-gradient(90deg, #002244, #004488); color: white; border-radius: 8px; font-weight: bold; width: 100%; height: 3.5em; border: none; font-size: 1.1em; }
    .result-text { color: #1e293b; line-height: 1.8; font-size: 1.15em; font-family: 'Georgia', serif; }
    .stat-box { text-align: center; padding: 12px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; }
    .trust-badge { text-align: center; font-size: 0.8em; color: #555; }
    @media (max-width: 600px) { .prof-card { flex-direction: column; } .prof-img { width: 100%; height: 250px; } .prof-text { width: 100%; } }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ VascularAge AI™")
st.write("#### Személyre szabott érrendszeri diagnosztikai protokoll")

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
    # BMI számítás a tudományosság kedvéért
    bmi = round(weight / ((height/100)**2), 1)
    
    symptoms = []
    if s1: symptoms.append("ödéma")
    if s2: symptoms.append("reggeli fejfájás")
    if s3: symptoms.append("fülzúgás")
    if s4: symptoms.append("zsibbadás")
    
    # Érrendszeri kor finomított számítása
    v_age = age + (len(symptoms) * 5) + (5 if bmi > 28 else 0) + (3 if stress == "Magas" else 0)
    
    with st.spinner('Adatok feldolgozása...'):
        prompt = f"""
        Te Jakab Tamás professzor vagy. Egy {gender} pácienshez beszélsz.
        Adatok: Kor: {age}, Súly: {weight} kg, Magasság: {height} cm, BMI: {bmi}.
        Tünetek: {', '.join(symptoms)}. Számított érrendszeri kor: {v_age} év.

        Írj egy nyers, sokkoló elemzést:
        - Szólítsd meg a nemének megfelelően (Uram/Asszonyom).
        - Utalj a súlyára: ha a BMI magas, mondd el, hogy a szíve minden dobbanással egy mázsás terhet cipel.
        - Használd: "6,1 kg lerakódás az erekben", "időzített bomba".
        - A megoldás a Cardiotensive tisztítókúra.
        - Stílus: rövid mondatok, tekintélyelvű, vészjósló.
        """
        
        try:
            response = model.generate_content(prompt)
            st.divider()
            
            # 1. DÁTUM ÉS MÉRŐSZÁMOK
            st.write(f"📅 **Lelet kiállítva:** {date.today().strftime('%Y. %m. %d.')}")
            
            risk_percent = min(100, (v_age - age) * 10 + 40)
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("BECSÜLT ÉRRENDSZERI KOR", f"{v_age} ÉV", f"+{v_age-age} év eltérés")
            with col_m2:
                st.write(f"**Érfal elzáródási szint: {risk_percent}%**")
                st.progress(risk_percent / 100)

            # 2. VIZUÁLIS SOKK
            st.write("### 🔍 Mikroszkópos érfal analízis")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.error("KRITIKUS ÁLLAPOT")
                st.image(ARTERY_BAD_URL, caption="Besűrűsödött vér és lerakódás")
            with col_img2:
                st.success("TISZTÍTÁS UTÁN")
                st.image(ARTERY_GOOD_URL, caption="Szabad véráramlás")

            # 3. PROFESSZOR DIAGNÓZISA
            st.markdown(f"""
            <div class='prof-card'>
                <img src='{PROFESSOR_IMAGE_URL}' class='prof-img'>
                <div class='prof-text'>
                    <h3 class='prof-name'>📋 Dr. Jakab Tamás Sürgősségi Lelete</h3>
                    <div class='result-text'>{response.text.replace('**', '<b>').replace('</b>', '</b>')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 4. CTA GOMB + TRUST BADGES
            st.warning("⚠️ HALASZTHATATLAN BEAVATKOZÁS JAVASOLT")
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank" style="text-decoration: none;">
                    <button style="width:100%; padding:25px; background: linear-gradient(90deg, #d93025, #a00000); color:white; font-size:22px; font-weight:bold; border:none; border-radius:12px; cursor:pointer; box-shadow: 0 10px 25px rgba(217, 48, 37, 0.4);">
                        IGÉNYLEM A TISZTÍTÓKÚRÁT (LIMITÁLT 50% KEDVEZMÉNY) »
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
            st.write("---")
            tb1, tb2, tb3, tb4 = st.columns(4)
            tb1.markdown("<div class='trust-badge'>🔒<br>SSL Biztonság</div>", unsafe_allow_html=True)
            tb2.markdown("<div class='trust-badge'>🌿<br>Natúr Összetevők</div>", unsafe_allow_html=True)
            tb3.markdown("<div class='trust-badge'>✅<br>Klinikai Teszt</div>", unsafe_allow_html=True)
            tb4.markdown("<div class='trust-badge'>🚚<br>Gyors Házhozszállítás</div>", unsafe_allow_html=True)

            st.write("---")
st.markdown("""
    <div style='font-size: 10px; color: #888; text-align: center; padding: 20px;'>
        NYILATKOZAT: Ez az alkalmazás mesterséges intelligencia alapú elemzést végez a megadott adatok alapján. 
        Az eredmények kizárólag tájékoztató jellegűek, és nem minősülnek orvosi diagnózisnak vagy tanácsadásnak. 
        Bármilyen egészségügyi döntés előtt konzultáljon szakorvossal. 
        A honlap nem áll kapcsolatban a Facebookkal vagy a Metával.
    </div>
""", unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Rendszerhiba lépett fel. Próbálja újra pár pillanat múlva.")


