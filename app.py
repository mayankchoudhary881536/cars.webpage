import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Car Analytics",
    page_icon="Car",
    layout="wide"
)


# ============================================================
# LOAD CSV FILE
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Cars.csv")

    return df


df = load_data()


# ============================================================
# BASIC DATA CLEANING
# ============================================================

# Remove duplicate rows
df = df.drop_duplicates()


# ------------------------------------------------------------
# Convert important columns to numeric
# ------------------------------------------------------------

numeric_columns = [
    "Year",
    "Kilometers_Driven",
    "Price",
    "Seats"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


# ------------------------------------------------------------
# Convert Mileage
# ------------------------------------------------------------

if "Mileage" in df.columns:

    df["Mileage"] = (
        df["Mileage"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
    )

    df["Mileage"] = pd.to_numeric(
        df["Mileage"],
        errors="coerce"
    )


# ------------------------------------------------------------
# Convert Engine
# ------------------------------------------------------------

if "Engine" in df.columns:

    df["Engine"] = (
        df["Engine"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
    )

    df["Engine"] = pd.to_numeric(
        df["Engine"],
        errors="coerce"
    )


# ------------------------------------------------------------
# Convert Power
# ------------------------------------------------------------

if "Power" in df.columns:

    df["Power"] = (
        df["Power"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
    )

    df["Power"] = pd.to_numeric(
        df["Power"],
        errors="coerce"
    )


# ============================================================
# CREATE COMPANY NAME IF NOT AVAILABLE
# ============================================================

if "Company_name" not in df.columns:

    if "Name" in df.columns:

        df["Company_name"] = (
            df["Name"]
            .astype(str)
            .str.split()
            .str[0]
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Car Analytics")

st.sidebar.write(
    "Vehicle Data Analysis"
)

st.sidebar.divider()


menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Market Analysis",
        "Vehicle Analysis",
        "Data Explorer",
        "Data Quality",
        "About Dataset"
    ]
)


st.sidebar.divider()


# ============================================================
# SIDEBAR DATA INFORMATION
# ============================================================

st.sidebar.subheader(
    "Dataset Information"
)

st.sidebar.metric(
    "Rows",
    f"{df.shape[0]:,}"
)

st.sidebar.metric(
    "Columns",
    df.shape[1]
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.title("Car Analytics")

    st.write(
        "Vehicle Data Analysis Dashboard"
    )

    st.divider()


    # ========================================================
    # KPI SECTION
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    # Total vehicles
    with col1:

        st.metric(
            "Total Vehicles",
            f"{len(df):,}"
        )


    # Average price
    with col2:

        if "Price" in df.columns:

            avg_price = df["Price"].mean()

            st.metric(
                "Average Price",
                f"{avg_price:.2f}"
            )

        else:

            st.metric(
                "Average Price",
                "N/A"
            )


    # Maximum price
    with col3:

        if "Price" in df.columns:

            max_price = df["Price"].max()

            st.metric(
                "Maximum Price",
                f"{max_price:.2f}"
            )

        else:

            st.metric(
                "Maximum Price",
                "N/A"
            )


    # Companies
    with col4:

        if "Company_name" in df.columns:

            companies = df[
                "Company_name"
            ].nunique()

            st.metric(
                "Companies",
                companies
            )

        else:

            st.metric(
                "Companies",
                "N/A"
            )


    st.divider()


    # ========================================================
    # COMPANY + PRICE CHART
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # TOP COMPANIES
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "Top Car Companies"
        )

        if "Company_name" in df.columns:

            company_count = (
                df["Company_name"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            company_count.columns = [
                "Company",
                "Number of Cars"
            ]


            fig = px.bar(
                company_count,
                x="Company",
                y="Number of Cars",
                color="Number of Cars",
                color_continuous_scale="Turbo",
                title="Top 10 Car Companies"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        else:

            st.warning(
                "Company information is not available."
            )


    # --------------------------------------------------------
    # PRICE DISTRIBUTION
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "Price Distribution"
        )


        if "Price" in df.columns:

            price_data = df[
                "Price"
            ].dropna()


            fig = px.histogram(
                price_data,
                x="Price",
                nbins=30,
                color_discrete_sequence=[
                    "#636EFA"
                ],
                title="Distribution of Car Prices"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        else:

            st.warning(
                "Price column is not available."
            )


    st.divider()


    # ========================================================
    # YEAR DISTRIBUTION
    # ========================================================

    if "Year" in df.columns:

        st.subheader(
            "Cars by Manufacturing Year"
        )


        year_count = (
            df["Year"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )


        year_count.columns = [
            "Year",
            "Number of Cars"
        ]


        fig = px.bar(
            year_count,
            x="Year",
            y="Number of Cars",
            color="Number of Cars",
            color_continuous_scale="Viridis",
            title="Number of Cars by Year"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# MARKET ANALYSIS
# ============================================================

elif menu == "Market Analysis":

    st.title(
        "Market Analysis"
    )

    st.write(
        "Explore car prices and company-level market information."
    )

    st.divider()


    # ========================================================
    # PRICE METRICS
    # ========================================================

    if "Price" in df.columns:

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Average Price",
                f"{df['Price'].mean():.2f}"
            )


        with col2:

            st.metric(
                "Minimum Price",
                f"{df['Price'].min():.2f}"
            )


        with col3:

            st.metric(
                "Maximum Price",
                f"{df['Price'].max():.2f}"
            )


        with col4:

            st.metric(
                "Median Price",
                f"{df['Price'].median():.2f}"
            )


        st.divider()


    # ========================================================
    # AVERAGE PRICE BY COMPANY
    # ========================================================

    if (
        "Company_name" in df.columns
        and
        "Price" in df.columns
    ):

        st.subheader(
            "Average Price by Company"
        )


        company_price = (
            df.groupby("Company_name")["Price"]
            .mean()
            .sort_values(
                ascending=False
            )
            .head(15)
            .reset_index()
        )


        fig = px.bar(
            company_price,
            x="Company_name",
            y="Price",
            color="Price",
            color_continuous_scale="Plasma",
            title="Average Price of Top Companies"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.divider()


        # ====================================================
        # BOX PLOT
        # ====================================================

        st.subheader(
            "Price Distribution by Company"
        )


        box_data = df[
            [
                "Company_name",
                "Price"
            ]
        ].dropna()


        # Limit to top companies for readability
        top_companies = (
            box_data["Company_name"]
            .value_counts()
            .head(15)
            .index
        )


        box_data = box_data[
            box_data["Company_name"]
            .isin(top_companies)
        ]


        fig = px.box(
            box_data,
            x="Company_name",
            y="Price",
            color="Company_name",
            title="Price Distribution"
        )


        fig.update_layout(
            showlegend=False
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# VEHICLE ANALYSIS
# ============================================================

elif menu == "Vehicle Analysis":

    st.title(
        "Vehicle Analysis"
    )

    st.write(
        "Analyze relationships between different vehicle parameters."
    )

    st.divider()


    # ========================================================
    # GET NUMERICAL COLUMNS
    # ========================================================

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()


    if len(numeric_cols) >= 2:


        # ====================================================
        # AXIS SELECTION
        # ====================================================

        col1, col2 = st.columns(2)


        with col1:

            x_axis = st.selectbox(
                "Select X-axis",
                numeric_cols
            )


        with col2:

            default_y = 1

            if (
                "Kilometers_Driven" in numeric_cols
                and
                x_axis != "Kilometers_Driven"
            ):

                default_y = numeric_cols.index(
                    "Kilometers_Driven"
                )


            y_axis = st.selectbox(
                "Select Y-axis",
                numeric_cols,
                index=default_y
            )


        st.divider()


        # ====================================================
        # IMPORTANT:
        # REMOVE NaN VALUES
        # ====================================================

        plot_columns = [
            x_axis,
            y_axis
        ]


        if "Price" in df.columns:

            plot_columns.append(
                "Price"
            )


        plot_df = df[
            plot_columns
        ].dropna()


        # ====================================================
        # SCATTER PLOT
        # ====================================================

        st.subheader(
            f"{y_axis} vs {x_axis}"
        )


        if (
            "Price" in plot_df.columns
            and
            x_axis != "Price"
            and
            y_axis != "Price"
        ):

            fig = px.scatter(
                plot_df,
                x=x_axis,
                y=y_axis,
                color="Price",
                color_continuous_scale="Turbo",
                hover_data=plot_df.columns,
                title=f"{y_axis} vs {x_axis}"
            )


        else:

            fig = px.scatter(
                plot_df,
                x=x_axis,
                y=y_axis,
                title=f"{y_axis} vs {x_axis}"
            )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ====================================================
        # CORRELATION
        # ====================================================

        if x_axis != y_axis:

            correlation = plot_df[
                [
                    x_axis,
                    y_axis
                ]
            ].corr().iloc[0, 1]


            st.subheader(
                "Correlation Analysis"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Correlation Coefficient",
                    f"{correlation:.3f}"
                )


            with col2:

                st.write(
                    "Correlation ranges from -1 to +1."
                )


            if correlation > 0:

                st.info(
                    "The variables have a positive correlation."
                )

            elif correlation < 0:

                st.info(
                    "The variables have a negative correlation."
                )

            else:

                st.info(
                    "The variables have approximately no linear correlation."
                )


    else:

        st.warning(
            "There are not enough numerical columns for analysis."
        )


# ============================================================
# DATA EXPLORER
# ============================================================

elif menu == "Data Explorer":

    st.title(
        "Data Explorer"
    )

    st.write(
        "Search, filter and explore the complete dataset."
    )

    st.divider()


    # ========================================================
    # SEARCH
    # ========================================================

    search = st.text_input(
        "Search in dataset",
        placeholder="Enter company, model, location, etc."
    )


    filtered_df = df.copy()


    if search:

        mask = filtered_df.astype(
            str
        ).apply(
            lambda row: row.str.contains(
                search,
                case=False,
                na=False
            ).any(),
            axis=1
        )


        filtered_df = filtered_df[
            mask
        ]


    # ========================================================
    # RESULT COUNT
    # ========================================================

    st.write(
        f"Showing {len(filtered_df):,} rows"
    )


    # ========================================================
    # DATA TABLE
    # ========================================================

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600
    )


# ============================================================
# DATA QUALITY
# ============================================================

elif menu == "Data Quality":

    st.title(
        "Data Quality"
    )

    st.write(
        "Check missing values, duplicates and column information."
    )

    st.divider()


    # ========================================================
    # DATA QUALITY METRICS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Rows",
            f"{df.shape[0]:,}"
        )


    with col2:

        st.metric(
            "Columns",
            df.shape[1]
        )


    with col3:

        st.metric(
            "Duplicate Rows",
            df.duplicated().sum()
        )


    with col4:

        total_missing = (
            df.isnull()
            .sum()
            .sum()
        )


        st.metric(
            "Missing Values",
            f"{total_missing:,}"
        )


    st.divider()


    # ========================================================
    # MISSING VALUES
    # ========================================================

    st.subheader(
        "Missing Values"
    )


    missing = (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )


    missing_df = (
        missing
        .reset_index()
    )


    missing_df.columns = [
        "Column",
        "Missing Values"
    ]


    missing_df = missing_df[
        missing_df[
            "Missing Values"
        ] > 0
    ]


    if len(missing_df) > 0:


        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing Values",
            color="Missing Values",
            color_continuous_scale="Reds",
            title="Missing Values by Column"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            missing_df,
            use_container_width=True
        )


    else:

        st.success(
            "No missing values found."
        )


    st.divider()


    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    st.subheader(
        "Column Information"
    )


    info_df = pd.DataFrame({

        "Column":
            df.columns,

        "Data Type":
            df.dtypes.astype(str),

        "Missing Values":
            df.isnull().sum().values,

        "Unique Values":
            df.nunique().values

    })


    st.dataframe(
        info_df,
        use_container_width=True
    )


# ============================================================
# ABOUT DATASET
# ============================================================

elif menu == "About Dataset":

    st.title(
        "About Dataset"
    )

    st.write(
        "Information and statistical summary of the Cars dataset."
    )

    st.divider()


    # ========================================================
    # DATASET SIZE
    # ========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Rows",
            f"{df.shape[0]:,}"
        )


    with col2:

        st.metric(
            "Columns",
            df.shape[1]
        )


    with col3:

        st.metric(
            "Duplicate Rows",
            df.duplicated().sum()
        )


    st.divider()


    # ========================================================
    # NUMERICAL COLUMNS
    # ========================================================

    st.subheader(
        "Numerical Columns"
    )


    numerical_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()


    st.write(
        numerical_columns
    )


    st.divider()


    # ========================================================
    # DATASET PREVIEW
    # ========================================================

    st.subheader(
        "Dataset Preview"
    )


    st.dataframe(
        df.head(20),
        use_container_width=True
    )


    st.divider()


    # ========================================================
    # STATISTICAL SUMMARY
    # ========================================================

    st.subheader(
        "Statistical Summary"
    )


    st.dataframe(
        df.describe(),
        use_container_width=True
    )