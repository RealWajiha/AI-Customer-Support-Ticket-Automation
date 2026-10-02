import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# 1. Page Config
st.set_page_config(
    page_title="AI Customer Support Ticket Automation",
    page_icon="⚡",
    layout="wide"
)

# 2. Dark Neon Glassmorphism Custom CSS
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #080B10;
        background-image: 
            radial-gradient(at 10% 10%, rgba(255, 0, 127, 0.15) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(0, 243, 255, 0.15) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(138, 43, 226, 0.1) 0px, transparent 50%);
        color: #E2E8F0;
    }

    /* Glassmorphic Container Card */
    .glass-card {
        background: rgba(18, 24, 38, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 0, 127, 0.3);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(255, 0, 127, 0.1);
        margin-bottom: 20px;
    }

    /* Cyan Glass Card */
    .glass-card-cyan {
        background: rgba(18, 24, 38, 0.65);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 243, 255, 0.3);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 243, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Neon Titles */
    .neon-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF007F 0%, #8A2BE2 50%, #00F3FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.4);
        margin-bottom: 5px;
    }

    /* Neon Badges */
    .badge-high {
        background: rgba(255, 0, 85, 0.2);
        color: #FF0055;
        border: 1px solid #FF0055;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.4);
    }
    
    .badge-medium {
        background: rgba(255, 170, 0, 0.2);
        color: #FFAA00;
        border: 1px solid #FFAA00;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 170, 0, 0.4);
    }

    .badge-low {
        background: rgba(0, 243, 255, 0.2);
        color: #00F3FF;
        border: 1px solid #00F3FF;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.4);
    }

    /* Streamlit Input Styling Override */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(10, 14, 23, 0.8) !important;
        color: #00F3FF !important;
        border: 1px solid rgba(138, 43, 226, 0.4) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FF007F !important;
        box-shadow: 0 0 10px rgba(255, 0, 127, 0.5) !important;
    }

    /* Primary Neon Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF007F 0%, #8A2BE2 100%) !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:first-child:hover {
        box-shadow: 0 0 25px rgba(0, 243, 255, 0.8) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("<h2 style='color: #00F3FF;'>⚙️ n8n Integration</h2>", unsafe_allow_html=True)
    n8n_webhook_url = st.text_input(
        "n8n Webhook URL:",
        value="https://your-n8n-instance.com/webhook/customer-support-ticket",
        type="password"
    )
    st.caption("Aap apne n8n workflow ka active Webhook URL yahan paste karein.")
    st.divider()
    st.markdown("### 🤖 Workflow Architecture")
    st.markdown("""
    - **Trigger:** Webhook POST
    - **AI Engine:** GPT-4o-mini
    - **Router:** Human Escalation vs Auto-Reply
    - **Alerts:** Slack Escalation
    - **Database:** Google Sheets Logging
    """)

# 4. App Main Header
col_logo, col_header = st.columns([1, 5])
with col_header:
    st.markdown("<div class='neon-title'>⚡AI Customer Support Ticket Automation</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A0AEC0;'>Autonomous Support Ticket Processing & Human Escalation System</p>", unsafe_allow_html=True)

st.write("")

# 5. Ticket Submission Form & Realtime Output Layout
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color: #FF007F; margin-top:0;'>📩 Submit Support Ticket</h3>
        <p style='font-size:0.85rem; color:#A0AEC0;'>Enter customer query details to trigger n8n AI workflow.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("ticket_form"):
        cust_name = st.text_input("Customer Name", value="Wajiha Fareed")
        cust_email = st.text_input("Customer Email", value="wajihafareed00@gmail.com")
        subject = st.text_input("Subject", value="URGENT: Payment Deducted But Subscription Inactive")
        message = st.text_area(
            "Issue Description",
            value="My payment of $50 was deducted yesterday via card, but my subscription status is still inactive. Please resolve or process refund immediately.",
            height=120
        )
        
        submit_btn = st.form_submit_button("🚀 Process Ticket with AI", use_container_width=True)

with col_output:
    st.markdown("""
    <div class='glass-card-cyan'>
        <h3 style='color: #00F3FF; margin-top:0;'>📊 AI Response & Routing Output</h3>
        <p style='font-size:0.85rem; color:#A0AEC0;'>Real-time decision logs returned from n8n pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

    if submit_btn:
        if not n8n_webhook_url or "your-n8n-instance" in n8n_webhook_url:
            st.error("Please sidebar me valid n8n Webhook URL enter karein.")
        else:
            ticket_id = f"TCK-{uuid.uuid4().hex[:5].upper()}"
            payload = {
                "ticket_id": ticket_id,
                "customer_name": cust_name,
                "customer_email": cust_email,
                "subject": subject,
                "message": message
            }

            with st.spinner("Connecting with n8n workflow & AI processing..."):
                try:
                    res = requests.post(n8n_webhook_url, json=payload, timeout=25)
                    
                    if res.status_code == 200:
                        st.success("Ticket Processed Successfully! ✅")
                        
                        try:
                            data = res.json()
                        except Exception:
                            data = payload
                        
                        # Category & Urgency Badges Display
                        category = data.get("category", "Billing")
                        urgency = data.get("urgency", "High")
                        requires_human = data.get("requires_human", True)
                        ai_reply = data.get("ai_response", "Assalam-o-Alaikum! We have received your query and escalated it to our human support team.")

                        urgency_class = "badge-high" if urgency.lower() == "high" else ("badge-medium" if urgency.lower() == "medium" else "badge-low")

                        st.markdown(f"""
                        <div class='glass-card'>
                            <p><strong>Ticket Reference:</strong> <span style='color:#00F3FF;'>{ticket_id}</span></p>
                            <p><strong>Category:</strong> <span style='color:#FF007F;'>{category}</span></p>
                            <p><strong>Urgency Level:</strong> <span class='{urgency_class}'>{urgency.upper()}</span></p>
                            <p><strong>Human Action Required:</strong> { "🚨 YES (Slack Escalated)" if requires_human else "✅ NO (Auto-Replied via Email)" }</p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("### 💬 Drafted / Sent AI Response")
                        st.info(ai_reply)

                    else:
                        st.error(f"n8n Webhook Error Code: {res.status_code}")
                        st.write("Response Text:", res.text)

                except Exception as err:
                    st.error(f"Failed to connect with n8n Webhook: {str(err)}")
    else:
        st.info("Form fill karke **Process Ticket with AI** button par click karein.")