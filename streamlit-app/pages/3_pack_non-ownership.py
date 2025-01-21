import streamlit as st 

from get_data import get_non_ownership_reason_data, filter_ownership_graph, get_purchase_data
from plot_methods import plot_percent_owner

def initialize():
    st.set_page_config(
        page_title="Sims4 DLC Survey"
    )
    '''
    # Pack Non-Ownership
    ### Do People Want Packs They Don't Own?

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
        index = 2,
        placeholder = 'Limit bars shown'
    )

    return pack_type, sorted_by, filter_by

def interpretation():
    '''
    Write in some interpretations with examples of what to look for
    '''
    exp = st.expander('Interpretation')
    exp.markdown(
    '''
    ### Waiting for Sales
    Sorting by "release date", showing only "Only on Sale" shows which packs people don't have but want if it were on sale.
    There's a trend where more recent release dates have a higher percent of people wanting it on sale. 

    ### Favorite Kit: Blooming Rooms
    **Sort by Kits only + Order by "Own: Not Promo" + Show Only "Only Owners"**

    Sorting by kits based on ownership ("total onwership") shows that Blooming Rooms is the most popular kit. 
    A large proportion of people (24% of respondents) got Blooming Rooms via promo ("own: promo").
    
    Interesting, even with that massive giveaway, Blooming Rooms is the #1 kit based only on
    purchases ("own: not promo") (51% of respondents).
    
    ### Most Hated Pack: Batuu
    **Sort by "Never want it", show only "Only non-owners"**

    Certain packs are very polarizing, where people don't even want it in their game even if it were free. 
    "Star Wars: Journey to Batuu" is basically a meme in the sims community because people hate it so much. 
    It checks out that it has the highest percent of people saying they never want it.

    Sorting by "never want it" also correlates with a decrease in people responding more positively with answers like
    "only on sale", "might buy" or "will buy"
    
    '''
    )

initialize()
pack_type, sorted_by, filter_by = sidebar()
data = get_non_ownership_reason_data(pack_type, sorted_by )
filtered = filter_ownership_graph(data, filter_by)

'''
Use the options on the left to select certain packs and sort by response. Choose certain responses to "show only" to minimize visual
clutter.

Hover over the plot to see more details
'''
fig = plot_percent_owner(filtered, sorted_by)
st.plotly_chart(fig)

interpretation()

exp = st.expander('Raw Data')
exp.dataframe(get_purchase_data())
