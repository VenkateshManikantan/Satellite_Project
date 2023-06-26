# UI libraries 
import streamlit as st
from streamlit_folium import folium_static
import folium
# Data libraries 
import pandas as pd 
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt
import ee
import geemap.foliumap as geemap
plt.rcParams["figure.figsize"] = (10,10)

# Custom Scripts libraries
from utli_img import npy_to_img 
from utli_img import normalize_img 
from utli_img import cmap_agri
from util_file import get_dir
from util_file import find_between


st.set_page_config(layout="wide")


if st.session_state['auth'] == False:
    st.error('Login Required')

if st.session_state['auth'] == True:
    st.write(st.session_state['auth'])
    st.title("Plant Health Monitor:")

    
