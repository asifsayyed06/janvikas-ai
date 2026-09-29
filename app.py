import streamlit as st
import pandas as pd
from database import init_db, add_request, get_requests, update_status, seed_demo_data
from ai_engine import analyze_request, summarize_request
from charts import priority_chart, category_chart, status_chart, district_chart, hotspot_map

st.set_page_config(page_title="JanVikas AI", page_icon="🏛️", layout="wide")

init_db()

if len(get_requests()) == 0:
    seed_demo_data()

st.markdown("""
<style>
.main-title {font-size: 2.3rem; font-weight: 800; margin-bottom: 0;}
.subtitle {color:#667085; margin-top:0;}
.card {padding:18px; border-radius:14px; border:1px solid #E5E7EB; background:#fff;}
.badge {padding:5px 10px; border-radius:20px; font-weight:600;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🏛️ JanVikas AI")
    st.caption("AI-powered citizen development intelligence")
    page = st.radio("Navigation", [
        "🏠 Overview",
        "📝 Submit Request",
        "🤖 AI Analysis",
        "🗺️ Hotspot Map",
        "📊 Analytics",
        "🏛️ Policymaker",
        "⚙️ Settings"
    ])
    st.divider()
    st.info("Demo mode is enabled. The app works without an external AI key.")

df = get_requests()

if page == "🏠 Overview":
    st.markdown('<p class="main-title">JanVikas AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Turning citizen voices into actionable public-infrastructure priorities.</p>', unsafe_allow_html=True)
    st.divider()

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Citizen requests", len(df))
    c2.metric("High priority", int((df.priority=="High").sum()) if len(df) else 0)
    c3.metric("Resolved", int((df.status=="Resolved").sum()) if len(df) else 0)
    c4.metric("Districts", df.district.nunique() if len(df) else 0)

    st.subheader("📌 Priority requests")
    if len(df):
        show = df.sort_values("priority_score", ascending=False).head(8)
        st.dataframe(show[["id","title","category","district","priority","priority_score","status"]], use_container_width=True)
    st.subheader("📈 Request distribution")
    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(priority_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(category_chart(df), use_container_width=True)

elif page == "📝 Submit Request":
    st.title("Submit a Citizen Development Request")
    st.caption("Text is enough for the demo. Voice/messaging integrations can be connected later.")

    with st.form("request_form"):
        title = st.text_input("Short title", placeholder="Example: Water supply interruption in Ward 12")
        description = st.text_area("Describe the issue", height=160)
        col1,col2,col3 = st.columns(3)
        with col1:
            district = st.text_input("District", "Pune")
        with col2:
            ward = st.text_input("Ward / Area", "Ward 12")
        with col3:
            language = st.selectbox("Language", ["English","Hindi","Marathi","Gujarati","Tamil","Telugu","Other"])
        category = st.selectbox("Category", ["Roads","Water","Sanitation","Healthcare","Education","Electricity","Public Safety","Environment","Other"])
        population = st.number_input("Estimated affected citizens", min_value=1, value=500)
        submitted = st.form_submit_button("Analyze & Submit", type="primary")

    if submitted:
        if not title or not description:
            st.error("Please enter a title and description.")
        else:
            analysis = analyze_request(title, description, category, population)
            add_request(title, description, district, ward, language, category, population, analysis)
            st.success(f"Request submitted. AI priority: {analysis['priority']} ({analysis['priority_score']}/100)")
            st.json(analysis)

elif page == "🤖 AI Analysis":
    st.title("🤖 AI Request Analyzer")
    st.write("Paste a citizen request and JanVikas AI will classify urgency, category, impact and recommended action.")

    title = st.text_input("Request title", "Broken road near school")
    description = st.text_area("Citizen message",
        "The road has many deep potholes near the school. Children and ambulances have difficulty passing during rain.")
    category = st.selectbox("Known category (optional)", ["Roads","Water","Sanitation","Healthcare","Education","Electricity","Public Safety","Environment","Other"])
    population = st.number_input("Affected citizens", 100, 100000, 3000)

    if st.button("Run AI Analysis", type="primary"):
        result = analyze_request(title, description, category, population)
        c1,c2,c3 = st.columns(3)
        c1.metric("Priority", result["priority"])
        c2.metric("Score", result["priority_score"] + "/100")
        c3.metric("Urgency", result["urgency"])
        st.subheader("AI explanation")
        st.write(result["reason"])
        st.subheader("Recommended action")
        st.success(result["recommendation"])
        st.subheader("Detected signals")
        st.write(", ".join(result["signals"]) if result["signals"] else "No strong risk signals detected.")
        st.subheader("Suggested department")
        st.info(result["department"])

elif page == "🗺️ Hotspot Map":
    st.title("🗺️ Demand Hotspot Map")
    st.caption("Demo coordinates are used for sample data. Real deployments should use verified geospatial data.")
    if len(df):
        st.plotly_chart(hotspot_map(df), use_container_width=True)
        st.dataframe(df[["district","ward","category","priority","priority_score","population_affected"]]
                     .sort_values("priority_score", ascending=False), use_container_width=True)
    else:
        st.info("No requests available.")

elif page == "📊 Analytics":
    st.title("📊 Public Infrastructure Analytics")
    if len(df):
        c1,c2 = st.columns(2)
        with c1:
            st.plotly_chart(category_chart(df), use_container_width=True)
        with c2:
            st.plotly_chart(status_chart(df), use_container_width=True)
        st.plotly_chart(district_chart(df), use_container_width=True)
        st.subheader("All requests")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data available.")

elif page == "🏛️ Policymaker":
    st.title("🏛️ Policymaker Decision Dashboard")
    st.caption("AI-generated recommendations should support—not replace—human government decisions.")

    if len(df):
        high = df[df.priority=="High"].sort_values("priority_score", ascending=False)
        st.subheader("Top development priorities")
        for _, row in high.head(6).iterrows():
            with st.container(border=True):
                st.markdown(f"### {row.title}")
                st.write(f"**Location:** {row.district} • {row.ward}")
                st.write(f"**Category:** {row.category} • **Affected:** {row.population_affected:,}")
                st.write(f"**AI priority:** {row.priority_score}/100")
                st.write(f"**Recommendation:** {row.recommendation}")
                if st.button("Mark resolved", key=f"resolve_{row.id}"):
                    update_status(int(row.id), "Resolved")
                    st.rerun()
    else:
        st.info("No requests available.")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.write("This prototype stores data locally in SQLite.")
    st.code("""
Database: janvikas.db
AI mode: local explainable scoring
Maps: Plotly
UI: Streamlit
""")
    st.warning("For production: add authentication, encrypted storage, verified GIS datasets, audit logs, human review and a secure LLM/API gateway.")
