import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="YouTube Analytics Pro",
    page_icon="🎥",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------
st.markdown("""
<style>

[data-testid="stSidebar"]{
    background-color:#111827;
}

.metric-card{
    background: linear-gradient(135deg,#1e293b,#0f172a);
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 0 12px rgba(59,130,246,0.3);
}

.metric-title{
    color:#94a3b8;
    font-size:15px;
}

.metric-value{
    color:white;
    font-size:28px;
    font-weight:bold;
}

.insight-box{
    background:#1e293b;
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
}

.block-container{
    padding-top:1rem;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("youtube_data_1000.csv")
    df["views"] = df["views"].fillna(df["views"].median())
    df["likes"] = df["likes"].fillna(df["likes"].median())
    df["comments"] = df["comments"].fillna(df["comments"].median())
    df["duration"] = df["duration"].fillna(df["duration"].median())

    df = df.drop_duplicates()


    df["upload_time"] = pd.to_datetime(df["upload_time"])

    df["hour"] = df["upload_time"].dt.hour
    df["day"] = df["upload_time"].dt.day_name()
    df["month"] = df["upload_time"].dt.strftime("%b")

    df["engagement_rate"] = (
        (df["likes"] + df["comments"])
        / df["views"]
    )

    return df

df = load_data()

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------
with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1384/1384060.png",
        width=80
    )
    selected = option_menu(
    menu_title="Navigation",
    options=[
        "Dashboard",
        "Analytics",
        "Insights",
        "Project Summary"
    ],
    icons=[
        "speedometer2",
        "graph-up",
        "lightbulb",
        "file-earmark-text"
    ],
    default_index=0
)
    st.markdown("---")

    st.subheader("🎯 Filters")

    category = st.selectbox(
        "Category",
        ["All"] + sorted(df["category"].unique())
    )

    min_views = int(df["views"].min())
    max_views = int(df["views"].max())

    view_range = st.slider(
        "Views Range",
        min_views,
        max_views,
        (min_views, max_views)
    )

# ------------------------------------------------
# FILTER DATA
# ------------------------------------------------
filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

filtered_df = filtered_df[
    (filtered_df["views"] >= view_range[0]) &
    (filtered_df["views"] <= view_range[1])
]

# ------------------------------------------------
# HERO SECTION
# ------------------------------------------------
st.markdown("""
<div style="
background:linear-gradient(
90deg,
#2563eb,
#7c3aed
);
padding:25px;
border-radius:20px;
text-align:center;
margin-bottom:20px;
">

<h1 style="
color:white;
margin:0;
">
🎥 YouTube Analytics Pro
</h1>

<p style="
color:white;
font-size:18px;
">
AI-Powered Video Performance Dashboard
</p>

</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# KPI SECTION
# ------------------------------------------------
total_videos = len(filtered_df)
total_views = filtered_df["views"].sum()
total_likes = filtered_df["likes"].sum()
avg_engagement = filtered_df["engagement_rate"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🎬 Total Videos</div>
        <div class="metric-value">{total_videos:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">👀 Total Views</div>
        <div class="metric-value">{total_views:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">👍 Total Likes</div>
        <div class="metric-value">{total_likes:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🔥 Engagement</div>
        <div class="metric-value">{avg_engagement:.2%}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


best_category = (
    filtered_df.groupby("category")["views"]
    .mean()
    .idxmax()
)

best_hour = (
    filtered_df.groupby("hour")["views"]
    .mean()
    .idxmax()
)

top_video = (
    filtered_df.sort_values(
        "views",
        ascending=False
    )
    .iloc[0]
)
highest_month = (
    filtered_df.groupby("month")["views"]
    .mean()
    .idxmax()
)

st.markdown("### 📌 Executive Summary")

e1,e2,e3,e4 = st.columns(4)

e1.info(f"🏆 Best Category\n\n{best_category}")
e2.success(f"⏰ Best Upload Hour\n\n{best_hour}:00")
e3.warning(f"🔥 Avg Engagement\n\n{avg_engagement:.2%}")
e4.error(f"🎬 Top Video\n\n{top_video['title']}")

# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------
if selected == "Dashboard":

    col1, col2 = st.columns(2)

    with col1:

        category_views = (
            filtered_df
            .groupby("category")["views"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            category_views,
            x="category",
            y="views",
            color="views",
            title="📺 Category Performance",
            template="plotly_dark",
            text_auto=".2s"
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        hourly_views = (
            filtered_df
            .groupby("hour")["views"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            hourly_views,
            x="hour",
            y="views",
            markers=True,
            title="⏰ Upload Time Analysis",
            template="plotly_dark"
        )

        fig.update_layout(height=500)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==========================
    # Leaderboard
    # ==========================

    st.markdown("---")

    st.subheader("🥇 Category Leaderboard")

    leaderboard = (
        filtered_df.groupby("category")["views"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    leaderboard.columns = [
        "Category",
        "Average Views"
    ]

    st.dataframe(
        leaderboard,
        use_container_width=True
    )
    st.markdown("---")

    st.subheader("📋 Data Quality Report")

    c1,c2,c3 = st.columns(3)

    c1.metric(
    "Missing Values",
    int(df.isnull().sum().sum())
)

    c2.metric(
    "Duplicate Rows",
    int(df.duplicated().sum())
)

    c3.metric(
    "Total Records",
    len(df)
)

    # ==========================
    # Monthly Trend
    # ==========================

    st.markdown("---")

    monthly_views = (
        filtered_df.groupby("month")["views"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        monthly_views,
        x="month",
        y="views",
        markers=True,
        title="📅 Monthly Views Trend",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    day_views = (
    filtered_df.groupby("day")["views"]
    .mean()
    .reset_index()
)

    fig = px.bar(
    day_views,
    x="day",
    y="views",
    title="📅 Best Upload Day",
    template="plotly_dark"
)

    st.plotly_chart(
    fig,
    use_container_width=True
)
    
# ------------------------------------------------
# ANALYTICS
# ------------------------------------------------
elif selected == "Analytics":

    col1, col2 = st.columns(2)

    with col1:

        fig = px.scatter(
            filtered_df,
            x="views",
            y="likes",
            size="comments",
            color="category",
            hover_name="title",
            title="📈 Views vs Likes",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.scatter(
            filtered_df,
            x="duration",
            y="engagement_rate",
            color="category",
            title="⏱ Duration vs Engagement",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    with col3:

        fig = px.pie(
            filtered_df,
            names="category",
            title="📊 Category Distribution",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col4:

        monthly_views = (
            filtered_df.groupby("month")["views"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            monthly_views,
            x="month",
            y="views",
            markers=True,
            title="📅 Monthly Trend",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("🔥 Correlation Heatmap")

    corr = filtered_df[
        [
            "views",
            "likes",
            "comments",
            "duration",
            "engagement_rate"
        ]
    ].corr()

    heatmap = ff.create_annotated_heatmap(
        z=corr.values,
        x=list(corr.columns),
        y=list(corr.index),
        annotation_text=round(corr,2).values,
        showscale=True
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )
# ------------------------------------------------
# INSIGHTS
# ------------------------------------------------
elif selected == "Insights":

    left, right = st.columns([2, 1])

    with left:

        st.subheader("🏆 Top 10 Videos")

        top_videos = (
            filtered_df
            .sort_values(
                "views",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top_videos[
                [
                    "title",
                    "category",
                    "views",
                    "likes",
                    "comments",
                    "engagement_rate"
                ]
            ],
            use_container_width=True
        )
        highest_month = (
    filtered_df.groupby("month")["views"]
    .mean()
    .idxmax()
)

    with right:

        st.subheader("🤖 AI Insights")

        best_category = (
            filtered_df
            .groupby("category")["views"]
            .mean()
            .idxmax()
        )

        best_hour = (
            filtered_df
            .groupby("hour")["views"]
            .mean()
            .idxmax()
        )

        st.markdown(
            f"""
            <div class="insight-box">
            🏆 Best Category:<br>
            <b>{best_category}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
            ⏰ Best Upload Hour:<br>
            <b>{best_hour}:00</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="insight-box">
            🔥 Higher engagement videos
            generally receive more views.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="insight-box">
            📈 Consistent posting improves
            overall channel performance.
            </div>
            """,
            unsafe_allow_html=True
        )
       
        st.markdown(
            f"""
            <div class="insight-box">
            📅 Highest Performing Month:<br>
            <b>{highest_month}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
            🎬 Top Video:<br>
            <b>{top_video['title']}</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        engagement_category = (
            filtered_df.groupby("category")["engagement_rate"]
            .mean()
            .idxmax()
        )

        st.markdown(
            f"""
            <div class="insight-box">
            🚀 Highest Engagement Category:<br>
            <b>{engagement_category}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        avg_duration = filtered_df["duration"].mean()

        st.markdown(
            f"""
            <div class="insight-box">
            🎥 Average Video Duration:<br>
            <b>{avg_duration:.0f} seconds</b>
            </div>
            """,
            unsafe_allow_html=True
        )

 # ------------------------------------------------
# PROJECT SUMMARY
# ------------------------------------------------
elif selected == "Project Summary":

    st.header("📄 Project Overview")

    st.markdown("""
    ### 🎯 Project Objective

    Analyze YouTube video performance data to identify
    factors influencing video popularity and engagement.

    The project helps content creators understand:

    - Best upload timing
    - Top performing categories
    - Engagement patterns
    - Content performance trends
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🛠 Technologies Used")

        st.markdown("""
        - Python
        - Pandas
        - Streamlit
        - Plotly
        - NumPy
        """)

    with col2:

        st.subheader("📊 Dataset Information")

        st.markdown(f"""
        - Total Records: **{len(df):,}**
        - Categories: **{df['category'].nunique()}**
        - Features: **{len(df.columns)}**
        - Data Type: **Structured CSV**
        """)

    st.markdown("---")

    st.subheader("⚙️ Project Workflow")

    st.markdown("""
    1. Data Collection
    2. Data Cleaning
    3. Feature Engineering
    4. Exploratory Data Analysis
    5. Trend Analysis
    6. Insight Generation
    7. Dashboard Development
    """)

    st.markdown("---")

    st.subheader("📈 Key Findings")

    st.success(
        f"🏆 Best Performing Category: {best_category}"
    )

    st.success(
        f"⏰ Best Upload Hour: {best_hour}:00"
    )

    st.success(
        f"📅 Highest Performing Month: {highest_month}"
    )

    st.success(
        f"🎬 Top Video: {top_video['title']}"
    )

    st.markdown("---")

    st.subheader("💼 Business Impact")

    st.info("""
    • Helps content creators optimize upload schedules.

    • Identifies categories generating maximum views.

    • Supports data-driven content strategy.

    • Improves audience engagement and channel growth.
    """)
# ------------------------------------------------
# DOWNLOAD
# ------------------------------------------------
st.markdown("---")

csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "youtube_report.csv",
    "text/csv"
)

st.markdown(
    """
    <hr>
    <center>
        <h4>🎥 YouTube Analytics Pro</h4>
        <p>
        Built with Python • Pandas • Plotly • Streamlit
        </p>
    </center>
    """,
    unsafe_allow_html=True
)