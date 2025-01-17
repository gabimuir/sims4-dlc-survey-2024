import pandas as pd
import streamlit as st 
import numpy as np

# this code is meant to keep all of the data logic. The pages should hold mostly formatting and UI

@st.cache_data
def open_promo_data():
    return pd.read_csv('../tables/all_promo_data.csv') 

@st.cache_data
def get_pack_info():
    '''
    Read the pack info (pack name, pack type) and add the additional info of the kit type (CAS/creator/etc)
    '''
    df = pd.read_csv('../tables/basic_pack_info.csv')
    kit_types = pd.read_csv('../kit_types.csv')
    pack_info = pd.merge(left = df,
         right = kit_types,
         right_on = 'kit_name',
         left_on = 'pack name',
         how = 'left'
        ).drop('kit_name', axis = 1).sort_values('release date', ascending = False)
    return pack_info

@st.cache_data
def get_play_style_df():
    return pd.read_csv('../tables/play_styles_raw.csv').set_index('survey_id')

@st.cache_data
def get_cluster_dfs():
    '''
    Open the clustering results for each pack type
    '''
    cluster_data = {
        'Kits': pd.read_csv('../tables/kit_pca_clusters.csv'),
        'Expansion Packs': pd.read_csv('../tables/clusters_expansions_3c.csv'),
        'Game Packs': pd.read_csv('../tables/cluster_game_packs.csv'),
        'Stuff Packs': pd.read_csv('../tables/cluster_stuff_packs.csv')
    }
    # set all the clusters as categorical variables
    for pt, df in cluster_data.items():
        df['cluster'] = df['cluster'].astype("category")

        # add a totals column for how many owners have each pack
        totals, total_respondents = prep_pack_ownership_promo( open_promo_data(), pack_type = pt, max_owned=81)
        with_totals = pd.merge(
            left = df,
            right = totals[['total']].rename(columns = {'total': 'total owners'}),
            right_index = True, # index is pack name
            left_on = 'pack name'
        )
        cluster_data[pt] = with_totals
    return cluster_data

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

@st.cache_data
def prep_venn_playstyle(pack_list, max_packs):
    '''
    Filter the play style to specific survey respondents based on filters. If 
    '''
    if len(pack_list) < 1:
        return pd.DataFrame(columns = ['player_cas', 'player_live', 'player_build'])
    
    # from promo_data we see each survey_id and which packs they own
    df = open_promo_data() 
    # first filter to respondents with less than the max num packs
    num_packs = df.groupby(['survey_id', 'pack_type'])['pack name'].count().reset_index()

    # isolate which survey respondents had that many responses
    lt_x_packs = num_packs[ (num_packs['pack name'] <= max_packs) ] ['survey_id'].to_list()

    # filter by pack owner and total pack ownership
    owner_list = df[(df['pack name'].isin(pack_list)) & (df['survey_id'].isin(lt_x_packs))
                     ]['survey_id'].drop_duplicates().to_list()
    play_style_df = get_play_style_df().loc[owner_list]

    # replace true/false with the index to become a unique value for the venn diagram set
    for_set = play_style_df.T.apply(
        lambda x: np.where(x, str(x.name), np.nan)
        ).T.reset_index().set_index('survey_id')
    
    return for_set

    