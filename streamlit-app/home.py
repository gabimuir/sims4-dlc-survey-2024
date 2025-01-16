import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly 
import streamlit as st

sns.set_style('white')

st.set_page_config(
    page_title="Sims4 2024 DLC Analysis"
)

def header():
    st.header("2024 Sims 4 DLC Survey Analysis")
    '''
    Testing if this writes subheader. 
    '''

def data_source():
    '''
    wait will it publish this too or does it know this is how ppl usually code their comments?
    '''
    st.header("Background on the Data")
    '''
    For more background on the Sims, see below. The data was ...

    [Link to James' Website](https://jamesturner.yt/sims-pack-ratings/2024)
    '''

def explain_sims():
    st.header('Background on the Sims 4 DLC')
    '''
    ## What is a 'DLC'?
    DLC stands for ... uh

    ##
    '''

if __name__ == '__main__':
    header()
    data_source()
    explain_sims()
