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

exp2 = st.expander('Interpretation')
exp2.markdown(
    '''
    ##### Zero Packs
    From all pack ownership, it's interesting that 0 respondents said they own 0 packs. The base game has been free since 2022
    and while there have been various pack promos over the years, out of 15000+ respondents, none said they only have base game.

    ##### Every Pack
    I can believe that many people are "completionists," wanting to own every pack available. That 11% of respondents were all
    completionists feels a bit higher than I expected. There was a button to select on the survey that autopopulated all packs, so 
    that's a possible source of bias.

    ##### Kits
    The Kits distribution looks different than the other distributions in that more people have either a handful (0-5) or all 33.
    The spike up at 33 could be from the bias of selecting all.

    Page [limited pack owners](https://sims4-dlc-survey-2024-analysis.streamlit.app/limited_pack_owners) goes into detail on what packs
    people *do* own, if they only own a few
    '''
)

exp = st.expander('raw data')
exp.dataframe(hist_df)



