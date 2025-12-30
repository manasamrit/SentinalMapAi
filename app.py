import streamlit as st
import time
import os
import plotly.graph_objects as go
from dotenv import load_dotenv
from src.agents.investigator import OsintInvestigatorAgent
from src.agents.auditor import PolicyAuditorAgent
from src.utils.risk_engine import calculate_trust_score

# Load Environment Variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="SentinelMap AI | Trust & Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open('src/ui/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---------------- NAVIGATION & SIDEBAR ---------------- #
try:
    st.sidebar.image("google-logo.png", width=120) 
except:
    st.sidebar.image("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png", width=120)

st.sidebar.title("SentinelMap AI")
st.sidebar.markdown("**Enterprise Edition**")
st.sidebar.markdown("---")
st.sidebar.subheader("🔐 API Credentials")
st.sidebar.caption("Loaded from System Environment if empty.")

# Use os.getenv as default value BUT still allow user override
# If env var is present, it shows as value, masking it is better if possible but text_input doesn't allow masking initial value easily without showing it?
# We will just use placeholders to indicate they are loaded.

maps_key_env = os.getenv("GOOGLE_MAPS_API_KEY", "")
serp_key_env = os.getenv("SERPAPI_KEY", "")
gemini_key_env = os.getenv("GEMINI_API_KEY", "")

maps_key = st.sidebar.text_input("Google Maps API Key", value=maps_key_env, type="password")
serp_key = st.sidebar.text_input("SerpApi Key", value=serp_key_env, type="password")
gemini_key = st.sidebar.text_input("Gemini API Key", value=gemini_key_env, type="password")

st.sidebar.markdown("---")
st.sidebar.caption("v2.0.0 Enterprise | Google Trust & Safety")

# ---------------- MAIN HEADER ---------------- #
st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px; padding-bottom: 20px;'>
        <img src='https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg' style='height: 40px;'>
        <h1 style='margin: 0; font-size: 2.2rem; color: #3c4043;'>Trust & Safety Maps Investigation Console</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #e8f0fe; padding: 12px 20px; border-radius: 8px; border-left: 5px solid #1a73e8; margin-bottom: 25px; font-family: 'Roboto', sans-serif;">
    <span style="font-weight: 500; color: #1a73e8;">SYSTEM STATUS:</span> 🟢 <b>Online</b> &nbsp;&nbsp;|&nbsp;&nbsp; 
    <span style="font-weight: 500; color: #1a73e8;">MODE:</span> <b>Enterprise Live Feed</b> &nbsp;&nbsp;|&nbsp;&nbsp; 
    <span style="font-weight: 500; color: #1a73e8;">LATENCY:</span> 23ms
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ---------------- #
with st.form(key='investigation_form'):
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        query = st.text_input("Target Business (Name + Location)", placeholder="e.g. Ace Locksmith, Anytown CA, or GK Vale Bangalore")
    
    with col_btn:
        st.write("") 
        st.write("")
        # Form submit button
        start_btn = st.form_submit_button("🚀 Run Investigation", use_container_width=True)

# ---------------- EXECUTION LOGIC ---------------- #
if start_btn and query:
    # Initialize Agents with provided keys
    investigator = OsintInvestigatorAgent(maps_key, serp_key)
    auditor = PolicyAuditorAgent(gemini_key)

    # Layout: 2 Columns for Live Feed
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📂 Case File")
        
        # Step 1: Investigation
        with st.status("🕵️ Agent A: Investigating...", expanded=True) as status:
            st.write("Initializing Maps API connection...")
            place_data, osint_data = investigator.investigate(query)
            
            for log in investigator.logs:
                st.text(log)
                time.sleep(0.1) 
            
            if place_data:
                status.update(label="Investigation Complete", state="complete", expanded=False)
            else:
                status.update(label="Investigation Failed", state="error")
                st.error("Business not found on Google Maps. Please check the query.")
                st.stop()

        # Display Basic Info
        with st.container():
            st.markdown(f"### {place_data.get('name', 'Unknown')}")
            st.markdown(f"📍 **Address**: {place_data.get('address', 'N/A')}")
            st.markdown(f"📞 **Phone**: {place_data.get('phone', 'N/A')}")
            website = place_data.get('website', 'N/A')
            st.markdown(f"🌐 **Website**: [{website}]({website})")
            
            # Display Rating Star
            rating = place_data.get('rating', 0)
            reviews = len(place_data.get('reviews', []))
            st.metric("Maps Rating", f"{rating} / 5.0", delta=f"{reviews} Reviews found")

    with col_right:
        st.subheader("⚖️ Policy Audit")
        
        # Step 2: Audit
        if place_data:
            with st.status("🤖 Agent B: Auditing Compliance...", expanded=True) as status:
                st.write("Loading Misrepresentation Policy guidelines...")
                
                # Run Audit
                audit_report = auditor.audit(place_data, osint_data)
                
                for log in auditor.logs:
                    st.text(log)
                    time.sleep(0.1)
                
                status.update(label="Audit Complete", state="complete", expanded=False)

    # ---------------- RESULTS SECTION ---------------- #
    st.markdown("---")
    st.subheader("📊 Final Risk Assessment")

    # Calculate Score
    trust_score, breakdown = calculate_trust_score(place_data, osint_data, audit_report)

    # Display Score
    score_col, summary_col = st.columns([1, 2])
    
    with score_col:
        # Plotly Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = trust_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Trust Score"},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1a73e8"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': '#ff4b4b'}, # Red
                    {'range': [40, 70], 'color': '#ffa726'}, # Orange
                    {'range': [70, 100], 'color': '#00c853'} # Green
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': trust_score
                }
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with summary_col:
        st.markdown("### 📋 Executive Summary")
        st.markdown(f"**Analysis ID**: {int(time.time())}")
        st.markdown(audit_report)
        
        with st.expander("Risk Factor Breakdown", expanded=True):
            if not breakdown:
                st.success("No negative risk factors detected.")
            for item in breakdown:
                st.markdown(f"- ⚠️ {item}")

    # ---------------- DEEP DIVE TABS ---------------- #
    st.markdown("---")
    tab1, tab2 = st.tabs(["🔍 Review Integrity Analysis", "🌐 OSINT Footprint"])
    
    with tab1:
        st.subheader("Suspicious Pattern Detection")
        reviews = place_data.get('reviews', [])
        if reviews and len(reviews) > 0:
            # Prepare data for plotting
            import pandas as pd
            df_reviews = pd.DataFrame(reviews)
            if 'time' in df_reviews.columns:
                df_reviews['datetime'] = pd.to_datetime(df_reviews['time'], unit='s')
                df_reviews = df_reviews.sort_values('datetime')
                
                # Plot 1: Review Velocity (Timeline)
                fig_timeline = go.Figure()
                fig_timeline.add_trace(go.Scatter(
                    x=df_reviews['datetime'], 
                    y=df_reviews['rating'],
                    mode='markers+lines',
                    marker=dict(size=10, color=df_reviews['rating'], colorscale='Viridis'),
                    name='Review'
                ))
                fig_timeline.update_layout(
                    title="Review Velocity Timeline (Burst Detection)",
                    xaxis_title="Date",
                    yaxis_title="Star Rating",
                    height=300
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
                
                # Burst Warning
                if len(reviews) >= 3:
                     timestamps = sorted([r.get('time', 0) for r in reviews], reverse=True)
                     if (timestamps[0] - timestamps[2]) < 86400:
                         st.error("🚨 CRITICAL: High Velocity Detected. 3+ Reviews in < 24 Hours. Typical of `Review Buying`.")
            else:
                st.info("No timestamp data available for velocity analysis.")
                
            # Display Review Text with detection
            st.markdown("#### recent_reviews_sample")
            for r in reviews[:3]:
                st.markdown(f"> *\"{r.get('text')}\"* - **{r.get('rating')} Stars**")
        else:
            st.info("No reviews found for this business.")

    with tab2:
        if osint_data:
            osint_cols = st.columns(3)
            # Handle cases where we have fewer results than columns
            count = min(len(osint_data), 6)
            for i in range(count):
                result = osint_data[i]
                col_idx = i % 3
                with osint_cols[col_idx]:
                     st.markdown(f"""
                    <div class="risk-card">
                        <b>{result.get('title', 'Unknown Source')}</b><br>
                        <a href="{result.get('link', '#')}" target="_blank" style="color: #1a73e8; text-decoration: none;">View Source</a><br>
                        <small style="color: #5f6368;">{result.get('snippet', '')[:120]}...</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No external OSINT signals found.")
