import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# ========================================================================================
# CAMBIO DE DISEÑO, SE IMPLEMENTÓ UN CSS PARA CAMBIAR EL FONDO, FUENTE Y COLORES DE LA APP
# ========================================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

/* Fuente para toda la app */
html, body, [class*="css"], .stMarkdown, p, label, div {
    font-family: 'Poppins', sans-serif;
}

/* Fondo de la página */
.stApp {
    background-color: #0f172a;
    color: #e2e8f0;
}

/* Título principal */
h1 {
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    color: #f43f5e !important;
    text-align: center;
    letter-spacing: 1px;
}

/* Subtítulos (##) */
h2 {
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    color: #38bdf8 !important;
    border-left: 6px solid #f43f5e;
    padding-left: 12px;
    margin-top: 30px;
}

/* Texto normal */
p, label {
    font-size: 1.05rem;
    color: #e2e8f0 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1e293b;
}
section[data-testid="stSidebar"] h2 {
    color: #fbbf24 !important;
    border-left: none;
    padding-left: 0;
}
</style>
""", unsafe_allow_html=True)

st.title("Crimes in San Francisco.")
st.markdown("Know the crimes in each area.")
df = pd.read_csv("Police.csv")
st.sidebar.header("Setting:")
day_group = df.groupby(['Incident Day of Week'])['Incident Number'].count()
st.markdown("## Most insecure areas.")
year = df['Incident Year'].unique()
year_selected = st.sidebar.selectbox("Year", year)
dist = df['Police District'].unique()
dist_selected = st.sidebar.selectbox("Area", dist)

mapa = pd.DataFrame()

mapa['lat'] = df[(df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected)]['Latitude']
mapa['lon'] = df[(df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected)]['Longitude']
mapa = mapa.dropna()
st.map(mapa)
st.markdown("## The most insecure day.")
val = df[(df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected)]['Incident Day of Week']
vals = pd.DataFrame(val)
val_count = vals['Incident Day of Week'].value_counts()
val_count = val_count.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])



fig = px.pie(values=val_count.values, names=val_count.index)
st.plotly_chart(fig, use_container_width=True)

cat = df[(df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected)]['Incident Category']
x2 = cat.value_counts()
y2 = cat.unique()

st.markdown("## Most frequent crimes.")
fig2 = go.Figure(go.Bar(
    x=x2, y=y2, orientation='h'
))


st.plotly_chart(fig2, use_container_width=True)

category = df['Incident Category']
genre = st.radio(
    "Have you suffered from a crime in these areas?",
    ('No', 'Yes')
)

if genre == 'Yes':
    st.write('Help us put the following information.')
    year = st.slider('In what year did it happen?', 1930, 2022, 1930)
    distrito = st.selectbox('In which area did it happen?', dist)
    dia = st.selectbox('What day was it?', val_count.index)
    crimen = st.selectbox('What happened?', category.unique())

    st.write("The crime was", crimen, "in", distrito, "it was a", dia, "in", year)
