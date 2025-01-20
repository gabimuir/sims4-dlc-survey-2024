import streamlit as st 

from get_data import get_hist_all_data, get_packtype_hist_data, prep_hist
from plot_methods import plot_ownership_hist

def initialize():
    st.set_page_config(
        page_title="Sims4 DLC Survey"
    )
    '''
    # Pack Ownership
    ### How many packs do people own?

    Histogram of ownership. Use the dropdown in the side bar to show based on pack type.

    Page [limited pack owners](https://sims4-dlc-survey-2024-analysis.streamlit.app/limited_pack_owners) goes into detail on what packs people own, if they only own a few
    '''

def sidebar():
    '''
    This is where the sliders go for changing the variables
    '''
    st.sidebar.markdown("Choose your filters")
    pack_type = st.sidebar.selectbox( 
        "Show Packs By",
        options = ['All', 'Expansion Packs', 'Game Packs', 'Stuff Packs', 'Kits'],
        key = "default_filter",
        index = 0,
        placeholder = 'Filter by pack type'
    )
    return pack_type

initialize()
pack_type = sidebar()

if pack_type == 'All':
    data = get_hist_all_data()
else:
    data = get_packtype_hist_data()[[pack_type]].reset_index()
    data.columns = ['survey_id', 'Num Packs Owned']

hist_df, max_packs = prep_hist(data)

fig = plot_ownership_hist(hist_df, pack_type, max_packs)
st.plotly_chart(fig)

exp = st.expander('raw data')
exp.dataframe(hist_df)



