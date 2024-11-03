import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

class PTTEnergyDashboard:
    def __init__(self):
        st.set_page_config(layout="wide", page_title="PTT Energy Management System")
        self.gsp_locations = {
            'GSP1': {'lat': 12.7503, 'lon': 101.1318},
            'GSP2': {'lat': 12.7432, 'lon': 101.1445},
            'GSP3': {'lat': 12.7366, 'lon': 101.1392},
            'GSP4': {'lat': 12.7299, 'lon': 101.1503},
            'GSP5': {'lat': 12.7233, 'lon': 101.1477},
            'GSP6': {'lat': 12.7166, 'lon': 101.1555}
        }

    def create_dashboard(self):
        # Sidebar
        self.create_sidebar()
        
        # Main dashboard
        st.title("🏭 PTT Gas Separation Plants Energy Management System")
        
        # Top metrics
        self.show_key_metrics()
        
        # Main content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.show_gsp_map()
            self.show_energy_consumption()
        
        with col2:
            self.show_carbon_credits()
            self.show_efficiency_metrics()
        
        # CO2 to Protein Conversion Monitor
        st.header("🧬 CO2 Conversion Monitoring")
        self.show_conversion_metrics()

    def create_sidebar(self):
        st.sidebar.title("Control Panel")
        st.sidebar.subheader("Plant Selection")
        selected_plant = st.sidebar.selectbox(
            "Select GSP",
            ["All Plants"] + list(self.gsp_locations.keys())
        )
        
        st.sidebar.subheader("Time Range")
        time_range = st.sidebar.select_slider(
            "Select Time Range",
            options=["24H", "7D", "30D", "YTD"]
        )
        
        st.sidebar.subheader("Alert Settings")
        st.sidebar.number_input("CO2 Threshold (tons)", 
                              min_value=0, 
                              max_value=1000, 
                              value=500)

    def show_key_metrics(self):
        cols = st.columns(4)
        
        with cols[0]:
            self.metric_card(
                "Total Energy Consumption",
                "1,234 MWh",
                "-2.5%",
                "⚡"
            )
        
        with cols[1]:
            self.metric_card(
                "Carbon Emissions",
                "456 tons",
                "-3.2%",
                "🌿"
            )
        
        with cols[2]:
            self.metric_card(
                "Carbon Credits",
                "789 units",
                "+5.1%",
                "💰"
            )
        
        with cols[3]:
            self.metric_card(
                "Efficiency Score",
                "94.5%",
                "+1.2%",
                "📈"
            )

    def metric_card(self, title, value, delta, emoji):
        st.metric(
            label=f"{emoji} {title}",
            value=value,
            delta=delta
        )

    def show_gsp_map(self):
        st.subheader("GSP Locations & Real-time Status")
        
        # Create map data
        df = pd.DataFrame({
            'GSP': list(self.gsp_locations.keys()),
            'lat': [loc['lat'] for loc in self.gsp_locations.values()],
            'lon': [loc['lon'] for loc in self.gsp_locations.values()],
            'Status': np.random.choice(['Optimal', 'Warning', 'Critical'], 6),
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
        
        st.plotly_chart(fig, use_container_width=True)

    def show_energy_consumption(self):
        st.subheader("Energy Consumption Trends")
        
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', periods=30)
        data = {
            'Date': dates,
            'GSP1': np.random.uniform(100, 150, 30),
            'GSP2': np.random.uniform(120, 170, 30),
            'GSP3': np.random.uniform(90, 140, 30),
            'GSP4': np.random.uniform(110, 160, 30),
            'GSP5': np.random.uniform(95, 145, 30),
            'GSP6': np.random.uniform(105, 155, 30)
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

    def show_carbon_credits(self):
        st.subheader("Carbon Credits Trading")
        
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', periods=30)
        credits = np.cumsum(np.random.normal(0, 10, 30)) + 1000
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=credits,
            fill='tozeroy',
            name='Carbon Credits'
        ))
        
        fig.update_layout(
            title='Carbon Credits Balance',
            xaxis_title='Date',
            yaxis_title='Credits'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def show_efficiency_metrics(self):
        st.subheader("Plant Efficiency Metrics")
        
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

    def show_conversion_metrics(self):
        cols = st.columns(2)
        
        with cols[0]:
            self.show_protein_conversion()
        
        with cols[1]:
            self.show_conversion_efficiency()

    def show_protein_conversion(self):
        st.subheader("CO2 to Protein Conversion")
        
        # Create sample data
        times = pd.date_range(start='now', periods=100, freq='1min')
        protein_levels = np.cumsum(np.random.normal(0, 0.1, 100)) + 5
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times,
            y=protein_levels,
            mode='lines+markers',
            name='Protein Level'
        ))
        
        fig.update_layout(
            title='Real-time Protein Production',
            xaxis_title='Time',
            yaxis_title='Protein Concentration (g/L)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def show_conversion_efficiency(self):
        st.subheader("Conversion Efficiency")
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 84.3,
            title = {'text': "Conversion Efficiency"},
            gauge = {
                'axis': {'range': [None, 100]},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "darkgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    dashboard = PTTEnergyDashboard()
    dashboard.create_dashboard()