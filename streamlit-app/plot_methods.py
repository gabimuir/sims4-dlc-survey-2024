import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from get_data import count_num_packs

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

    color_map = {}
    for name, (r,g,b) in color_map_raw.items():
        new_rgb = ( r / 255.0, g / 255.0, b / 255.0, 1 )
        color_map[name] = new_rgb
        

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


def plot_percent_promo(to_plot, pack_type, max_owned, sorted_by, num_people='?'):
    '''
    Plot a histplot type figure for the top packs owned by a certain number, and whether they got them on promo
    '''
    color_map = get_colors()
    fig, ax = plt.subplots(figsize = (12,8), dpi = 200)

    to_plot.plot.bar(
        stacked = True,
        color = {'not promo': color_map[pack_type],
                 'promo': color_map[f'{pack_type}_dark']},
        ax = ax,
        width = 1,
        edgecolor = color_map['gray']
    )
    max_packs = count_num_packs(pack_type)

    if max_owned == max_packs:
        title = f'{pack_type} owned by people with all {pack_type} (n = {num_people})'
    else:
        title = f'{pack_type} owned by people with <= {max_owned} {pack_type} total (n = {num_people})'

    ax.set_title(title)
    ax.set_ylabel('Owner Count')
    ax.set_xlim((-0.5, max_packs - 0.5))
    ax.set_xlabel(f'Pack Name (ordered by {sorted_by})')

    return fig 