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
        st.set_page_config(layout="wide", 
                          page_title="PTT Integrated Management System",
                          initial_sidebar_state="expanded")
        self.setup_styles()
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
        .main-header {
            font-size: 2.5rem;
            color: #0066b2;
            text-align: center;
            margin-bottom: 2rem;
        }
        .tab-content {
            padding: 1rem;
            border-radius: 10px;
            background: #f8f9fa;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 24px;
            background: #ffffff;
            border-radius: 4px 4px 0 0;
        }
        </style>
        """, unsafe_allow_html=True)

    def create_sidebar(self):
        st.sidebar.title("Control Panel")
        
        # GSP Selection
        selected_gsp = st.sidebar.selectbox(
            "Select GSP",
            ["All Plants"] + list(self.gsp_locations.keys())
        )
        
        # Time Range
        time_range = st.sidebar.select_slider(
            "Time Range",
            options=["24H", "7D", "30D", "YTD"]
        )
        
        # Alert Settings
        st.sidebar.subheader("Alert Settings")
        co2_threshold = st.sidebar.number_input(
            "CO2 Threshold (tons)",
            min_value=0,
            max_value=1000,
            value=500
        )
        
        return selected_gsp, time_range, co2_threshold

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
            mapbox_style='carto-positron',
            title="PTT Gas Separation Plants - Rayong Province"
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

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

    def show_energy_trends(self):
        # Generate sample data
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

    def protein_conversion_view(self):
        # Reuse the protein visualization code
        self.create_3d_protein_simulation()
        self.show_conversion_pipeline()
        self.show_molecular_animation()

    def create_3d_protein_simulation(self):
        st.subheader("Protein Formation Simulation")
        
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
            title="3D Protein Structure Formation",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z"
            ),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def show_conversion_pipeline(self):
        stages = ['CO2 Capture', 'Bacterial Processing', 
                 'Protein Synthesis', 'Final Product']
        progress = [85, 92, 78, 95]
        
        cols = st.columns(len(stages))
        for col, stage, prog in zip(cols, stages, progress):
            with col:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prog,
                    title={'text': stage},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "lightgreen"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "gray"},
                            {'range': [80, 100], 'color': "darkgreen"}
                        ]
                    }
                ))
                fig.update_layout(height=200)
                st.plotly_chart(fig, use_container_width=True)

    def show_molecular_animation(self):
        st.subheader("Molecular Transformation Process")
        
        times = np.linspace(0, 2*np.pi, 100)
        df = pd.DataFrame({
            'x': np.cos(times),
            'y': np.sin(times),
            'size': np.abs(np.sin(times)) * 10
        })
        
        fig = px.scatter(df, x='x', y='y', 
                        size='size',
                        range_x=[-2, 2], range_y=[-2, 2])
        
        fig.update_layout(
            title="Molecular Transformation",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

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
            st.markdown("</div>", unsafe_allow_html=True)
        
        # CO2 to Protein Tab
        with tab2:
            st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
            self.protein_conversion_view()
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    dashboard = IntegratedDashboard()
    dashboard.run_dashboard()