import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import random
import numpy as np
import pymongo
import requests
import time

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="ConnectFast Broadband Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# MONGODB CONNECTION
# ===============================
MONGO_URI = "mongodb+srv://prasadpolisetti12345_db_user:chanti123@broadbandplan.e8xj3fs.mongodb.net/?retryWrites=true&w=majority&appName=BroadbandPlan"
client = pymongo.MongoClient(MONGO_URI)
db = client["BroadbandDB"]
users_collection = db["users"]
plans_collection = db["Plans"]
customers_collection = db["CustomerPlans"]
tickets_collection = db["Tickets"]

# ===============================
# ENHANCED CSS STYLING - LIGHT THEME
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
/* Global Variables */
:root {
    --primary-color: #4A90E2;
    --secondary-color: #5D6D7E;
    --accent-color: #3498DB;
    --success-color: #2ECC71;
    --warning-color: #F39C12;
    --danger-color: #E74C3C;
    --light-bg: #F8F9FA;
    --card-bg: #FFFFFF;
    --text-primary: #2C3E50;
    --text-secondary: #7F8C8D;
    --border-radius: 12px;
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    --gradient-1: linear-gradient(135deg, #4A90E2 0%, #3498DB 100%);
    --gradient-2: linear-gradient(135deg, #AED6F1 0%, #D6EAF8 100%);
    --gradient-3: linear-gradient(135deg, #ABEBC6 0%, #D5F4E6 100%);
}
/* Remove Streamlit branding and margins */
#MainMenu {visibility: visible;}
footer {visibility: visible;}
header {visibility: visible;}
/* Main container styling */
.stApp {
    background-color: #F8F9FA;
    font-family: 'Inter', sans-serif;
}
/* Content container */
[data-testid="stAppViewContainer"] {
    background-color: #F8F9FA;
    border-radius: 20px;
    margin: 20px;
    padding: 20px;
    box-shadow: var(--shadow);
}
/* Header styling */
h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    color: var(--primary-color);
    text-align: center;
    margin-bottom: 2rem;
}
/* Subheader styling */
h2, h3 {
    color: var(--text-primary);
    font-weight: 600;
    margin: 1.5rem 0;
}
/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: var(--card-bg);
    padding: 8px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 0 24px;
    background: transparent;
    border-radius: 12px;
    color: var(--text-secondary);
    font-weight: 500;
    transition: all 0.3s ease;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: var(--gradient-1);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
}
/* Enhanced card styling */
.metric-card {
    background: var(--card-bg);
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border: 1px solid rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient-1);
    border-radius: var(--border-radius) var(--border-radius) 0 0;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}
.plan-card {
    background: var(--card-bg);
    padding: 2rem;
    margin: 1rem 0;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border-left: 6px solid var(--primary-color);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.plan-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, transparent, rgba(74, 144, 226, 0.1), transparent);
    transform: rotate(45deg);
    transition: all 0.3s ease;
    opacity: 0;
}
.plan-card:hover::after {
    animation: shimmer 0.6s ease-in-out;
}
@keyframes shimmer {
    0% { transform: translateX(-100%) rotate(45deg); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateX(100%) rotate(45deg); opacity: 0; }
}
.plan-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 24px rgba(74, 144, 226, 0.15);
    border-left-color: var(--accent-color);
}
.plan-card h3 {
    color: var(--primary-color);
    font-size: 1.5rem;
    margin-bottom: 1rem;
}
/* Form styling */
.stForm {
    background: var(--card-bg);
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}
/* Button styling */
.stButton > button {
    background: var(--gradient-1);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.4);
}
/* DataFrame styling */
[data-testid="stDataFrame"] {
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.05);
}
/* Metric styling */
[data-testid="metric-container"] {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border: 1px solid rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}
/* Status indicators */
.status-normal {
    color: var(--success-color);
    font-weight: 600;
}
.status-anomaly {
    color: var(--danger-color);
    font-weight: 600;
}
/* Animation classes */
.fade-in {
    animation: fadeIn 0.6s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.slide-in {
    animation: slideIn 0.8s ease-out;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}
/* Success message styling */
.element-container:has([data-testid="stAlert"]) {
    position: relative;
}
[data-testid="stAlert"] {
    border-radius: var(--border-radius);
    border: none;
    box-shadow: var(--shadow);
}
/* Divider styling */
hr {
    margin: 2rem 0;
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(74, 144, 226, 0.3), transparent);
}
/* Input field styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 12px;
    border: 2px solid rgba(74, 144, 226, 0.2);
    transition: all 0.3s ease;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}
/* Loading animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.loading {
    animation: pulse 2s infinite;
}
/* Additional styles from broadband portal */
.main-header {
    font-size: 50px;
    color: var(--primary-color);
    text-align: center;
    margin-bottom: 30px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
.sub-header {
    font-size: 30px;
    color: var(--primary-color);
    border-bottom: 3px solid var(--accent-color);
    padding-bottom: 10px;
    margin-top: 30px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
}
.feature-card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: var(--shadow);
    height: 100%;
}
.hero-section {
    background: var(--gradient-1);
    color: white;
    border-radius: 15px;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: var(--shadow);
}
.testimonial-card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 20px;
    box-shadow: var(--shadow);
    border-left: 4px solid var(--accent-color);
    height: 100%;
}
.quick-action-btn {
    background: var(--gradient-3) !important;
    color: white !important;
    border: none !important;
}
.secondary-btn {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
}
.current-plan {
    background: var(--gradient-3);
    animation: pulse 2s infinite;
}
.bill-card {
    background: var(--gradient-2);
    color: var(--text-primary);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: var(--shadow);
    border: 3px solid var(--accent-color);
    position: relative;
}
.usage-details-card {
    background: var(--gradient-1);
    border-radius: 20px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: var(--shadow);
    color: white;
    border: 2px solid var(--accent-color);
}
.quick-actions {
    display: flex;
    justify-content: flex-end;
    gap: 15px;
    margin-bottom: 25px;
    flex-wrap: wrap;
}
.option-card {
    background: var(--gradient-2);
    border-radius: 20px;
    padding: 25px;
    box-shadow: var(--shadow);
    margin-bottom: 25px;
    border: 3px solid var(--accent-color);
    animation: slideIn 0.5s ease-out;
}
.notification-panel {
    background: var(--gradient-2);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: var(--shadow);
    border-left: 5px solid var(--warning-color);
}
.support-panel {
    background: var(--gradient-2);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: var(--shadow);
    border-left: 5px solid var(--success-color);
}
.faq-panel {
    background: var(--gradient-2);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: var(--shadow);
    border-left: 5px solid var(--primary-color);
}
.sidebar-metric {
    background: var(--gradient-1);
    color: white;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    text-align: center;
    box-shadow: var(--shadow);
}
.status-good { color: var(--success-color); font-weight: bold; }
.status-warning { color: var(--warning-color); font-weight: bold; }
.status-error { color: var(--danger-color); font-weight: bold; }
.footer {
    background: var(--gradient-1);
    color: white;
    text-align: center;
    padding: 30px;
    border-radius: 15px;
    margin-top: 40px;
    box-shadow: var(--shadow);
}
.full-page-container {
    background-color: var(--card-bg);
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: var(--shadow);
}

/* Sidebar collapse button fix */
.css-1lcbmhc {
    display: block !important;
}

/* Ensure sidebar collapse button is always visible */
div[data-testid="stSidebar"] > div:first-child {
    display: block !important;
    visibility: visible !important;
}

/* Make sure the sidebar collapse button is properly positioned */
button[aria-label="sidebar"] {
    display: block !important;
    visibility: visible !important;
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 1000 !important;
}

@media (max-width: 768px) {
    .quick-actions {
        flex-direction: column;
        align-items: stretch;
    }
    .main-header {
        font-size: 40px;
    }
}
</style>
""", unsafe_allow_html=True)

# ===============================
# DEFAULT ADMIN
# ===============================
def create_default_admin():
    if not users_collection.find_one({"email": "admin@portal.com"}):
        users_collection.insert_one({
            "name": "Super Admin",
            "email": "admin@portal.com",
            "password": "admin@123",
            "role": "admin",
            "approved": True,
            "created_at": datetime.now()
        })
create_default_admin()

# ===============================
# AUTH FUNCTIONS
# ===============================
def signup(name, email, password):
    if users_collection.find_one({"email": email}):
        return False, "⚠ Email already registered!"
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "role": "customer",
        "approved": False,
        "current_plan": None,
        "created_at": datetime.now()
    })
    return True, "✅ Signup successful! Wait for admin approval."

def login(email, password):
    user = users_collection.find_one({"email": email, "password": password})
    if not user:
        return None, "❌ Invalid email or password!"
    if user["role"] == "customer" and not user.get("approved", False):
        return None, "⏳ Waiting for admin approval."
    return user, f"✅ Welcome {user['name']}!"

# ===============================
# ADMIN DASHBOARD
# ===============================
def admin_dashboard(user):
    st.markdown(f"### 👑 Welcome, {user['name']} (Admin)")
    
    # Admin Sidebar - Removed profile section
    with st.sidebar:
        st.markdown("### 👑 Admin Panel")
        
        st.divider()
        
        # Quick stats
        total_users = len(list(users_collection.find()))
        total_plans = len(list(plans_collection.find()))
        total_tickets = len(list(tickets_collection.find()))
        
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Users", total_users)
        st.metric("Total Plans", total_plans)
        st.metric("Open Tickets", len([t for t in tickets_collection.find() if "Open" in t.get("Status", "")]))
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", key="admin_logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()
    
    tabs = st.tabs([
        "📊 Analytics", 
        "🔮 AI Predictions", 
        "🛠 Manage Plans", 
        "🎫 Support Tickets", 
        "👥 Users",
        "➕ Add User",
        "➕ Add Plan"
    ])
    
    # ---------- ANALYTICS TAB ----------
    with tabs[0]:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        
        # KPI Animation Placeholder
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="display: inline-block; padding: 15px; background: linear-gradient(135deg, #4A90E2, #3498DB); border-radius: 15px; color: white; font-weight: bold;">
                📊 Key Performance Indicators
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📌 Key Performance Indicators")
        
        # Get data from MongoDB
        all_plans = list(plans_collection.find())
        all_customers = list(customers_collection.find())
        
        # Calculate metrics
        total_subscribers = len(all_customers)
        total_revenue = sum(customer.get('monthly_cost', 0) for customer in all_customers)
        avg_price = sum(plan.get('monthly_cost', 0) for plan in all_plans) / len(all_plans) if all_plans else 0
        active_plans = len(all_plans)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Subscribers", f"{total_subscribers:,}", "▲ +12 this month 🚀")
        col2.metric("Monthly Revenue", f"₹{total_revenue:,}", "▲ ₹15,600 💰")
        col3.metric("Average Plan Price", f"₹{avg_price:,.0f}", "▲ ₹200 📈")
        col4.metric("Active Plans", active_plans, "➕ 1 new plan 🎯")
        
        st.divider()
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Subscribers by Plan")
            if all_plans:
                plan_subscribers = []
                for plan in all_plans:
                    subscribers_count = len([c for c in all_customers if c.get('plan_name') == plan.get('plan_name')])
                    plan_subscribers.append({
                        "Plan": plan.get('plan_name'),
                        "Subscribers": subscribers_count
                    })
                
                subscribers_df = pd.DataFrame(plan_subscribers)
                colors = ['#4A90E2', '#5D6D7E', '#3498DB', '#AED6F1']
                fig = px.bar(
                    subscribers_df, 
                    x="Plan", 
                    y="Subscribers", 
                    color="Plan",
                    color_discrete_sequence=colors,
                    text="Subscribers"
                )
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No plans available")
        
        with col2:
            st.markdown("### 💰 Revenue Distribution")
            if all_plans:
                revenue_data = []
                for plan in all_plans:
                    plan_customers = [c for c in all_customers if c.get('plan_name') == plan.get('plan_name')]
                    revenue = len(plan_customers) * plan.get('monthly_cost', 0)
                    revenue_data.append({
                        "Plan": plan.get('plan_name'),
                        "Revenue": revenue
                    })
                
                revenue_df = pd.DataFrame(revenue_data)
                colors = ['#4A90E2', '#5D6D7E', '#3498DB', '#AED6F1']
                fig = px.pie(
                    revenue_df, 
                    values="Revenue", 
                    names="Plan",
                    color_discrete_sequence=colors,
                    hole=0.4
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No plans available")
        
        st.divider()
        
        # Revenue trends
        st.markdown("### 📊 Revenue Trends (6 Months)")
        revenue_df = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Revenue": [65000, 72000, 68000, 78000, 74000, 82000],
            "Subscribers": [220, 235, 240, 255, 250, 275]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=revenue_df["Month"], 
            y=revenue_df["Revenue"],
            mode='lines+markers',
            name='Revenue (₹)',
            line=dict(color='#4A90E2', width=4),
            marker=dict(size=10, color='#4A90E2')
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            yaxis_title="Revenue (₹)",
            xaxis_title="Month"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.markdown("### 📋 Plans Overview")
        if all_plans:
            plans_df = pd.DataFrame(all_plans)
            styled_df = plans_df.style.apply(lambda x: ['background: linear-gradient(90deg, #f8f9ff, #fff)'] * len(x), axis=1)
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.info("No plans available")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- PREDICTIONS TAB ----------
    with tabs[1]:
        st.markdown("<div class='slide-in'>", unsafe_allow_html=True)
        
        # Analytics Animation Placeholder
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="display: inline-block; padding: 15px; background: linear-gradient(135deg, #4A90E2, #3498DB); border-radius: 15px; color: white; font-weight: bold;">
                🔮 AI Analytics
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔮 Customer Churn Prediction")
        
        # Generate more realistic churn data
        churn_data = pd.DataFrame({
            "user_id": range(1, 26),
            "total_usage": [850, 1200, 750, 400, 300, 1600, 1250, 1500, 250, 150,
                            2000, 2400, 2800, 400, 600, 1500, 1000, 750, 450, 200,
                            1800, 2200, 1900, 350, 800],
            "months": [12, 18, 15, 3, 2, 24, 20, 22, 2, 1,
                       36, 42, 30, 3, 6, 20, 15, 12, 4, 2,
                       28, 32, 26, 3, 10],
            "support_tickets": [0, 1, 2, 5, 8, 0, 1, 0, 12, 15,
                               0, 0, 1, 8, 4, 1, 2, 3, 6, 10,
                               0, 1, 0, 9, 3]
        })
        
        # Enhanced churn prediction
        churn_data["churn"] = ((churn_data["months"] < 6) | (churn_data["support_tickets"] > 7)).astype(int)
        X = churn_data[["total_usage", "months", "support_tickets"]]
        y = churn_data["churn"]
        
        model = LogisticRegression(random_state=42).fit(X, y)
        churn_data["churn_risk"] = model.predict_proba(X)[:, 1].round(3)
        churn_data["risk_level"] = pd.cut(churn_data["churn_risk"], 
                                          bins=[0, 0.3, 0.7, 1.0], 
                                          labels=["Low 🟢", "Medium 🟡", "High 🔴"])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📊 Churn Risk Analysis")
            # Create scatter plot
            fig = px.scatter(churn_data, 
                            x="months", 
                            y="total_usage", 
                            size="support_tickets",
                            color="churn_risk",
                            color_continuous_scale="RdYlGn_r",
                            hover_data=["user_id", "risk_level"])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Risk Summary")
            risk_summary = churn_data["risk_level"].value_counts()
            for level, count in risk_summary.items():
                st.metric(f"{level} Risk", count)
        
        st.markdown("#### 📋 Detailed Churn Risk Table")
        display_df = churn_data[["user_id", "total_usage", "months", "support_tickets", "churn_risk", "risk_level"]]
        st.dataframe(
            display_df.style.background_gradient(subset=["churn_risk"], cmap="RdYlGn_r"),
            use_container_width=True
        )
        
        st.divider()
        
        st.markdown("### ⚡ Usage Anomaly Detection")
        
        # Enhanced anomaly detection
        usage_data = pd.DataFrame({
            "user_id": range(1, 31),
            "data_used_gb": [45, 52, 48, 156, 50, 47, 189, 51, 49, 52,
                            46, 234, 53, 48, 51, 47, 278, 49, 52, 48,
                            50, 312, 47, 51, 49, 346, 52, 48, 50, 298]
        })
        
        model_if = IsolationForest(contamination=0.15, random_state=42)
        usage_data["anomaly"] = model_if.fit_predict(usage_data[["data_used_gb"]])
        usage_data["status"] = usage_data["anomaly"].map({-1: "Anomaly 🚨", 1: "Normal ✅"})
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            colors = ['#E74C3C' if x == 'Anomaly 🚨' else '#3498DB' for x in usage_data["status"]]
            fig = px.bar(usage_data, 
                        x="user_id", 
                        y="data_used_gb",
                        color="status",
                        color_discrete_map={"Normal ✅": "#3498DB", "Anomaly 🚨": "#E74C3C"})
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            normal_count = sum(usage_data["status"] == "Normal ✅")
            anomaly_count = sum(usage_data["status"] == "Anomaly 🚨")
            st.metric("Normal Usage", normal_count)
            st.metric("Anomalies Detected", anomaly_count)
        
        st.dataframe(usage_data, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- MANAGE PLANS TAB ----------
    with tabs[2]:
        st.markdown("### 🛠 Manage Broadband Plans")
        
        all_plans = list(plans_collection.find())
        
        for plan in all_plans:
            subscribers_count = len([c for c in customers_collection.find() if c.get('plan_name') == plan.get('plan_name')])
            revenue = plan.get('monthly_cost', 0) * subscribers_count
            st.markdown(f"""
            <div class='plan-card'>
                <h3>📦 {plan.get('plan_name')}</h3>
                <p><strong>💰 Price:</strong> ₹{plan.get('monthly_cost', 0):,}/month</p>
                <p><strong>👥 Subscribers:</strong> {subscribers_count:,}</p>
                <p><strong>💵 Monthly Revenue:</strong> ₹{revenue:,}</p>
                <p><strong>📝 Description:</strong> {plan.get('description', 'No description')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Plan comparison
        st.markdown("### 📊 Plan Comparison")
        if all_plans:
            comparison_data = []
            for plan in all_plans:
                subscribers_count = len([c for c in customers_collection.find() if c.get('plan_name') == plan.get('plan_name')])
                revenue = plan.get('monthly_cost', 0) * subscribers_count
                comparison_data.append({
                    "Plan": plan.get('plan_name'),
                    "Price": plan.get('monthly_cost', 0),
                    "Subscribers": subscribers_count,
                    "Revenue": revenue
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            fig = px.scatter(comparison_df, 
                            x="Price", 
                            y="Subscribers",
                            size="Revenue",
                            color="Plan",
                            hover_data=["Revenue"])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No plans available")
    
    # ---------- SUPPORT TICKETS TAB - Remove resolved tickets ----------
    with tabs[3]:
        st.markdown("### 🎫 Customer Support Tickets")
        
        # Get tickets from MongoDB
        all_tickets = list(tickets_collection.find())
        
        if len(all_tickets) == 0:
            st.info("🎉 No open tickets! Great job team!")
        else:
            # Tickets overview
            col1, col2, col3 = st.columns(3)
            
            open_tickets = sum(1 for t in all_tickets if "Open" in t.get("Status", ""))
            in_progress = sum(1 for t in all_tickets if "Progress" in t.get("Status", ""))
            resolved = sum(1 for t in all_tickets if "Resolved" in t.get("Status", ""))
            
            col1.metric("🔴 Open Tickets", open_tickets)
            col2.metric("🟡 In Progress", in_progress)  
            col3.metric("🟢 Resolved", resolved)
            
            st.divider()
            
            # Tickets table
            tickets_df = pd.DataFrame(all_tickets)
            st.dataframe(tickets_df, use_container_width=True)
            
            st.divider()
            
            # Ticket management - Remove resolved tickets
            st.markdown("### 🛠 Ticket Management")
            
            with st.form("update_ticket_form"):
                if all_tickets:
                    ticket_options = [f"ID {t.get('ID')}: {t.get('Customer')}" for t in all_tickets]
                    selected = st.selectbox("Select Ticket", ticket_options)
                    new_status = st.selectbox("New Status", [
                        "Open 🔴", 
                        "In Progress 🟡", 
                        "Resolved ✅"
                    ])
                    submitted = st.form_submit_button("Update Status")
                    
                    if submitted:
                        ticket_id = int(selected.split(":")[0].replace("ID ", "")) - 1
                        ticket_to_update = all_tickets[ticket_id]
                        
                        if new_status == "Resolved ✅":
                            # Delete the ticket from database
                            tickets_collection.delete_one({"_id": ticket_to_update["_id"]})
                            st.success(f"✅ Ticket resolved and removed from the system!")
                        else:
                            # Update the ticket status
                            tickets_collection.update_one(
                                {"_id": ticket_to_update["_id"]},
                                {"$set": {"Status": new_status}}
                            )
                            st.success(f"✅ Ticket status updated!")
                        st.rerun()
    
    # ---------- USERS TAB ----------
    with tabs[4]:
        st.markdown("### 👥 All Users")
        all_users = list(users_collection.find())
        if all_users:
            users_data = []
            for u in all_users:
                users_data.append({
                    "Name": u['name'],
                    "Email": u['email'],
                    "Role": u['role'],
                    "Status": "Approved" if u.get("approved", False) else "Pending",
                    "Current Plan": u.get("current_plan", "None")
                })
            df_users = pd.DataFrame(users_data)
            st.dataframe(df_users, use_container_width=True)
            
            # Approve pending users
            for u in all_users:
                if not u.get("approved", False):
                    if st.button(f"Approve {u['email']}", key=f"approve_{u['_id']}"):
                        users_collection.update_one({"_id": u["_id"]}, {"$set": {"approved": True}})
                        st.success(f"✅ Approved {u['name']}")
        else:
            st.info("No users found.")
    
    # ---------- ADD USER TAB ----------
    with tabs[5]:
        st.markdown("### ➕ Add New User")
        name = st.text_input("Full Name", key="add_user_name")
        email = st.text_input("Email", key="add_user_email")
        password = st.text_input("Password", type="password", key="add_user_pass")
        role = st.selectbox("Role", ["customer", "admin"], key="add_user_role")
        if st.button("Add User", key="add_user_btn"):
            if name and email and password:
                if users_collection.find_one({"email": email}):
                    st.error("Email already exists!")
                else:
                    users_collection.insert_one({
                        "name": name,
                        "email": email,
                        "password": password,
                        "role": role,
                        "approved": True if role=="admin" else False,
                        "current_plan": None,
                        "created_at": datetime.now()
                    })
                    st.success(f"User {name} added!")
            else:
                st.warning("Please fill all fields.")
    
    # ---------- ADD PLAN TAB ----------
    with tabs[6]:
        st.markdown("### ➕ Add New Broadband Plan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("add_plan_form"):
                st.markdown("#### 📋 Plan Details")
                new_plan = st.text_input("Plan Name", placeholder="e.g., Premium Pro")
                new_price = st.number_input("Monthly Price (₹)", min_value=100, step=100, value=1000)
                new_data = st.number_input("Data Limit (GB)", min_value=0, step=1, value=100)
                new_voice = st.number_input("Voice Minutes", min_value=0, step=10, value=100)
                new_validity = st.number_input("Validity (Days)", min_value=1, step=1, value=30)
                new_desc = st.text_area("Plan Description", 
                                       placeholder="Describe the features and benefits of this plan...")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    submitted = st.form_submit_button("✅ Add Plan", use_container_width=True)
                with col_b:
                    if st.form_submit_button("🔄 Reset Form", use_container_width=True):
                        st.rerun()
                
                if submitted and new_plan:
                    plans_collection.insert_one({
                        "plan_name": new_plan,
                        "monthly_cost": new_price,
                        "data_limit_gb": new_data,
                        "voice_minutes": new_voice,
                        "validity_days": new_validity,
                        "description": new_desc
                    })
                    st.success(f"🎉 Plan '{new_plan}' added successfully!")
                    st.balloons()
                    st.rerun()
        
        with col2:
            st.markdown("#### 📊 Plan Statistics")
            
            total_plans = len(list(plans_collection.find()))
            all_plans_list = list(plans_collection.find())
            avg_price = sum(plan.get('monthly_cost', 0) for plan in all_plans_list) / len(all_plans_list) if all_plans_list else 0
            total_subs = len(list(customers_collection.find()))
            
            st.metric("Total Plans", total_plans)
            st.metric("Average Price", f"₹{avg_price:,.0f}")
            st.metric("Total Subscribers", f"{total_subs:,}")
            
            st.markdown("#### 💡 Quick Tips")
            st.info("""
            *Best Practices:*
            - Keep plan names short and memorable
            - Price competitively with market rates
            - Write clear, benefit-focused descriptions
            - Consider your target audience
            """)
            
            # Preview section
            if 'new_plan' in locals() and new_plan:
                st.markdown("#### 👀 Live Preview")
                st.markdown(f"""
                <div class='plan-card' style='margin-top: 1rem;'>
                    <h3>📦 {new_plan}</h3>
                    <p><strong>💰 Price:</strong> ₹{new_price:,}/month</p>
                    <p><strong>📊 Data Limit:</strong> {new_data} GB</p>
                    <p><strong>📞 Voice Minutes:</strong> {new_voice}</p>
                    <p><strong>📅 Validity:</strong> {new_validity} days</p>
                    <p><strong>📝 Description:</strong> {new_desc if new_desc else 'No description provided'}</p>
                </div>
                """, unsafe_allow_html=True)

# ===============================
# CUSTOMER DASHBOARD
# ===============================
def customer_dashboard(user):
    # Initialize session state for user data
    if 'user_plan' not in st.session_state:
        # Get user's current plan from database
        st.session_state.user_plan = user.get("current_plan", None)
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            "name": user['name'],
            "join_date": "2023-01-15",
            "plan_start_date": "2024-01-15",
            "plan_end_date": "2024-12-31",
            "due_date": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
            "bill_amount": 49.99,
            "notifications": [
                "🎉 Your bill is due in 10 days", 
                "🚀 New premium plan available with 50% off!", 
                "💰 Special discount for Ultra Plan this month - Save $20!",
                "📊 Your data usage is at 75% this month",
                "🔧 Scheduled maintenance tonight from 2-4 AM"
            ]
        }
    
    # Initialize all session state variables
    session_vars = [
        'show_upgrade_options', 'show_downgrade_options', 'show_usage_details',
        'show_notifications', 'show_support', 'usage_data_generated',
        'show_billing_history', 'show_plan_optimizer', 'show_pause_confirmation',
        'show_cancel_confirmation', 'service_paused', 'subscription_cancelled',
        'show_faq'
    ]
    for var in session_vars:
        if var not in st.session_state:
            st.session_state[var] = False
    
    # Generate usage data if not exists
    if 'usage_data' not in st.session_state or not st.session_state.usage_data_generated:
        # Generate realistic usage data for the past 30 days
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        daily_usage = np.random.normal(25, 8, 30)  # Average 25GB per day
        daily_usage = np.clip(daily_usage, 5, 50)  # Ensure realistic range
        
        st.session_state.usage_data = pd.DataFrame({
            'Date': dates,
            'Usage_GB': daily_usage,
            'Upload_GB': daily_usage * 0.1,  # Upload is typically 10% of download
            'Peak_Hours': np.random.choice([True, False], 30, p=[0.3, 0.7])
        })
        st.session_state.usage_data_generated = True
    
    # Get plans from MongoDB - same data as admin dashboard
    all_plans = list(plans_collection.find())
    
    # Convert MongoDB plans to customer dashboard format
    plans_data = []
    for plan in all_plans:
        # Map MongoDB plan to customer dashboard format
        plan_data = {
            "name": plan.get("plan_name", "Unknown Plan"),
            "price": plan.get("monthly_cost", 0),
            "speed": f"{plan.get('monthly_cost', 0) // 10} Mbps",  # Derive speed from price
            "upload_speed": f"{plan.get('monthly_cost', 0) // 20} Mbps",  # Derive upload speed
            "data_cap": f"{plan.get('data_limit_gb', 0)} GB" if plan.get('data_limit_gb', 0) > 0 else "Unlimited",
            "benefits": [
                f"📊 {plan.get('data_limit_gb', 0)} GB Data" if plan.get('data_limit_gb', 0) > 0 else "📊 Unlimited Data",
                f"📞 {plan.get('voice_minutes', 0)} Minutes",
                f"📅 {plan.get('validity_days', 30)} Days Validity",
                "🔧 24/7 Support"
            ],
            "popular": plan.get("plan_name") == "Standard Plan",  # Make Standard Plan popular
            "color": "#4FC3F7" if plan.get("plan_name") == "Basic Plan" else 
                     "#7986CB" if plan.get("plan_name") == "Standard Plan" else
                     "#4DB6AC" if plan.get("plan_name") == "Premium Plan" else "#FFB74D",
            "features": plan.get("description", "Great value broadband plan")
        }
        plans_data.append(plan_data)
    
    # App header
    st.markdown('<h1 class="main-header">🌐 ConnectFast Broadband Experience</h1>', unsafe_allow_html=True)
    
    # Quick actions at the top right
    cols = st.columns([2, 1])
    with cols[1]:
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📞 Support", key="top_support", use_container_width=True):
                st.session_state.show_support = True
                st.session_state.show_notifications = False
                st.session_state.show_faq = False
        with col2:
            notification_count = len(st.session_state.user_data['notifications'])
            if st.button(f"🔔 ({notification_count})", key="top_notifications", use_container_width=True):
                st.session_state.show_notifications = not st.session_state.show_notifications
                st.session_state.show_support = False
                st.session_state.show_faq = False
        with col3:
            if st.button("❓ FAQ", key="top_faq", use_container_width=True):
                st.session_state.show_faq = not st.session_state.show_faq
                st.session_state.show_notifications = False
                st.session_state.show_support = False
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Notification panel
    if st.session_state.show_notifications:
        st.markdown('<div class="notification-panel">', unsafe_allow_html=True)
        st.markdown("### 🔔 Your Notifications")
        for i, notification in enumerate(st.session_state.user_data['notifications']):
            st.info(f"{notification}")
        if st.button("✅ Mark All as Read", key="clear_notifications", use_container_width=True):
            st.session_state.user_data['notifications'] = []
            st.success("All notifications cleared!")
            st.session_state.show_notifications = False
            st.rerun()
        if st.button("❌ Close Notifications", key="close_notifications", use_container_width=True):
            st.session_state.show_notifications = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Support panel
    if st.session_state.show_support:
        st.markdown('<div class="support-panel">', unsafe_allow_html=True)
        st.markdown("### 📞 Contact Support")
        
        col1, col2 = st.columns(2)
        with col1:
            issue_type = st.selectbox("🔍 Issue type", 
                                     ["Billing", "Technical", "Plan Change", "Installation", "Speed Issues", "Other"])
        with col2:
            priority = st.selectbox("⚡ Priority", ["Low", "Medium", "High", "Urgent"])
        
        description = st.text_area("📝 Describe your issue", placeholder="Please provide detailed information about your issue...")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Submit Request", key="submit_request", use_container_width=True):
                # Add ticket to MongoDB
                new_ticket = {
                    "ID": len(list(tickets_collection.find())) + 1,
                    "Customer": st.session_state.user_data['name'],
                    "Issue": f"{issue_type}: {description}",
                    "Status": "Open 🔴",
                    "Priority": priority,
                    "created_at": datetime.now()
                }
                tickets_collection.insert_one(new_ticket)
                st.success("🎉 Support request submitted! We'll contact you within 24 hours.")
                # Add to notifications
                st.session_state.user_data['notifications'].append(f"📞 Support request #{new_ticket['ID']} submitted for {issue_type}")
                st.session_state.show_support = False
                st.rerun()
        with col2:
            if st.button("❌ Close", key="close_support", use_container_width=True):
                st.session_state.show_support = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # FAQ panel
    if st.session_state.show_faq:
        st.markdown('<div class="faq-panel">', unsafe_allow_html=True)
        st.markdown("### ❓ Frequently Asked Questions")
        
        faqs = [
            {
                "question": "What broadband speeds do you offer?",
                "answer": "We offer a range of speeds from 50 Mbps to 1 Gbps, depending on the plan you choose. Our Basic Plan offers 50 Mbps, Standard Plan offers 100 Mbps, Premium Plan offers 200 Mbps, and Ultra Plan offers 1 Gbps."
            },
            {
                "question": "Is there a data limit on your plans?",
                "answer": "Our Basic and Standard plans have data limits of 100GB and 200GB respectively. Our Premium and Ultra plans offer unlimited data usage."
            },
            {
                "question": "How long does installation take?",
                "answer": "Standard installation typically takes 2-4 hours. Our technician will arrive at your scheduled time and complete the setup including modem configuration and connection testing."
            },
            {
                "question": "Do you offer a satisfaction guarantee?",
                "answer": "Yes! We offer a 30-day money-back guarantee. If you're not satisfied with our service within the first 30 days, we'll refund your installation fee and first month's payment."
            },
            {
                "question": "What happens if I move to a new address?",
                "answer": "We provide free relocation service within our coverage area. Just contact us at least 7 days before your move, and we'll transfer your service to your new address."
            },
            {
                "question": "How can I upgrade or downgrade my plan?",
                "answer": "You can upgrade or downgrade your plan at any time through your customer dashboard. Changes take effect immediately, and any prorated amounts will be reflected in your next bill."
            },
            {
                "question": "Do you provide customer support 24/7?",
                "answer": "Yes, our customer support team is available 24/7 via phone, email, and live chat. Technical support is available 24/7 for urgent issues."
            },
            {
                "question": "What equipment do I need?",
                "answer": "We provide a modem and router as part of your installation. You don't need to purchase any additional equipment unless you want to use your own compatible devices."
            }
        ]
        
        for i, faq in enumerate(faqs):
            with st.expander(f"Q{i+1}: {faq['question']}", expanded=False):
                st.markdown(f"**A:** {faq['answer']}")
        
        if st.button("❌ Close FAQ", key="close_faq", use_container_width=True):
            st.session_state.show_faq = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # User info sidebar - Removed profile section
    with st.sidebar:
        st.markdown("### 👤 User Dashboard")
        
        # Connection status
        st.markdown("---")
        st.markdown("### 📊 Live Connection Status")
        
        # Simulate real-time data
        download_speed = random.uniform(95, 102)
        upload_speed = random.uniform(43, 48)
        latency = random.uniform(15, 22)
        
        status_color = "status-good" if download_speed > 90 else "status-warning" if download_speed > 70 else "status-error"
        
        st.markdown(f"""
        <div class="sidebar-metric">
            <div class="{status_color}">⬇ Download: {download_speed:.1f} Mbps</div>
            <div class="status-good">⬆ Upload: {upload_speed:.1f} Mbps</div>
            <div class="status-good">⚡ Latency: {latency:.0f} ms</div>
            <div class="status-good">📶 Signal: Excellent</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Data usage this month
        total_usage = st.session_state.usage_data['Usage_GB'].sum()
        st.markdown(f"""
        <div class="sidebar-metric">
            <strong>📊 This Month's Usage</strong><br>
            📈 Total: {total_usage:.1f} GB<br>
            📉 Daily Avg: {total_usage/30:.1f} GB<br>
            🎯 Efficiency: {"Excellent" if total_usage < 800 else "Good" if total_usage < 1200 else "High"}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Run Speed Test", key="speed_test"):
            with st.spinner("Running speed test..."):
                time.sleep(1)  # Reduced sleep time for faster response
            st.success("Speed test completed! Results updated above.")
            st.rerun()
        
        if st.button("📊 Data Usage Report", key="usage_report"):
            st.session_state.show_usage_details = True
            st.rerun()
        
        if st.button("💡 Optimize Connection", key="optimize"):
            st.success("Connection optimized for better performance!")
        
        # Logout button
        st.divider()
        if st.button("🚪 Logout", key="logout"):
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()
    
    # Show service paused message if applicable
    if st.session_state.service_paused:
        st.markdown("""
        <div class="full-page-container">
            <h2 style="text-align: center; color: #F39C12;">⏸ Service Paused</h2>
            <p style="text-align: center; font-size: 18px;">
                Your broadband service has been paused as requested. Your service will automatically resume in 3 months.
            </p>
            <p style="text-align: center; font-size: 16px; color: #7F8C8D;">
                If you wish to resume your service earlier, please contact customer support.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Show subscription cancelled message if applicable
    if st.session_state.subscription_cancelled:
        st.markdown("""
        <div class="full-page-container">
            <h2 style="text-align: center; color: #E74C3C;">❌ Subscription Cancelled</h2>
            <p style="text-align: center; font-size: 18px;">
                Your broadband subscription has been successfully cancelled.
            </p>
            <p style="text-align: center; font-size: 16px; color: #7F8C8D;">
                We're sorry to see you go. Thank you for being a ConnectFast customer.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Wait for 3 seconds and then reset the dashboard (reduced from 10 seconds)
        time.sleep(3)
        st.session_state.subscription_cancelled = False
        st.session_state.user_plan = None
        # Update database
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"current_plan": None}}
        )
        st.rerun()
    
    # Show billing history if applicable
    if st.session_state.show_billing_history:
        st.markdown('<div class="full-page-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">📋 Billing History</h2>', unsafe_allow_html=True)
        
        # Generate sample billing data
        billing_data = pd.DataFrame({
            "Date": [(datetime.now() - timedelta(days=30*i)).strftime("%Y-%m-%d") for i in range(6, 0, -1)],
            "Amount": [49.99, 49.99, 59.99, 49.99, 49.99, 39.99],
            "Status": ["Paid", "Paid", "Paid", "Paid", "Paid", "Pending"],
            "Invoice": [f"INV-{1000+i}" for i in range(6, 0, -1)]
        })
        
        st.dataframe(billing_data, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            total_paid = billing_data[billing_data["Status"] == "Paid"]["Amount"].sum()
            st.metric("Total Paid", f"₹{total_paid:.2f}")
        with col2:
            pending_amount = billing_data[billing_data["Status"] == "Pending"]["Amount"].sum()
            st.metric("Pending Amount", f"₹{pending_amount:.2f}")
        with col3:
            avg_monthly = billing_data["Amount"].mean()
            st.metric("Average Monthly", f"₹{avg_monthly:.2f}")
        
        if st.button("❌ Close Billing History", key="close_billing_history", use_container_width=True):
            st.session_state.show_billing_history = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Show plan optimizer if applicable
    if st.session_state.show_plan_optimizer:
        st.markdown('<div class="full-page-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">🎯 Plan Optimizer</h2>', unsafe_allow_html=True)
        
        # Show plan recommendation based on usage
        total_usage = st.session_state.usage_data['Usage_GB'].sum()
        if total_usage < 400:
            recommended_plan = "Basic Plan"
        elif total_usage < 800:
            recommended_plan = "Standard Plan"
        elif total_usage < 1500:
            recommended_plan = "Premium Plan"
        else:
            recommended_plan = "Ultra Plan"
        
        current_plan_name = st.session_state.user_plan
        if recommended_plan == current_plan_name:
            st.success(f"🎯 Perfect! Your current {current_plan_name} is ideal for your usage pattern.")
        else:
            st.info(f"💡 Based on your usage ({total_usage:.0f}GB/month), we recommend the {recommended_plan} for optimal value!")
            
            # Show recommended plan details
            recommended_plan_data = next((p for p in plans_data if p["name"] == recommended_plan), None)
            if recommended_plan_data:
                st.markdown(f"""
                <div class="plan-card">
                    <h3>🌟 Recommended Plan: {recommended_plan_data['name']}</h3>
                    <p><strong>💰 Price:</strong> ₹{recommended_plan_data['price']}/month</p>
                    <p><strong>⚡ Speed:</strong> {recommended_plan_data['speed']} ⬇ / {recommended_plan_data['upload_speed']} ⬆</p>
                    <p><strong>📊 Data:</strong> {recommended_plan_data['data_cap']}</p>
                    <p><strong>📝 Features:</strong> {recommended_plan_data['features']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Switch to Recommended Plan", key="switch_recommended", use_container_width=True):
                    st.session_state.user_plan = recommended_plan_data["name"]
                    st.session_state.user_data['bill_amount'] = recommended_plan_data['price']
                    # Update plan dates
                    st.session_state.user_data['plan_start_date'] = datetime.now().strftime("%Y-%m-%d")
                    st.session_state.user_data['plan_end_date'] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
                    # Update database
                    users_collection.update_one(
                        {"_id": user["_id"]},
                        {"$set": {"current_plan": recommended_plan_data["name"]}}
                    )
                    st.balloons()
                    st.success(f"🎉 Successfully switched to {recommended_plan_data['name']}!")
                    st.session_state.show_plan_optimizer = False
                    st.rerun()
        
        # Usage breakdown
        st.markdown("### 📊 Your Usage Breakdown")
        col1, col2 = st.columns(2)
        
        with col1:
            # Simulated usage by category
            usage_categories = {
                'Streaming': 45,
                'Gaming': 20,
                'Browsing': 15,
                'Downloads': 12,
                'Video Calls': 8
            }
            
            fig_pie = px.pie(values=list(usage_categories.values()), 
                             names=list(usage_categories.keys()),
                             title='🎯 Usage by Category',
                             color_discrete_sequence=px.colors.qualitative.Set3)
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Peak hours analysis
            hours = list(range(24))
            usage_by_hour = [random.uniform(0.5, 3.0) if h in [19,20,21,22] else random.uniform(0.1, 1.5) for h in hours]
            
            fig_bar = px.bar(x=hours, y=usage_by_hour,
                             title='⏰ Usage by Hour of Day',
                             labels={'x': 'Hour', 'y': 'Average GB'},
                             color=usage_by_hour,
                             color_continuous_scale='Viridis')
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", size=12)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        if st.button("❌ Close Plan Optimizer", key="close_plan_optimizer", use_container_width=True):
            st.session_state.show_plan_optimizer = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Main content - Usage Details Section (if activated)
    if st.session_state.show_usage_details:
        st.markdown('<div class="usage-details-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">📊 Detailed Usage Analytics</h2>', unsafe_allow_html=True)
        
        # Usage statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_usage = st.session_state.usage_data['Usage_GB'].sum()
        avg_daily = total_usage / 30
        max_usage = st.session_state.usage_data['Usage_GB'].max()
        peak_days = st.session_state.usage_data['Peak_Hours'].sum()
        
        with col1:
            st.metric("📈 Total Usage (30 days)", f"{total_usage:.1f} GB", f"{total_usage-750:.1f} GB from target")
        with col2:
            st.metric("📊 Daily Average", f"{avg_daily:.1f} GB", f"+{avg_daily-20:.1f} GB from typical")
        with col3:
            st.metric("🔥 Peak Day Usage", f"{max_usage:.1f} GB")
        with col4:
            st.metric("⏰ Peak Usage Days", f"{peak_days}")
        
        # Usage chart
        fig = px.line(st.session_state.usage_data, x='Date', y='Usage_GB', 
                      title='📈 Daily Internet Usage (Last 30 Days)',
                      color_discrete_sequence=['#4ECDC4'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=20
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Usage recommendations
        st.markdown("### 💡 Smart Recommendations")
        recommendations = [
            "🎯 Your peak usage is during evening hours (7-10 PM). Consider scheduling large downloads during off-peak times.",
            "📺 Streaming accounts for 45% of your usage. Consider adjusting video quality settings to reduce data consumption.",
            "⚡ Your current plan supports your usage well with room for growth.",
            "🔄 Enable automatic quality adjustment for streaming services to optimize data usage."
        ]
        
        for rec in recommendations:
            st.info(rec)
        
        if st.button("❌ Close Usage Details", key="close_usage_details", use_container_width=True):
            st.session_state.show_usage_details = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content - two columns
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<h2 class="sub-header">🚀 Available Broadband Plans</h2>', unsafe_allow_html=True)
        
        # Display plans in a more attractive format
        for i, plan in enumerate(plans_data):
            is_current = plan["name"] == st.session_state.user_plan
            
            # Create a beautiful plan card
            if is_current:
                st.markdown(f"""
                <div class="plan-card current-plan">
                    <h3>✨ {plan['name']} - ₹{plan['price']}/month (CURRENT PLAN)</h3>
                    <p><strong>Speed:</strong> {plan['speed']} ⬇ / {plan['upload_speed']} ⬆</p>
                    <p><strong>Data:</strong> {plan['data_cap']} | <strong>Features:</strong> {plan['features']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="plan-card">
                    <h3>🌟 {plan['name']} - ₹{plan['price']}/month</h3>
                    <p><strong>Speed:</strong> {plan['speed']} ⬇ / {plan['upload_speed']} ⬆</p>
                    <p><strong>Data:</strong> {plan['data_cap']} | <strong>Features:</strong> {plan['features']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Plan details in expander
            expander_title = f"📋 View Details - {plan['name']}"
            
            with st.expander(expander_title, expanded=False):
                # Create columns for plan details
                detail_col1, detail_col2, detail_col3 = st.columns(3)
                
                with detail_col1:
                    st.metric("🚀 Download Speed", plan["speed"])
                    st.metric("⬆ Upload Speed", plan["upload_speed"])
                    
                with detail_col2:
                    st.metric("📊 Data Allowance", plan["data_cap"])
                    st.metric("💰 Monthly Price", f"₹{plan['price']}")
                    
                with detail_col3:
                    if plan["popular"]:
                        st.success("🔥 Most Popular Choice!")
                    st.info(f"🎯 {plan['features']}")
                
                # Benefits list with better styling
                st.markdown("### ✨ Plan Benefits:")
                benefit_cols = st.columns(2)
                for idx, benefit in enumerate(plan["benefits"]):
                    with benefit_cols[idx % 2]:
                        st.markdown(f"• {benefit}")
                
                # Action buttons
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if is_current:
                        st.button("✅ Current Plan", key=f"curr_{plan['name']}", disabled=True)
                    else:
                        if st.session_state.user_plan is None:
                            button_text = "Select Plan"
                        else:
                            button_text = "Switch to This Plan"
                            
                        if st.button(button_text, key=f"switch_{plan['name']}"):
                            st.session_state.user_plan = plan["name"]
                            st.session_state.user_data['bill_amount'] = plan['price']
                            # Update plan dates
                            st.session_state.user_data['plan_start_date'] = datetime.now().strftime("%Y-%m-%d")
                            st.session_state.user_data['plan_end_date'] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
                            # Update database
                            users_collection.update_one(
                                {"_id": user["_id"]},
                                {"$set": {"current_plan": plan["name"]}}
                            )
                            st.balloons()
                            st.success(f"🎉 Successfully selected {plan['name']}!")
                            st.rerun()
                with btn_col2:
                    if st.button("🛒 Add to Cart", key=f"cart_{plan['name']}"):
                        st.info(f"🛒 {plan['name']} added to cart for comparison!")
                with btn_col3:
                    if st.button("📞 Get Quote", key=f"quote_{plan['name']}"):
                        st.success(f"📋 Quote requested for {plan['name']}! We'll contact you soon.")
    
    with col2:
        st.markdown('<h2 class="sub-header">🔧 Your Subscription Dashboard</h2>', unsafe_allow_html=True)
        
        # Current plan info with enhanced styling
        current_plan = next((p for p in plans_data if p["name"] == st.session_state.user_plan), None)
        
        if current_plan:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌟 Current Plan</h3>
                <h2>{current_plan['name']}</h2>
                <p><strong>₹{current_plan['price']}/month</strong></p>
                <p>⚡ {current_plan['speed']} / {current_plan['upload_speed']}</p>
                <p>📊 {current_plan['data_cap']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced billing information - Removed pay bill and email bill buttons
            days_until_due = (datetime.strptime(st.session_state.user_data['due_date'], "%Y-%m-%d") - datetime.now()).days
            bill_status = "🔴 Overdue" if days_until_due < 0 else "🟡 Due Soon" if days_until_due <= 3 else "🟢 Current"
            
            st.markdown(f"""
            <div class="bill-card">
                <h3>💵 Billing Information</h3>
                <h2>₹{st.session_state.user_data['bill_amount']}</h2>
                <p><strong>Due Date:</strong> {st.session_state.user_data['due_date']}</p>
                <p><strong>Status:</strong> {bill_status}</p>
                <p><strong>Days Until Due:</strong> {abs(days_until_due)} days</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Plan dates information
            st.markdown(f"""
            <div class="metric-card">
                <h3>📅 Plan Duration</h3>
                <p><strong>Start Date:</strong> {st.session_state.user_data['plan_start_date']}</p>
                <p><strong>End Date:</strong> {st.session_state.user_data['plan_end_date']}</p>
                <p><strong>Days Remaining:</strong> {(datetime.strptime(st.session_state.user_data['plan_end_date'], '%Y-%m-%d') - datetime.now()).days} days</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Plan management options
            st.markdown('<h3 class="sub-header" style="font-size: 24px;">🛠 Plan Management</h3>', unsafe_allow_html=True)
            
            management_col1, management_col2 = st.columns(2)
            with management_col1:
                if st.button("⬆ Upgrade Plan", use_container_width=True, key="upgrade_btn"):
                    st.session_state.show_upgrade_options = True
                    st.session_state.show_downgrade_options = False
                    st.rerun()
            
            with management_col2:
                if st.button("⬇ Downgrade Plan", use_container_width=True, key="downgrade_btn"):
                    st.session_state.show_downgrade_options = True
                    st.session_state.show_upgrade_options = False
                    st.rerun()
    
    # Plan Management Options Display (Full Width)
    if st.session_state.show_upgrade_options:
        st.markdown("""
        <div class="option-card">
            <h2>⬆ Available Upgrade Options</h2>
            <p>🚀 Boost your internet experience with faster speeds and better features!</p>
        </div>
        """, unsafe_allow_html=True)
        
        current_plan = next((p for p in plans_data if p["name"] == st.session_state.user_plan), None)
        upgrade_options = [p for p in plans_data if p['price'] > current_plan['price']]
        
        if upgrade_options:
            cols = st.columns(len(upgrade_options))
            for idx, plan in enumerate(upgrade_options):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="plan-card">
                        <h3>🌟 {plan['name']}</h3>
                        <h4>₹{plan['price']}/month</h4>
                        <p>⚡ {plan['speed']} / {plan['upload_speed']}</p>
                        <p>📊 {plan['data_cap']}</p>
                        <p>💰 <strong>+₹{plan['price'] - current_plan['price']:.2f}</strong> more per month</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    benefit_text = " • ".join(plan['benefits'][:3])  # Show first 3 benefits
                    st.markdown(f"*Top Benefits:* {benefit_text}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Select", key=f"upg_select_{plan['name']}", use_container_width=True):
                            st.session_state.user_plan = plan["name"]
                            st.session_state.user_data['bill_amount'] = plan['price']
                            # Update plan dates
                            st.session_state.user_data['plan_start_date'] = datetime.now().strftime("%Y-%m-%d")
                            st.session_state.user_data['plan_end_date'] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
                            # Update database
                            users_collection.update_one(
                                {"_id": user["_id"]},
                                {"$set": {"current_plan": plan["name"]}}
                            )
                            st.session_state.show_upgrade_options = False
                            st.balloons()
                            st.success(f"🎉 Successfully upgraded to {plan['name']}!")
                            st.rerun()
                    with col2:
                        if st.button("ℹ Details", key=f"upg_details_{plan['name']}", use_container_width=True):
                            st.info(f"📋 {plan['features']}")
        else:
            st.info("🏆 You're already on our highest tier plan!")
        
        if st.button("❌ Close Upgrade Options", key="close_upgrade", use_container_width=True):
            st.session_state.show_upgrade_options = False
            st.rerun()
    
    # Show downgrade options
    if st.session_state.show_downgrade_options:
        st.markdown("""
        <div class="option-card">
            <h2>⬇ Available Downgrade Options</h2>
            <p>💰 Save money with a plan that better fits your usage needs!</p>
        </div>
        """, unsafe_allow_html=True)
        
        current_plan = next((p for p in plans_data if p["name"] == st.session_state.user_plan), None)
        downgrade_options = [p for p in plans_data if p['price'] < current_plan['price']]
        
        if downgrade_options:
            cols = st.columns(len(downgrade_options))
            for idx, plan in enumerate(downgrade_options):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="plan-card">
                        <h3>💰 {plan['name']}</h3>
                        <h4>₹{plan['price']}/month</h4>
                        <p>⚡ {plan['speed']} / {plan['upload_speed']}</p>
                        <p>📊 {plan['data_cap']}</p>
                        <p>💚 <strong>Save ₹{current_plan['price'] - plan['price']:.2f}</strong> per month</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    benefit_text = " • ".join(plan['benefits'][:3])
                    st.markdown(f"*Benefits:* {benefit_text}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Select", key=f"downg_select_{plan['name']}", use_container_width=True):
                            st.session_state.user_plan = plan["name"]
                            st.session_state.user_data['bill_amount'] = plan['price']
                            # Update plan dates
                            st.session_state.user_data['plan_start_date'] = datetime.now().strftime("%Y-%m-%d")
                            st.session_state.user_data['plan_end_date'] = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
                            # Update database
                            users_collection.update_one(
                                {"_id": user["_id"]},
                                {"$set": {"current_plan": plan["name"]}}
                            )
                            st.session_state.show_downgrade_options = False
                            st.success(f"💰 Successfully downgraded to {plan['name']}! You'll save ₹{current_plan['price'] - plan['price']:.2f}/month.")
                            st.rerun()
                    with col2:
                        if st.button("ℹ Details", key=f"downg_details_{plan['name']}", use_container_width=True):
                            st.info(f"📋 {plan['features']}")
        else:
            st.info("📊 You're already on our most basic plan!")
        
        if st.button("❌ Close Downgrade Options", key="close_downgrade", use_container_width=True):
            st.session_state.show_downgrade_options = False
            st.rerun()
    
    # Additional Management Options (Full Width)
    st.markdown('<h2 class="sub-header">🔧 Additional Services & Support</h2>', unsafe_allow_html=True)
    # Create columns for additional options
    service_col1, service_col2, service_col3, service_col4 = st.columns(4)
    with service_col1:
        if st.button("📊 View Usage Details", use_container_width=True, key="usage_details_btn"):
            st.session_state.show_usage_details = True
            st.rerun()
    with service_col2:
        if st.button("🔧 Technical Support", use_container_width=True, key="tech_support_btn"):
            st.session_state.show_support = True
            st.rerun()
    with service_col3:
        if st.button("📋 Billing History", use_container_width=True, key="billing_history_btn"):
            st.session_state.show_billing_history = True
            st.rerun()
    with service_col4:
        if st.button("🎯 Plan Optimizer", use_container_width=True, key="optimizer_btn"):
            st.session_state.show_plan_optimizer = True
            st.rerun()
    
    # Account Management Section
    st.markdown('<h2 class="sub-header" style="color: black;"> Account Management</h2>', unsafe_allow_html=True)
    danger_col1, danger_col2 = st.columns(2)  # Reduced from 3 to 2 columns
    with danger_col1:
        if st.button("⏸ Pause Service", use_container_width=True, key="pause_service"):
            st.session_state.show_pause_confirmation = True
            st.rerun()
    with danger_col2:
        if st.button("❌ Cancel Subscription", use_container_width=True, key="cancel_btn"):
            st.session_state.show_cancel_confirmation = True
            st.rerun()
    
    # Show pause confirmation if applicable
    if st.session_state.show_pause_confirmation:
        st.markdown("""
        <div class="full-page-container">
            <h2 style="text-align: center; color: #F39C12;">⏸ Pause Service Confirmation</h2>
            <p style="text-align: center; font-size: 18px;">
                Are you sure you want to pause your broadband service?
            </p>
            <p style="text-align: center; font-size: 16px; color: #7F8C8D;">
                Your service will be paused for up to 3 months and will automatically resume after that period.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Pause", key="confirm_pause", use_container_width=True):
                st.session_state.show_pause_confirmation = False
                st.session_state.service_paused = True
                st.rerun()
        with col2:
            if st.button("❌ Cancel", key="cancel_pause", use_container_width=True):
                st.session_state.show_pause_confirmation = False
                st.rerun()
    
    # Show cancel confirmation if applicable
    if st.session_state.show_cancel_confirmation:
        st.markdown("""
        <div class="full-page-container">
            <h2 style="text-align: center; color: #E74C3C;">❌ Cancel Subscription Confirmation</h2>
            <p style="text-align: center; font-size: 18px;">
                Are you sure you want to cancel your subscription?
            </p>
            <p style="text-align: center; font-size: 16px; color: #7F8C8D;">
                This action will terminate your internet service at the end of your current billing period.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Cancellation", key="confirm_cancel", use_container_width=True):
                st.session_state.show_cancel_confirmation = False
                st.session_state.subscription_cancelled = True
                st.rerun()
        with col2:
            if st.button("❌ Keep My Plan", key="keep_plan", use_container_width=True):
                st.session_state.show_cancel_confirmation = False
                st.success("🎉 Great choice! We're glad you're staying with us!")
                st.rerun()
    
    # Enhanced Footer
    st.divider()
    st.markdown("""
    <div class="footer">
        <h3>🌐 ConnectFast Broadband</h3>
        <p><strong>📞 24/7 Support:</strong> 1-800-CONNECT | <strong>📧 Email:</strong> support@connectfast.com</p>
        <p><strong>🌍 Website:</strong> www.connectfast.com | <strong>📱 Mobile App:</strong> Available on iOS & Android</p>
        <p>🏢 <strong>Address:</strong> 123 Internet Avenue, Tech City, TC 12345</p>
        <p>📋 <a href="#" style="color: #AED6F1;">Terms of Service</a> | 🛡 <a href="#" style="color: #AED6F1;">Privacy Policy</a> | 🍪 <a href="#" style="color: #AED6F1;">Cookie Policy</a></p>
        <p style="margin-top: 20px; font-size: 14px; opacity: 0.8;">© 2024 ConnectFast Broadband. All rights reserved. | Bringing the world to your doorstep! 🚀</p>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# AUTH PAGE
# ===============================
def auth_page():
    st.markdown("<h1 style='text-align:center; color:#4A90E2;'>🌐 Broadband Subscription Portal</h1>", unsafe_allow_html=True)
    menu = ["Login", "Signup"]
    choice = st.sidebar.radio("Menu", menu)
    
    if choice == "Signup":
        st.subheader("📝 Customer Signup")
        name = st.text_input("Full Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Signup", use_container_width=True, key="signup_btn"):
            if name and email and password:
                success, msg = signup(name, email, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("⚠ Please fill all fields.")
    
    elif choice == "Login":
        st.subheader("🔑 Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True, key="login_btn"):
            if email and password:
                user, msg = login(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.page = "dashboard"
                    # Set user plan from database
                    st.session_state.user_plan = user.get("current_plan", None)
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("⚠ Please enter email and password.")

# ===============================
# HOME PAGE
# ===============================
def home_page():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    # Function to handle page navigation
    def navigate_to(page_name):
        st.session_state.page = page_name
        st.rerun()
    
    # App header
    st.markdown('<h1 class="main-header">📶 ConnectFast Broadband</h1>', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h2 style="font-size: 36px; margin-bottom: 20px;">High-Speed Internet for Everyone</h2>
        <p style="font-size: 20px; margin-bottom: 30px;">Experience blazing fast internet with our reliable broadband services</p>
        <div style="display: flex; justify-content: center; gap: 20px;">
            <button style="background: #F39C12; color: white; border: none; border-radius: 8px; padding: 12px 24px; font-size: 16px; font-weight: bold; cursor: pointer;">View Plans</button>
            <button style="background: transparent; color: white; border: 2px solid white; border-radius: 8px; padding: 12px 24px; font-size: 16px; font-weight: bold; cursor: pointer;">Contact Sales</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    st.markdown('<h2 class="sub-header">📊 Why Choose ConnectFast?</h2>', unsafe_allow_html=True)
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Speed</h3>
            <h2>Up to 1 Gbps</h2>
            <p>Blazing fast internet speeds</p>
        </div>
        """, unsafe_allow_html=True)
    with metric_col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📅 Reliability</h3>
            <h2>99.9% Uptime</h2>
            <p>Consistent connection</p>
        </div>
        """, unsafe_allow_html=True)
    with metric_col3:
        st.markdown("""
        <div class="metric-card">
            <h3>👪 Coverage</h3>
            <h2>98% Areas</h2>
            <p>Available in your area</p>
        </div>
        """, unsafe_allow_html=True)
    with metric_col4:
        st.markdown("""
        <div class="metric-card">
            <h3>⏰ Support</h3>
            <h2>24/7 Help</h2>
            <p>Always available</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown('<h2 class="sub-header">✨ Our Features</h2>', unsafe_allow_html=True)
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    with feature_col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🏠 Home Internet</h3>
            <p>Perfect for streaming, gaming, and working from home</p>
        </div>
        """, unsafe_allow_html=True)
    with feature_col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💼 Business Solutions</h3>
            <p>Reliable connectivity for your business needs</p>
        </div>
        """, unsafe_allow_html=True)
    with feature_col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎮 Gaming Package</h3>
            <p>Low latency for competitive gaming</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown('<h2 class="sub-header">💬 What Our Customers Say</h2>', unsafe_allow_html=True)
    testimonial_col1, testimonial_col2, testimonial_col3 = st.columns(3)
    with testimonial_col1:
        st.markdown("""
        <div class="testimonial-card">
            <p>"The best internet service I've ever had! Consistent speeds and great customer support."</p>
            <p><strong>- Sarah Johnson</strong></p>
            <p>⭐⭐⭐⭐⭐</p>
        </div>
        """, unsafe_allow_html=True)
    with testimonial_col2:
        st.markdown("""
        <div class="testimonial-card">
            <p>"Switched from my old provider and couldn't be happier. The gaming package is amazing!"</p>
            <p><strong>- Michael Chen</strong></p>
            <p>⭐⭐⭐⭐⭐</p>
        </div>
        """, unsafe_allow_html=True)
    with testimonial_col3:
        st.markdown("""
        <div class="testimonial-card">
            <p>"Perfect for working from home. Reliable connection even during peak hours."</p>
            <p><strong>- Emily Rodriguez</strong></p>
            <p>⭐⭐⭐⭐⭐</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #F0F7FF, #E1E8FF); border-radius: 15px; margin: 30px 0;">
        <h2>Ready to experience faster internet?</h2>
        <p style="font-size: 18px; margin-bottom: 30px;">Join thousands of satisfied customers today</p>
    """, unsafe_allow_html=True)
    
    # Add the working "Get Started Now" button
    if st.button("Get Started Now", key="get_started_button", 
                 use_container_width=True, 
                 type="primary"):
        navigate_to("auth")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #7F8C8D; padding: 40px 20px; margin-top: 50px;">
        <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 20px;">
            <a href="#" style="color: #4A90E2; text-decoration: none;">Home</a>
            <a href="#" style="color: #4A90E2; text-decoration: none;">Plans</a>
            <a href="#" style="color: #4A90E2; text-decoration: none;">Coverage</a>
            <a href="#" style="color: #4A90E2; text-decoration: none;">Support</a>
            <a href="#" style="color: #4A90E2; text-decoration: none;">About Us</a>
        </div>
        <p>ConnectFast Broadband &copy; 2023 | 📞 1-800-CONNECT | 📧 support@connectfast.com</p>
        <p>24/7 Customer Support | Terms of Service | Privacy Policy</p>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# MAIN APP LOGIC
# ===============================
def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Navigation
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "auth":
        auth_page()
    elif st.session_state.page == "dashboard":
        if st.session_state.user:
            if st.session_state.user["role"] == "admin":
                admin_dashboard(st.session_state.user)
            else:
                customer_dashboard(st.session_state.user)
        else:
            st.session_state.page = "auth"
            st.rerun()

if __name__ == "__main__":
    main()