import pandas as pd
import streamlit as st 
import numpy as np

# this code is meant to keep all of the data logic. The pages should hold mostly formatting and UI

github_path = 'https://raw.githubusercontent.com/gabimuir/sims4-dlc-survey-2024/refs/heads/main/tables/'

@st.cache_data
def get_promo_data():
    return pd.read_csv(github_path + 'all_promo_data.csv') 

@st.cache_data
def get_pack_info():
    '''
    Read the pack info (pack name, pack type) and add the additional info of the kit type (CAS/creator/etc)
    '''
    df = pd.read_csv(github_path + 'basic_pack_info.csv')
    kit_types = pd.read_csv(github_path + '../kit_types.csv')
    pack_info = pd.merge(left = df,
         right = kit_types,
         right_on = 'kit_name',
         left_on = 'pack name',
         how = 'left'
        ).drop('kit_name', axis = 1).sort_values('release date', ascending = False)
    return pack_info

@st.cache_data
def get_play_style_df():
    return pd.read_csv(github_path + 'play_styles_raw.csv').set_index('survey_id')

@st.cache_data
def get_purchase_data():
    return pd.read_csv(github_path + 'bought_and_not_all.csv')

@st.cache_data
def get_hist_all_data():
    return pd.read_csv(github_path + 'num_packs_owned_all.csv')

@st.cache_data
def get_packtype_hist_data():
    '''
    read the histogram data per pack type. Use T because survey_id was saved as the column instead of the row
    '''
    return pd.read_csv(github_path + 'per_player_per_type_count.csv').set_index('pack_type').T

@st.cache_data
def get_cluster_dfs():
    '''
    Open the clustering results for each pack type
    '''
    cluster_data = {
        'Kits': pd.read_csv(github_path + 'kit_pca_clusters.csv'),
        'Expansion Packs': pd.read_csv(github_path + 'clusters_expansions_3c.csv'),
        'Game Packs': pd.read_csv(github_path + 'cluster_game_packs.csv'),
        'Stuff Packs': pd.read_csv(github_path + 'cluster_stuff_packs.csv')
    }
    # set all the clusters as categorical variables
    for pt, df in cluster_data.items():
        df['cluster'] = df['cluster'].astype("category")

        # add a totals column for how many owners have each pack
        totals, total_respondents = prep_pack_ownership_promo( get_promo_data(), pack_type = pt, max_owned=81)
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
def prep_hist(df):
    '''
    Prep the data into a histogram format. df is two columns, survey_id and Num Packs Owned
    '''
    max_packs = df['Num Packs Owned'].max()
    total_resp = df.shape[0]
    hist_df = pd.DataFrame(df.set_index('survey_id').groupby('Num Packs Owned').value_counts())
    hist_df['percent'] = hist_df['count'] / total_resp 
    hist_df = hist_df.reset_index()
    return hist_df, max_packs

@st.cache_data
def get_radar_baseline():
    '''
    Create the counts for the baseline dist of play styles
    '''
    all_response = get_play_style_df()
    df = get_playstyle_counts(all_response)
    return df

@st.cache_data
def prep_pack_ownership_promo(df, pack_type = 'Kits', max_owned = 3, sorted_by = 'total'):
    '''
    Takes one pack type, and a designed max num owned and preps the data to plot the packs from 
    most owned to least (sorted_by total) or by pack release date ()
    '''
    # isolate which survey respondents had that many responses
    if pack_type == 'All':
        num_packs = df.groupby('survey_id')['pack name'].count().reset_index()
        # the column "pack name" becomes total packs
        lt_3_kits_list = num_packs[ (num_packs['pack name'] <= max_owned) ] ['survey_id'].to_list()
    else:
        num_packs = df.groupby(['survey_id', 'pack_type'])['pack name'].count().reset_index()
        # the column "pack name" becomes total packs
        lt_3_kits_list = num_packs[ 
                            (num_packs['pack_type'] == pack_type) & 
                            (num_packs['pack name'] <= max_owned) 
                            ] ['survey_id'].to_list()
    
    num_people = len(lt_3_kits_list)
    
    if pack_type == 'All':
        lt_3_data = df[(df['survey_id'].isin(lt_3_kits_list))]
    else:
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

    # prep to plot by adding percent and sorting by the selected
    per_pack_promo_kits['percent promo'] = per_pack_promo_kits['promo'] / per_pack_promo_kits['total'] 
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
def get_non_ownership_reason_data(pack_type='All', sorted_by='total'):
    '''
    Melt the df down into something for plotly to plot.
    '''
    df = get_purchase_data()
    if pack_type != 'All':
        # filter based on pack_type
        df = df[df['pack_type'] == pack_type]
    
    # sort here before melting by the user's choice
    owned = ['Own: Not Promo', 'Own: Promo']
    not_owned = ['Will buy', 'Might buy', 'Only on Sale', 'Only if Free', 'Never want it']
    responses = owned + not_owned

    # add total owners
    df['total ownership'] = df[owned].sum(axis = 1)
    df['not owned'] = df[not_owned].sum(axis = 1)

    # they have the same total respondents so just grab the first
    total_repondents = df[responses].sum(axis = 1).iloc[0]        
    df = df.sort_values(sorted_by)

    melted = pd.melt(
        df, 
        value_vars = responses,
        id_vars = ['release date', 'total ownership', 'pack name', 'pack_type'],
        var_name = 'pack ownership', value_name = 'count'
    )
    melted['percent'] = melted['count'] / total_repondents
    return melted

@st.cache_data
def filter_ownership_graph(data, filter):
    '''
    A user can select if they want to filter the graph to one type of result (similar to sorted_by)
    '''
    owned = ['Own: Not Promo', 'Own: Promo']
    not_owned = ['Will buy', 'Might buy', 'Only on Sale', 'Only if Free', 'Never want it']
    responses = owned + not_owned

    if filter in responses:
        filtered = data[data['pack ownership'] == filter]
    elif filter == 'Only Owners':
        filtered = data[data['pack ownership'].isin(owned)]
    elif filter == 'Only Non-Owners':
        filtered = data[data['pack ownership'].isin(not_owned)]
    else:
        # they selected "All" or I haven't written it in yet lol
        filtered = data 
    return filtered

@st.cache_data
def prep_playstyle_df(pack_list, max_packs):
    '''
    Filter the play style to specific survey respondents based on filters. If 
    '''
    if len(pack_list) < 1:
        return pd.DataFrame(columns = ['player_cas', 'player_live', 'player_build'])
    
    # from promo_data we see each survey_id and which packs they own
    df = get_promo_data() 

    # first filter to respondents with less than the max num packs, then filter to respondents with that many
    num_packs = df.groupby(['survey_id'])['pack name'].count().reset_index().rename(columns = {'pack name': 'pack count'})
    lt_x_packs = num_packs[ (num_packs['pack count'] <= max_packs) ] ['survey_id'].to_list()

    # filter by pack owner and total pack ownership
    owner_list = df[(df['pack name'].isin(pack_list)) & (df['survey_id'].isin(lt_x_packs))
                     ]['survey_id'].drop_duplicates().to_list()
    play_style_df = get_play_style_df().loc[owner_list]
    return play_style_df

@st.cache_data
def prep_venn_playstyle(play_style_df):
    '''
    Get the play style df for this set of packs, then format for the venn diagram (with unique entries)
    '''
    # replace true/false with the index to become a unique value for the venn diagram set
    for_set = play_style_df.T.apply(
        lambda x: np.where(x, str(x.name), np.nan)
        ).T.reset_index().set_index('survey_id')
    return for_set

@st.cache_data
def get_playstyle_counts(df):
    '''
    Use value_counts to get the count of each playstyle combination, 
    then rename to prettify and put in order
    '''
    totals = pd.DataFrame(df.value_counts())
    new_index = totals.reset_index()[['player_cas', 'player_build', 'player_live']].apply(
            lambda x: np.where(x, str(x.name).split('_')[1], np.nan)
            ).apply(lambda x: ','.join(x).replace('nan,','').replace(',nan',''), axis = 1)
    cat_order = ['cas,build,live', 'build,live', 'live', 'cas,live', 'cas', 'cas,build', 'build']
    cat_type = pd.CategoricalDtype(categories=cat_order, ordered=True)
    totals.index = new_index.astype(cat_type)
    totals['percent'] = totals['count'] / df.shape[0]
    return totals

@st.cache_data
def get_radar_diffs(play_style_df):
    '''
    Calculate the difference in play styles between this set of packs and baseline (all respondents)
    '''
    totals = get_radar_baseline()
    counts = get_playstyle_counts(play_style_df)
    diffdf = pd.merge(
        left = counts,
        right = totals.rename(columns = {'percent': 'baseline %', 'count': 'baseline total'}),
        right_index = True,
        left_index = True
    )
    diffdf['percent diff'] = (diffdf['percent'] - diffdf['baseline %']) * 100
    diffdf.index = diffdf.index.rename('play style')
    diffdf = diffdf.reset_index().sort_values('play style')
    return diffdf