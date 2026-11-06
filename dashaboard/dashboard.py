import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="Steam Analytics 2021–2025",
    page_icon="🎮",
    layout="wide",
)


# ==============================================================================
# 2. LOAD & CLEANING DATASET
# ==============================================================================
@st.cache_data
def load_data():
  base_dir = os.path.dirname(os.path.abspath(__file__))
  file_path = os.path.join(base_dir, "data", "rawday.csv")

  df = pd.read_csv(file_path)
  df.columns = df.columns.str.strip().str.lower()

  if "release_date" in df.columns:
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year

  df = df[(df["release_year"] >= 2021) & (df["release_year"] <= 2025)].copy()

  if "price" in df.columns:
    df["price_usd"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["price_idr"] = df["price_usd"] * 16000

  if "recommendations" in df.columns:
    df["recommendations"] = pd.to_numeric(
        df["recommendations"], errors="coerce"
    ).fillna(0)

  def parse_genres(val):
    if pd.isna(val) or str(val).strip() == "":
      return ["Uncategorized"]
    items = str(val).replace(";", ",").split(",")
    return [g.strip() for g in items if g.strip()]

  genre_col = "genres" if "genres" in df.columns else "genre"
  df["genre_list"] = df[genre_col].apply(parse_genres)

  return df


df = load_data()

# ==============================================================================
# 3. HEADER
# ==============================================================================
st.title("🎮 Steam Analytics 2021–2025")
st.caption("Statistika Deskriptif dan Distribusi Data Game Steam")
st.markdown("---")

# ==============================================================================
# 4. SIDEBAR FILTER
# ==============================================================================
st.sidebar.header("Filter Data")

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
selected_years = st.sidebar.slider(
    "Tahun Rilis",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

all_single_genres = sorted(
    list(set(g for genres in df["genre_list"] for g in genres))
)
default_selection = [
    g
    for g in ["Action", "Casual", "Adventure", "Indie", "RPG"]
    if g in all_single_genres
] or all_single_genres[:5]

selected_genres = st.sidebar.multiselect(
    "Genre Game", options=all_single_genres, default=default_selection
)

cap_price = 1500000.0
selected_price = st.sidebar.slider(
    "Harga Maksimal Rp",
    min_value=0.0,
    max_value=cap_price,
    value=cap_price,
    step=50000.0,
)

filtered_df = df[
    (df["release_year"] >= selected_years[0])
    & (df["release_year"] <= selected_years[1])
    & (df["price_idr"] <= selected_price)
    & (
        df["genre_list"].apply(
            lambda g_list: any(g in selected_genres for g in g_list)
        )
    )
].copy()

if filtered_df.empty:
  st.warning("Tidak ada data yang sesuai filter.")
  st.stop()

# ==============================================================================
# 5. METRIK UTAMA
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Game", f"{len(filtered_df):,}")
col2.metric("Rata-rata Rekomendasi", f"{filtered_df['recommendations'].mean():,.0f}")
col3.metric("Rata-rata Harga", f"Rp {filtered_df['price_idr'].mean():,.0f}")
col4.metric("Median Harga", f"Rp {filtered_df['price_idr'].median():,.0f}")

st.markdown("---")

# ==============================================================================
# 6. TABEL STATISTIKA DESKRIPTIF
# ==============================================================================
st.subheader("📑 Ringkasan Statistika Deskriptif")


def build_summary_table(df_input):
  p = df_input["price_idr"]
  r = df_input["recommendations"]

  metrics_data = [
      {
          "Ukuran Statistika": "Mean",
          "Harga Rp": f"Rp {p.mean():,.0f}",
          "Rekomendasi": f"{r.mean():,.0f}",
      },
      {
          "Ukuran Statistika": "Standar Deviasi",
          "Harga Rp": f"Rp {p.std():,.0f}",
          "Rekomendasi": f"{r.std():,.0f}",
      },
      {
          "Ukuran Statistika": "Q1",
          "Harga Rp": f"Rp {p.quantile(0.25):,.0f}",
          "Rekomendasi": f"{r.quantile(0.25):,.0f}",
      },
      {
          "Ukuran Statistika": "Median",
          "Harga Rp": f"Rp {p.median():,.0f}",
          "Rekomendasi": f"{r.median():,.0f}",
      },
      {
          "Ukuran Statistika": "Q3",
          "Harga Rp": f"Rp {p.quantile(0.75):,.0f}",
          "Rekomendasi": f"{r.quantile(0.75):,.0f}",
      },
      {
          "Ukuran Statistika": "IQR",
          "Harga Rp": f"Rp {p.quantile(0.75) - p.quantile(0.25):,.0f}",
          "Rekomendasi": f"{r.quantile(0.75) - r.quantile(0.25):,.0f}",
      },
      {
          "Ukuran Statistika": "Minimum",
          "Harga Rp": f"Rp {p.min():,.0f}",
          "Rekomendasi": f"{p.min():,.0f}",
      },
      {
          "Ukuran Statistika": "Maksimum",
          "Harga Rp": f"Rp {p.max():,.0f}",
          "Rekomendasi": f"{r.max():,.0f}",
      },
  ]
  return pd.DataFrame(metrics_data)


summary_table = build_summary_table(filtered_df)
st.dataframe(summary_table, use_container_width=True, hide_index=True)

st.markdown("---")

# ==============================================================================
# 7. VISUALISASI BOXPLOT
# ==============================================================================
st.subheader("📦 Distribusi Data dan Outlier")

col_box1, col_box2 = st.columns(2)

with col_box1:
  fig_b1 = px.box(
      filtered_df,
      y="price_idr",
      title="Distribusi Harga Game",
      labels={"price_idr": "Harga Rp"},
      points=False,
      color_discrete_sequence=["#00B4D8"],
  )
  fig_b1.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
  st.plotly_chart(fig_b1, use_container_width=True)

with col_box2:
  fig_b2 = px.box(
      filtered_df,
      y="recommendations",
      title="Distribusi Rekomendasi Skala Logaritmik",
      labels={"recommendations": "Rekomendasi"},
      points=False,
      color_discrete_sequence=["#7209B7"],
  )
  fig_b2.update_yaxes(type="log")
  fig_b2.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
  st.plotly_chart(fig_b2, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 8. TREN & TOP GENRE
# ==============================================================================
col_g1, col_g2 = st.columns(2)

with col_g1:
  st.subheader("📈 Tren Rekomendasi per Tahun")
  yearly_rec = (
      filtered_df.groupby("release_year")["recommendations"]
      .mean()
      .reset_index()
  )
  fig_line = px.line(
      yearly_rec,
      x="release_year",
      y="recommendations",
      markers=True,
      title="Rerata Rekomendasi per Tahun",
      labels={"release_year": "Tahun", "recommendations": "Rerata Rekomendasi"},
      color_discrete_sequence=["#4CC9F0"],
  )
  fig_line.update_layout(height=380)
  st.plotly_chart(fig_line, use_container_width=True)

with col_g2:
  st.subheader("📊 Top 10 Genre Terpopuler")
  exploded_df = filtered_df.explode("genre_list")
  exploded_df = exploded_df[exploded_df["genre_list"].isin(selected_genres)]

  genre_rec = (
      exploded_df.groupby("genre_list")["recommendations"]
      .mean()
      .reset_index()
      .sort_values(by="recommendations", ascending=False)
      .head(10)
  )

  fig_bar = px.bar(
      genre_rec,
      x="genre_list",
      y="recommendations",
      title="Rerata Rekomendasi per Genre",
      labels={"genre_list": "Genre", "recommendations": "Rerata Rekomendasi"},
      color="recommendations",
      color_continuous_scale="Blues",
  )
  fig_bar.update_layout(height=380, showlegend=False)
  st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 9. KORELASI
# ==============================================================================
st.subheader("🔍 Korelasi Harga dan Rekomendasi")

col_corr1, col_corr2 = st.columns([2.5, 1])

with col_corr1:
  filtered_df["primary_genre"] = filtered_df["genre_list"].apply(
      lambda x: x[0] if len(x) > 0 else "Uncategorized"
  )

  fig_scatter = px.scatter(
      filtered_df,
      x="price_idr",
      y="recommendations",
      color="primary_genre",
      hover_data=["name", "release_year"],
      title="Harga vs Rekomendasi",
      labels={
          "price_idr": "Harga Rp",
          "recommendations": "Rekomendasi",
          "primary_genre": "Genre Utama",
      },
      opacity=0.7,
  )
  fig_scatter.update_layout(height=420)
  st.plotly_chart(fig_scatter, use_container_width=True)

with col_corr2:
  st.markdown("#### Koefisien Korelasi")

  corr_pearson = filtered_df["price_idr"].corr(
      filtered_df["recommendations"], method="pearson"
  )
  corr_spearman = (
      filtered_df["price_idr"]
      .rank()
      .corr(filtered_df["recommendations"].rank())
  )

  st.metric("Pearson r", f"{corr_pearson:.4f}")
  st.metric("Spearman rho", f"{corr_spearman:.4f}")

st.markdown("---")

# ==============================================================================
# 10. TABEL DATASET
# ==============================================================================
with st.expander("📄 Data Terfilter"):
  st.dataframe(
      filtered_df[[
          "appid",
          "name",
          "release_year",
          "genre_list",
          "price_idr",
          "recommendations",
          "developer",
      ]],
      use_container_width=True,
      hide_index=True,
  )