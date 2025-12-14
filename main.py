import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Agentic Quality Monitor", layout="wide", page_icon="📞")

@st.cache_data
def load_data():
    data_path = 'call_center_data'
    try:
        df = pd.read_csv(f'{data_path}/PRODUCTION_COMPLETE.csv')
        return df
    except:
        try:
            df = pd.read_csv(f'{data_path}/FULL_PIPELINE_RESULTS.csv')
            return df
        except:
            return pd.DataFrame()

df = load_data()
if df.empty:
    st.warning("📁 Upload your CSV files to `call_center_data/` folder")
    st.stop()

st.title("🏭 Agentic Quality Monitor")
st.markdown("*ML + GenAI Call Center Quality System*")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("📊 Total Calls", len(df))
col2.metric("🚨 Flagged", len(df[df['Quality_Score']<70]), "100%")
col3.metric("🎯 Avg Score", f"{df['Quality_Score'].mean():.1f}")

# Charts
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(df, x='Quality_Score', title="Quality Scores")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if 'Review_Flags' in df.columns:
        fig = px.pie(df, names='Review_Flags', title="Review Reasons")
        st.plotly_chart(fig)

# Flagged calls
st.subheader("🚨 Calls Needing Review")
st.dataframe(df[df['Quality_Score']<70][['id','Quality_Score','Review_Flags','Type']])

st.sidebar.success("🎓 Project-II 241C208 Complete!")
