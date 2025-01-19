# Sims 4 2024 DLC Survey Results Analysis

This is a personal project based on the data from [JamesTurnerYT's 2024 Sims 4 DLC Survey](https://jamesturner.yt/sims-pack-ratings/2024)

## Streamlit App
Access the streamlit app [here](https://sims4-dlc-survey-2024-analysis.streamlit.app/)

## Data Analysis
The Jupyter notebook contains all the background data analysis done to set up the streamlit app's input data.

It's not a fully finished product, partially train of thought and not perfectly organized. 

### Requirements
It's recommended to set up a new conda environment to include all the necessary packages
```
conda create -n data-review jupyter seaborn matplotlib==3.7 scikit-learn pandas numpy conda-forge::matplotlib-venn beautifulsoup4 statsmodels prince kmodes openpyxl conda-forge::altair plotly::plotly conda-forge::jupyterlab-plotly-extension
pip install streamlit
pip install watchdog # increases performance on mac 
```