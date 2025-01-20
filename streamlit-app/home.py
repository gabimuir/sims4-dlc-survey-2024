import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly 
import streamlit as st

sns.set_style('white')

st.set_page_config(
    page_title="Sims4 DLC Survey"
)

def header():
    st.header("2024 Sims 4 DLC Survey Analysis")

def data_source():
    '''
    wait will it publish this too or does it know this is how ppl usually code their comments?
    '''
    st.header("Data Background")
    st.link_button("Link to James' Website and 2024 Survey Results", 
                    url = 'https://jamesturner.yt/sims-pack-ratings/2024',
                    icon = '📊',
                    type = 'primary'
                   )
    '''
    Sims Youtuber JamesTurnerYT (formerly known as the SimSupply) created a survey on his website and asked his subscribers 
    to respond. 
    
    The survey asks to self-describe a "play style", then give a rating 
    for each DLC pack they own. If they did not own a pack, they were asked to rank their likelihood of ever getting it. 
    '''
    st.link_button("James' video on pack scores",
                   url = 'https://youtu.be/i90rK_zEpL0?si=KOTUqhz_-sp6aKA5',
                   icon = '🎥'
                   )
    '''
    I focused my analysis on the survey respondent data. 
    Which packs do people own? Do they want packs they don't own? Does playstyle correlate
    to pack ownership?  
    '''
   

def explain_sims():
    st.markdown('#### Background on the Sims')
    exp = st.expander('## What is a DLC?')
    exp.markdown(
        '''
        DLC stands for "Downloadable Content". In the Sims, it refers to additional packs of content that are purchasable outside of the base game.

        #### Expansion Packs
        **Avg Price**: $50

        These are the biggest DLC. They're meant to include many features including:
        * New outfits
        * New furniture, wallpapers, and floors
        * New gameplay features (for example: weather; or a more intricate romance system)
        * A new environment (world) 

        #### Game Packs
        **Avg Price**: $30

        These packs include some of the features of an Expansion, but are more focused on one theme. 
        The amount of items is smaller, and the gameplay feature is very focused. 

        Examples:
        * Vampires added
        * Restaurants added

        #### Stuff Packs
        **Avg Price**: $15
        
        These packs were originally just "Stuff" (new clothes and build items, one tiny gameplay feature) 
        until Tiny Living (2020), when stuff packs started including much more substantial gameplay features. 
        Overall, there are still limited features compared to Game Packs. 
        
        For example, Tiny Living introduced gameplay mechanics where living in a "tiny home" gives skill bonuses. 
        It also included a few clothes and some furniture

        #### Kits
        **Avg Price**: $5

        Kits were newly introduced in 2021, at the lowest price point. These have very limited content, and, up until 2025,
        were limited to either "CAS Kits" or "Build Kits" depending on if they including clothing (CAS) or furniture, wallpaper, 
        windows and doors (build). There was also one initial "Gameplay" kit - Bust the Dust (where the main feature is adding vaccuums)
        '''
    )

    exp = st.expander('## What are these pack styles? "CAS"? "Build"? "Live?"')
    exp.markdown(
        '''
        In James' DLC survey, the respondent can choose "yes or no" to each of these aspects of play:

        #### CAS ("Create-a-Sim")
        This is the character creation mode, where the user can sculpt a face and body, and select outfits for their characters

        #### Build
        In the Sims, a player can create homes and community lots with build tools. 
        "Build" also includes furnishing those buildings with furniture and decorations.

        #### Live
        The Sims is ultimately a "life simulator" game, where you control characters through their lives. 
        This refers to the main gameplay aspects of the game, like growing up, starting romances, dying, etc.
        '''
    )

if __name__ == '__main__':
    header()
    data_source()
    explain_sims()
