# UI libraries 
import streamlit as st
from streamlit_folium import folium_static
import folium
# Data libraries 
import pandas as pd 
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import ee
import geemap.foliumap as geemap
import cv2 
import plotly.express as px

# Custom Scripts libraries
from utli_img import normalize_img 
from utli_img import cmap_agri
from util_file import get_dir
from util_file import find_between



def value_to_class(value):
    if value == 0:
        #print("double_plant")
        return('normal_farm')
    if value == 30:
        #print("double_plant")
        return('double_plant')
    if value == 60:
        #print("drydown")
        return('drydown')
    if value == 90:
        #print("endrow")
        return('endrow')
    if value == 120:
        #print("nutrient_deficiency")
        return('nutrient_deficiency')
    if value == 150:
        #print("planter_skip")
        return('planter_skip')
    if value == 180:
        #print("water")
        return('water')
    if value == 210:
        #print("waterway")
        return('waterway')
    if value == 255:    
        #print("weed_cluster")
        return('weed_cluster')
    
#config: page layout
st.set_page_config(layout="wide")


if st.session_state['auth'] == False:
    st.error('Login Required')

if st.session_state['auth'] == True:
    #config: body
    st.title("Land Cover: Aerial ML Model:")

    file_n,path_n = get_dir("data\RGB")
    file          = st.selectbox("Select Image", path_n)
    button_0      = st.button('Run Segmentation Analysis')
    
   
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        image = cv2.imread(file)
        fig = px.imshow(image)
        st.write("RGB Image:")
        st.plotly_chart(fig)
        
        path_t = "data/nir/"
        key_a  = find_between(file,'RGB\\','.jpg')
        path_t = path_t + key_a + ".jpg"
        
        image2 = cv2.imread(path_t)
        fig2 = px.imshow(image2)

        st.write("Near Infrared Image:")
        st.plotly_chart(fig2)

    with col2:
        if button_0:
            path_t = "data/results_r101_mod/"
            key_a  = find_between(file,'RGB\\','.jpg')
            path_t2 = path_t + key_a + ".png"

            img = mpimg.imread(path_t2)
            img = img*255
            img[0,0] = 255

            fig3 = px.imshow(img,color_continuous_scale="portland")

            st.write("Segmentation Result:")
            st.plotly_chart(fig3)

            background = cv2.imread(file)
            overlay = cv2.imread(path_t2)

            added_image = cv2.addWeighted(background,0.3,overlay,0.5,0)
            fig4 = px.imshow(added_image)

            st.write("Segmentation Overlay:")
            st.plotly_chart(fig4)

    with col3:
        if button_0:
             pie1 = img
             val_p,count_p = np.unique(pie1,return_counts=True)
             df_pie = pd.DataFrame()
             df_pie['value'] = val_p
             df_pie['count'] = count_p
             df_pie['class'] = df_pie['value'].apply(value_to_class)
             
             df_pie = df_pie.drop(df_pie[df_pie["count"] < 2].index)
             
             

             fig5 = px.pie(df_pie,values='count', names='class',color='class',
                           color_discrete_map={
                            "normal_farm":"blue",
                            "weed_cluster": "#c40a29",
                            "double_plant": "#0B5B9D",
                            "endrow": "#6AA784",
                            "waterway": "#EB6E30",
                            "nutrient_deficiency": "#D7CA47",
                            "planter_skip": "#F2BC38",
                            "water": "#F29238",
                            "drydown": "#0A85B8",},title='Land Segmentation: Pie Graph')
             

             bar1 = img[img != 0]
             val_p,count_p = np.unique(bar1,return_counts=True)
             df_bar = pd.DataFrame()
             df_bar['value'] = val_p
             df_bar['count'] = count_p
             df_bar['class'] = df_bar['value'].apply(value_to_class)
             
             df_bar = df_bar.drop(df_bar[df_bar["count"] < 2].index)
            
             fig6 = px.bar(df_bar,y='count', x='class',color='class',
                           color_discrete_map={
                            "weed_cluster": "#c40a29",
                            "double_plant": "#0B5B9D",
                            "endrow": "#6AA784",
                            "waterway": "#EB6E30",
                            "nutrient_deficiency": "#D7CA47",
                            "planter_skip": "#F2BC38",
                            "water": "#F29238",
                            "drydown": "#0A85B8",},title='Land Segmentation: Bar Graph')
             
             st.plotly_chart(fig5)
             st.plotly_chart(fig6)