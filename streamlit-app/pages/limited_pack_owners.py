import streamlit as st 

from get_data import get_promo_data, prep_pack_ownership_promo, count_num_packs, melt_for_plotly
from plot_methods import plot_percent_promo_plotly

def initialize():
    st.set_page_config(
        page_title="Sims4 DLC Survey"
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
    exp2 = st.expander('Interpretation')
    exp2.markdown('')


initialize()
data = get_promo_data()
pack_type, max_owned, sorted_by = sidebar(data)
to_plot, num_respondents = prep_pack_ownership_promo(data, pack_type, max_owned, sorted_by )

# i like ### level better but to match other pages just use #
st.markdown('# Total Pack Ownership and Promos')

'''
Use the slider on the left to see how pack popularity changes as people own more/less packs. Notice how
the percent of promo goes up as people own fewer packs
'''
st.markdown('')
if max_owned == count_num_packs(pack_type):
    st.markdown(f'#### You selected survey respondents with any {pack_type}')
else:
    st.markdown(f'#### You selected survey respondents with at most {max_owned} {pack_type}')

melted_plotter = melt_for_plotly(to_plot, pack_type)
plotlyplot = plot_percent_promo_plotly(melted_plotter, pack_type, max_owned, sorted_by, num_respondents)
st.plotly_chart(plotlyplot)

interpretation(pack_type)

exp = st.expander('Raw Data')
exp.dataframe(to_plot)
