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
    pack_type = st.sidebar.selectbox( 
        "Show Packs By",
        options = ['All', 'Expansion Packs', 'Game Packs', 'Stuff Packs', 'Kits'],
        key = "default_filter",
        index = 0,
        placeholder = 'Filter by pack type'
    )

    if pack_type in pack_list:
        max_packs = count_num_packs(pack_type)
    else:
        max_packs = 81 # sorry hardcoding
    
    max_owned = st.sidebar.slider(f'Max {pack_type} owned', 
                                  0,  # min
                                  max_packs,  # max
                                  10 # default
                                  )
    
    sorted_by = st.sidebar.radio(
        "Sorted by",
        options = ['total owners', 'release date', 'purchased (not promo)'],
        key = "sorted_by",
    )
    # clarify the text on the page, but use the real underlying sort order
    if sorted_by == 'purchased (not promo)':
        sorted_by = 'not promo'
    elif sorted_by == 'total owners':
        sorted_by = 'total'

    return pack_type, max_owned, sorted_by

def interpretation(pack_type):
    '''
    Text for some key interpretations of each pack type
    '''
    exp2 = st.expander('Interpretation')
    exp2.markdown(
        '''
        The aim of this page is to show more information on the promotions. Main question:
            
        **If people own only 3 Kits, did they just get the free ones?**

        Set pack type to "Kits" and max kits owned to the max of 33. If they own any number of kits, the
        three most popular are Blooming Rooms (32% promo), Desert Luxe (63% promo), and Book Nook (1.7% promo).

        Set max kits owned to 3, and now the top three are Blooming Room (now 74% promo), Desert Luxe (now 88% promo),
        and Fashion Street Set (94% promo). From all respondents Fashion Street Set is like 15th most popular, but from people
        who don't own many Kits its popularity is driven by the fact it was given away as part of a promotion.

        So, total pack ownership definitely impacts which packs are most popular
        ''')


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
if pack_type == 'All':
    pack_label = 'packs total'
else: 
    pack_label = pack_type
if max_owned == count_num_packs(pack_type):
    st.markdown(f'#### You selected survey respondents with any {pack_label}')
else:
    st.markdown(f'#### You selected survey respondents with at most {max_owned} {pack_label}')

melted_plotter = melt_for_plotly(to_plot, pack_type)
plotlyplot = plot_percent_promo_plotly(melted_plotter, pack_type, max_owned, sorted_by, num_respondents)
st.plotly_chart(plotlyplot)

interpretation(pack_type)

exp = st.expander('Raw Data')
exp.dataframe(to_plot)
