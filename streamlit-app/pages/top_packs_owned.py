import streamlit as st 

from get_data import open_promo_data, prep_pack_ownership_promo, count_num_packs, melt_for_plotly
from plot_methods import plot_percent_promo_plotly

def initialize():
    st.set_page_config(
        page_title="Top Packs Owned"
    )

def sidebar(df):
    '''
    This is where the sliders go for changing the variables
    '''
    st.sidebar.markdown("Choose your filters")

    pack_list = sorted(list(set(df['pack_type'].to_list())))
    pack_type: str = st.sidebar.selectbox(
        "Pack Type",
        options = pack_list,
        key = "pack_type",
    )

    max_owned = st.sidebar.slider(f'Max {pack_type} owned', 
                                  0,  # min
                                  count_num_packs(pack_type),  # max
                                  count_num_packs(pack_type)) # default
    
    sorted_by = st.sidebar.radio(
        "Sorted by",
        options = ['total', 'release date'],
        key = "sorted_by",
    )

    return pack_type, max_owned, sorted_by

def interpretation(pack_type):
    '''
    Text for some key interpretations of each pack type
    '''
    '''
    ### Interpretation:
    '''


initialize()
data = open_promo_data()
pack_type, max_owned, sorted_by = sidebar(data)
to_plot, num_respondents = prep_pack_ownership_promo(data, pack_type, max_owned, sorted_by )

if max_owned == count_num_packs(pack_type):
    f'''
    ## You selected survey respondents with any {pack_type}
    '''
else:
    f'''
    ## You selected survey respondents with at most {max_owned} {pack_type}
    '''
'''
Use the slider on the left to see how pack popularity changes as people own more/less packs
'''

if max_owned == count_num_packs(pack_type):
    f'''
    Total survey respondents with any {pack_type}: {num_respondents}
    '''
else:
    f'''
    Total survey respondents with at most {max_owned} {pack_type}: {num_respondents}
    '''

melted_plotter = melt_for_plotly(to_plot, pack_type)
plotlyplot = plot_percent_promo_plotly(melted_plotter, pack_type, max_owned, sorted_by, num_respondents)
st.plotly_chart(plotlyplot)

interpretation(pack_type)

'''

### Raw data:
'''
st.dataframe(to_plot)
