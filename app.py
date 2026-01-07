import streamlit as st
import google.generativeai as genai

# 1. KONFIGURÁCIÓ
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Hiba a Secrets beállításoknál! Ellenőrizd a GEMINI_API_KEY-t.")

# Ide jön a végleges AdCombo linked
AFFILIATE_LINK = "https://a-te-linked-ide.hu" 

st.set_page_config(page_title="VascularAge AI - Pro", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-card { background-color: #f0f2f6; padding: 25px; border-radius: 15px; border-left: 10px solid #d93025; margin-bottom: 20px; }
    .stButton>button { background: #003366; color: white; border-radius: 8px; font-weight: bold; width: 100%; height: 3em; }
    .result-text { color: #1e293b; line-height: 1.7; font-size: 1.1em; }
    .metric-container { background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ VascularAge AI™")
st.write("#### Professzionális érrendszeri állapotfelmérés")

# --- KÉRDŐÍV ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Életkor", 18, 100, 48)
        lifestyle = st.selectbox("Életmód", ["Ülőmunka", "Kevés mozgás", "Aktív"])
    with col2:
        weight_status = st.selectbox("Testsúly", ["Normál", "Túlsúly"])
        stress = st.select_slider("Stressz-szint", ["Alacsony", "Átlagos", "Magas"])

    st.write("---")
    st.write("**Jelölje be az Önre jellemző tüneteket:**")
    s1 = st.checkbox("Lábdagadás (ödéma)")
    s2 = st.checkbox("Reggeli fejfájás")
    s3 = st.checkbox("Fülzúgás / Szédülés")
    s4 = st.checkbox("Zsibbadó végtagok")

# --- ELEMZÉS ---
if st.button("KLINIKAI JELENTÉS GENERÁLÁSA"):
    symptoms = []
    if s1: symptoms.append("ödéma")
    if s2: symptoms.append("reggeli fejfájás")
    if s3: symptoms.append("fülzúgás")
    if s4: symptoms.append("zsibbadás")
    
    v_age = age + (len(symptoms) * 5)
    
    with st.spinner('Jakab professzor AI modulja elemzi az adatokat...'):
        prompt = f"""
        Te Jakab Tamás professzor vagy, az érrendszer specialistája. 
        A páciens adatai: Kor: {age}, Tünetek: {', '.join(symptoms)}. 
        Számított érrendszeri kor: {v_age} év.

        Írj egy sokkoló, de szakmai elemzést a következő pontok alapján:
        1. Diagnózis: Mondd el, hogy a {v_age} éves érrendszeri kor kritikus állapotot jelez. 
        2. Magyarázat: Használd a "6,1 kg lerakódás" és az "elzáródott erek a betegségek 90%-ának okai" kifejezéseket.
        3. Veszély: Említsd meg a vérrögök (trombusok) kockázatát, amik bármikor leválhatnak.
        4. Megoldás: Mutasd be a Cardiotensive-et mint az erek "tisztítókúráját", ami olajfalevéllel és galagonyával kalapácsként veri le a koleszterin-plakkokat.
        5. Sürgetés: Mondd el, hogy a szervezetének nincs több ideje várni, a tisztítást ma kell megkezdeni.

        FONTOS: Ne használj unalmas jogi nyilatkozatokat. Legyél határozott, tekintélyelvű és meggyőző. Magyarul írj, tagolatlan, hosszú bekezdések helyett használj figyelemfelkeltő stílust.
        """
        
        try:
            response = model.generate_content(prompt)
            
            st.divider()

            # --- VIZUÁLIS BLOKK 1: MÉRŐSZÁMOK ---
            risk_percent = min(100, (v_age - age) * 10 + 35)
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Becsült érrendszeri életkor", f"{v_age} év", f"+{v_age-age} év eltérés")
            with col_m2:
                st.write(f"**Érfal elzáródási szint: {risk_percent}%**")
                st.progress(risk_percent / 100)

            # --- VIZUÁLIS BLOKK 2: ÖSSZEHASONLÍTÁS ---
            st.write("### 🔍 Mikroszkópos érfal analízis")
            
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.error("KRITIKUS ÁLLAPOT")
                st.image("https://img.freepik.com/free-photo/clogged-artery-with-cholesterol-plaque_1048-12444.jpg", caption="Jelenlegi lerakódások")
            with col_img2:
                st.success("TISZTÍTÁS UTÁN")
                st.image("https://img.freepik.com/free-photo/healthy-artery-without-plaque_1048-12445.jpg", caption="Optimális keringés")

            # --- VIZUÁLIS BLOKK 3: PROFESSZORI LELET ---
            st.markdown(f"""
            <div class='main-card'>
                <h3 style="color: #d93025; margin-top:0;">📋 Jakab Professzor Diagnózisa</h3>
                <div class='result-text'>
                    {response.text.replace('**', '<b>').replace('</b>', '</b>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sürgősségi jelzés
            st.warning("⚠️ AZONNALI BEAVATKOZÁS SZÜKSÉGES")
            
            # CALL TO ACTION GOMB
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank" style="text-decoration: none;">
                    <button style="width:100%; padding:25px; background: linear-gradient(90deg, #e11d48, #be123c); color:white; font-size:22px; font-weight:bold; border:none; border-radius:12px; cursor:pointer; box-shadow: 0 10px 20px rgba(225, 29, 72, 0.3);">
                        IGÉNYLEM A TISZTÍTÓKÚRÁT (LIMITÁLT 50% KEDVEZMÉNY) »
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Hiba az AI generálás során: {e}")
