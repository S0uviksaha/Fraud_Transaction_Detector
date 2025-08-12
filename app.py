import streamlit as st
import pandas as pd
import joblib
import time

# Page configuration
st.set_page_config(
    page_title="FraudNet AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for cyberpunk/dark theme
st.markdown("""
<style>
    /* Import cyberpunk font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Terminal-style container */
    .terminal-container {
        background: rgba(0, 0, 0, 0.85);
        border: 2px solid #00ff41;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 
            0 0 20px rgba(0, 255, 65, 0.3),
            inset 0 0 20px rgba(0, 255, 65, 0.1);
        position: relative;
    }
    
    .terminal-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #ff0080, #00ff41, #0080ff);
        animation: scan 2s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Cyberpunk header */
    .cyber-header {
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .cyber-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #ff0080, #00ff41, #0080ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
        animation: glitch 3s infinite;
    }
    
    @keyframes glitch {
        0%, 90%, 100% { transform: translateX(0); }
        92% { transform: translateX(-2px); }
        94% { transform: translateX(2px); }
        96% { transform: translateX(-1px); }
        98% { transform: translateX(1px); }
    }
    
    .cyber-subtitle {
        font-size: 1.2rem;
        color: #00ff41;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.8;
    }
    
    /* Grid system */
    .data-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Input panels */
    .input-panel {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid #00ff41;
        border-radius: 8px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .input-panel:hover {
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        border-color: #ff0080;
    }
    
    .input-panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        animation: slideIn 2s infinite;
    }
    
    @keyframes slideIn {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .panel-label {
        color: #00ff41;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    /* Matrix-style background */
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.03;
        z-index: -1;
        font-family: monospace;
        color: #00ff41;
        overflow: hidden;
    }
    
    /* Status display */
    .status-display {
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #00ff41;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        animation: powerUp 0.8s ease-out;
    }
    
    @keyframes powerUp {
        0% { 
            opacity: 0;
            transform: scale(0.8);
            border-color: transparent;
        }
        50% { 
            border-color: #ff0080;
        }
        100% { 
            opacity: 1;
            transform: scale(1);
            border-color: #00ff41;
        }
    }
    
    .status-fraud {
        border-color: #ff0080 !important;
        box-shadow: 0 0 30px rgba(255, 0, 128, 0.3) !important;
    }
    
    .status-safe {
        border-color: #00ff41 !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.3) !important;
    }
    
    .status-text {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 1rem;
    }
    
    .status-fraud .status-text {
        color: #ff0080;
        animation: pulse-red 1.5s infinite;
    }
    
    .status-safe .status-text {
        color: #00ff41;
        animation: pulse-green 1.5s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes pulse-green {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Command line style button */
    .cmd-button {
        background: linear-gradient(45deg, #0a0a0a, #1a1a2e);
        border: 2px solid #00ff41;
        color: #00ff41;
        padding: 1rem 3rem;
        font-family: 'Orbitron', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        cursor: pointer;
        border-radius: 5px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .cmd-button:hover {
        background: linear-gradient(45deg, #00ff41, #0080ff);
        color: #000000;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        transform: translateY(-2px);
    }
    
    .cmd-button::before {
        content: '> ';
        font-weight: bold;
    }
    
    /* Data stream visualization */
    .data-stream {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #0080ff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .stream-line {
        color: #0080ff;
        margin: 0.2rem 0;
        opacity: 0;
        animation: typewriter 0.5s ease-in-out forwards;
    }
    
    .stream-line:nth-child(1) { animation-delay: 0.1s; }
    .stream-line:nth-child(2) { animation-delay: 0.2s; }
    .stream-line:nth-child(3) { animation-delay: 0.3s; }
    .stream-line:nth-child(4) { animation-delay: 0.4s; }
    
    @keyframes typewriter {
        0% { opacity: 0; transform: translateX(-10px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    /* Loading animation */
    .neural-loading {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .neural-spinner {
        width: 80px;
        height: 80px;
        border: 3px solid transparent;
        border-top: 3px solid #00ff41;
        border-right: 3px solid #ff0080;
        border-bottom: 3px solid #0080ff;
        border-radius: 50%;
        animation: neural-spin 1s linear infinite;
        position: relative;
    }
    
    .neural-spinner::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 40px;
        height: 40px;
        border: 2px solid transparent;
        border-top: 2px solid #ff0080;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        animation: neural-spin 0.5s linear infinite reverse;
    }
    
    @keyframes neural-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00ff41;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ff0080;
    }
    
</style>
""", unsafe_allow_html=True)

# Matrix-style background effect
st.markdown("""
<div class="matrix-bg">
    <div style="position: absolute; top: 10%; left: 5%; animation: fadeInOut 3s infinite;">01010110</div>
    <div style="position: absolute; top: 30%; left: 80%; animation: fadeInOut 4s infinite;">11001010</div>
    <div style="position: absolute; top: 60%; left: 15%; animation: fadeInOut 2s infinite;">10110001</div>
    <div style="position: absolute; top: 80%; left: 70%; animation: fadeInOut 3.5s infinite;">01101100</div>
    <div style="position: absolute; top: 20%; left: 50%; animation: fadeInOut 2.8s infinite;">11010110</div>
</div>
<style>
@keyframes fadeInOut {
    0%, 100% { opacity: 0; }
    50% { opacity: 0.1; }
}
</style>
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

# Cyberpunk header
st.markdown("""
<div class="cyber-header">
    <div class="cyber-title">⚡ FRAUDNET AI ⚡</div>
    <div class="cyber-subtitle">Neural Fraud Detection System v2.1</div>
</div>
""", unsafe_allow_html=True)

if model is not None:
    # Transaction data input
    st.markdown("### 📡 DATA INPUT INTERFACE")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">⚡ Transaction Protocol</div>', unsafe_allow_html=True)
        transaction_type = st.selectbox("", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">💰 Credit Amount</div>', unsafe_allow_html=True)
        amount = st.number_input("", min_value=0.0, value=1000.0, format="%.2f", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📊 Origin Balance [OLD]</div>', unsafe_allow_html=True)
        oldbalanceOrg = st.number_input("", min_value=0.0, value=10000.0, format="%.2f", label_visibility="collapsed", key="old_orig")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📈 Origin Balance [NEW]</div>', unsafe_allow_html=True)
        newbalanceOrig = st.number_input("", min_value=0.0, value=9000.0, format="%.2f", label_visibility="collapsed", key="new_orig")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📡 Target Balance [OLD]</div>', unsafe_allow_html=True)
        oldbalanceDest = st.number_input("", min_value=0.0, value=0.0, format="%.2f", label_visibility="collapsed", key="old_dest")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">🎯 Target Balance [NEW]</div>', unsafe_allow_html=True)
        newbalanceDest = st.number_input("", min_value=0.0, value=0.0, format="%.2f", label_visibility="collapsed", key="new_dest")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data stream display
    st.markdown("""
    <div class="data-stream">
        <div class="stream-line">> TRANSACTION_TYPE: """ + transaction_type + """</div>
        <div class="stream-line">> AMOUNT_USD: $""" + f"{amount:,.2f}" + """</div>
        <div class="stream-line">> ORIGIN_DELTA: $""" + f"{oldbalanceOrg - newbalanceOrig:,.2f}" + """</div>
        <div class="stream-line">> TARGET_DELTA: $""" + f"{newbalanceDest - oldbalanceDest:,.2f}" + """</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Neural network analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("INITIATE NEURAL SCAN", key="analyze", help="Execute fraud detection algorithm")
        if analyze_button:
            st.markdown('<style>.cmd-button { all: unset; }</style>', unsafe_allow_html=True)
    
    # Analysis results
    if analyze_button:
        # Loading animation
        with st.empty():
            st.markdown("""
            <div class="neural-loading">
                <div class="neural-spinner"></div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1.5)
        
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
            
            # Display results
            is_fraud = prediction[0] == 1
            status_class = "status-fraud" if is_fraud else "status-safe"
            status_icon = "🚨 THREAT DETECTED 🚨" if is_fraud else "✅ SECURE TRANSACTION ✅"
            status_message = "FRAUDULENT ACTIVITY IDENTIFIED" if is_fraud else "LEGITIMATE TRANSACTION CONFIRMED"
            
            confidence_text = ""
            if prediction_proba is not None:
                confidence = max(prediction_proba[0]) * 100
                confidence_text = f"<div style='color: #0080ff; font-size: 1.2rem; margin-top: 1rem;'>NEURAL CONFIDENCE: {confidence:.1f}%</div>"
            
            st.markdown(f"""
            <div class="status-display {status_class}">
                <div class="status-text">{status_message}</div>
                <div style="color: #ffffff; font-size: 1.3rem; font-family: 'Rajdhani', sans-serif;">
                    {status_icon}
                </div>
                {confidence_text}
            </div>
            """, unsafe_allow_html=True)
            
            # Additional system messages
            if is_fraud:
                st.markdown("""
                <div style="background: rgba(255, 0, 128, 0.1); border-left: 4px solid #ff0080; padding: 1rem; margin: 1rem 0; border-radius: 5px;">
                    <strong>⚠️ SECURITY ALERT:</strong> Neural patterns indicate high probability of fraudulent activity. Immediate review recommended.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(0, 255, 65, 0.1); border-left: 4px solid #00ff41; padding: 1rem; margin: 1rem 0; border-radius: 5px;">
                    <strong>✅ SYSTEM STATUS:</strong> Transaction parameters within acceptable ranges. Neural network approves.
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown(f"""
            <div style="background: rgba(255, 0, 0, 0.1); border: 2px solid #ff0000; padding: 1rem; margin: 1rem 0; border-radius: 5px; text-align: center;">
                <strong>❌ SYSTEM ERROR:</strong> Neural network malfunction - {str(e)}
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="status-display" style="border-color: #ff0000;">
        <div style="color: #ff0000; font-size: 2rem; font-family: 'Orbitron', monospace;">
            🔧 SYSTEM OFFLINE 🔧
        </div>
        <div style="color: #ffffff; margin-top: 1rem;">
            Neural network model not detected. Please load fraud_detection_model.pkl
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1rem; color: #00ff41; font-family: 'Orbitron', monospace; font-size: 0.9rem; border-top: 1px solid #00ff41;">
    🔒 FRAUDNET AI SYSTEM • NEURAL SECURITY PROTOCOLS ACTIVE • v2.1.0
</div>
</div>
""", unsafe_allow_html=True)