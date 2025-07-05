import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page setup
st.set_page_config(layout="wide", page_title="Tensile Strength Analysis")
st.title("📊 Tensile Strength Analysis Dashboard")

# Load CSV
file_path = "Combined_Sample_Data.csv"
df = pd.read_csv(file_path)

# Explicit sample IDs and tab labels
sample_ids = ['S1', 'S2', 'S3', 'S4']
tab_labels = ["Sample 1", "Sample 2", "Sample 3", "Sample 4"]

# Create Tabs
st.subheader("📈 Tensile Strength Over Time (Per Sample)")
tabs = st.tabs(tab_labels)

for i, sample in enumerate(sample_ids):
    with tabs[i]:
        sample_cols = [col for col in df.columns if col.startswith(sample)]
        melted_df = df[['Time'] + sample_cols].melt(id_vars="Time", var_name="Treatment", value_name="Tensile Strength")
        melted_df["Treatment"] = melted_df["Treatment"].str.replace(f"{sample}_", "", regex=False)

        # Max points
        max_idx = melted_df.groupby("Treatment")["Tensile Strength"].idxmax().dropna()
        max_points = melted_df.loc[max_idx]
        max_points["Label"] = max_points.apply(
            lambda row: f"Max: {row['Tensile Strength']:.2f} (Treatment {row['Treatment']})", axis=1
        )

        # Max time for axis scaling
        sample_times = pd.concat([
            df[['Time', col]].dropna(subset=[col])['Time'] for col in sample_cols
        ])
        max_time = sample_times.max()

        # Plot line graph
        fig = px.line(melted_df, x="Time", y="Tensile Strength", color="Treatment",
                      title=f"{tab_labels[i]} - Tensile Strength Over Time")

        # Add red marker points (only show label on hover)
        fig.add_trace(go.Scatter(
            x=max_points["Time"],
            y=max_points["Tensile Strength"],
            mode='markers',
            marker=dict(color='red', size=8),
            hovertext=max_points["Label"],
            hoverinfo="text",
            name="Max Points"
        ))

        fig.update_layout(xaxis=dict(range=[0, max_time]), height=400, legend_title_text="Treatment")
        st.plotly_chart(fig, use_container_width=True)

        # Show individual sample DataFrame
        st.markdown("**🔍 Sample Data:**")
        st.dataframe(df[['Time'] + sample_cols], use_container_width=True)

# Static max data
max_data = {
    'S1_Pre': 1.034401, 'S1_T1': 1.105019, 'S1_T2': 1.142403, 'S1_T3': 1.215111, 'S1_T4': 1.046860, 'S1_T5': 1.279495,
    'S2_Pre': 2.207954, 'S2_T1': 1.248337, 'S2_T2': 1.821617, 'S2_T3': 1.863159, 'S2_T4': 0.932617, 'S2_T5': 1.977402,
    'S3_Pre': 1.337654, 'S3_T1': 1.051018, 'S3_T2': 1.821617, 'S3_T3': 1.480972, 'S3_T4': 1.150719, 'S3_T5': 1.393738,
    'S4_Pre': 1.541206, 'S4_T1': 1.850700, 'S4_T2': 2.139412, 'S4_T3': 1.750999, 'S4_T4': 1.528748, 'S4_T5': 1.183952
}

# Process max values
df_max = pd.Series(max_data).rename_axis("Sample_Treatment").reset_index(name="MaxValue")
df_max[['Sample', 'Treatment']] = df_max['Sample_Treatment'].str.extract(r'(S\d+)_(T\d|Pre)')
pivoted = df_max.pivot(index='Treatment', columns='Sample', values='MaxValue').sort_index()
pivoted_reset = pivoted.reset_index().melt(id_vars="Treatment", var_name="Sample", value_name="MaxValue")

# Treatment mean
treatment_means = pivoted.mean(axis=1).reset_index()
treatment_means.columns = ["Treatment", "Mean"]

# Bar chart with line
st.subheader("📊 Max Tensile Strength by Sample and Treatment")
bar_fig = px.bar(pivoted_reset, x="Treatment", y="MaxValue", color="Sample", barmode="group",
                 title="Max Tensile Strength by Sample and Treatment")

bar_fig.add_trace(go.Scatter(x=treatment_means["Treatment"], y=treatment_means["Mean"],
                             mode='lines+markers', name='Treatment Mean',
                             line=dict(color='black', width=2), marker=dict(size=6)))
bar_fig.update_layout(legend_title_text='Sample', height=500)
st.plotly_chart(bar_fig, use_container_width=True)

# Full data
st.subheader("📄 Full Data Preview")
st.dataframe(df, use_container_width=True)