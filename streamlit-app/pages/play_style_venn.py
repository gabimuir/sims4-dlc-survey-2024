import streamlit as st 

from get_data import prep_venn_playstyle, get_pack_info
from plot_methods import plot_venn_gamertype

def initialize():
    st.set_page_config(
        page_title="Sims4 DLC Survey"
    )
    '''
    # Create a Venn Diagram of Playstyles Based on Packs Owned
    Remove or add packs in the selector. Use the dropdown on the left to add suggested packs. 
    Use the slider to limit respondents to people with at most that many packs. 

    As total pack ownership decreases, it's more obvious which "play styles" own that pack
    '''

def sidebar(pack_info):
    '''
    Initialize a sidebar where the user can choose a selection of pack types to filter
    '''
    st.sidebar.markdown("Filters")

    default_filter: str = st.sidebar.selectbox(
        "Show Packs By",
        options = ['All', 'Expansion Packs', 'Game Packs', 'Stuff Packs', 
                   'All Kits', 'CAS Kits', 'Build Kits'],
        key = "default_filter",
        index = None,
        placeholder = 'Add Suggested Packs'
    )
    if default_filter in ['Expansion Packs', 'Game Packs', 'Stuff Packs']:
        default = pack_info[pack_info['pack_type'] == default_filter]['pack name'].to_list()
    elif default_filter == 'All':
        default = pack_info['pack name'].to_list()
    elif default_filter == 'All Kits':
        default = pack_info[pack_info['pack_type'] == 'Kits']['pack name'].to_list()
    elif default_filter == 'CAS Kits':
        default = pack_info[pack_info['kit_type'] == 'CAS']['pack name'].to_list()
    elif default_filter == 'Build Kits':
        default = pack_info[pack_info['kit_type'] == 'build']['pack name'].to_list()
    else:
        default = ['Bust The Dust Kit']

    # also add a slider to select the max packs those people own, to filter out people who have all of them
    num_packs = st.sidebar.slider(f'Max Total Packs Owned', 
                                  1,  # min
                                  len(pack_info['pack name'].to_list()),  # max
                                  10
     ) # default

    return default, num_packs

initialize()
pack_info = get_pack_info()
all_packs = pack_info['pack name'].drop_duplicates().to_list()

# initialize the sidebar, which also picks some to use in the picker
default, max_packs = sidebar(pack_info)
pack_list = st.multiselect(
    "Packs Owned", options = all_packs, default = default
)

to_plot = prep_venn_playstyle(pack_list, max_packs)
title = f'Owners of any of the packs selected as one of their at most {max_packs} total packs'
fig = plot_venn_gamertype(to_plot, title)
st.pyplot(fig)


exp = st.expander('Interpretation')
exp.markdown(
    '''
    There's more information available when you get down some of the people with all packs
    '''
)

# really cool idea: do some calculation against a baseline,
# then do a radar chart to plot. probably instead of the venn
# https://plotly.com/python/radar-chart/
# i imagine "all respondents" is baseline 1,1,1 
# and then up or down percent diff when filtered