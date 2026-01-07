import streamlit as st
import google.generativeai as genai

# 1. KONFIGURÁCIÓ ÉS TITKOK
# A Streamlit Secrets-ből olvassuk ki a kulcsot
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Itt definiáljuk a modellt - EZ HIÁNYZOTT KORÁBBAN
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Hiba a konfiguráció során: {e}. Ellenőrizd a Secrets beállításokat!")

# Ide írd a saját AdCombo linkedet
AFFILIATE_LINK = "https://a-te-linked-ide.hu" 

# --- OLDAL BEÁLLÍTÁSA ---
st.set_page_config(page_title="VascularAge AI - Pro", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-card { background-color: #f8fafc; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; border-left: 5px solid #003366; }
    .stButton>button { background: #003366; color: white; border-radius: 8px; font-weight: bold; width: 100%; height: 3em; }
    .result-text { color: #1e293b; line-height: 1.6; }
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
    
    with st.spinner('AI Diagnosztika futtatása...'):
        prompt = f"Kardiológusként elemezd: Kor: {age}, Tünetek: {', '.join(symptoms)}. Életkor becslés: {v_age} év. Javasold a Cardiotensive-et (olajfalevél, galagonya). Magyarul válaszolj."
        
        try:
            # Most már a 'model' változó biztosan létezik
            response = model.generate_content(prompt)
            
            st.divider()
            st.metric("Becsült érrendszeri életkor:", f"{v_age} év", f"{v_age-age} év eltérés")
            
            st.markdown(f"<div class='main-card'><div class='result-text'>{response.text}</div></div>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <a href="{AFFILIATE_LINK}" target="_blank">
                    <button style="width:100%; padding:20px; background: #dc2626; color:white; font-size:18px; font-weight:bold; border:none; border-radius:10px; cursor:pointer; margin-top:20px;">
                        MEGNÉZEM A JAVASOLT KÚRÁT (50% KEDVEZMÉNY) >>
                    </button>
                </a>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Hiba az AI generálás során: {e}")
