import os
import pandas as pd
import streamlit as st
import plotly.express as px


folder_name = "assets" # Folder of assets used in dashboard

try:
    script_dir = os.path.dirname(os.path.abspath(__file__)) # File path where script is running
    folder = os.path.join(script_dir, folder_name)

except Exception:
    # __file__ does not exist in colab
    script_dir = f"."
    folder = os.path.join(script_dir, folder_name)

os.makedirs(folder, exist_ok=True)

df = pd.read_csv(os.path.join(folder, "datasets/indicators_fra.csv")) # Load csv into dataframe

# List of indicators for the homepage

home_indicator_names = [
      
"GDP (current US$)", 
"GDP per capita (current US$)",
"GDP (constant 2015 US$)",
"GDP per capita (constant 2015 US$)",

"Exports of goods and services (current US$)",
"Exports of goods and services (% of GDP)",

"Imports of goods and services (current US$)",
"Imports of goods and services (% of GDP)",

"Exports of goods and services (annual % growth)",
"Imports of goods and services (annual % growth)",

# Industry sectors indicators

"Agriculture, forestry, and fishing, value added (current US$)",
"Industry (including construction), value added (current US$)",
"Services, value added (current US$)",
"Manufacturing, value added (current US$)"
]

home_df = df[df["Indicator Name"].isin(home_indicator_names)] # Filter dataframe to include homepage indicators

# List of indicators for economic structure page

econ_indicator_names = [
    
# Industry sectors indicators

"Agriculture, forestry, and fishing, value added (current US$)",
"Agriculture, forestry, and fishing, value added (% of GDP)",
"Agriculture, forestry, and fishing, value added (annual % growth)"


"Industry (including construction), value added (current US$)",
"Industry (including construction), value added (% of GDP)",
"Industry (including construction), value added (annual % growth)"

"Services, value added (current US$)",
"Services, value added (% of GDP)",
"Services, value added (annual % growth)",

"Manufacturing, value added (% of GDP)",
"Manufacturing, value added (current US$)",
"Manufacturing, value added (annual % growth)"]

econ_df = df[df["Indicator Name"].isin(econ_indicator_names)] # Filter dataframe to include economic structure indicators

# List of indicators for trade page

trade_indicator_names = [
    
# Merchandise trade region indicators

# Imports

'Merchandise imports (current US$)',

'Merchandise imports from economies in the Arab World (% of total merchandise imports)',
'Merchandise imports from high-income economies (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies outside region (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in East Asia & Pacific (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Europe & Central Asia (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Latin America & the Caribbean (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Middle East & North Africa (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in South Asia (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Sub-Saharan Africa (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies within region (% of total merchandise imports)',

# Exports

'Merchandise exports (current US$)',

'Merchandise exports to economies in the Arab World (% of total merchandise exports)',
'Merchandise exports to high-income economies (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies outside region (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in East Asia & Pacific (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Europe & Central Asia (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Latin America & the Caribbean (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Middle East & North Africa (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in South Asia (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Sub-Saharan Africa (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies within region (% of total merchandise exports)'


]

trade_df = df[df["Indicator Name"].isin(trade_indicator_names)] # Filter dataframe to include trade indicators



# Initialise page state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Functions defining page content and navigation

def go(page_name):
    st.session_state.page = page_name # Used for page navigation
    

def home_page():
    
    st.set_page_config(layout="wide")
    
    # Create two columns for flag and title (adjusting positions)
    col1, col2 = st.columns([0.1, 1])
    with col1:
        st.image(os.path.join(folder, "images/flag.png"), width=500) # Flag image
        

    with col2:
        st.title("France Economic & Sustainability Dashboard")
        st.write("Explore France\'s economic growth in GDP, trade, and industry sectors. Use the buttons to navigate.")
    
    # Year slider based on available data range in dataset
    
    year = st.slider(
        "Select Year",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=int(df["Year"].max())
    )
    
    # Toggle for full chart range vs last 10 years, using columns to position toggle on the right side of the page
    
    col1, col2 = st.columns([0.7, 0.1])
    with col2:
        use_full_range = st.toggle("Full Chart Range", value=False)
    
    home_df["Indicator Name"] = home_df["Indicator Name"].replace({
        "GDP (current US$)": "GDP",
        "GDP per capita (current US$)": "GDP per capita",
        "GDP (constant 2015 US$)":"GDP (inflation adjusted)",
        "GDP per capita (constant 2015 US$)":"GDP per capita (inflation adjusted)"
    })    

    # Radio buttons to select GDP indicator for display and chart
    indicator_choice = st.radio(
        "Select GDP Indicator",
        ["GDP", "GDP per capita", "GDP (inflation adjusted)", "GDP per capita (inflation adjusted)"],
        horizontal=True
    )
    
    # Extract GDP value for selected year and indicator, handling missing data
    gdp_series = home_df[
        (home_df["Indicator Name"] == indicator_choice) &
        (home_df["Year"] == year)]["Value"]
    
    gdp_value = gdp_series.iloc[0] if not gdp_series.empty else 0
    
    left, right = st.columns([0.7,0.3])
    with right:
        if gdp_value == 0: # Handle case where GDP value is missing for selected year and indicator
            st.warning(f"No data available for {indicator_choice} in {year}. Please select a different year or indicator.")
        else:    
            st.metric(f"{indicator_choice} {year}", f"${gdp_value:,.0f}") 
    
    
    min_year = home_df["Year"].min()
    max_year = home_df["Year"].max()
    
    if use_full_range: # If full range toggle is on, set start and end years to min and max available in dataset
        start_year = min_year
        end_year = max_year
    else: # If full range toggle is off, set start year to 10 years before selected year and end year to selected year
        start_year = year - 10
        end_year = year
        
    gdp_df = home_df[
        (home_df["Indicator Name"] == indicator_choice) &
        (home_df["Year"] >= start_year) &
        (home_df["Year"] <= end_year)
    ]
    
    gdp_df.rename(columns={"Value": "US$"}, inplace=True) # Rename column for clarity in charts
    
    # Line chart for GDP growth over time based on selected indicator and year range
    fig = px.line(
        gdp_df,
        x="Year",
        y="US$",
        title=f"{indicator_choice} growth over time in US$ ({start_year} - {end_year})",
        subtitle=f"Hover over point to see exact value."
    )
    
    # Adjust chart height and margins for better display
    fig.update_layout(
    height=300,  
    margin=dict(l=10, r=10, t=80, b=100)
    )
    
    # If full range toggle is off, set x-axis ticks to every year for better readability
    
    if not use_full_range:
        fig.update_xaxes(dtick=1)
    
    # Display chart in left column, with warning if selected year is outside available data range
    with left:
        if year <= min_year:
            st.warning(f"Not enough historical data available for selected year. Please use slider to select a year greater than {min_year}")
            st.warning("Or Instead 📊 Dive into Economic Structure or 🌍 Explore Trade with Other Countries.")
        else:
            st.plotly_chart(fig) 

    st.divider() # Horizontal divider to separate sections
    
    # Preparing data for economic structure and trade charts
    
    sector_indicators = ["Agriculture, forestry, and fishing, value added (current US$)",
    "Industry (including construction), value added (current US$)",
    "Services, value added (current US$)",
    "Manufacturing, value added (current US$)"]
    
    sector_df = df[
        (df["Year"] == year) &
        (df["Indicator Name"].isin(sector_indicators))
    ]
    
    trade_indicators = ["Imports of goods and services (annual % growth)",
    "Exports of goods and services (annual % growth)"]
    
    trade_df = df[
        (df["Indicator Name"].isin(trade_indicators))
    ]
    
    # Pie chart for economic structure based on value added by industry sectors for selected year
    fig_pie = px.pie(
        sector_df,
        names="Indicator Name",
        values="Value",
        title=f"How each Industry contributed to GDP in {year}",
        subtitle=f"Press Legend to toggle industries on/off"
    )
    
    fig_pie.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=50, b=10)

    )
    
    min_year = trade_df["Year"].min()
    max_year = trade_df["Year"].max()

    if use_full_range: # If full range toggle is on, set start and end years to min and max available in dataset
        start_year = min_year
        end_year = max_year
    else:
        start_year = year - 10
        end_year = year
        
    import_df = trade_df[
        (trade_df["Indicator Name"] == "Imports of goods and services (annual % growth)") &
        (trade_df["Year"] >= start_year) &
        (trade_df["Year"] <= end_year)
    ]
            
    # Line chart for import
    fig_import = px.line(
        import_df,
        x="Year",
        y="Value",
        title=f"% Change in Imports {start_year} - {end_year}",
        subtitle=f"Hover over point to see exact value. Use slider to adjust time range."
    )
    
    fig_import.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=70, b=10)
    )
    
    export_df = trade_df[
        (trade_df["Indicator Name"] == "Exports of goods and services (annual % growth)") &
        (trade_df["Year"] >= start_year) &
        (trade_df["Year"] <= end_year)
    ]
     
    # Line chart for export
       
    fig_export = px.line(
        export_df,
        x="Year",
        y="Value",
        title=f"% Change in Exports {start_year} - {end_year}",
        subtitle=f"Hover over point to see exact value. Use slider to adjust time range." 
    )
    
    
    fig_export.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=70, b=10)
    )
    
    if not use_full_range:
        fig_import.update_xaxes(dtick=1)
        fig_export.update_xaxes(dtick=1)
    
    # Split section into left and right columns for economic structure and trade charts
    
    left, right = st.columns(2)
    
    with left:
        # Use 3 columns to center in column
        b1,b2,b3 = st.columns(3)
        with b2:
            st.button(" 📊 Dive into Economic Structure", on_click=go, args=("economy",))
        if year >= max_year: # Handle case where no data
            st.warning(f"Not data available for selected year. Explore other years using slider, or 📊 Dive into Economic Structure.")
        else:
            st.plotly_chart(fig_pie)
    
    # Same concept as left column but for trade
    with right:
        b1,b2,b3 = st.columns(3)
        with b2:
            st.button("🌍 Explore Trade with Other Countries", on_click=go, args=("trade",))
        if year <= min_year:
            st.warning(f"Not enough historical data available for selected year. Please use slider to select a year greater than {min_year}, or 🌍 Explore Trade with Other Countries.")
        else:
            # 2 columns to plot trade charts side by side
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_import)
            with col2:
                st.plotly_chart(fig_export)
      
        
    return

def econ_page():
    
    st.title("Economic Structure")

    st.write("Text")

    # placeholders for charts:
    st.write("charts")
    st.write("charts")
    st.write("charts")

    st.button("Go Back", on_click=go, args=("home",))
    
def trade_page():
    
    st.title("Trade Page")

    st.write("Analyse trade....")

    # placeholders:
    st.write("charts")
    st.write("charts")
    st.write("charts")

    st.button("Go Back", on_click=go, args=("home",))
    
    
if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "economy":

    econ_page()
    
elif st.session_state.page == "trade":

    trade_page()
