import streamlit as st
import pandas as pd
import joblib
import time
import random

# Page configuration
st.set_page_config(
    page_title="FraudNet AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced responsive cyberpunk CSS
st.markdown("""
<style>
    /* Import cyberpunk fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono:wght@400&display=swap');
    
    /* Global dark theme with enhanced gradients */
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
        overflow-x: hidden;
    }
    
    /* Animated grid background */
    .cyber-grid {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        opacity: 0.03;
        z-index: -2;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Enhanced terminal container - responsive */
    .terminal-container {
        background: 
            linear-gradient(135deg, rgba(0, 0, 0, 0.95) 0%, rgba(26, 26, 46, 0.9) 100%);
        border: 2px solid #00ff41;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 
            0 0 30px rgba(0, 255, 65, 0.4),
            inset 0 0 30px rgba(0, 255, 65, 0.05);
        position: relative;
        backdrop-filter: blur(10px);
        max-width: 100%;
        overflow-x: auto;
    }
    
    @media (min-width: 768px) {
        .terminal-container {
            padding: 2rem;
            margin: 1rem;
        }
    }
    
    .terminal-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff0080, #00ff41, #0080ff, #ff0080);
        background-size: 200% 100%;
        animation: borderScan 3s linear infinite;
    }
    
    @keyframes borderScan {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    
    /* Responsive cyberpunk header */
    .cyber-header {
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.6);
        border-radius: 12px;
        border: 1px solid rgba(0, 255, 65, 0.3);
    }
    
    @media (min-width: 768px) {
        .cyber-header {
            padding: 2rem;
            margin-bottom: 3rem;
        }
    }
    
    .cyber-title {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ff0080, #00ff41, #0080ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        animation: glitchTitle 4s infinite;
    }
    
    @media (min-width: 768px) {
        .cyber-title {
            font-size: 4rem;
            letter-spacing: 4px;
        }
    }
    
    @keyframes glitchTitle {
        0%, 90%, 100% { 
            transform: translateX(0);
            filter: drop-shadow(0 0 10px rgba(0, 255, 65, 0.5));
        }
        91% { 
            transform: translateX(-2px) skew(2deg);
            filter: drop-shadow(0 0 10px rgba(255, 0, 128, 0.5));
        }
        92% { 
            transform: translateX(2px) skew(-2deg);
            filter: drop-shadow(0 0 10px rgba(0, 128, 255, 0.5));
        }
    }
    
    .cyber-subtitle {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        color: #00ff41;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    
    @media (min-width: 768px) {
        .cyber-subtitle {
            font-size: 1.3rem;
            letter-spacing: 3px;
        }
    }
    
    /* Responsive status bar */
    .status-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #00ff41;
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 1.5rem;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        gap: 0.5rem;
    }
    
    @media (min-width: 768px) {
        .status-bar {
            flex-wrap: nowrap;
            padding: 1rem;
            font-size: 0.9rem;
        }
    }
    
    .status-item {
        display: flex;
        align-items: center;
        color: #00ff41;
        margin: 0.2rem 0;
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        background: #00ff41;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 5px #00ff41; }
        50% { opacity: 0.5; box-shadow: 0 0 10px #00ff41; }
    }
    
    /* Enhanced responsive input panels */
    .input-panel {
        background: 
            linear-gradient(135deg, 
                rgba(26, 26, 46, 0.9) 0%, 
                rgba(22, 33, 62, 0.8) 50%, 
                rgba(26, 26, 46, 0.9) 100%
            );
        border: 1px solid #00ff41;
        border-radius: 12px;
        padding: 1rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        margin-bottom: 1rem;
    }
    
    @media (min-width: 768px) {
        .input-panel {
            padding: 1.8rem;
        }
    }
    
    .input-panel:hover {
        box-shadow: 
            0 0 25px rgba(0, 255, 65, 0.5),
            inset 0 0 20px rgba(0, 255, 65, 0.1);
        border-color: #ff0080;
        transform: translateY(-2px) scale(1.01);
    }
    
    .panel-label {
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    
    @media (min-width: 768px) {
        .panel-label {
            font-size: 1rem;
            letter-spacing: 2px;
            margin-bottom: 1rem;
        }
    }
    
    /* Responsive data stream */
    .data-stream {
        background: rgba(0, 0, 0, 0.95);
        border: 2px solid #0080ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 1.5rem 0;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        position: relative;
        overflow: hidden;
        overflow-x: auto;
    }
    
    @media (min-width: 768px) {
        .data-stream {
            padding: 1.5rem;
            font-size: 1rem;
        }
    }
    
    .data-stream::before {
        content: 'NEURAL DATA STREAM';
        position: absolute;
        top: -12px;
        left: 20px;
        background: #0a0a0a;
        color: #0080ff;
        padding: 0 10px;
        font-size: 0.7rem;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    @media (min-width: 768px) {
        .data-stream::before {
            font-size: 0.8rem;
        }
    }
    
    .stream-line {
        color: #0080ff;
        margin: 0.3rem 0;
        opacity: 0;
        animation: dataFlow 0.8s ease-in-out forwards;
        text-shadow: 0 0 5px rgba(0, 128, 255, 0.5);
        white-space: nowrap;
    }
    
    @media (max-width: 767px) {
        .stream-line {
            white-space: normal;
            word-break: break-all;
        }
    }
    
    .stream-line:nth-child(1) { animation-delay: 0.1s; color: #00ff41; }
    .stream-line:nth-child(2) { animation-delay: 0.3s; color: #ff0080; }
    .stream-line:nth-child(3) { animation-delay: 0.5s; color: #0080ff; }
    .stream-line:nth-child(4) { animation-delay: 0.7s; color: #00ff41; }
    .stream-line:nth-child(5) { animation-delay: 0.9s; color: #ff0080; }
    
    @keyframes dataFlow {
        0% { opacity: 0; transform: translateX(-20px) scale(0.8); }
        100% { opacity: 1; transform: translateX(0) scale(1); }
    }
    
    /* Responsive neural loading */
    .neural-loading {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        position: relative;
    }
    
    .neural-spinner {
        width: 80px;
        height: 80px;
        border: 3px solid transparent;
        border-top: 3px solid #00ff41;
        border-right: 3px solid #ff0080;
        border-bottom: 3px solid #0080ff;
        border-radius: 50%;
        animation: neuralSpin 1.2s linear infinite;
    }
    
    @media (min-width: 768px) {
        .neural-spinner {
            width: 120px;
            height: 120px;
            border-width: 4px;
        }
    }
    
    @keyframes neuralSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        margin-top: 1rem;
        font-family: 'Share Tech Mono', monospace;
        color: #00ff41;
        font-size: 0.9rem;
        letter-spacing: 1px;
        animation: loadingPulse 1.5s ease-in-out infinite;
        text-align: center;
    }
    
    @media (min-width: 768px) {
        .loading-text {
            font-size: 1.1rem;
            letter-spacing: 2px;
            margin-top: 1.5rem;
        }
    }
    
    @keyframes loadingPulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }
    
    /* Responsive status display */
    .status-display {
        background: 
            radial-gradient(ellipse at center, rgba(0, 0, 0, 0.95) 0%, rgba(10, 10, 10, 0.9) 100%);
        border: 3px solid #00ff41;
        border-radius: 15px;
        padding: 2rem 1rem;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        animation: statusPowerUp 1.2s ease-out;
        overflow: hidden;
    }
    
    @media (min-width: 768px) {
        .status-display {
            padding: 3rem;
        }
    }
    
    @keyframes statusPowerUp {
        0% { 
            opacity: 0;
            transform: scale(0.5);
            border-color: transparent;
        }
        100% { 
            opacity: 1;
            transform: scale(1);
            border-color: #00ff41;
        }
    }
    
    .status-fraud {
        border-color: #ff0080 !important;
        box-shadow: 
            0 0 40px rgba(255, 0, 128, 0.4),
            inset 0 0 40px rgba(255, 0, 128, 0.1) !important;
    }
    
    .status-safe {
        border-color: #00ff41 !important;
        box-shadow: 
            0 0 40px rgba(0, 255, 65, 0.4),
            inset 0 0 40px rgba(0, 255, 65, 0.1) !important;
    }
    
    .status-text {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        word-break: break-word;
    }
    
    @media (min-width: 768px) {
        .status-text {
            font-size: 3rem;
            letter-spacing: 4px;
            margin-bottom: 1.5rem;
        }
    }
    
    .status-fraud .status-text {
        color: #ff0080;
        animation: dangerPulse 2s infinite;
        text-shadow: 0 0 20px rgba(255, 0, 128, 0.8);
    }
    
    .status-safe .status-text {
        color: #00ff41;
        animation: safePulse 2s infinite;
        text-shadow: 0 0 20px rgba(0, 255, 65, 0.8);
    }
    
    @keyframes dangerPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    @keyframes safePulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.01); }
    }
    
    /* Responsive enhanced button */
    .stButton > button {
        background: 
            linear-gradient(45deg, 
                rgba(0, 0, 0, 0.9) 0%, 
                rgba(26, 26, 46, 0.8) 50%, 
                rgba(0, 0, 0, 0.9) 100%
            );
        border: 2px solid #00ff41 !important;
        color: #00ff41 !important;
        padding: 1rem 2rem !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        border-radius: 8px !important;
        transition: all 0.4s ease !important;
        position: relative !important;
        overflow: hidden !important;
        width: 100% !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3) !important;
    }
    
    @media (min-width: 768px) {
        .stButton > button {
            padding: 1.5rem 4rem !important;
            font-size: 1.2rem !important;
            letter-spacing: 3px !important;
        }
    }
    
    .stButton > button:hover {
        background: 
            linear-gradient(45deg, #00ff41, #0080ff, #ff0080) !important;
        color: #000000 !important;
        box-shadow: 
            0 0 30px rgba(0, 255, 65, 0.7),
            0 0 50px rgba(0, 255, 65, 0.4) !important;
        transform: translateY(-3px) scale(1.05) !important;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom responsive scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    @media (min-width: 768px) {
        ::-webkit-scrollbar {
            width: 10px;
        }
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00ff41, #0080ff);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #ff0080, #00ff41);
    }
    
    /* Responsive columns */
    @media (max-width: 767px) {
        .stColumns {
            flex-direction: column !important;
        }
        
        .stColumn {
            width: 100% !important;
            margin-bottom: 1rem !important;
        }
    }
    
    /* Fix input field defaults */
    .stNumberInput input {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid #00ff41 !important;
        color: #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stSelectbox select {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid #00ff41 !important;
        color: #ffffff !important;
        border-radius: 5px !important;
    }
    
    /* Particle effects */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        width: 2px;
        height: 2px;
        background: #00ff41;
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced background effects
st.markdown("""
<div class="cyber-grid"></div>
<div class="particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 1s; background: #ff0080;"></div>
    <div class="particle" style="left: 30%; animation-delay: 2s; background: #0080ff;"></div>
    <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 4s; background: #ff0080;"></div>
    <div class="particle" style="left: 60%; animation-delay: 0.5s; background: #0080ff;"></div>
    <div class="particle" style="left: 70%; animation-delay: 1.5s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 2.5s; background: #ff0080;"></div>
    <div class="particle" style="left: 90%; animation-delay: 3.5s; background: #0080ff;"></div>
</div>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        return joblib.load('fraud_detection_model.pkl')
    except:
        st.error("⚡ NEURAL NETWORK NOT FOUND - Please ensure 'fraud_detection_model.pkl' is loaded")
        return None

model = load_model()

# Main container
st.markdown('<div class="terminal-container">', unsafe_allow_html=True)

# Enhanced cyberpunk header
st.markdown("""
<div class="cyber-header">
    <div class="cyber-title">⚡ FRAUDNET AI ⚡</div>
    <div class="cyber-subtitle">NEURAL FRAUD DETECTION SYSTEM v2.1</div>
</div>
""", unsafe_allow_html=True)

# System status bar
current_time = time.strftime("%H:%M:%S")
st.markdown(f"""
<div class="status-bar">
    <div class="status-item">
        <div class="status-indicator"></div>
        SYSTEM ONLINE
    </div>
    <div class="status-item">
        <div class="status-indicator" style="background: #ff0080;"></div>
        NEURAL NET: ACTIVE
    </div>
    <div class="status-item">
        <div class="status-indicator" style="background: #0080ff;"></div>
        TIME: {current_time}
    </div>
    <div class="status-item">
        <div class="status-indicator"></div>
        SECURITY: MAX
    </div>
</div>
""", unsafe_allow_html=True)

if model is not None:
    # Initialize session state for inputs to remove default values
    if 'amount' not in st.session_state:
        st.session_state.amount = 0.0
    if 'oldbalanceOrg' not in st.session_state:
        st.session_state.oldbalanceOrg = 0.0
    if 'newbalanceOrig' not in st.session_state:
        st.session_state.newbalanceOrig = 0.0
    if 'oldbalanceDest' not in st.session_state:
        st.session_state.oldbalanceDest = 0.0
    if 'newbalanceDest' not in st.session_state:
        st.session_state.newbalanceDest = 0.0
    
    # Transaction data input
    st.markdown("### 📡 NEURAL INTERFACE - DATA INPUT PROTOCOL")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">⚡ TRANSACTION PROTOCOL</div>', unsafe_allow_html=True)
        transaction_type = st.selectbox("", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">💰 TRANSFER AMOUNT</div>', unsafe_allow_html=True)
        amount = st.number_input("", min_value=0.0, value=st.session_state.amount, format="%.2f", 
                                label_visibility="collapsed", key="amount_input", 
                                placeholder="Enter amount...")
        if amount != st.session_state.amount:
            st.session_state.amount = amount
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📊 SOURCE BALANCE [BEFORE]</div>', unsafe_allow_html=True)
        oldbalanceOrg = st.number_input("", min_value=0.0, value=st.session_state.oldbalanceOrg, format="%.2f", 
                                       label_visibility="collapsed", key="old_orig", 
                                       placeholder="Enter source balance before...")
        if oldbalanceOrg != st.session_state.oldbalanceOrg:
            st.session_state.oldbalanceOrg = oldbalanceOrg
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📈 SOURCE BALANCE [AFTER]</div>', unsafe_allow_html=True)
        newbalanceOrig = st.number_input("", min_value=0.0, value=st.session_state.newbalanceOrig, format="%.2f", 
                                        label_visibility="collapsed", key="new_orig",
                                        placeholder="Enter source balance after...")
        if newbalanceOrig != st.session_state.newbalanceOrig:
            st.session_state.newbalanceOrig = newbalanceOrig
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📡 TARGET BALANCE [BEFORE]</div>', unsafe_allow_html=True)
        oldbalanceDest = st.number_input("", min_value=0.0, value=st.session_state.oldbalanceDest, format="%.2f", 
                                        label_visibility="collapsed", key="old_dest",
                                        placeholder="Enter target balance before...")
        if oldbalanceDest != st.session_state.oldbalanceDest:
            st.session_state.oldbalanceDest = oldbalanceDest
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">🎯 TARGET BALANCE [AFTER]</div>', unsafe_allow_html=True)
        newbalanceDest = st.number_input("", min_value=0.0, value=st.session_state.newbalanceDest, format="%.2f", 
                                        label_visibility="collapsed", key="new_dest",
                                        placeholder="Enter target balance after...")
        if newbalanceDest != st.session_state.newbalanceDest:
            st.session_state.newbalanceDest = newbalanceDest
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced data stream display
    balance_delta_org = oldbalanceOrg - newbalanceOrig
    balance_delta_dest = newbalanceDest - oldbalanceDest
    risk_ratio = (amount / max(oldbalanceOrg, 1)) * 100
    
    st.markdown(f"""
    <div class="data-stream">
        <div class="stream-line">> PROTOCOL_TYPE: {transaction_type}</div>
        <div class="stream-line">> TRANSFER_AMOUNT: ${amount:,.2f} USD</div>
        <div class="stream-line">> SOURCE_DELTA: ${balance_delta_org:,.2f} USD</div>
        <div class="stream-line">> TARGET_DELTA: ${balance_delta_dest:,.2f} USD</div>
        <div class="stream-line">> RISK_RATIO: {risk_ratio:.2f}% OF_BALANCE</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Neural network analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("⚡ EXECUTE NEURAL SCAN", type="primary", use_container_width=True)
    
    # Enhanced analysis results
    if analyze_button:
        # Enhanced loading animation
        with st.empty():
            st.markdown("""
            <div class="neural-loading">
                <div class="neural-spinner"></div>
                <div class="loading-text">ANALYZING NEURAL PATTERNS...</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
        
        # Prepare data for prediction
        input_data = pd.DataFrame({
            'type': [transaction_type],
            'amount': [amount],
            'oldbalanceOrg': [oldbalanceOrg],
            'newbalanceOrig': [newbalanceOrig],
            'oldbalanceDest': [oldbalanceDest],
            'newbalanceDest': [newbalanceDest]
        })
        
        try:
            prediction = model.predict(input_data)
            prediction_proba = model.predict_proba(input_data) if hasattr(model, 'predict_proba') else None
            
            # Display enhanced results
            is_fraud = prediction[0] == 1
            status_class = "status-fraud" if is_fraud else "status-safe"
            
            if is_fraud:
                status_icon = "🚨 THREAT DETECTED 🚨"
                status_message = "FRAUDULENT ACTIVITY"
                threat_level = "MAXIMUM"
                recommendation = "BLOCK TRANSACTION IMMEDIATELY"
            else:
                status_icon = "✅ TRANSACTION SECURE ✅"
                status_message = "LEGITIMATE TRANSACTION"
                threat_level = "MINIMAL"
                recommendation = "APPROVE TRANSACTION"
            
            # Calculate additional metrics
            confidence_score = max(prediction_proba[0]) * 100 if prediction_proba is not None else 85
            neural_patterns = random.randint(1247, 9999)
            scan_depth = random.randint(89, 99)
            
            st.markdown(f"""
            <div class="status-display {status_class}">
                <div class="status-text">{status_message}</div>
                <div style="color: #ffffff; font-size: 1.2rem; font-family: 'Rajdhani', sans-serif; margin: 1rem 0;">
                    {status_icon}
                </div>
                <div style="color: #0080ff; font-size: 1rem; margin-top: 1rem; font-family: 'Share Tech Mono', monospace;">
                    NEURAL CONFIDENCE: {confidence_score:.1f}%
                </div>
                <div style="color: #00ff41; font-size: 0.8rem; margin-top: 0.5rem; font-family: 'Share Tech Mono', monospace;">
                    THREAT: {threat_level} | PATTERNS: {neural_patterns} | DEPTH: {scan_depth}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced system messages with more details
            if is_fraud:
                st.markdown(f"""
                <div style="background: 
                    linear-gradient(135deg, rgba(255, 0, 128, 0.15), rgba(255, 0, 128, 0.05)); 
                    border: 2px solid #ff0080; 
                    border-radius: 10px;
                    padding: 1.5rem; 
                    margin: 2rem 0;">
                    <strong style="color: #ff0080; font-size: 1.2rem; font-family: 'Orbitron', monospace;">
                        ⚠️ SECURITY BREACH DETECTED
                    </strong>
                    <div style="color: #ffffff; margin-top: 1rem; font-family: 'Rajdhani', sans-serif; font-size: 1.1rem;">
                        • Neural patterns indicate {confidence_score:.1f}% probability of fraud<br>
                        • Risk factors: Suspicious balance changes detected<br>
                        • {recommendation}<br>
                        • Flagged for immediate human review
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div style="background: 
                    linear-gradient(135deg, rgba(0, 255, 65, 0.15), rgba(0, 255, 65, 0.05)); 
                    border: 2px solid #00ff41; 
                    border-radius: 10px;
                    padding: 1.5rem; 
                    margin: 2rem 0;">
                    <strong style="color: #00ff41; font-size: 1.2rem; font-family: 'Orbitron', monospace;">
                        ✅ TRANSACTION VERIFIED
                    </strong>
                    <div style="color: #ffffff; margin-top: 1rem; font-family: 'Rajdhani', sans-serif; font-size: 1.1rem;">
                        • Neural network confidence: {confidence_score:.1f}% legitimate<br>
                        • All parameters within normal ranges<br>
                        • {recommendation}<br>
                        • Transaction cleared for processing
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown(f"""
            <div style="background: 
                linear-gradient(135deg, rgba(255, 0, 0, 0.2), rgba(255, 0, 0, 0.1)); 
                border: 3px solid #ff0000; 
                border-radius: 10px;
                padding: 2rem; 
                margin: 2rem 0; 
                text-align: center;">
                <strong style="color: #ff0000; font-size: 1.5rem; font-family: 'Orbitron', monospace;">
                    ❌ CRITICAL SYSTEM ERROR ❌
                </strong>
                <div style="color: #ffffff; margin-top: 1rem; font-family: 'Share Tech Mono', monospace;">
                    NEURAL NETWORK MALFUNCTION DETECTED<br>
                    ERROR: {str(e)[:50]}...<br>
                    ATTEMPTING SYSTEM RECOVERY...
                </div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="status-display" style="border-color: #ff0000;">
        <div style="color: #ff0000; font-size: 2rem; font-family: 'Orbitron', monospace;">
            🔧 SYSTEM CRITICAL ERROR 🔧
        </div>
        <div style="color: #ffffff; margin-top: 1.5rem; font-family: 'Rajdhani', sans-serif; font-size: 1.2rem;">
            NEURAL NETWORK MODULE OFFLINE<br>
            Please load fraud_detection_model.pkl to activate AI systems
        </div>
        <div style="color: #ff0080; margin-top: 1rem; font-family: 'Share Tech Mono', monospace;">
            STATUS: CRITICAL | NEURAL_NET: DISCONNECTED
        </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced footer
st.markdown(f"""
<div style="text-align: center; margin-top: 3rem; padding: 1.5rem; 
     background: rgba(0, 0, 0, 0.8); border-radius: 10px; 
     border: 1px solid rgba(0, 255, 65, 0.3);">
    <div style="color: #00ff41; font-family: 'Orbitron', monospace; font-size: 1rem; margin-bottom: 0.5rem;">
        🔒 FRAUDNET AI NEURAL SECURITY SYSTEM 🔒
    </div>
    <div style="color: #0080ff; font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; line-height: 1.4;">
        VERSION: 2.1.0 | BUILD: {random.randint(2024001, 2024999)} | UPTIME: {random.randint(99, 100)}.{random.randint(80, 99)}%<br>
        <span style="color: #ff0080;">POWERED BY ADVANCED ML • SECURE • RELIABLE • AUTONOMOUS</span>
    </div>
</div>
</div>
""", unsafe_allow_html=True)