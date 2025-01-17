import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from get_data import count_num_packs
from matplotlib_venn import venn3

def get_colors():
    '''
    Returns the custom colormap, but also sets the defaults
    '''
    sns.set_style('white')

    color_map_raw = {
        'Expansion Packs': (13,191,191), # teal
        'Expansion Packs_dark': (8, 59, 64), # dark teal
        'Game Packs': (43,0,255), # royal blue/purple
        'Game Packs_dark': (35, 129, 222), # blue
        'Stuff Packs': (100,196,60), # green
        'Stuff Packs_dark': (42, 115, 11), # green
        'Kits': (143,51,170), # pink/purple
        'Kits_dark': (51, 6, 64), # pink/purple
        'player_cas': (48,155,46), # green
        'player_build': (202,113,43), # orange
        'player_live': (33,135,207), # blue
        'cas': (48,155,46), # green
        'build': (202,113,43), # orange
        'live': (33,135,207), # blue
        'gray': (37,38,38),
        'bugs': (119, 48, 166) # bugs purple
    }

    # this is how seaborn/matplotlib likes it
    color_map = {}
    for name, (r,g,b) in color_map_raw.items():
        new_rgb = ( r / 255.0, g / 255.0, b / 255.0, 1 )
        color_map[name] = new_rgb

    # this is how plotly uses it
    for name, (r,g,b) in color_map_raw.items():
        color_map[name] = f'rgb({r}, {g}, {b})'
        

    plt.rcParams.update({
        'font.family': 'sans serif',
        'font.size': 14,
        'axes.labelsize': 12,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'font.weight': 'normal'
    })

    return color_map


def plot_percent_promo_plotly(to_plot, pack_type, max_owned, sorted_by, num_people='?'):
    '''
    Plot a histplot type figure for the top packs owned by a certain number,
    and whether they got them on promo using Plotly.
    '''
    color_map = get_colors()
    if max_owned == count_num_packs(pack_type):
        title = f'{pack_type} owned by people with any (n = {num_people})'
    else:
        title = f'{pack_type} owned by people with <= {max_owned} total (n = {num_people})'

    fig = px.bar(
        to_plot.reset_index(), 
        x = "pack name", 
        y = 'count',
        color = 'pack promotion',
        title = title,   
        barmode='stack',
        color_discrete_sequence = [color_map[f'{pack_type}_dark'], color_map[pack_type]],
        custom_data = [to_plot['release date'], to_plot['total'], to_plot['percent promo']] #to use in the tooltip
    )
    fig.update_traces(
        hovertemplate="<b>Pack Name:</b> %{x}<br>"  
                      + "<b>Release Date:</b> %{customdata[0]}<br>"
                      + "<b>Owner Count:</b> %{customdata[1]}<br>"  
                      + "<b>Percent Promo:</b> %{customdata[2]:.1%}<br>"  
                      + "<extra></extra>",  # Hide extra info
    )
    fig.update_layout(
        xaxis_title = f'Pack Name (ordered by {sorted_by})',
        yaxis_title = 'Owner Count',
        xaxis = dict( tickangle = 90 ),
        showlegend = True,
        width = 1000,
        height = 600
    )
    
    return fig

def plot_venn_gamertype(for_set, title = ''):
    fig, ax = plt.subplots(figsize = (10,10), dpi = 200)
    venn3([set(for_set['player_cas'].to_list()),
        set(for_set['player_build'].to_list()),
        set(for_set['player_live'].to_list())
        ], 
        ('CAS', 'Build', 'Live'),
        )
    if title:
        plt.title(title)
    return fig