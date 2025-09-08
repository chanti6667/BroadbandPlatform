# modern_admin_dashboard_enhanced.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
from streamlit_lottie import st_lottie
import requests

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Modern Admin Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# ENHANCED CSS STYLING
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Variables */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --success-color: #4facfe;
    --warning-color: #f6d55c;
    --danger-color: #ff6b6b;
    --dark-bg: #1a1a2e;
    --card-bg: rgba(255, 255, 255, 0.1);
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --border-radius: 16px;
    --shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

/* Remove Streamlit branding and margins */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container styling */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #43e97b 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    font-family: 'Inter', sans-serif;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Content container */
[data-testid="stAppViewContainer"] {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
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
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 2rem;
    animation: fadeInDown 1s ease-out;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
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
    background: rgba(255, 255, 255, 0.8);
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
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* Enhanced card styling */
.metric-card {
    background: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
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
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.plan-card {
    background: rgba(255, 255, 255, 0.9);
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
    background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
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
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
    border-left-color: var(--accent-color);
}

.plan-card h3 {
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

/* Form styling */
.stForm {
    background: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
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
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* DataFrame styling */
[data-testid="stDataFrame"] {
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
}

/* Metric styling */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.9);
    padding: 1.5rem;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
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
    backdrop-filter: blur(10px);
}

/* Divider styling */
hr {
    margin: 2rem 0;
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
}

/* Input field styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 12px;
    border: 2px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Loading animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading {
    animation: pulse 2s infinite;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOTTIE ANIMATION LOADER
# ===============================
def load_lottie(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load animations with fallback
lottie_kpi = load_lottie("https://assets10.lottiefiles.com/packages/lf20_xlmz9xwm.json")
lottie_analytics = load_lottie("https://assets10.lottiefiles.com/packages/lf20_HpFqiS.json")

# ===============================
# SESSION STATE INIT
# ===============================
if "plans" not in st.session_state:
    st.session_state.plans = pd.DataFrame({
        "Plan": ["Basic", "Pro", "Ultra", "Enterprise"],
        "Price": [499, 999, 1499, 2499],
        "Subscribers": [120, 80, 50, 25],
        "Description": [
            "Perfect for home users with basic internet needs",
            "Ideal for small businesses and remote workers", 
            "High-speed connection for heavy users",
            "Premium enterprise solution with dedicated support"
        ]
    })

if "tickets" not in st.session_state:
    st.session_state.tickets = [
        {"ID": 1, "Customer": "John Doe", "Issue": "Slow connection", "Status": "Open 🔴", "Priority": "High"},
        {"ID": 2, "Customer": "Jane Smith", "Issue": "Billing inquiry", "Status": "In Progress 🟡", "Priority": "Medium"},
        {"ID": 3, "Customer": "Mike Johnson", "Issue": "Installation request", "Status": "Open 🔴", "Priority": "Low"}
    ]

# ===============================
# HEADER
# ===============================
st.markdown("<h1>🚀 Modern Admin Dashboard</h1>", unsafe_allow_html=True)

# ===============================
# HORIZONTAL NAVIGATION
# ===============================
tabs = st.tabs([
    "📊 Analytics", 
    "🔮 AI Predictions", 
    "🛠 Manage Plans", 
    "🎫 Support Tickets", 
    "➕ Add New Plan"
])

# ===============================
# ANALYTICS TAB
# ===============================
with tabs[0]:
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    # Lottie animation
    if lottie_kpi:
        st_lottie(lottie_kpi, height=150, key="kpi_anim")
    
    st.markdown("### 📌 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_subscribers = int(st.session_state.plans["Subscribers"].sum())
    total_revenue = int((st.session_state.plans['Subscribers'] * st.session_state.plans['Price']).sum())
    avg_price = int(st.session_state.plans['Price'].mean())
    active_plans = len(st.session_state.plans)
    
    col1.metric("Total Subscribers", f"{total_subscribers:,}", "▲ +12 this month 🚀")
    col2.metric("Monthly Revenue", f"₹{total_revenue:,}", "▲ ₹15,600 💰")
    col3.metric("Average Plan Price", f"₹{avg_price:,}", "▲ ₹200 📈")
    col4.metric("Active Plans", active_plans, "➕ 1 new plan 🎯")

    st.divider()
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Subscribers by Plan")
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
        fig = px.bar(
            st.session_state.plans, 
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
    
    with col2:
        st.markdown("### 💰 Revenue Distribution")
        revenue_data = st.session_state.plans.copy()
        revenue_data['Revenue'] = revenue_data['Subscribers'] * revenue_data['Price']
        
        fig = px.pie(
            revenue_data, 
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
        line=dict(color='#667eea', width=4),
        marker=dict(size=10, color='#667eea')
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
    styled_df = st.session_state.plans.style.apply(lambda x: ['background: linear-gradient(90deg, #f8f9ff, #fff)'] * len(x), axis=1)
    st.dataframe(styled_df, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# PREDICTIONS TAB
# ===============================
with tabs[1]:
    st.markdown("<div class='slide-in'>", unsafe_allow_html=True)
    
    if lottie_analytics:
        st_lottie(lottie_analytics, height=150, key="analytics_anim")
    
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
        colors = ['#ff6b6b' if x == 'Anomaly 🚨' else '#4facfe' for x in usage_data["status"]]
        fig = px.bar(usage_data, 
                    x="user_id", 
                    y="data_used_gb",
                    color="status",
                    color_discrete_map={"Normal ✅": "#4facfe", "Anomaly 🚨": "#ff6b6b"})
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

# ===============================
# MANAGE PLANS TAB
# ===============================
with tabs[2]:
    st.markdown("### 🛠 Manage Broadband Plans")
    
    for idx, row in st.session_state.plans.iterrows():
        revenue = row['Price'] * row['Subscribers']
        st.markdown(f"""
        <div class='plan-card'>
            <h3>📦 {row['Plan']}</h3>
            <p><strong>💰 Price:</strong> ₹{row['Price']:,}/month</p>
            <p><strong>👥 Subscribers:</strong> {row['Subscribers']:,}</p>
            <p><strong>💵 Monthly Revenue:</strong> ₹{revenue:,}</p>
            <p><strong>📝 Description:</strong> {row['Description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Plan comparison
    st.markdown("### 📊 Plan Comparison")
    comparison_df = st.session_state.plans.copy()
    comparison_df['Revenue'] = comparison_df['Price'] * comparison_df['Subscribers']
    comparison_df['Avg_Revenue_Per_User'] = comparison_df['Price']
    
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

# ===============================
# CUSTOMER TICKETS TAB
# ===============================
with tabs[3]:
    st.markdown("### 🎫 Customer Support Tickets")
    
    if len(st.session_state.tickets) == 0:
        st.info("🎉 No open tickets! Great job team!")
    else:
        # Tickets overview
        col1, col2, col3 = st.columns(3)
        
        open_tickets = sum(1 for t in st.session_state.tickets if "Open" in t["Status"])
        in_progress = sum(1 for t in st.session_state.tickets if "Progress" in t["Status"])
        resolved = sum(1 for t in st.session_state.tickets if "Resolved" in t["Status"])
        
        col1.metric("🔴 Open Tickets", open_tickets)
        col2.metric("🟡 In Progress", in_progress)  
        col3.metric("🟢 Resolved", resolved)
        
        st.divider()
        
        # Tickets table
        tickets_df = pd.DataFrame(st.session_state.tickets)
        st.dataframe(tickets_df, use_container_width=True)
        
        st.divider()
        
        # Ticket management
        st.markdown("### 🛠 Ticket Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 Add New Ticket")
            with st.form("add_ticket_form"):
                customer = st.text_input("Customer Name")
                issue = st.text_area("Issue Description")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                submitted = st.form_submit_button("Add Ticket")
                
                if submitted and customer and issue:
                    new_ticket = {
                        "ID": len(st.session_state.tickets) + 1,
                        "Customer": customer,
                        "Issue": issue,
                        "Status": "Open 🔴",
                        "Priority": priority
                    }
                    st.session_state.tickets.append(new_ticket)
                    st.success(f"✅ Ticket added for {customer}")
                    st.rerun()
        
        with col2:
            st.markdown("#### ✅ Update Ticket Status")
            with st.form("update_ticket_form"):
                if st.session_state.tickets:
                    ticket_options = [f"ID {t['ID']}: {t['Customer']}" for t in st.session_state.tickets]
                    selected = st.selectbox("Select Ticket", ticket_options)
                    new_status = st.selectbox("New Status", [
                        "Open 🔴", 
                        "In Progress 🟡", 
                        "Resolved ✅"
                    ])
                    submitted = st.form_submit_button("Update Status")
                    
                    if submitted:
                        ticket_id = int(selected.split(":")[0].replace("ID ", "")) - 1
                        st.session_state.tickets[ticket_id]["Status"] = new_status
                        st.success(f"✅ Ticket status updated!")
                        st.rerun()

# ===============================
# ADD NEW PLAN TAB
# ===============================
with tabs[4]:
    st.markdown("### ➕ Add New Broadband Plan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("add_plan_form"):
            st.markdown("#### 📋 Plan Details")
            new_plan = st.text_input("Plan Name", placeholder="e.g., Premium Pro")
            new_price = st.number_input("Monthly Price (₹)", min_value=100, step=100, value=1000)
            new_subs = st.number_input("Initial Subscribers", min_value=0, step=1, value=0)
            new_desc = st.text_area("Plan Description", 
                                   placeholder="Describe the features and benefits of this plan...")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submitted = st.form_submit_button("✅ Add Plan", use_container_width=True)
            with col_b:
                if st.form_submit_button("🔄 Reset Form", use_container_width=True):
                    st.rerun()
            
            if submitted and new_plan:
                new_entry = pd.DataFrame({
                    "Plan": [new_plan], 
                    "Price": [new_price], 
                    "Subscribers": [new_subs], 
                    "Description": [new_desc]
                })
                st.session_state.plans = pd.concat([st.session_state.plans, new_entry], ignore_index=True)
                st.success(f"🎉 Plan '{new_plan}' added successfully!")
                st.balloons()
                st.rerun()
    
    with col2:
        st.markdown("#### 📊 Plan Statistics")
        
        total_plans = len(st.session_state.plans)
        avg_price = st.session_state.plans['Price'].mean()
        total_subs = st.session_state.plans['Subscribers'].sum()
        
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
                <p><strong>👥 Subscribers:</strong> {new_subs:,}</p>
                <p><strong>📝 Description:</strong> {new_desc if new_desc else 'No description provided'}</p>
            </div>
            """, unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #718096;'>
    <p>🚀 <strong>Modern Admin Dashboard</strong> | Built with ❤ using Streamlit</p>
    <p>💡 <em>Eye-efficient design with smooth animations and modern aesthetics</em></p>
</div>
""", unsafe_allow_html=True)

# ===============================
# JAVASCRIPT FOR ENHANCED UX
# ===============================
st.markdown("""
<script>
// Add smooth scrolling behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Add loading states for better UX
window.addEventListener('load', function() {
    // Remove any loading classes
    document.querySelectorAll('.loading').forEach(el => {
        el.classList.remove('loading');
    });
    
    // Add entrance animations
    const cards = document.querySelectorAll('.metric-card, .plan-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Add intersection observer for scroll animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, { threshold: 0.1 });

// Observe elements for scroll animations
document.querySelectorAll('[data-testid="stDataFrame"], .stPlotlyChart').forEach(el => {
    observer.observe(el);
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Alt + 1-5 for quick tab navigation
    if (e.altKey && e.key >= '1' && e.key <= '5') {
        e.preventDefault();
        const tabIndex = parseInt(e.key) - 1;
        const tabs = document.querySelectorAll('[data-baseweb="tab"]');
        if (tabs[tabIndex]) {
            tabs[tabIndex].click();
        }
    }
});

// Add custom tooltips for metrics
document.querySelectorAll('[data-testid="metric-container"]').forEach(metric => {
    metric.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
    });
    
    metric.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Add pulse animation for important alerts
const alerts = document.querySelectorAll('[data-testid="stAlert"]');
alerts.forEach(alert => {
    if (alert.textContent.includes('High') || alert.textContent.includes('🔴')) {
        alert.style.animation = 'pulse 2s infinite';
    }
});

// Add smooth hover effects for buttons
document.querySelectorAll('.stButton button').forEach(button => {
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px) scale(1.05)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Add ripple effect for interactive elements
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    circle.style.width = circle.style.height = ${diameter}px;
    circle.style.left = ${event.clientX - button.offsetLeft - radius}px;
    circle.style.top = ${event.clientY - button.offsetTop - radius}px;
    circle.classList.add('ripple');
    
    const ripple = button.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove();
    }
    
    button.appendChild(circle);
}

document.querySelectorAll('.stButton button, .plan-card').forEach(el => {
    el.addEventListener('click', createRipple);
});
</script>

<style>
/* Ripple effect styles */
.ripple {
    position: absolute;
    border-radius: 50%;
    transform: scale(0);
    animation: ripple 600ms linear;
    background-color: rgba(255, 255, 255, 0.6);
    pointer-events: none;
}

@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

/* Additional responsive styles */
@media (max-width: 768px) {
    .stTabs [data-baseweb="tab"] {
        padding: 0 12px;
        font-size: 14px;
    }
    
    .metric-card, .plan-card {
        margin: 0.5rem 0;
        padding: 1.5rem;
    }
    
    h1 {
        font-size: 2rem;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    :root {
        --card-bg: rgba(45, 55, 72, 0.9);
        --text-primary: #f7fafc;
        --text-secondary: #a0aec0;
    }
    
    .metric-card, .plan-card, .stForm {
        background: var(--card-bg);
        color: var(--text-primary);
    }
}

/* Print styles */
@media print {
    .stTabs [data-baseweb="tab-list"],
    .stButton,
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    .stApp {
        background: white !important;
    }
}
</style>
""", unsafe_allow_html=True)