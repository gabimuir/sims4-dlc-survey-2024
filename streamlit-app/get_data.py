import pandas as pd
import streamlit as st 

# this code is meant to keep all of the data logic. The pages should hold mostly formatting and UI

@st.cache_data
def open_promo_data():
    return pd.read_csv('../tables/all_promo_data.csv') 

@st.cache_data
def get_pack_info():
    pack_info = pd.read_csv('../tables/basic_pack_info.csv')
    return pack_info

@st.cache_data
def count_num_packs(pack_type):
    '''
    For one pack type, returns total count of packs
    '''
    df = get_pack_info()
    return len(df[df['pack_type'] == pack_type]['pack name'].to_list())

@st.cache_data
def prep_pack_ownership_promo(df, pack_type = 'Kits', max_owned = 3, sorted_by = 'total'):
    '''
    Takes one pack type, and a designed max num owned and preps the data to plot the packs from 
    most owned to least (sorted_by total) or by pack release date ()
    '''
    # prep data
    num_packs = df.groupby(['survey_id', 'pack_type'])['pack name'].count().reset_index()
    
    # isolate which survey respondents had that many responses
    lt_3_kits_list = num_packs[ 
                            (num_packs['pack_type'] == pack_type) & 
                            (num_packs['pack name'] <= max_owned) 
                            ] ['survey_id'].to_list()
    
    num_people = len(lt_3_kits_list)

    lt_3_data = df[
                    (df['survey_id'].isin(lt_3_kits_list)) &
                    (df['pack_type'] == pack_type)
                ]
    
    # count those packs
    promo = lt_3_data.groupby('pack name')[['promo']].sum().sort_values('promo')
    total = lt_3_data.groupby('pack name')[['promo']].count().rename(columns = {'promo': 'total'})
    per_pack_promo_kits = pd.merge(
        left = total,
        left_index = True,
        right = promo,
        right_index = True
    ).sort_values('promo')
    
    per_pack_promo_kits['not promo'] = per_pack_promo_kits['total'] - per_pack_promo_kits['promo']
    # add back in the pack info
    per_pack_promo_kits = pd.merge(
        left = get_pack_info(),
        left_on = 'pack name',
        right = per_pack_promo_kits,
        right_index = True,
        how = 'right'
    )

    per_pack_promo_kits['percent promo'] = per_pack_promo_kits['promo'] / per_pack_promo_kits['total'] 

    # prep for PLOT
    to_plot = per_pack_promo_kits.sort_values(sorted_by, ascending = False
                                ).drop(['total', 'release date'], axis = 1
                                      ).set_index('pack name')
    to_plot = per_pack_promo_kits.sort_values(sorted_by, ascending = False).set_index('pack name')
    return to_plot, num_people

@st.cache_data
def melt_for_plotly(to_plot, pack_type):
    '''
    Instead of having the stacked components as separate columns, have them as melted form.
    Then add a literal color variable
    '''
    def color_val(promo_state):
        if 'not' in promo_state:
            return f'{pack_type}_dark'
        else:
            return f'{pack_type}'

    df = to_plot.melt( value_vars = ['promo', 'not promo'], ignore_index = False, 
                      id_vars = ['release date', 'total', 'percent promo'],
                      var_name = 'pack promotion', value_name = 'count'
                       )
    df['color'] = df['pack promotion'].apply( color_val )
    return df