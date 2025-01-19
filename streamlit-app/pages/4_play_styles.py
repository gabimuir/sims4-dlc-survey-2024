import streamlit as st 
import pandas as pd

from get_data import prep_venn_playstyle, get_pack_info, get_radar_diffs, prep_playstyle_df, get_playstyle_counts, get_radar_baseline
from plot_methods import plot_venn_gamertype, plot_radar

def initialize():
    st.set_page_config(
        page_title="Sims4 DLC Survey"
    )
    '''
    # Play Styles
    ### Respondents were asked to self-describe a play style, and could select more than one. 

    Use the selector below to view play styles for a selected pack. Multiple packs can be chosen at once.
     
    Use the dropdown on the left sidebar to add suggested packs. The slider limits respondents to 
    people with at most that many packs. As total pack ownership decreases, the effect of play styles is more obvious.
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
                                  18
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

# venn and radar plot share the same entry data. Reduce calcs and have it available to display
playstyle_df = prep_playstyle_df(pack_list, max_packs)

# put this below the selection bar
title = f'Owners of any of [{", ".join(pack_list)}] as one of their (at most) **{max_packs} total** packs. \
    (Applies to {playstyle_df.shape[0]} respondents)'
st.markdown(title)

# plot the radar plot
to_plot_radar = get_radar_diffs(playstyle_df)
if len(pack_list) == 1:
    title = 'The difference in play style responses (%) for this pack vs baseline'
else:
    title = 'The difference in play style responses (%) for these packs vs baseline'
fig = plot_radar(to_plot_radar, title)
st.plotly_chart(fig)
# prefer this below the plot to being the actual title of the plot


st.markdown('##### Play styles as a venn diagram')
to_plot_venn = prep_venn_playstyle(playstyle_df)
title = f'Owners of any of the packs selected as one of their (at most) {max_packs} total packs'
fig = plot_venn_gamertype(to_plot_venn, title)
st.pyplot(fig)

def display_df(df):
    '''
    Format the dataframes for display inc sorting and printing percent as percent
    '''
    df = df.reset_index().sort_values('index')
    df['percent'] = df['percent'].apply(lambda x: str(f'{x:.2%}'))
    return df 

exp2 = st.expander('Raw data')
# display the data as counts of each section instead of long raw data
to_plot_radar['percent'] = to_plot_radar['percent'].apply(lambda x: str(f'{x:.2%}'))
to_plot_radar['baseline %'] = to_plot_radar['baseline %'].apply(lambda x: str(f'{x:.2%}'))
to_plot_radar['percent diff'] = to_plot_radar['percent diff'].apply(lambda x: str(f'{x:.2}%'))
exp2.dataframe(to_plot_radar.drop('baseline total', axis = 1), hide_index = True)

exp = st.expander('Interpretation')
exp.markdown(
    '''
    #### Bust the Dust
    There's more information available when you get down some of the people with all packs. For example, with the Bust the Dust Kit
    (the only "gameplay" kit to date), looking at Bust the Dust owners in total shows that slightly more than usual respondents were
    all 3 styles. But, dragging max_packs down to ~18 packs, "Live Mode" style players really jumps out. This aligns with what we know 
    about the pack itself, which is that it focuses on Live Mode, so it makes sense that people who prioritized this pack as 
    one of only 18 packs say they care most about Live Mode.

    #### CAS Kits Overall
    When people own any CAS kits as one of any of their kits, the biggest play style diff is in all 3. When their CAS Kit becomes one of
    fewer packs (say, 32), more people jump out as only caring about CAS.
    '''
)