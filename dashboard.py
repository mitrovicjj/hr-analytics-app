import plotly.express as px

def plot_job_change_by_experience(df):
    fig = px.line(
        df,
        x='experience',
        y='change_ratio',
        title="Stopa promjene posla po iskustvu"
    )
    return fig

def plot_masters_phd_change_ratio(df):
    fig = px.bar(
        df,
        x='education_level',
        y='change_ratio',
        title="Promjena posla kod MSc/PhD kandidata"
    )
    return fig

def plot_training_hours_by_city_edu(df):
    fig = px.bar(
        df.head(10),
        x='city',
        y='avg_training_hours',
        color='education_level',
        title="Sati obuke po gradu i obrazovanju"
    )
    return fig

def plot_change_ratio_by_company_type(df):
    fig = px.bar(
        df,
        x='company_type',
        y='change_ratio',
        title="Stopa promjene po tipu kompanije"
    )
    return fig

import plotly.express as px

def plot_top_cities(df):
    fig = px.bar(
        df,
        x='city',
        y='count',
        title='Top gradovi po broju kandidata',
        labels={'city': 'Grad', 'count': 'Broj kandidata'},
        color='count',
        color_continuous_scale='Viridis'
    )
    return fig