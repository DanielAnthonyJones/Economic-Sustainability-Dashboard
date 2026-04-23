import os
import pandas as pd
import streamlit as st
import plotly.express as px


folder_name = "Datasets" # Folder where datasets will be saved

try:
    script_dir = os.path.dirname(os.path.abspath(__file__)) # File path where script is running
    folder = os.path.join(script_dir, folder_name)

except Exception:
    # __file__ does not exist in colab
    script_dir = f"."
    folder = os.path.join(script_dir, folder_name)

os.makedirs(folder, exist_ok=True)

df = pd.read_csv(os.path.join(folder, "indicators_fra.csv")) # Load csv into dataframe

home_indicator_names = [
      
"GDP (current US$)", 
"GDP per capita (current US$)",

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

home_df = df[df["Indicator Name"].isin(home_indicator_names)]

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

econ_df = df[df["Indicator Name"].isin(econ_indicator_names)]

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

trade_df = df[df["Indicator Name"].isin(trade_indicator_names)]



# Initialise page state
if "page" not in st.session_state:
    st.session_state.page = "home"


def go(page_name):
    st.session_state.page = page_name
    

def home_page():
    
    st.title("France Dashboard")

    st.write("Explore France\'s growth in GDP, trade, and industry sectors.")
    
    year = 2024

    gdp_value = home_df[
        (home_df["Indicator Name"] == "GDP (current US$)") &
        (home_df["Year"] == year)]["Value"].values[0]
    
    st.metric(f"GDP {year}", f"${gdp_value:,.0f}")
    fig = px.line(
        home_df[home_df["Indicator Name"] == "GDP (current US$)"],
        x="Year",
        y="Value",
        title="GDP Growth over time"
    )
    
    st.plotly_chart(fig) 

  
    left, right = st.columns(2)

    with left:
        st.button(" Dive into Economic Structure", on_click=go, args=("economy",))
     
    
    
    with right:
        st.button("Explore Trade with Other Countries", on_click=go, args=("trade",))
        
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
