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
        value=2015
    )
    
    # Code for above divider
    
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

    # Radio buttons to select GDP indicator for display and chart depending on if adjusted for inflation
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
    
    # Change hover functionality
    
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
    
    # Ability to see dataset and download in an expander
           
    if not (year <= min_year) and (not use_full_range):
        with st.expander("Expand to see/download the dataframe used to create the chart"):
            st.dataframe(gdp_df)
            
    st.divider() # Horizontal divider to separate sections
    
    # Code for below divider
    
    for _ in range(3): # Add spacing  
        st.write("")
    
    # Preparing data for economic structure and trade charts (hopefully this means the graphs will update closer to simultaneously)
    
    # Left side
    
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
    
    # Right side
    
    trade_indicators = ["Imports of goods and services (annual % growth)",
    "Exports of goods and services (annual % growth)"]
    
    trade_df = df[
        (df["Indicator Name"].isin(trade_indicators))
    ]


    # Hard coding colours for consistency (colour picker used to keep same as default because it looks nice and matches french flag)
    
    color_map = {
        "Agriculture, forestry, and fishing": "#FF2B2B", 
        "Industry (including construction)": "#0068C9",  
        "Services": "#83C9FF",                         
        "Manufacturing": "#FFABAB"                      
    }
    
    # Left side 
    
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
    
    # Adjusting plot space and removing option to over
    
    fig_pie.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode=False

    )
   
   # Right side
    
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
    
    # Adjusting plot area
    
    fig_import.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=70, b=10)
    )
    
    # Adjusting hover descriptions
    
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
    
    # Adjusting plot area
    
    fig_export.update_layout(
        height=300,   
        margin=dict(l=10, r=10, t=70, b=10)
    )
    
    # Adjusting hover descriptions
    
    fig_export.update_traces(
    hovertemplate="Year: %{x}<br>Percentage Change: %{y:.2f}%<extra></extra>"
    )
    
    # Changing tick rate for readability
    
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
            with st.expander("Expand to see/download the dataframe used to create the pie chart"):
                st.dataframe(sector_df)
    
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
                with st.expander("Expand to see/download the dataframe used to create the import chart"):
                    st.dataframe(import_df)
            with col2:
                st.plotly_chart(fig_export)
                with st.expander("Expand to see/download the dataframe used to create the export chart"):
                    st.dataframe(export_df)
      
        
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
        
    # Warning for comparing manufacturing data due to  observed scale difference
        
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
    
    temp_df = econ_df[(econ_df["Indicator Name"].isin(selected_sectors)) & (econ_df["Year"] >= start_year)].sort_values("Year")
    
    fig_line = px.line(
        temp_df,
        x="Year",
        y="Value",
        color="Indicator Name",
        color_discrete_map=color_map,
        title=f"Economic Sector over time ({selected_indicator})",
        labels={"Value": f"{selected_indicator}", "Indicator Name": "Economic Sector"},
    )
    
    fig_bar = px.bar(
        temp_df,
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
    elif selected_indicator == "annual % growth":
        fig_line.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>% Change: %{y:.2f}%<extra></extra>"
        )
        fig_bar.update_traces(
            hovertemplate="%{fullData.name}<br>Year: %{x}<br>% Change: %{y:.2f}%<extra></extra>"
        )
    
    elif selected_indicator == "% of GDP":
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
        with st.expander("Expand to see/download the dataset used to create the charts"):
            st.dataframe(temp_df)

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
        value=2015
    )
    
    def clean_regions(dataframe):
        
        temp_df = dataframe.copy()
        
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise imports from low- and middle-income economies in ", "", case=False, regex=False) # Removing first section before region in indicator
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise imports)", "", case=False, regex=False) # Removing section after region in indicator
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("Merchandise exports to low- and middle-income economies in ", "", case=False, regex=False) # Removing section after region in indicator
        temp_df["Indicator Name"] = temp_df["Indicator Name"].str.replace("(% of total merchandise exports)", "", case=False, regex=False) # Removing section after region in indicator
        
        return temp_df
    
    temp_df = clean_regions(trade_df)    
    regions = temp_df["Indicator Name"].unique().tolist() # List of only region section of indicator

    
    # Filtering dataframe for figures at specific year
    
    import_series = trade_df_totals[(trade_df_totals['Indicator Name'] == 'Merchandise imports (current US$)') 
                & (trade_df_totals['Year'] == year)]['Value']
    
    export_series = trade_df_totals[(trade_df_totals['Indicator Name'] == 'Merchandise exports (current US$)') 
                & (trade_df_totals['Year'] == year)]['Value']
    
    # If there is missing data
    
    import_value = import_series.iloc[0] if not import_series.empty else 0
    export_value = export_series.iloc[0] if not export_series.empty else 0
    
    # Import/Export Metrics
    
    col1, col2, col3, col4 = st.columns([1, 0.1, 0.3, 0.3])
    with col1:
        selected_region = st.multiselect("Select Region", regions)
    with col3:
        if import_value == 0:
            st.warning(f"No import data available for {year}. Please select a different year.")
        else:
            st.metric(f"Total Imports US$ ({year})", 
                  f"${import_value:,.0f}")
    with col4:    
        if export_value == 0:
            st.warning(f"No export data available for {year}. Please select a different year.")
        else:
            st.metric(f"Total Exports US$ ({year})", 
                  f"${export_value:,.0f}")
    
    plot_df = trade_df[trade_df["Year"] == year].copy() # Create temporary dataframe for cleaning and filtering based on user selections
    
    # Filter for rows that contain either imports or exports
    
    plot_df = plot_df[plot_df["Indicator Name"].str.contains("imports|exports", case=False, na=False)]
            
    plot_df["Type"] = plot_df["Indicator Name"].apply(lambda x: "Exports" if "export" in x.lower() else "Imports") # New columns for type
    
    temp_df = clean_regions(plot_df)
                        
    color_map = {
        "Imports": "#FF2B2B", 
        "Exports": "#0068C9"                    
    }    
            
    fig_bar = px.bar(
                    temp_df[temp_df["Indicator Name"].isin(selected_region)],
                    x="Indicator Name",
                    y="Value",
                    color="Type",
                    color_discrete_map=color_map,
                    barmode="group",       
                    title=f"Regional Trade Breakdown ({year})",
                    subtitle=f"Press Legend to toggle Import/Export, Hover over bars to see exact values and use the dropdown to compare different regions.",
                    labels={"Indicator Name": "Region", "Value": "Percentage of Total (%)"}
                )
    
    fig_bar.update_layout(
    legend_title_text='', # Remove legend title
    
    legend=dict(
        title_font_size=20,   # Size of the "Type" title
        orientation="v",      # Vertical orientation
        yanchor="top",        # Anchor the legend at its top
        y=1,                  # Top of the chart
        xanchor="right",      # Anchor the legend at its right edge
        x=-0.05,              # Move it to the left of the y-axis
        font=dict(size=18)    # Size of the "Import" and "Export" text
        )
    )
    
    
    # Changed hover display
    
    fig_bar.update_traces(
            hovertemplate="%{x}%{fullData.name}<br>Total: %{y:,.2f}%<extra></extra>"
        )

    
    # Some logic to display warnings instead of plotting graphs for certain conditions
    
    if (len(selected_region) < 2) or (fig_bar.data == ()):
        
        if not fig_bar.data: # Check if there is data to display in the chart
            st.warning("No data available for selected year and regions. Please select a different year or regions.")
                
        if len(selected_region) < 2:
            st.warning("Select at least 2 regions to compare trade flows. Please select more regions from the dropdown to view the chart.")
    else:
        st.plotly_chart(fig_bar)

    with st.expander("Expand to see/download the dataset used to create the chart"):
        st.dataframe(temp_df)


# Calling functions to load page depending on state
    
if st.session_state.page == "home":
    home_page()

elif st.session_state.page == "economy":

    econ_page()
    
elif st.session_state.page == "trade":

    trade_page()
