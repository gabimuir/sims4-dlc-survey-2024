import streamlit as st 

from get_data import get_cluster_dfs, get_pack_info
from plot_methods import plot_cluster_plots

def initialize():
    st.set_page_config(
        page_title="Sims4 DLC Survey"
    )
    '''
    # Pack Clusters Based on Ownership
    ##### Based *only* on what packs people own, we can make clusters of packs.

    '''

    '''
    Use the sidebar to select a different pack type. Hover over the plots to see which packs are in which clusters.
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

st.markdown('#### Cluster Data Tables')

for cluster, cluster_df in cluster_dfs[pack_type].groupby('cluster'):
    st.markdown(f'*Packs in Cluster {cluster}*')
    if pack_type == 'Kits':
        to_disp = cluster_df[['pack name', 'release date', 'total owners', 'kit_type']].sort_values('release date')
    else:
        to_disp = cluster_df[['pack name', 'release date', 'total owners']].sort_values('release date')
    
    # make it all print instead of adding a scroll
    height = (to_disp.shape[0] + 1) * 36
    st.dataframe(to_disp, hide_index = True, height = height)

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
    The input data is a dataframe of survey respondents (rows) by packs owned (columns), where pack ownership was listed
    as True or False for each respondent.

    The x and y positions graphed are the PC1 and PC2 of a Principle Component analysis on the input data, where
    features were packs owned. PCA converts multiple features (packs owned) into a smaller dimensional space.
    
    PCA was first done on the packs as whole, but the first PC was clearly "pack type" (expansion vs kit, etc), so 
    PCA was done on each set of pack types separately.

    Using the PCA results, K-Means clustering was done on each set of pack types.
    Cluster size was chosen based on manual review of performance of clustering at 2, 3, or 4 clusters for each pack type.

    See jupyter notebook in github for more details
    '''
)