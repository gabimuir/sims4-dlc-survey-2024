import streamlit as st 

from get_data import get_non_ownership_reason_data, filter_ownership_graph, get_purchase_data
from plot_methods import plot_percent_owner

def initialize():
    st.set_page_config(
        page_title="Sims4 DLC Survey"
    )
    '''
    # Will People Get Packs They Don't Own?

    Look into ownership data and responses for likelihood of getting it
    '''

def sidebar():
    '''
    This is where the sliders go for changing the variables
    '''
    st.sidebar.markdown("Choose your filters")

    pack_type: str = st.sidebar.selectbox(
        "Show Packs by Type",
        options = ['All', 'Expansion Packs', 'Game Packs', 'Stuff Packs', 'Kits'],
        key = "pack-type-selector",
        index = 0,
        placeholder = 'Filter to pack type'
    )
    responses = ['Own: Promo', 'Own: Not Promo', 'Will buy', 
                      'Might buy', 'Only on Sale', 'Only if Free', 'Never want it']
    
    sorted_by = st.sidebar.selectbox(
        "Sorted by",
        options = ['total ownership', 'release date'] + responses,
        key = "sorted_by",
        index = 0,
        placeholder = 'Choose the sorting direction'
    )

    filter_by = st.sidebar.selectbox(
        "Show only",
        options = ['Show All', 'Only Owners', 'Only Non-Owners'] + responses,
        key = "filter",
        index = 0,
        placeholder = 'Choose the sorting direction'
    )

    return pack_type, sorted_by, filter_by

def interpretation(pack_type):
    '''
    Text for some key interpretations of each pack type
    '''
    '''
    ### Interpretation:
    '''

initialize()
pack_type, sorted_by, filter_by = sidebar()
data = get_non_ownership_reason_data(pack_type, sorted_by )
filtered = filter_ownership_graph(data, filter_by)

'''
Use the options on the left to select certain packs and sort by response
'''
fig = plot_percent_owner(filtered, sorted_by)
st.plotly_chart(fig)

'''
Interpretation

'''

exp = st.expander('Raw Data')
exp.dataframe(get_purchase_data())
