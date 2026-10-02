# AI-Customer-Support-Ticket-Automation
An end-to-end AI-powered customer support automation pipeline using n8n, OpenAI (GPT-4o-mini), Slack, Google Sheets, Gmail, and a Dark Neon Streamlit Web Portal
# Demo Link
https://ai-customer-support-ticket-automation.streamlit.app/
# ⚡ AI Customer Support Ticket Automation

An intelligent, end-to-end customer support ticket processing pipeline powered by **n8n workflow automation**, **OpenAI (GPT-4o-mini)**, and a modern **Dark Neon Streamlit Web Portal**.

This system automates incoming support query classification, evaluates urgency, automatically sends email responses, escalates critical issues to Slack, logs all records to Google Sheets, and provides an interactive web interface.

---

## 🌟 Key Features

- 🤖 **AI-Powered Categorization:** Automatically classifies support queries into *Billing*, *Technical*, *Account*, or *General*.
- 🚨 **Smart Escalation Routing:** Evaluates issue urgency (*High*, *Medium*, *Low*) and checks if human intervention (`requires_human`) is needed.
- 💬 **Slack Real-Time Alerts:** Instantly sends escalated high-priority tickets to a dedicated `#support-escalations` Slack channel.
- 📧 **Automated Gmail Auto-Replies:** Generates polite, empathetic, and contextual replies directly to customers via Gmail.
- 📊 **Google Sheets Logging:** Stores ticket metadata, urgency level, category, and AI draft responses for full auditability.
- 🎨 **Dark Neon Streamlit Portal:** Interactive glassmorphism UI with live status indicators and real-time n8n webhook integration.

---

## 🏗️ Architecture & Workflow

```text
[ User / Webhook ] 
       │
       ▼
[ Incoming Ticket Webhook (n8n) ]
       │
       ▼
[ Support AI Agent (GPT-4o-mini) ]
       │
       ▼
[ Parse AI Output (JSON Structuring) ]
       │
       ▼
[ Route Ticket (Switch Node) ]
      ├───► (Requires Human = True)  ──► [ Slack Escalation Alert ] ──┐
      └───► (Requires Human = False) ──► [ Send Gmail Auto-Response ] ─┼──► [ Log Ticket to Google Sheets ]
