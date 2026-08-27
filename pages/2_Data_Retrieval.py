import streamlit as st
import time
from backend import apply_custom_css, fetch_uniprot_data, fetch_alphafold_url

st.set_page_config(page_title="Step 2 | ProtMind AI", page_icon="🔍")
apply_custom_css()

st.markdown("<h2>🔍 Step 2: Data Retrieval Results</h2>", unsafe_allow_html=True)

if not st.session_state.get('payload'):
    st.warning("⚠️ No active protein data found. Please complete Step 1: User Input first.")
    st.stop()

payload = st.session_state['payload']

with st.spinner(f"🔬 Querying live databases for {payload['uniprot_id']}..."):
    uniprot_metadata = fetch_uniprot_data(payload['uniprot_id'])
    af_pdb_url = fetch_alphafold_url(payload['uniprot_id'])
    time.sleep(1)

tab1, tab2, tab3, tab4 = st.tabs(["🔵 UniProt", "🏥 NIH", "👥 gnomAD", "🧬 Structure"])

with tab1:
    st.markdown("<h3>Protein Knowledgebase</h3>", unsafe_allow_html=True)
    st.json(uniprot_metadata)
        
with tab2:
    st.markdown("<h3>Clinical Significance</h3>", unsafe_allow_html=True)
    st.metric(label="Target Mutation", value=payload['mutation'])

with tab3:
    st.markdown("<h3>Population Genomics</h3>", unsafe_allow_html=True)
    st.bar_chart({"European": 0.005, "African": 0.001, "Asian": 0.003, "Global": 0.004})

with tab4:
    st.markdown("<h3>Predicted 3D Structure</h3>", unsafe_allow_html=True)
    if af_pdb_url:
        st.success(f"AlphaFold structure located!")
        st.markdown(f"**[Download .PDB File]({af_pdb_url})**")
    else:
        st.warning("No AlphaFold structure found.")