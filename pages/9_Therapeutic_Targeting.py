import streamlit as st
import pandas as pd
from backend import apply_custom_css, fetch_chembl_drugs, fetch_uniprot_data

st.set_page_config(page_title="Step 9 | ProtMind AI", page_icon="💊")
apply_custom_css()

st.markdown("<h2>💊 Step 9: Therapeutic Targeting</h2>", unsafe_allow_html=True)

if not st.session_state.get('payload'):
    st.warning("⚠️ No active protein data found. Please complete Step 1: User Input first.")
    st.stop()

payload = st.session_state['payload']

with st.spinner("🔗 Scanning ChEMBL for pharmacological targets..."):
    # We still fetch the gene name for the UI display
    uniprot_data = fetch_uniprot_data(payload['uniprot_id'])
    gene = uniprot_data.get("Gene", "Unknown")
    
    # FIX: Pass the exact UniProt ID to the backend function instead of the gene name
    drugs = fetch_chembl_drugs(payload['uniprot_id'])

st.markdown(f"### Pharmacological Network for Target: **{gene} ({payload['uniprot_id']})**")

if drugs:
    df = pd.DataFrame(drugs)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("Use these Molecule IDs in PubChem or ChEMBL to design docking simulations against the mutant pocket.")
else:
    st.warning(f"No documented small molecules or targeted therapies found in the ChEMBL database for {payload['uniprot_id']}.")