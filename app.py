import os
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

# Page setup
st.set_page_config(layout="wide", page_title="Tensile Strength Analysis")
st.title("📊 Tensile Strength Analysis Dashboard")

# Load CSV
file_path = "Combined_Sample_Data_Sigfigs.csv"
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

        # Add red marker points
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

        # Collapsible sample data
        with st.expander(f"🔍 View {tab_labels[i]} Raw Data"):
            sample_df = df[['Time'] + sample_cols].copy()
            formatted_sample_df = sample_df.applymap(lambda x: f"{x:.4g}" if isinstance(x, (float, int)) else x)
            st.dataframe(formatted_sample_df, use_container_width=True)

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

st.title("📊 Percent Change in Max Tensile Strength by Sample and Treatment")

# Percent change data
percent_change_data = {
    "Treatment": ['T1', 'T1', 'T1', 'T1',
                  'T2', 'T2', 'T2', 'T2',
                  'T3', 'T3', 'T3', 'T3',
                  'T4', 'T4', 'T4', 'T4',
                  'T5', 'T5', 'T5', 'T5'],
    "Sample": ['S1', 'S2', 'S3', 'S4'] * 5,
    "Percent Change": [
        (1.105019 - 1.034401) / 1.034401 * 100,
        (1.248337 - 2.207954) / 2.207954 * 100,
        (1.051018 - 1.337654) / 1.337654 * 100,
        (1.850700 - 1.541206) / 1.541206 * 100,

        (1.142403 - 1.034401) / 1.034401 * 100,
        (1.821617 - 2.207954) / 2.207954 * 100,
        (1.821617 - 1.337654) / 1.337654 * 100,
        (2.139412 - 1.541206) / 1.541206 * 100,

        (1.215111 - 1.034401) / 1.034401 * 100,
        (1.863159 - 2.207954) / 2.207954 * 100,
        (1.480972 - 1.337654) / 1.337654 * 100,
        (1.750999 - 1.541206) / 1.541206 * 100,

        (1.046860 - 1.034401) / 1.034401 * 100,
        (0.932617 - 2.207954) / 2.207954 * 100,
        (1.150719 - 1.337654) / 1.337654 * 100,
        (1.528748 - 1.541206) / 1.541206 * 100,

        (1.279495 - 1.034401) / 1.034401 * 100,
        (1.977402 - 2.207954) / 2.207954 * 100,
        (1.393738 - 1.337654) / 1.337654 * 100,
        (1.183952 - 1.541206) / 1.541206 * 100
    ]
}

df_pc = pd.DataFrame(percent_change_data)

# Create combined category for x-axis
df_pc['Treatment_Sample'] = df_pc['Treatment'] + '_' + df_pc['Sample']

# Define ordering for combined categories
treatments = ['T1', 'T2', 'T3', 'T4', 'T5']
samples = ['S1', 'S2', 'S3', 'S4']
order = [f"{t}_{s}" for t in treatments for s in samples]

color_scale = alt.Scale(domain=samples,
                        range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])

chart = alt.Chart(df_pc).mark_bar().encode(
    x=alt.X('Treatment_Sample:N',
            sort=order,
            axis=alt.Axis(title='Treatment and Sample', labelAngle=-45),
            scale=alt.Scale(paddingInner=0.1, paddingOuter=0.3)
           ),
    y=alt.Y('Percent Change:Q', title='Percent Change vs Pre (%)'),
    color=alt.Color('Sample:N', scale=color_scale, legend=alt.Legend(title='Sample')),
    tooltip=['Sample', 'Treatment', alt.Tooltip('Percent Change', format='.1f')]
).properties(
    width=700,
    height=400,
    title='Percent Change in Max Tensile Strength by Sample and Treatment'
)

st.altair_chart(chart, use_container_width=True)

# --- Insert Microscopy Image Viewer Section Here ---
st.markdown("---")
st.subheader("🖼️ Microscopy Images Viewer")

# Load image files
image_dir = "ResearchPics"
if os.path.exists(image_dir):
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".png"))]
else:
    image_files = []

# Parse image metadata into list of (Sample, Treatment, Magnification, FilePath)
image_records = []
for file in image_files:
    clean_name = file.replace(" ", "").replace("_", "").replace("-", "").lower()
    sample, treatment, magnification = None, None, None

    for s in ['s1', 's2', 's3', 's4']:
        if s in clean_name:
            sample = s.upper()
            break

    if "pretreatment" in clean_name:
        treatment = "Pre"
    elif "t1" in clean_name:
        treatment = "T1"
    elif "t2" in clean_name:
        treatment = "T2"
    elif "t3" in clean_name:
        treatment = "T3"
    elif "t4" in clean_name:
        treatment = "T4"
    elif "t5" in clean_name:
        treatment = "T5"

    if "10x" in clean_name:
        magnification = "10x"
    elif "40x" in clean_name:
        magnification = "40x"

    if sample and treatment and magnification:
        image_records.append((sample, treatment, magnification, os.path.join(image_dir, file)))

if image_records:
    image_array = np.array(image_records, dtype=object)

    # UI Step 1: Sample and Treatment selection
    samples = sorted(set(rec[0] for rec in image_array))
    treatments = ["Pre", "T1", "T2", "T3", "T4", "T5"]

    sample_sel = st.selectbox("Select Sample", samples)
    treatment_sel = st.selectbox("Select Treatment", treatments)

    # Step 2: Filter to available magnifications for selected sample & treatment
    available_mags = sorted(set(
        rec[2] for rec in image_array
        if rec[0] == sample_sel and rec[1] == treatment_sel
    ))

    if available_mags:
        mag_sel = st.selectbox("Select Magnification", available_mags)

        # Find matching image
        matches = [rec for rec in image_array if rec[0] == sample_sel and rec[1] == treatment_sel and rec[2] == mag_sel]

        if matches:
            img_path = matches[0][3]
            st.image(img_path, caption=f"{sample_sel} - {treatment_sel} - {mag_sel}", use_container_width=True)
        else:
            st.warning("No image found for this selection.")
    else:
        st.info("No available images for this sample and treatment combination.")
else:
    st.info("No microscopy images found in the 'ResearchPics' folder.")


# GitHub link
st.markdown("---")
st.markdown("[🔗 View this project on GitHub](https://github.com/lifeissad21/GHPHairProject)")