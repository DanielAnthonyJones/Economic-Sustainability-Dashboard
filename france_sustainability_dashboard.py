import os
import pandas as pd
import numpy as np
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
"Agriculture, forestry, and fishing, value added (annual % growth)",


"Industry (including construction), value added (current US$)",
"Industry (including construction), value added (% of GDP)",
"Industry (including construction), value added (annual % growth)",

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


'Merchandise imports from low- and middle-income economies in East Asia & Pacific (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Europe & Central Asia (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Latin America & the Caribbean (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Middle East & North Africa (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in South Asia (% of total merchandise imports)',
'Merchandise imports from low- and middle-income economies in Sub-Saharan Africa (% of total merchandise imports)',

# Exports

'Merchandise exports to low- and middle-income economies in East Asia & Pacific (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Europe & Central Asia (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Latin America & the Caribbean (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Middle East & North Africa (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in South Asia (% of total merchandise exports)',
'Merchandise exports to low- and middle-income economies in Sub-Saharan Africa (% of total merchandise exports)',


]

trade_df_totals = df[df["Indicator Name"].isin(["Merchandise imports (current US$)", "Merchandise exports (current US$)"])] # Dataframe for total merchandise imports and exports indicators
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
    
    col1, col2, col3 = st.columns([0.7, 0.1, 0.1])
    with col2:
        use_full_range = st.toggle("Full Chart Range", value=False)
    with col3:
        adjust_inflation = st.toggle("Adjust for Inflation", value=False)
    
    home_df["Indicator Name"] = home_df["Indicator Name"].replace({
        "GDP (current US$)": "GDP",
        "GDP per capita (current US$)": "GDP per capita",
        "GDP (constant 2015 US$)":"GDP (inflation adjusted)",
        "GDP per capita (constant 2015 US$)":"GDP per capita (inflation adjusted)"
    })    

    for _ in range(3): # Add spacing  
        st.write("")

    # Radio buttons to select GDP indicator for display and chart
    if adjust_inflation:
        indicator_choice = st.radio(
        "Select GDP Indicator",
        ["GDP (inflation adjusted)", "GDP per capita (inflation adjusted)"],
        horizontal=True
    )
    else:
        indicator_choice = st.radio(
            "Select GDP Indicator",
            ["GDP", "GDP per capita"],
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
    
    fig.update_traces(
        hovertemplate="Year: %{x}<br>$%{y:,.0f}<extra></extra>"
    )
    
    # If full range toggle is off, set x-axis ticks to every year for better readability
    
    if not use_full_range:
        fig.update_xaxes(dtick=1)
    
    # Display chart in left column, with warning if selected year is outside available data range
    with left:
        if (year <= min_year) and (not use_full_range):
            st.warning(f"Not enough historical data available for selected year. Please use slider to select a year greater than {min_year}")
            st.warning("Or Instead 📊 Dive into Economic Structure or 🌍 Explore Trade with Other Countries.")
        else:
            st.plotly_chart(fig) 
            
    for _ in range(3): # Add spacing  
        st.write("")
    
    st.divider() # Horizontal divider to separate sections
    
    for _ in range(3): # Add spacing  
        st.write("")
    
    # Preparing data for economic structure and trade charts
    
    sector_indicators = ["Agriculture, forestry, and fishing, value added (current US$)",
    "Industry (including construction), value added (current US$)",
    "Services, value added (current US$)",
    "Manufacturing, value added (current US$)"]
    
    sector_df = df[
        (df["Year"] == year) &
        (df["Indicator Name"].isin(sector_indicators))
    ]
    
    sector_df["Indicator Name"] = sector_df["Indicator Name"].replace({
        "Agriculture, forestry, and fishing, value added (current US$)": "Agriculture, forestry, and fishing",
        "Industry (including construction), value added (current US$)": "Industry (including construction)",
        "Services, value added (current US$)": "Services",
        "Manufacturing, value added (current US$)": "Manufacturing"})
    
    trade_indicators = ["Imports of goods and services (annual % growth)",
    "Exports of goods and services (annual % growth)"]
    
    trade_df = df[
        (df["Indicator Name"].isin(trade_indicators))
    ]

    color_map = {
        "Agriculture, forestry, and fishing": "#FF2B2B", 
        "Industry (including construction)": "#0068C9",  
        "Services": "#83C9FF",                         
        "Manufacturing": "#FFABAB"                      
    }
    
    # Pie chart for economic structure based on value added by industry sectors for selected year
    fig_pie = px.pie(
        sector_df,
        names="Indicator Name",
        values="Value",
        color="Indicator Name",
        color_discrete_map=color_map,
        title=f"How each Industry contributed to GDP in {year}",
        subtitle=f"Press Legend to toggle industries on/off"
    )
    
    fig_pie.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode=False

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
    
    import_df.rename(columns={"Value": "Percentage Change (%)"}, inplace=True) # Rename column for clarity in charts
            
    # Line chart for import
    fig_import = px.line(
        import_df.sort_values("Year"),
        x="Year",
        y="Percentage Change (%)",
        title=f"% Change in Imports {start_year} - {end_year}",
        subtitle=f"Hover over point to see exact value. Use slider to adjust time range."
    )
    
    fig_import.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=70, b=10)
    )
    
    fig_import.update_traces(
    hovertemplate="Year: %{x}<br>Percentage Change: %{y:.2f}%<extra></extra>"
    )
    
    export_df = trade_df[
        (trade_df["Indicator Name"] == "Exports of goods and services (annual % growth)") &
        (trade_df["Year"] >= start_year) &
        (trade_df["Year"] <= end_year)
    ]
    
    export_df.rename(columns={"Value": "Percentage Change (%)"}, inplace=True) # Rename column for clarity in charts
            
    # Line chart for export
       
    fig_export = px.line(
        export_df.sort_values("Year"),
        x="Year",
        y="Percentage Change (%)",
        title=f"% Change in Exports {start_year} - {end_year}",
        subtitle=f"Hover over point to see exact value. Use slider to adjust time range." 
    )
    
    
    fig_export.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=70, b=10)
    )
    
    fig_export.update_traces(
    hovertemplate="Year: %{x}<br>Percentage Change: %{y:.2f}%<extra></extra>"
    )
    
    if not use_full_range:
        fig_import.update_xaxes(dtick=2)
        fig_export.update_xaxes(dtick=2)
    
    # Split section into left and right columns for economic structure and trade charts
    
    left, right = st.columns(2)
    
    with left:
        # Use 3 columns to center in column
        b1,b2,b3 = st.columns(3)
        with b2:
            st.button(" 📊 Dive into Economic Structure", on_click=go, args=("economy",))
        if year >= max_year: # Handle case where no data
            st.warning(f"No data available for selected year. Explore other years using slider, or 📊 Dive into Economic Structure.")
        else:
            st.plotly_chart(fig_pie)
    
    # Same concept as left column but for trade
    with right:
        b1,b2,b3 = st.columns(3)
        with b2:
            st.button("🌍 Explore Trade with Other Countries", on_click=go, args=("trade",))
        if year <= min_year and not use_full_range: # Handle case where no data
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
    
    # Create 3 columns for flag and title and back button (adjusting positions)
    col1, col2, col3 = st.columns([0.1, 1, 0.1])
    with col1:
        st.image(os.path.join(folder, "images/flag.png"), width=500) # Flag image
        

    with col2:
        st.title("Economic Structure 📊")
        st.write("How each economic sector contributes to France\'s economic growth.")
    
    with col3:
        st.button("⬅️ Go Back", on_click=go, args=("home",))
    
    # Colour map for consistent colours across charts for each industry sector
    color_map = {
        "Agriculture, forestry, and fishing": "#FF2B2B", 
        "Industry (including construction)": "#0068C9",  
        "Services": "#83C9FF",                         
        "Manufacturing": "#FFABAB"                      
    }

    st.divider()

    for _ in range(3): # Add spacing  
        st.write("")
    
    #  Creating and adjusting multiselect for economic sectors and segmented control for date range
    
    left,middle, right = st.columns([3,0.1, 1])
    with left:
        selected_sectors = st.multiselect("Select Economic Sector", ["Agriculture, forestry, and fishing", "Industry (including construction)", "Services", "Manufacturing"])
    with right:
        time_frame = st.segmented_control(
        "Select Date Range",
        ["Last 5 Years", "Last 10 Years", "Last 20 Years", "All Time"],
    )
        
    for _ in range(3): # Add spacing  
        st.write("")
        
    # Warning for comparing manufacturing data due to scale difference
        
    if "Manufacturing" in selected_sectors and len(selected_sectors) > 1:
        st.info("Comparing Manufacturing with other sectors may make its trend harder to see because of the difference in scale. Try viewing it individually for more detail.")
    
    for _ in range(3): # Add spacing  
        st.write("")
    
    # Creating segmented control for indicator selection
    col1, col2, col3 = st.columns([5, 6.5, 1])
    with col2:
        selected_indicator = st.segmented_control("Select Indicator", ["current US$", "% of GDP", "annual % growth"],
                                    )
    
    for _ in range(3): # Add spacing  
        st.write("")
    
    # Replace indicator names in dataframe to be more concise for display in charts
    econ_df["Indicator Name"] = econ_df["Indicator Name"].replace({
        f"Agriculture, forestry, and fishing, value added ({selected_indicator})": "Agriculture, forestry, and fishing",
        f"Industry (including construction), value added ({selected_indicator})": "Industry (including construction)",
        f"Services, value added ({selected_indicator})": "Services",
        f"Manufacturing, value added ({selected_indicator})": "Manufacturing"})
    
    max_year = econ_df["Year"].max()
    
    # Set start year based on selected time frame
    
    if time_frame == "Last 5 Years":
        start_year = max_year - 5
    elif time_frame == "Last 10 Years":
        start_year = max_year - 10
    elif time_frame == "Last 20 Years":
        start_year = max_year - 20
    else: # "All Time" or if nothing is selected
        start_year = int(econ_df["Year"].min())
    
    # Creatings graphs 
    
    fig_line = px.line(
        econ_df[(econ_df["Indicator Name"].isin(selected_sectors)) & (econ_df["Year"] >= start_year)].sort_values("Year"),
        x="Year",
        y="Value",
        color="Indicator Name",
        color_discrete_map=color_map,
        title=f"Economic Sector over time ({selected_indicator})",
        labels={"Value": f"{selected_indicator}", "Indicator Name": "Economic Sector"},
    )
    
    fig_bar = px.bar(
        econ_df[(econ_df["Indicator Name"].isin(selected_sectors)) & (econ_df["Year"] >= start_year)].sort_values("Year"),
        x="Year",
        y="Value",
        color="Indicator Name",
        color_discrete_map=color_map,
        title=f"Economic Sector Composition ({selected_indicator})",
        labels={"Value": f"{selected_indicator}", "Indicator Name": " Economic Sector"}
    )
    
    # Adjusting hover behaviour based on selected indicator
    
    if selected_indicator == "current US$":
        fig_line.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>$%{y:,.0f}<extra></extra>"
        )
        fig_bar.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>$%{y:,.0f}<extra></extra>"
        )
    if selected_indicator == "annual % growth":
        fig_line.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>% Change: %{y:.2f}%<extra></extra>"
        )
        fig_bar.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>% Change: %{y:.2f}%<extra></extra>"
        )
    
    if selected_indicator == "% of GDP":
        fig_line.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>% of GDP: %{y:.2f}%<extra></extra>"
        )
        fig_bar.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>% of GDP: %{y:.2f}%<extra></extra>"
        )
    
    # Display warning if user has not made all necessary selections to view charts
    
    if not selected_sectors or not selected_indicator or not time_frame:
        if not selected_sectors:
                st.warning("Please select at least one economic sector to display the charts.")
        if not selected_indicator:
                st.warning("Please select an indicator to display the charts.")
        if not time_frame:
                st.warning("Please select a time range to display the charts.")
    
    else:
        left, right = st.columns(2)
        with left:
            st.plotly_chart(fig_line)
        with right:
            st.plotly_chart(fig_bar)
    

def trade_page():
    #
    
    col1, col2, col3 = st.columns([0.1, 1, 0.1])
    with col1:
        st.image(os.path.join(folder, "images/flag.png"), width=500) # Flag image
        
    with col2:
        st.title("Global Trade 🌍")
        st.write("Analyse France's trade with different low & middle-income economies around the world.")
    
    with col3:
        st.button("⬅️ Go Back", on_click=go, args=("home",))

        
    year = st.slider(
        "Select Year",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=int(df["Year"].max())
    )
    
    trade_type = st.radio("Select Trade Flow", ["Imports & Exports", "Imports only", "Exports Only"], horizontal=True)
    
    temp_df = trade_df.copy()
    
    temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise imports from low- and middle-income economies in ", "", case=False, regex=False)
    temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise imports)", "", case=False, regex=False)
    temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise exports to low- and middle-income economies in ", "", case=False, regex=False)
    temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise exports)", "", case=False, regex=False)
        
    
    
    regions = temp_df["Indicator Name"].unique().tolist()
    
    
    selected_region = st.multiselect("Select Region", regions)
    
    temp_df = trade_df[trade_df["Year"] == year].copy() # Create temporary dataframe for cleaning and filtering based on user selections
    
    
    if trade_type == "Imports only":
        temp_df = temp_df[temp_df["Indicator Name"].str.contains("imports", case=False, na=False)]
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise imports from low- and middle-income economies in ", "", case=False, regex=False)
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise imports)", "", case=False, regex=False)
        
        fig_bar = px.bar(
            temp_df[temp_df["Indicator Name"].isin(selected_region)],
            x="Indicator Name",
            y="Value",
            title=f"Regional Trade Breakdown ({year})",
            color_discrete_sequence=["#FF2B2B"]
     )
        
    elif trade_type == "Exports Only":
        temp_df = temp_df[temp_df["Indicator Name"].str.contains("exports", case=False, na=False)]
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise exports to low- and middle-income economies in ", "", case=False, regex=False)
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise exports)", "", case=False, regex=False)
        
        fig_bar = px.bar(
            temp_df[temp_df["Indicator Name"].isin(selected_region)],
            x="Indicator Name",
            y="Value",
            title=f"Regional Trade Breakdown ({year})",
            color_discrete_sequence=["#0068C9"]
     )
    
    else:
            # Filter for rows that contain either imports or exports
            temp_df = temp_df[temp_df["Indicator Name"].str.contains("imports|exports", case=False, na=False)]
            
            temp_df["Type"] = temp_df["Indicator Name"].apply(lambda x: "Export" if "export" in x.lower() else "Import")

            
            temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise imports from low- and middle-income economies in ", "", case=False, regex=False)
            temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise imports)", "", case=False, regex=False)
            temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise exports to low- and middle-income economies in ", "", case=False, regex=False)
            temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise exports)", "", case=False, regex=False)
            
            
            color_map = {
                "Import": "#FF2B2B", 
                "Export": "#0068C9"                    
            }
        
            
            fig_bar = px.bar(
                    temp_df[temp_df["Indicator Name"].isin(selected_region)],
                    x="Indicator Name",
                    y="Value",
                    color="Type",
                    color_discrete_map=color_map,
                    barmode="group",       
                    title=f"Regional Trade Breakdown ({year})",
                    labels={"Indicator Name": "Region", "Value": "Percentage of Total"}
                )
    

    if len(selected_region) < 2:
        st.warning("Select at least 2 regions to compare trade flows. Please select more regions from the dropdown to view the chart.")
    else:
        st.plotly_chart(fig_bar)

    st.subheader("Text")

    with st.expander("Expand"):
        st.write("Test")
    st.write("")
    st.write("---")

    
    st.write("Analyze trade....")
    st.write("charts")
    st.write("charts")
    st.write("charts")
    
if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "economy":

    econ_page()
    
elif st.session_state.page == "trade":

    trade_page()
