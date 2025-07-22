import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

from queries import (
    get_avg_training_by_city_edu,
    get_change_ratio_by_experience,
    get_top_cities,
    get_company_type_counts,
    get_education_counts,
    get_avg_experience_by_gender,
    get_last_new_job_counts,
    get_masters_phd_change_ratio,
    get_change_ratio_by_company_type
)

from dashboard import (
    plot_top_cities,
    plot_job_change_by_experience,
    plot_masters_phd_change_ratio,
    plot_training_hours_by_city_edu,
    plot_change_ratio_by_company_type
)

st.set_page_config(
    page_title="HR Analytics Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# STYLE FIXES
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
        padding: 0.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #fff;
    }
    .main-header h1 {
        color: white !important;
        margin: 0;
        text-align: center;
        font-size: 1.5rem;
        font-family: sans-serif;
        text-shadow: 1px 1px 0px rgba(0,0,0,0.3);
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Minimalistički metrike - bez background, bez senki */
    [data-testid="stMetric"], .stMetric {
        background: transparent !important;
        padding: 0.5rem 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        border: none !important;
        text-align: left;
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: #333;
        border-bottom: 1px solid #ddd;
    }
    [data-testid="stMetric"]:hover {
        transform: none !important;
        box-shadow: none !important;
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        background: #dda0dd;
    }

    /* Select box */
    [data-baseweb="select"] {
        background-color: #98fb98 !important;
        border: 2px solid #32cd32 !important;
        border-radius: 8px !important;
    }

    /* Minimalistička analiza sekcija */
    .analysis-section {
        background: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        border: none !important;
        margin: 1rem 0;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #ffd700;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Section header */
    .section-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-family: sans-serif;
    }
    .section-header h2 {
        margin: 0;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# MAIN HEADER
st.markdown('<div class="main-header"><h1>📊 HR Analytics Dashboard</h1></div>', unsafe_allow_html=True)

# DATA
conn = sqlite3.connect("job_data.db")
df_all = pd.read_sql_query("SELECT * FROM candidates", conn)

# SIDEBAR
with st.sidebar:
    st.markdown("### Filteri")
    with st.expander("Demografski filteri", expanded=True):
        gender = st.multiselect("Pol", df_all["gender"].unique(), default=df_all["gender"].unique())
        education = st.multiselect("Obrazovanje", df_all["education_level"].unique(), default=df_all["education_level"].unique())
    with st.expander("Poslovni filteri", expanded=True):
        company_type = st.multiselect("Tip kompanije", df_all["company_type"].unique(), default=df_all["company_type"].unique())
        experience_range = st.slider("Iskustvo (godine)", 0, 5, (0, 5))
    if st.button("🔄 Resetuj filtere", use_container_width=True):
        st.experimental_rerun()

# FILTERED DATA
df_filtered = df_all[
    df_all["gender"].isin(gender) &
    df_all["education_level"].isin(education) &
    df_all["company_type"].isin(company_type) &
    df_all["experience"].between(*experience_range)
]

# METRICS
st.markdown("##### 📈 Ključni pokazatelji")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ukupno kandidata", f"{len(df_filtered)}")

with col2:
    change_ratio = df_filtered[df_filtered["target"] == 1].shape[0] / len(df_filtered) * 100 if len(df_filtered) > 0 else 0
    st.metric("Stopa promjene posla", f"{change_ratio:.1f}%")

with col3:
    avg_training = df_filtered["training_hours"].mean() if len(df_filtered) > 0 else 0
    st.metric("Prosječna obuka", f"{avg_training:.0f}h")

with col4:
    avg_experience = df_filtered["experience"].mean() if len(df_filtered) > 0 else 0
    st.metric("Prosječno iskustvo", f"{avg_experience:.1f} god")

st.divider()

st.markdown("##### Analiza podataka")

option = st.selectbox("Izaberite tip analize:", [
    "Pregled kandidata po gradu",
    "Poredjenje grupa (pol, obrazovanje)",
    "Eksplorativna analiza (distribucije)",
    "Prosječni sati obuke po gradu i obrazovanju",
    "Promjena posla po godinama iskustva",
    "Promjena posla kod MSc/PhD kandidata",
    "Najpopularniji gradovi po broju kandidata",
    "Distribucija po tipu kompanije"
], index=0)

if option == "Prosječni sati obuke po gradu i obrazovanju":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Sati obuke po gradu i obrazovanju")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            df = pd.read_sql_query(get_avg_training_by_city_edu(), conn)
            st.dataframe(df.head(10), use_container_width=True)
        with col2:
            fig = plot_training_hours_by_city_edu(df)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Eksplorativna analiza (distribucije)":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("🔬 Eksplorativna analiza")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Iskustvo", "👥 Pol", "📚 Obuka", "🗺️ Geo. distribucija"])
        
        with tab1:
            fig = px.histogram(df_filtered, x="experience", nbins=6, title="Distribucija godina iskustva")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            gender_counts = df_filtered["gender"].value_counts().reset_index()
            gender_counts.columns = ["Pol", "Broj"]
            fig = px.bar(gender_counts, x="Pol", y="Broj", title="Broj kandidata po polu")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = px.histogram(df_filtered, x="training_hours", nbins=20, title="Distribucija sati obuke")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("📍 Geografska distribucija")
            col1, col2 = st.columns(2)
            
            with col1:
                city_counts = df_filtered["city"].value_counts().head(10).reset_index()
                city_counts.columns = ["Grad", "Broj kandidata"]
                fig = px.bar(city_counts, x="Broj kandidata", y="Grad", orientation="h",
                           title="Top 10 gradova po broju kandidata")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                city_change = df_filtered.groupby("city").agg({
                    "target": ["mean", "count"]
                }).round(3)
                city_change.columns = ["Stopa_promjene", "Ukupno"]
                city_change = city_change[city_change["Ukupno"] >= 5]
                city_change = city_change.sort_values("Stopa_promjene", ascending=False).head(10).reset_index()
                
                fig = px.bar(city_change, x="Stopa_promjene", y="city", orientation="h",
                           title="Stopa promjene posla po gradovima")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Poredjenje grupa (pol, obrazovanje)":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Poređenje grupa")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Prosječni sati obuke po polu**")
            avg_hours_by_gender = df_filtered.groupby("gender")["training_hours"].mean().reset_index()
            fig = px.bar(avg_hours_by_gender, x="gender", y="training_hours", 
                        title="Prosječni sati obuke po polu")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Stopa promjene posla po obrazovanju**")
            edu_change = df_filtered.groupby("education_level")["target"].mean().reset_index()
            fig = px.bar(edu_change, x="education_level", y="target", 
                        title="Stopa promjene posla po obrazovanju (%)")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Pregled kandidata po gradu":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Pregled kandidata po gradu")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            selected_city = st.selectbox("Odaberite grad:", df_filtered["city"].unique())
            city_stats = df_filtered[df_filtered["city"] == selected_city]
            st.metric("Broj kandidata", len(city_stats))
            st.metric("Stopa promjene", f"{city_stats['target'].mean()*100:.1f}%")
        
        with col2:
            st.write(f"**Kandidati iz grada: {selected_city}**")
            st.dataframe(city_stats, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Promjena posla po godinama iskustva":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Promjena posla po iskustvu")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            df = pd.read_sql_query(get_change_ratio_by_experience(), conn)
            st.dataframe(df, use_container_width=True)
        with col2:
            fig = plot_job_change_by_experience(df)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Promjena posla kod MSc/PhD kandidata":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("MSc/PhD analiza")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            df = pd.read_sql_query(get_masters_phd_change_ratio(), conn)
            st.dataframe(df, use_container_width=True)
        with col2:
            fig = plot_masters_phd_change_ratio(df)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Najpopularniji gradovi po broju kandidata":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Top gradovi")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            df = pd.read_sql_query(get_top_cities(), conn)
            st.dataframe(df, use_container_width=True)
        with col2:
            fig = plot_top_cities(df)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif option == "Distribucija po tipu kompanije":
    with st.container():
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.subheader("Analiza po tipu kompanije")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            df = pd.read_sql_query(get_change_ratio_by_company_type(), conn)
            st.dataframe(df, use_container_width=True)
        with col2:
            fig = plot_change_ratio_by_company_type(df)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# BUTTON
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.download_button(
        "📥 Preuzmi filtrirane podatke (CSV)",
        df_filtered.to_csv(index=False),
        file_name="filtrirani_kandidati.csv",
        mime="text/csv",
        use_container_width=True
    )

conn.close()