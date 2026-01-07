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
    .main-card { background-color: #f8fafc; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; border-left: 5px solid #003366; margin-bottom: 20px; }
    .stButton>button { background: #003366; color: white; border-radius: 8px; font-weight: bold; width: 100%; height: 3em; }
    .result-text { color: #1e293b; line-height: 1.7; font-size: 1.1em; }
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
            # ITT TÖRTÉNIK A GENERÁLÁS (Ez hiányzott)
            response = model.generate_content(prompt)
            
            # Eredmény megjelenítése
            st.divider()
            st.metric("Becsült érrendszeri életkor:", f"{v_age} év", f"{v_age-age} év eltérés")
            
            st.markdown(f"""
            <div class='main-card'>
                <div class='result-text'>
                    {response.text}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # A gomb csak a jelentés után jelenik meg
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank" style="text-decoration: none;">
                    <button style="width:100%; padding:25px; background: linear-gradient(90deg, #e11d48, #be123c); color:white; font-size:22px; font-weight:bold; border:none; border-radius:12px; cursor:pointer; box-shadow: 0 10px 20px rgba(225, 29, 72, 0.3);">
                        IGÉNYLEM A TISZTÍTÓKÚRÁT (LIMITÁLT 50% KEDVEZMÉNY) »
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Hiba az AI generálás során: {e}")

