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

        /* Dark Theme for CO2 to Protein Page */
        .dark-theme {
            background-color: #1a1a1a;
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        }

        .dark-theme h1, .dark-theme h2, .dark-theme h3 {
            color: white;
            margin-bottom: 1rem;
        }

        .gauge-container {
            background: #2d2d2d;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }

        .visualization-container {
            background: #2d2d2d;
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        }

        /* Custom Metric Styling */
        div[data-testid="stMetricValue"] {
            background: linear-gradient(120deg, #1e88e5 0%, #00acc1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.8rem !important;
        }

        /* Map Container */
        .map-container {
            background: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        /* Chart Container */
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }

        /* Animation */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .animated-card {
            animation: pulse 2s infinite;
        }
        </style>
        """, unsafe_allow_html=True)
    def create_sidebar(self):
        st.sidebar.markdown("""
            <div style='
                background: linear-gradient(120deg, #1e88e5 0%, #00acc1 100%);
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 1rem;
            '>
                <h2 style='color: white; text-align: center;'>Control Panel</h2>
            </div>
        """, unsafe_allow_html=True)

        selected_gsp = st.sidebar.selectbox(
            "Select GSP",
            ["All Plants"] + list(self.gsp_locations.keys()),
            help="Choose a specific Gas Separation Plant or view all plants"
        )

        time_range = st.sidebar.select_slider(
            "Time Range",
            options=["24H", "7D", "30D", "YTD"],
            value="7D",
            help="Select the time range for data visualization"
        )

        st.sidebar.markdown("""
            <div style='
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 1rem;
                border-radius: 10px;
                margin-top: 1rem;
            '>
                <h3 style='color: #1e88e5;'>Alert Settings</h3>
            </div>
        """, unsafe_allow_html=True)

        co2_threshold = st.sidebar.number_input(
            "CO2 Threshold (tons)",
            min_value=0,
            max_value=1000,
            value=500,
            help="Set the CO2 emission threshold for alerts"
        )

        return selected_gsp, time_range, co2_threshold

    def show_energy_metrics(self):
        metrics = [
            {
                'title': 'Total Energy Consumption',
                'value': '1,234 MWh',
                'delta': '-2.5%',
                'icon': '⚡',
                'color': '#1e88e5'
            },
            {
                'title': 'Carbon Emissions',
                'value': '456 tons',
                'delta': '-3.2%',
                'icon': '🌿',
                'color': '#00acc1'
            },
            {
                'title': 'Carbon Credits',
                'value': '789 units',
                'delta': '+5.1%',
                'icon': '💰',
                'color': '#43a047'
            },
            {
                'title': 'Efficiency Score',
                'value': '94.5%',
                'delta': '+1.2%',
                'icon': '📈',
                'color': '#7cb342'
            }
        ]

        cols = st.columns(4)
        for col, metric in zip(cols, metrics):
            with col:
                st.markdown(f"""
                    <div class='metric-card' style='border-left: 4px solid {metric["color"]};'>
                        <h4 style='color: {metric["color"]};'>{metric['icon']} {metric['title']}</h4>
                        <h2 style='font-size: 1.8rem; margin: 0.5rem 0;'>{metric['value']}</h2>
                        <p style='color: {'green' if '+' in metric['delta'] else 'red'};'>
                            {metric['delta']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    def show_gsp_map(self):
        st.markdown("""
            <div class='map-container'>
                <h3 style='color: #1e88e5; margin-bottom: 1rem;'>
                    GSP Locations & Real-time Status
                </h3>
            </div>
        """, unsafe_allow_html=True)

        df = pd.DataFrame({
            'GSP': list(self.gsp_locations.keys()),
            'lat': [loc['lat'] for loc in self.gsp_locations.values()],
            'lon': [loc['lon'] for loc in self.gsp_locations.values()],
            'Status': [loc['status'] for loc in self.gsp_locations.values()],
            'Energy': np.random.uniform(100, 500, 6),
            'Efficiency': np.random.uniform(85, 98, 6)
        })

        fig = px.scatter_mapbox(
            df,
            lat='lat',
            lon='lon',
            color='Status',
            size='Energy',
            hover_name='GSP',
            hover_data=['Efficiency'],
            zoom=11,
            mapbox_style='carto-positron',
            color_discrete_map={
                'Operational': '#00acc1',
                'Maintenance': '#ffd700',
                'Under Review': '#ff7043'
            }
        )

        fig.update_layout(
            height=600,
            margin=dict(l=0, r=0, t=0, b=0),
            mapbox=dict(
                center=dict(lat=12.7333, lon=101.1500),
                zoom=11
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    def show_energy_trends(self):
        st.markdown("""
            <div class='chart-container'>
                <h3 style='color: #1e88e5; margin-bottom: 1rem;'>
                    Energy Consumption Trends
                </h3>
            </div>
        """, unsafe_allow_html=True)

        dates = pd.date_range(start='2024-01-01', periods=30)
        data = {
            'Date': dates,
            **{f'GSP{i}': np.random.uniform(100, 150, 30) + i * 10 + 
               np.sin(np.linspace(0, 10, 30)) * 20 for i in range(1, 7)}
        }
        df = pd.DataFrame(data)

        fig = go.Figure()
        colors = px.colors.qualitative.Set3

        for i, gsp in enumerate([f'GSP{i}' for i in range(1, 7)]):
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df[gsp],
                name=gsp,
                mode='lines+markers',
                line=dict(width=2, color=colors[i]),
                marker=dict(size=6),
                hovertemplate=
                f"{gsp}<br>" +
                "Date: %{x|%Y-%m-%d}<br>" +
                "Energy: %{y:.1f} MWh<br>" +
                "<extra></extra>"
            ))

        fig.update_layout(
            height=500,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Date",
            yaxis_title="Energy Consumption (MWh)"
        )

        st.plotly_chart(fig, use_container_width=True)
    def protein_conversion_view(self):
        st.markdown("""
        <div class='dark-theme'>
            <h1 style='display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 2.5rem;'>🧬</span> 
                CO2 to Protein Conversion Visualizer
            </h1>
        </div>
        """, unsafe_allow_html=True)

        # Pipeline Section
        st.markdown("""
        <div class='dark-theme'>
            <h2>CO2 to Protein Conversion Pipeline ⚡</h2>
        </div>
        """, unsafe_allow_html=True)

        # Create gauge charts for conversion stages
        stages = [
            {
                'title': 'CO2 Capture',
                'value': 85,
                'color': '#4CAF50',
                'icon': '🌪️'
            },
            {
                'title': 'Bacterial Processing',
                'value': 92,
                'color': '#2196F3',
                'icon': '🦠'
            },
            {
                'title': 'Protein Synthesis',
                'value': 78,
                'color': '#FFC107',
                'icon': '🧬'
            },
            {
                'title': 'Final Product',
                'value': 95,
                'color': '#9C27B0',
                'icon': '🥩'
            }
        ]

        cols = st.columns(4)
        for col, stage in zip(cols, stages):
            with col:
                st.markdown(f"""
                    <div class='gauge-container'>
                        <h3 style='text-align: center; color: white;'>
                            {stage['icon']} {stage['title']}
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=stage['value'],
                    title={'text': '', 'font': {'color': 'white'}},
                    gauge={
                        'axis': {
                            'range': [None, 100], 
                            'tickwidth': 1, 
                            'tickcolor': "white",
                            'tickfont': {'color': 'white'}
                        },
                        'bar': {'color': stage['color']},
                        'bgcolor': "rgba(255, 255, 255, 0.1)",
                        'borderwidth': 2,
                        'bordercolor': "white",
                        'steps': [
                            {'range': [0, 50], 'color': f"{stage['color']}22"},
                            {'range': [50, 80], 'color': f"{stage['color']}44"},
                            {'range': [80, 100], 'color': f"{stage['color']}66"}
                        ]
                    }
                ))

                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': 'white', 'size': 16},
                    height=300,
                    margin=dict(l=20, r=20, t=30, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

        # Main visualizations
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown("""
            <div class='dark-theme'>
                <h2>Protein Formation Simulation</h2>
                <h3>3D Protein Structure Formation</h3>
            </div>
            """, unsafe_allow_html=True)
            self.create_3d_protein_simulation(dark_theme=True)

        with col2:
            st.markdown("""
            <div class='dark-theme'>
                <h2>Molecular Transformation Process</h2>
            </div>
            """, unsafe_allow_html=True)
            self.show_molecular_animation(dark_theme=True)
            self.show_process_metrics()

    def create_3d_protein_simulation(self, dark_theme=False):
        # Generate 3D protein structure data
        n_points = 1000
        theta = np.random.uniform(0, 2*np.pi, n_points)
        phi = np.random.uniform(0, np.pi, n_points)
        r = np.random.normal(1, 0.1, n_points)

        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)

        df = pd.DataFrame({
            'x': x,
            'y': y,
            'z': z,
            'size': np.random.uniform(2, 8, n_points),
            'color': np.random.uniform(0, 1, n_points)
        })

        bgcolor = 'rgba(0,0,0,0)' if dark_theme else 'white'
        gridcolor = 'white' if dark_theme else 'black'

        fig = go.Figure(data=[go.Scatter3d(
            x=df['x'],
            y=df['y'],
            z=df['z'],
            mode='markers',
            marker=dict(
                size=df['size'],
                color=df['color'],
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(
                    title='Protein Density',
                    titleside='right',
                    titlefont={'color': 'white' if dark_theme else 'black'}
                )
            ),
            hovertemplate=
            "Position:<br>" +
            "X: %{x:.2f}<br>" +
            "Y: %{y:.2f}<br>" +
            "Z: %{z:.2f}<br>" +
            "Density: %{marker.color:.2f}" +
            "<extra></extra>"
        )])

        fig.update_layout(
            paper_bgcolor=bgcolor,
            plot_bgcolor=bgcolor,
            scene=dict(
                xaxis=dict(
                    gridcolor=gridcolor,
                    showbackground=False,
                    zeroline=False
                ),
                yaxis=dict(
                    gridcolor=gridcolor,
                    showbackground=False,
                    zeroline=False
                ),
                zaxis=dict(
                    gridcolor=gridcolor,
                    showbackground=False,
                    zeroline=False
                ),
                bgcolor=bgcolor
            ),
            height=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

    def show_molecular_animation(self, dark_theme=False):
        bgcolor = 'rgba(0,0,0,0)' if dark_theme else 'white'
        gridcolor = 'white' if dark_theme else 'black'

        # Create animated molecular visualization
        t = np.linspace(0, 2*np.pi, 100)
        x = np.cos(t)
        y = np.sin(t)

        fig = go.Figure(
            data=[go.Scatter(
                x=x,
                y=y,
                mode='lines',
                line=dict(
                    color='#2196F3',
                    width=4
                ),
                fill='toself',
                fillcolor='rgba(33, 150, 243, 0.2)'
            )]
        )

        fig.update_layout(
            paper_bgcolor=bgcolor,
            plot_bgcolor=bgcolor,
            xaxis=dict(
                gridcolor=gridcolor,
                showgrid=True,
                zeroline=False,
                showline=False,
                range=[-2, 2]
            ),
            yaxis=dict(
                gridcolor=gridcolor,
                showgrid=True,
                zeroline=False,
                showline=False,
                range=[-2, 2]
            ),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    def show_process_metrics(self):
        st.markdown("""
            <div style='
                background: #2d2d2d;
                padding: 1.5rem;
                border-radius: 10px;
                margin-top: 1rem;
            '>
                <h3 style='color: white; margin-bottom: 1rem;'>Process Metrics</h3>
            </div>
        """, unsafe_allow_html=True)

        metrics = {
            'Temperature': {'value': f"{37.2:.1f}°C", 'delta': 'Optimal'},
            'pH Level': {'value': '7.2', 'delta': 'Optimal'},
            'Pressure': {'value': '1.2 atm', 'delta': 'Optimal'},
            'Flow Rate': {'value': '2.5 L/min', 'delta': 'Optimal'}
        }

        for key, data in metrics.items():
            st.metric(
                label=key,
                value=data['value'],
                delta=data['delta'],
                delta_color='normal'
            )

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
            self.protein_conversion_view()

if __name__ == "__main__":
    dashboard = IntegratedDashboard()
    dashboard.run_dashboard()