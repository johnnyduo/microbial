import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import time
import requests

class IntegratedDashboard:
    def __init__(self):
        st.set_page_config(
            layout="wide",
            page_title="PTT Integrated Management System",
            initial_sidebar_state="expanded"
        )
        self.initialize_data()
        self.setup_styles()

    def initialize_data(self):
        self.gsp_locations = {
            'GSP1': {'lat': 12.7503, 'lon': 101.1318, 'status': 'Operational'},
            'GSP2': {'lat': 12.7432, 'lon': 101.1445, 'status': 'Operational'},
            'GSP3': {'lat': 12.7366, 'lon': 101.1392, 'status': 'Maintenance'},
            'GSP4': {'lat': 12.7299, 'lon': 101.1503, 'status': 'Operational'},
            'GSP5': {'lat': 12.7233, 'lon': 101.1477, 'status': 'Operational'},
            'GSP6': {'lat': 12.7166, 'lon': 101.1555, 'status': 'Under Review'}
        }

    def setup_styles(self):
        st.markdown("""
        <style>
        /* Main Theme Colors */
        :root {
            --primary-color: #1e88e5;
            --secondary-color: #00acc1;
            --background-gradient: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
            --card-gradient: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        /* Main Container */
        .main-header {
            background: linear-gradient(120deg, #1e88e5 0%, #00acc1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 10px 20px;
            border-radius: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 24px;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 8px;
            border: none;
            color: #1e88e5;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, #1e88e5 0%, #00acc1 100%);
            color: white;
            transform: translateY(-2px);
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #1e88e5 0%, #00acc1 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(30,136,229,0.2);
        }

        /* Cards and Containers */
        .metric-card {
            background: var(--card-gradient);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
        }

        .conversion-container {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }

        .process-stage {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            min-height: 200px;
        }
        </style>
        """, unsafe_allow_html=True)

    def run_dashboard(self):
        # Sidebar
        selected_gsp, time_range, co2_threshold = self.create_sidebar()

        # Main content
        st.markdown("<h1 class='main-header'>PTT Integrated Management System</h1>", 
                   unsafe_allow_html=True)

        # Create tabs
        tab1, tab2 = st.tabs(["🏭 Energy Management", "🧬 CO2 to Protein"])

        # Energy Management Tab
        with tab1:
            st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
            self.show_energy_metrics()
            self.show_gsp_map()
            self.show_energy_trends()
            self.show_efficiency_analysis()
            st.markdown("</div>", unsafe_allow_html=True)

        # CO2 to Protein Tab
        with tab2:
            st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
            self.protein_conversion_view()
            st.markdown("</div>", unsafe_allow_html=True)

    def create_sidebar(self):
        st.sidebar.title("Control Panel")
        
        selected_gsp = st.sidebar.selectbox(
            "Select GSP",
            ["All Plants"] + list(self.gsp_locations.keys())
        )
        
        time_range = st.sidebar.select_slider(
            "Time Range",
            options=["24H", "7D", "30D", "YTD"]
        )
        
        st.sidebar.subheader("Alert Settings")
        co2_threshold = st.sidebar.number_input(
            "CO2 Threshold (tons)",
            min_value=0,
            max_value=1000,
            value=500
        )
        
        return selected_gsp, time_range, co2_threshold

    def show_energy_metrics(self):
        cols = st.columns(4)
        metrics = [
            ("Total Energy Consumption", "1,234 MWh", "-2.5%", "⚡"),
            ("Carbon Emissions", "456 tons", "-3.2%", "🌿"),
            ("Carbon Credits", "789 units", "+5.1%", "💰"),
            ("Efficiency Score", "94.5%", "+1.2%", "📈")
        ]
        
        for col, (title, value, delta, emoji) in zip(cols, metrics):
            with col:
                st.metric(label=f"{emoji} {title}", value=value, delta=delta)

    def show_gsp_map(self):
        st.subheader("GSP Locations & Real-time Status")
        
        df = pd.DataFrame({
            'GSP': list(self.gsp_locations.keys()),
            'lat': [loc['lat'] for loc in self.gsp_locations.values()],
            'lon': [loc['lon'] for loc in self.gsp_locations.values()],
            'Status': [loc['status'] for loc in self.gsp_locations.values()],
            'Energy': np.random.uniform(100, 500, 6)
        })
        
        fig = px.scatter_mapbox(
            df,
            lat='lat',
            lon='lon',
            color='Status',
            size='Energy',
            hover_name='GSP',
            zoom=11,
            mapbox_style='carto-positron'
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    def show_energy_trends(self):
        st.subheader("Energy Consumption Trends")
        
        dates = pd.date_range(start='2024-01-01', periods=30)
        data = {
            'Date': dates,
            **{f'GSP{i}': np.random.uniform(100, 150, 30) + i * 10 
               for i in range(1, 7)}
        }
        df = pd.DataFrame(data)
        
        fig = px.line(
            df.melt(id_vars=['Date'], var_name='Plant', value_name='Energy'),
            x='Date',
            y='Energy',
            color='Plant',
            title='Daily Energy Consumption by Plant'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def show_efficiency_analysis(self):
        st.subheader("Plant Efficiency Analysis")
        
        efficiency_data = {
            'Plant': list(self.gsp_locations.keys()),
            'Efficiency': np.random.uniform(85, 98, 6)
        }
        
        fig = px.bar(
            efficiency_data,
            x='Plant',
            y='Efficiency',
            color='Efficiency',
            color_continuous_scale='viridis'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def protein_conversion_view(self):
        st.subheader("CO2 to Protein Conversion Process")
        
        # Show conversion stages
        stages = [
            ("CO2 Capture", 85),
            ("Bacterial Processing", 92),
            ("Protein Synthesis", 78),
            ("Final Product", 95)
        ]
        
        cols = st.columns(len(stages))
        for col, (stage, value) in zip(cols, stages):
            with col:
                st.metric(label=stage, value=f"{value}%")
        
        # Show 3D visualization
        self.create_3d_protein_simulation()

    def create_3d_protein_simulation(self):
        n_points = 1000
        df = pd.DataFrame({
            'x': np.random.normal(0, 1, n_points),
            'y': np.random.normal(0, 1, n_points),
            'z': np.random.normal(0, 1, n_points),
            'size': np.random.uniform(2, 8, n_points),
            'color': np.random.uniform(0, 1, n_points)
        })
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df['x'],
            y=df['y'],
            z=df['z'],
            mode='markers',
            marker=dict(
                size=df['size'],
                color=df['color'],
                colorscale='Viridis',
                opacity=0.8
            )
        )])
        
        fig.update_layout(
            height=600,
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    dashboard = IntegratedDashboard()
    dashboard.run_dashboard()