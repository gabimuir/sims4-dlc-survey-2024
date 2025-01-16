import streamlit as st 
import pandas as pd

from get_data import open_promo_data, plot_pack_ownership_promo, count_num_packs
from plot_methods import plot_percent_promo

def initialize():
    st.set_page_config(
        page_title="Top Packs Owned"
    )

    '''
    Use the slider on the left to see how pack popularity changes as people own more/less packs
    '''

def sidebar(df):
    # this is where I'll put all my sliders and stuff for changing the variables?
    st.sidebar.markdown("Something here...")

    pack_type: str = st.sidebar.selectbox(
        "Color theme",
        options = list(set(df['pack_type'].to_list())),
        key = "pack_type",
    )

    max_owned = st.sidebar.slider(f'Total {pack_type} owned', 
                                  0,  # min
                                  count_num_packs(pack_type),  # max
                                  count_num_packs(pack_type)) # default
    
    sorted_by = st.sidebar.radio(
        "Sorted by",
        options = ['total', 'release date'],
        key = "sorted_by",
    )

    if max_owned == count_num_packs(pack_type):
        f'''
        ## You selected survey respondents with all {pack_type}
        '''
    else:
        f'''
        ## You selected survey respondents with at most {max_owned} {pack_type}
        '''

    return pack_type, max_owned, sorted_by


initialize()
data = open_promo_data()
pack_type, max_owned, sorted_by = sidebar(data)
to_plot, num_respondents = plot_pack_ownership_promo(data, pack_type, max_owned, sorted_by )

if max_owned == count_num_packs(pack_type):
    f'''
    Total survey respondents with all {pack_type}: {num_respondents}
    '''
else:
    f'''
    Total survey respondents with at most {max_owned} {pack_type}: {num_respondents}
    '''

myplot = plot_percent_promo(to_plot, pack_type, max_owned, sorted_by, num_respondents)
st.pyplot(myplot)
'''

Raw data:
'''
st.dataframe(to_plot)
