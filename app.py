import streamlit as st
import pymongo
from datetime import datetime

# ---------------- MongoDB Connection ----------------
MONGO_URI = "mongodb+srv://prasadpolisetti12345_db_user:chanti123@broadbandplan.e8xj3fs.mongodb.net/?retryWrites=true&w=majority&appName=BroadbandPlan"
client = pymongo.MongoClient(MONGO_URI)
db = client["BroadbandDB"]
users_collection = db["users"]

# ---------------- Default Admin ----------------
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

# ---------------- Functions ----------------
def signup(name, email, password):
    if users_collection.find_one({"email": email}):
        return False, "⚠️ Email already registered!"
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "role": "customer",
        "approved": False,   # needs admin approval
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

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Broadband Portal", page_icon="🌐", layout="wide")

# Session state to persist login
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- Auth Pages ----------------
def auth_page():
    st.markdown("<h1 style='text-align:center; color:#0ea5e9;'>🌐 Broadband Subscription Portal</h1>", unsafe_allow_html=True)

    menu = ["Login", "Signup"]
    choice = st.sidebar.radio("Menu", menu)

    # --- Signup ---
    if choice == "Signup":
        st.subheader("📝 Customer Signup")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Signup", use_container_width=True):
            if name and email and password:
                success, msg = signup(name, email, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("⚠️ Please fill all fields.")


    # --- Login ---
    elif choice == "Login":
        st.subheader("🔑 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if email and password:
                user, msg = login(email, password)
                if user:
                    st.session_state.user = user  # Save user session
                    st.success(msg)
                    st.rerun()  # Reload into dashboard
                else:
                    st.error(msg)
            else:
                st.warning("⚠️ Please enter email and password.")

# ---------------- Dashboards ----------------
def admin_dashboard(user):
    st.markdown(f"### 👑 Welcome, {user['name']} (Admin)")
    tabs = st.tabs(["✅ Approvals", "📦 Manage Plans", "📊 Analytics"])

    # --- Approvals Tab ---
    with tabs[0]:
        st.subheader("Pending Approvals")
        pending_users = users_collection.find({"role": "customer", "approved": False})
        for u in pending_users:
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        padding:12px; margin-bottom:10px;
                        border-radius:10px; 
                        background: linear-gradient(180deg, #f9fafb, #eef2ff);
                        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);">
                        <b>👤 {u['name']}</b> ({u['email']})
                    </div>
                    """, unsafe_allow_html=True
                )
                if st.button(f"Approve {u['email']}", key=u["email"]):
                    users_collection.update_one({"_id": u["_id"]}, {"$set": {"approved": True}})
                    st.success(f"✅ Approved {u['name']}")
                    st.rerun()  # stays in Admin Dashboard

    # --- Other Tabs ---
    with tabs[1]:
        st.info("📦 Manage broadband plans here.")
    with tabs[2]:
        st.info("📊 View customer analytics here.")

def customer_dashboard(user):
    st.markdown(f"### 🙋 Welcome, {user['name']} (Customer)")
    st.success("This is your Broadband Portal!")

# ---------------- Main ----------------
if st.session_state.user:
    if st.session_state.user["role"] == "admin":
        admin_dashboard(st.session_state.user)
    else:
        customer_dashboard(st.session_state.user)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()
else:
    auth_page()

