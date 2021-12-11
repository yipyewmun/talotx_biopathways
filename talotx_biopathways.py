# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
# import pyautogui


sideb=st.sidebar

# Set header title
st.title('Network Graph Visualization of Biological Pathways')

# Read dataset (CSV)
url = 'https://docs.google.com/spreadsheets/d/1zSuV2TWHMgCnzk-RZ0GvAhihpk2bdeV9L0dLTtGYUGc/edit#gid=1648521135'
url2 =  url.replace('/edit#gid=', '/export?format=csv&gid=')
df_interact = pd.read_csv(url2)

# Define selection options and sort alphabetically
target_list = df_interact['target_1'].tolist() + df_interact['target_2'].tolist()
target_list = list(set(target_list))
target_list.sort()

sideb.write(
    """
    Step 1: Open the spreadsheet by pressing 'Spreadsheet for Inputing Targets'.\n
    Step 2: Press the "Refresh App" button.\n
    Step 3: Now you can select target(s) from the dropdown menu.
    """
)
link = '[Spreadsheet for Inputing Targets](https://docs.google.com/spreadsheets/d/1zSuV2TWHMgCnzk-RZ0GvAhihpk2bdeV9L0dLTtGYUGc/edit?usp=sharing)'
sideb.markdown(link, unsafe_allow_html=True)
refresh = sideb.button('Refresh App')
if refresh:
    pass
    # pyautogui.hotkey("ctrl","F5")

# Implement multiselect dropdown menu for option selection
selected_targets = sideb.multiselect('Select target to visualize', target_list)

# Set info message on initial site load
# if len(selected_drugs) == 0:
if len(selected_targets) == 0:
    sideb.text('Please choose 1 target to get started')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['target_1'].isin(selected_targets) | \
                                df_interact['target_2'].isin(selected_targets)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'target_1', 'target_2', 'weight')

    # Initiate PyVis network object
    drug_net = Network(height='800px', width='100%', bgcolor='#222222', font_color='white')

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout settings
    drug_net.repulsion(node_distance=420, central_gravity=0.33,
                    spring_length=110, spring_strength=0.10,
                    damping=0.95)

# Save and read graph as HTML file (on Streamlit Sharing)
try:
    path = 'tmp'
    try:
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')
    except:
        pass

# Save and read graph as HTML file (locally)
except:
    path = 'html_files'
    try:
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')
    except:
        pass

# Load HTML into HTML component for display on Streamlit
try:
    components.html(HtmlFile.read(), height=800)
except:
    pass
