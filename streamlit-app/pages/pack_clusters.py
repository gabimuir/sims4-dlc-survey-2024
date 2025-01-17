import streamlit as st 

from get_data import get_cluster_dfs, get_pack_info
from plot_methods import plot_cluster_plots

def initialize():
    st.set_page_config(
        page_title="Clustering Packs"
    )
    '''
    # Pack Clusters Based on Ownership
    Based *only* on what packs people own, we can make clusters of packs.
    '''

    '''
    Use the sidebar to select a different pack type
    '''

initialize()

def sidebar():
    '''
    This is where the sliders go for changing the variables
    '''
    st.sidebar.markdown("Choose your filters")
    df = get_pack_info()
    pack_list = sorted(list(set(df['pack_type'].to_list())))
    pack_type: str = st.sidebar.selectbox(
        "Pack Type",
        options = pack_list,
        index = 1, # initialize with Game Packs
        key = "pack_type",
    )
    return pack_type

# initialize the sidebar and get a pack type to display
pack_type = sidebar()
cluster_dfs = get_cluster_dfs()

fig = plot_cluster_plots(cluster_dfs[pack_type], pack_type)
st.plotly_chart(fig)

exp3 = st.expander('Data Tables')

for cluster, cluster_df in cluster_dfs[pack_type].groupby('cluster'):
    exp3.markdown(f'*Packs in Cluster {cluster}*')
    if pack_type == 'Kits':
        to_disp = cluster_df[['pack name', 'release date', 'total owners', 'kit_type']].sort_values('release date')
    else:
        to_disp = cluster_df[['pack name', 'release date', 'total owners']].sort_values('release date')
    
    # make it all print instead of adding a scroll
    height = (to_disp.shape[0] + 1) * 36
    exp3.dataframe(to_disp, hide_index = True, height = height)

exp2 = st.expander('Interpretation')
exp2.markdown(
    '''
    ## Interpretation
    The clustering algorithm ONLY had access to which packs people had, it doesn't know anything about the packs themselves.

    * In Game Packs, the X-axis looks like popularity, while the y-axis looks like a measure of "realism". 
    The supernatural packs (Werewolves, Vampires, and Realm of Magic) clearly cluster separately from the more realistic packs.

    * In Kits, the clustering was clearly able to pick out the CAS kits vs BUILD kits.

    Generally, this could mean that if a person buys a few CAS kits, they might buy more than one, but maybe not a BUILD kit.

    And if a person avoided Vampires, they might be more likely to avoid Werewolves and Realm of Magic, too.
    '''
)

expander = st.expander('Methodology')
expander.markdown(
    '''
    Principal Component Analysis was done to plot the owners into dimensional space, then K-Means clustering was done 
    Clusters were chosen based on manual review of performance of clustering at 2, 3, or 4 clusters.

    I separated the clustering by pack type because the first PC was mostly pack type
    '''
)