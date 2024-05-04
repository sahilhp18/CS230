"""
Name: Sahil Patel
CS230: Section 6
Data: starbucks.csv
URL: not yet posted
Description:
This program is a web application designed to analyze and visualize Starbucks store locations globally.
It loads data from a CSV file and employs pandas for data manipulation, matplotlib and seaborn for creating various types
of charts, and folium for geographical mapping. The user interface, organized into tabs, allows for interactive data exploration
through cleaning processes, generating descriptive statistics, and viewing multiple visualizations. These include histograms,
bar plots, scatter plots, box plots, and more, tailored to reveal insights about store distributions, timezone offsets,
and store characteristics by country. Additional interactivity is provided through sidebar widgets that let users control
which data and visualizations are displayed, enhancing user engagement with dynamic content exploration.
"""


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


# Load the CSV file to understand the data
data = pd.read_csv('starbucks.csv')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    page_title="Your Streamlit App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("<h1 style='text-align: center; color:green; font-family: Times New Roman, Times, serif; white-space: nowrap;'>Starbucks Store Locations Analysis</h1>", unsafe_allow_html=True)
st.markdown("""<h1 style='text-align: center; font-family: "Times New Roman", Times, serif; white-space: nowrap; font-size: 16px;'>This web app visualizes data of Starbucks locations around the world.</h1>""", unsafe_allow_html=True)

# [ST4]: SIDEBAR LOGO
st.sidebar.image("1020x1024.png", width=280)

# Giphy
st.markdown("""
    <div style='text-align: center'>
        <img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGwxdGN4a21tZXNlOHZrNmg5YWlyZG5lb2N3NXpqZmtwNzMzYnlkeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gw3JcFhu2YiUDOG4/giphy.gif' width='350'>
    </div>
""", unsafe_allow_html=True)


# Helper functions for data processing and visualization
def display_top_stores(country_code, n):
    top_stores = filter_sort_top_stores(data, country_code, n)
    return top_stores[['Name', 'CountryCode', 'Longitude', 'Latitude']]


# [VIZ4]: Map
def plot_store_locations(dataframe):
    # Rename the columns to comply with Streamlit's expectations
    dataframe = dataframe.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

    # Drop rows where 'lat' or 'lon' is null to avoid StreamlitAPIException
    dataframe = dataframe.dropna(subset=['lat', 'lon'])
    # Create a map using the renamed columns
    st.map(dataframe[['lat', 'lon']])


# [PY3] -> Visualization: Plotting charts
def plot_charts(dataframe):
    # Example: Plotting a histogram of Timezone Offsets
    fig, ax = plt.subplots()
    ax.hist(dataframe['TimezoneOffset'], bins=20)
    ax.set_title('Histogram of Timezone Offsets')
    ax.set_xlabel('Timezone Offset')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)


# Set the Seaborn theme
sns.set_theme(style="whitegrid")


# Visualization of store counts by country code
def plot_store_counts(dataframe):
    plt.figure(figsize=(10, 6))
    store_counts = dataframe['CountryCode'].value_counts().head(10)  # Top 10 countries
    # Update to the correct syntax for seaborn barplot
    sns.barplot(x=store_counts.index, y=store_counts.values, palette="coolwarm") # [VIZ2]
    plt.title('Top 10 Countries by Number of Starbucks Stores')
    plt.xlabel('Country Code')
    plt.ylabel('Number of Stores')
    st.pyplot(plt.gcf())


# Visualization: Scatter plot of Stores by Longitude and Latitude
def plot_longitude_latitude_scatter(dataframe, country_code):
    plt.figure(figsize=(10, 6))
    country_data = dataframe[dataframe['CountryCode'] == country_code]
    sns.scatterplot(data=country_data, x='Longitude', y='Latitude', hue='OwnershipType', palette="muted")
    plt.title(f'Starbucks Stores Location Scatter Plot for {country_code}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    st.pyplot(plt.gcf())


# Visualization: Boxplot of Timezone Offset by Country Code
def plot_timezone_offset_boxplot(dataframe):
    plt.figure(figsize=(40, 25))
    sns.boxplot(x='CountryCode', y='TimezoneOffset', data=dataframe, palette="pastel")
    plt.title('Timezone Offset by Country Code')
    plt.xlabel('Country Code')
    plt.ylabel('Timezone Offset')
    st.pyplot(plt.gcf())


def hexbin_with_marginals(dataframe, x_var, y_var):
    g = sns.jointplot(x=x_var, y=y_var, data=dataframe, kind="hex", color="skyblue", marginal_kws=dict(bins=30, fill=True))
    g.set_axis_labels('Longitude', 'Latitude', fontsize=12)
    g.fig.suptitle('Hexbin Plot with Marginal Distributions')
    st.pyplot(g.fig)


# Violinplot from a wide-form dataset
def wide_form_violinplot(dataframe, columns):
    plt.figure(figsize=(10, 6))
    # Simulate wide-form data by taking a sample for the demonstration
    wide_form_data = dataframe[columns].sample(n=50, random_state=42)
    sns.violinplot(data=wide_form_data, palette="light:g", inner="points", orient="h")
    plt.title('Violin Plot for Multiple Distributions')
    st.pyplot(plt.gcf())

# [PY1]: Two parameters with default values
def filter_sort_top_stores(dataframe, country_code='US', n=5):
    # Filter the stores by country code
    filtered_stores = dataframe[dataframe['CountryCode'] == country_code]

    # Sort the filtered stores by longitude
    sorted_stores = filtered_stores.sort_values(by='Longitude', ascending=True) # [DA2]

    # Return the top N stores with the highest latitude
    top_stores = sorted_stores.nlargest(n, 'Latitude') # [DA3]

    return top_stores


# Create tabs
tab1, tab2, tab3 = st.tabs(["Data Cleaning and Display", "Store Analysis", "Visualizations"])
# [PY4]
with tab1:
    st.markdown("""
            <h1 style='text-align: center; color: green; font-family: "Times New Roman", Times, serif;'>
                Data Cleaning and Display
            </h1>
            """, unsafe_allow_html=True)
    # Data cleaning steps
    data_cleaned = data.drop_duplicates()
    numeric_columns = data_cleaned.select_dtypes(include=['float64', 'int64']).columns
    data_cleaned[numeric_columns] = data_cleaned[numeric_columns].fillna(data_cleaned[numeric_columns].mean())
    categorical_columns = data_cleaned.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        mode = data_cleaned[column].mode()[0]
        data_cleaned[column] = data_cleaned[column].fillna(mode)
    missing_data_after_cleaning = data_cleaned.isnull().sum()
    st.write(data_cleaned.head())
    st.write("Missing data after cleaning:", missing_data_after_cleaning)

    # Displaying Descriptive Statistics
    st.markdown("<h2 style='color: green; font-family: Times New Roman, Times, serif;'>Descriptive Statistics</h2>", unsafe_allow_html=True)
    # Calculate descriptive statistics
    descriptive_stats = data_cleaned.describe()
    # Display descriptive statistics
    st.table(descriptive_stats)

with tab2:
    st.markdown("""
            <h1 style='text-align: center; color: green; font-family: "Times New Roman", Times, serif;'>
                Store Analysis
            </h1>
            """, unsafe_allow_html=True)
    # [ST1],[ST2],[ST3]: Widgets for selecting parameters
    country_code = st.selectbox('Select a Country Code', data['CountryCode'].unique(), key='country_code_select') # [DA4]
    n_stores = st.slider('Number of Stores to Display', min_value=1, max_value=10, value=5, key='n_stores_slider')
    if st.button('Show Top Stores', key='show_top_stores_tab2'):
        top_stores_df = display_top_stores(country_code, n_stores)
        st.write(top_stores_df)
    if st.checkbox("Show Random Sample", False):
        st.subheader("Random Sample of Starbucks Locations")
        st.write(data.sample(5))

with tab3:
    st.markdown("""
            <h1 style='text-align: center; color: green; font-family: "Times New Roman", Times, serif;'>
                Visualizations
            </h1>
            """, unsafe_allow_html=True)
    if st.sidebar.checkbox('Show Histogram of Timezone offsets', key='show_charts'):
        st.write("Histogram of Timezone offsets") # [VIZ1]
        plot_charts(data)
        st.write("This histogram displays the distribution of timezone offsets for Starbucks store locations. The graph shows that the most common timezone offsets are around -400 and 800, with significant frequencies also observed around -600 and 200, indicating a global spread of store locations across various time zones.")

    if st.sidebar.checkbox('Show Map of Stores', key='show_map'):
        st.write("Map of Stores")
        plot_store_locations(data) # [DA7]
        st.write("This map visualizes the global distribution of Starbucks stores, highlighted in red dots across the continents. The concentration of stores is particularly dense in North America and East Asia, reflecting the market penetration of Starbucks in these regions.")

    if st.sidebar.checkbox('Show Store Counts Chart', key='show_store_counts_chart'):
        st.write("Store Counts Chart")
        plot_store_counts(data)
        st.write("This bar chart illustrates the top 10 countries by the number of Starbucks stores, with the United States overwhelmingly leading with over 13,000 stores. Other countries like China, Canada, and Japan also show significant numbers but are considerably less compared to the U.S.")

    if st.sidebar.checkbox('Show Longitude and Latitude Scatter Plot', key='show_scatter_plot'):
        st.write("Longitude and Latitude Scatter Plot") # [VIZ3]
        plot_longitude_latitude_scatter(data, country_code)
        st.write("This scatter plot illustrates the geographic distribution of Starbucks stores across the United States, categorized by their ownership type. Blue dots represent licensed stores (LS), while orange dots indicate company-operated stores (CO), showing a widespread presence across the country with a notable concentration in major urban areas.")

    if st.sidebar.checkbox('Show Timezone Offset Boxplot', key='show_box_plot'):
        st.write("Timezone Offset Boxplot")
        plot_timezone_offset_boxplot(data)
        st.write("This plot displays the distribution of timezone offsets by country code using a box plot format, where each country's data variability is represented by the spread and central value of its timezone offset.")

    if st.sidebar.checkbox('Show Hexbin Plot with Marginals', key='show_hexbin_plot'):
        st.write("Hexbin Plot with Marginals")
        hexbin_with_marginals(data, 'Longitude', 'Latitude')
        st.write("This plot is a hexbin chart with marginal distributions, used to visualize the density of data points over a geographical area, measured by latitude and longitude. The hexbins, which vary in color intensity, indicate the concentration of data points, with darker hexbins showing higher densities, while the histograms on the top and right margins depict the frequency distribution of latitude and longitude values, respectively.")

    if st.sidebar.checkbox('Show Wide Form Violinplot', key='show_violin_plot'):
        st.write("Wide Form Violinplot")
        wide_form_violinplot(data, ['Longitude', 'Latitude', 'TimezoneOffset'])
        st.write("This violin plot displays the distribution of three different variables: Longitude, Latitude, and TimezoneOffset.")

    # Show a histogram of locations by country
    if st.sidebar.checkbox("Show Locations by Country", False):
        st.write("Histogram of Locations by Country")
        plt.figure(figsize=(40, 25))
        filtered_data = data[data['CountryCode'].isin(['CA', 'JP', 'CN', 'KR'])]
        sns.histplot(data=filtered_data, x="CountryCode", binwidth=1)
        st.pyplot()
