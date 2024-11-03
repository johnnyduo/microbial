import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import time
import requests

class CO2ProteinVisualizer:
    def __init__(self):
        st.set_page_config(layout="wide", page_title="CO2 to Protein Conversion")
        self.setup_styles()

    def setup_styles(self):
        st.markdown("""
        <style>
        .protein-stage {
            background: #1E1E1E;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }
        .conversion-step {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
        </style>
        """, unsafe_allow_html=True)

    def create_3d_protein_simulation(self):
        st.subheader("Protein Formation Simulation")
        
        # Create 3D scatter plot representing protein formation
        np.random.seed(42)
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

    def create_conversion_pipeline(self):
        st.subheader("CO2 to Protein Conversion Pipeline")
        
        # Create pipeline visualization
        stages = ['CO2 Capture', 'Bacterial Processing', 
                 'Protein Synthesis', 'Final Product']
        progress = [85, 92, 78, 95]
        
        fig = go.Figure()
        
        # Add pipeline stages
        for i, (stage, prog) in enumerate(zip(stages, progress)):
            fig.add_trace(go.Indicator(
                mode = "gauge+number",
                value = prog,
                title = {'text': stage},
                domain = {'row': 0, 'column': i},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "lightgreen"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"},
                        {'range': [80, 100], 'color': "darkgreen"}
                    ]
                }
            ))
        
        fig.update_layout(
            grid = {'rows': 1, 'columns': 4, 'pattern': "independent"},
            height = 300
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def show_molecular_animation(self):
        st.subheader("Molecular Transformation Process")
        
        # Create animated scatter plot
        times = np.linspace(0, 2*np.pi, 100)
        
        def generate_frame(t):
            return pd.DataFrame({
                'x': np.cos(times + t),
                'y': np.sin(times + t),
                'size': np.abs(np.sin(times + t)) * 10
            })
        
        frames = [generate_frame(t) for t in np.linspace(0, 2*np.pi, 30)]
        
        fig = px.scatter(frames[0], x='x', y='y', 
                        size='size', animation_frame=None,
                        range_x=[-2, 2], range_y=[-2, 2])
        
        fig.update_layout(
            title="Molecular Transformation",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def show_real_time_metrics(self):
        st.subheader("Real-time Conversion Metrics")
        
        cols = st.columns(3)
        
        with cols[0]:
            self.create_metric_card(
                "CO2 Consumed",
                f"{np.random.uniform(80, 90):.1f}%",
                "↑ 2.3%"
            )
        
        with cols[1]:
            self.create_metric_card(
                "Protein Yield",
                f"{np.random.uniform(70, 80):.1f}%",
                "↑ 1.8%"
            )
        
        with cols[2]:
            self.create_metric_card(
                "Process Efficiency",
                f"{np.random.uniform(85, 95):.1f}%",
                "↑ 3.2%"
            )

    def create_metric_card(self, title, value, delta):
        st.metric(
            label=title,
            value=value,
            delta=delta
        )

    def show_process_details(self):
        st.subheader("Process Details")
        
        with st.expander("See detailed explanation"):
            st.write("""
            1. **CO2 Capture**: Atmospheric CO2 is captured using specialized bacterial strains
            2. **Bacterial Processing**: Bacteria convert CO2 into organic compounds
            3. **Protein Synthesis**: Organic compounds are transformed into protein structures
            4. **Final Product**: Pure protein is extracted and processed
            """)
            
            # Add process parameters
            st.markdown("### Key Parameters")
            params = pd.DataFrame({
                'Parameter': ['Temperature', 'pH', 'Pressure', 'Flow Rate'],
                'Value': ['37°C', '7.2', '1 atm', '2.5 L/min'],
                'Status': ['Optimal', 'Optimal', 'Warning', 'Optimal']
            })
            st.table(params)

    def run_dashboard(self):
        st.title("🧬 CO2 to Protein Conversion Visualizer")
        
        # Main sections
        self.create_conversion_pipeline()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.create_3d_protein_simulation()
        
        with col2:
            self.show_molecular_animation()
            self.show_process_details()
        
        self.show_real_time_metrics()

if __name__ == "__main__":
    visualizer = CO2ProteinVisualizer()
    visualizer.run_dashboard()