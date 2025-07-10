import streamlit as st

# Farbdefinitionen (STW-Farben)
STW_TUERKIS = "#00B2A9"
DUNKELGRAU = "#333333"
HINTERGRUND = "#F9F9F9"

# --- Design-Anpassung via HTML/CSS ---
st.markdown(
    f"""
    <style>
    body {{
        background-color: {HINTERGRUND};
        color: {DUNKELGRAU};
    }}
    .stApp {{
        background-color: {HINTERGRUND};
    }}
    h1, h2, h3 {{
        color: {STW_TUERKIS};
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    .stButton > button {{
        background-color: {STW_TUERKIS};
        color: white;
        border-radius: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Passwortschutz ---
PASSWORT = "fernwaerme2025"
pass_eingabe = st.text_input("🔒 Bitte Passwort eingeben:", type="password")

if pass_eingabe != PASSWORT:
    st.warning("Zugriff verweigert. Bitte gültiges Passwort eingeben.")
    st.stop()

# --- Titel ---
st.title("💡 Fernwärmekostenberechnung pro Jahr")

# --- Konstante Preise ---
ENERGIEPREIS_CENT_PRO_KWH = 8.0469     # in Cent
GRUNDPREIS_EURO_PRO_KW_JAHR = 42.9324  # in Euro
WAERMEZAEHLER_MONATLICH = 2.8414       # Euro pro Monat (netto)
OEKO_UMWELT_CENT_PRO_KWH = 0.1624      # in Cent pro kWh

# --- Funktion zur Berechnung der Messleistungskosten ---
def berechne_messleistungskosten(anschlussleistung_kw):
    if anschlussleistung_kw <= 105:
        return 8.8986 * 12
    elif anschlussleistung_kw <= 245:
        return 17.1616 * 12
    elif anschlussleistung_kw <= 420:
        return 21.6109 * 12
    elif anschlussleistung_kw <= 1050:
        return 26.0602 * 12
    elif anschlussleistung_kw <= 1750:
        return 28.6027 * 12
    else:
        return 28.6027 * 12

# --- Benutzereingabe ---
anschlussleistung_kw = st.number_input("🔌 Anschlussleistung (kW):", min_value=0.0, format="%.2f")
verbrauch_kwh = st.number_input("🔥 Jahresverbrauch (kWh):", min_value=0.0, format="%.2f")

if anschlussleistung_kw > 0 and verbrauch_kwh > 0:
    # Einzelkosten berechnen
    energiekosten = verbrauch_kwh * (ENERGIEPREIS_CENT_PRO_KWH / 100)
    grundkosten = anschlussleistung_kw * GRUNDPREIS_EURO_PRO_KW_JAHR
    messleistungskosten = berechne_messleistungskosten(anschlussleistung_kw)
    waermezaehler_kosten = WAERMEZAEHLER_MONATLICH * 12

    # Zwischensumme netto
    zwischensumme = energiekosten + grundkosten + messleistungskosten + waermezaehler_kosten

    # Abgaben
    oekobeitrag = verbrauch_kwh * (OEKO_UMWELT_CENT_PRO_KWH / 100)
    benutzungsabgabe = (zwischensumme + oekobeitrag) * 0.06
    netto_gesamt = zwischensumme + oekobeitrag + benutzungsabgabe
    mehrwertsteuer = netto_gesamt * 0.20
    brutto_gesamt = netto_gesamt + mehrwertsteuer

    # --- Ausgabe ---
    st.subheader("📊 Kostenaufstellung Fernwärme")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Energiekosten:")
        st.write(f"Grundpreis:")
        st.write(f"Messleistungskosten:")
        st.write(f"Wärmezählerkosten:")
        st.markdown("---")
        st.write(f"Öko- und Umweltbeitrag:")
        st.write(f"Benutzungsabgabe (6%):")
        st.markdown("---")
        st.write(f"**Gesamtkosten netto:**")
        st.write(f"Mehrwertsteuer (20%):")
        st.markdown("---")
        st.write(f"**Gesamtkosten (brutto):**")

    with col2:
        st.write(f"{energiekosten:10.2f} €")
        st.write(f"{grundkosten:10.2f} €")
        st.write(f"{messleistungskosten:10.2f} €")
        st.write(f"{waermezaehler_kosten:10.2f} €")
        st.markdown("---")
        st.write(f"{oekobeitrag:10.2f} €")
        st.write(f"{benutzungsabgabe:10.2f} €")
        st.markdown("---")
        st.write(f"{netto_gesamt:10.2f} €")
        st.write(f"{mehrwertsteuer:10.2f} €")
        st.markdown("---")
        st.success(f"{brutto_gesamt:10.2f} € / Jahr")
