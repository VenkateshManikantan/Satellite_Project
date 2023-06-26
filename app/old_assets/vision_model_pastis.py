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


#config: page layout
st.set_page_config(layout="wide")

st.write(st.session_state['auth'])


#Header
col1, col2, col3 = st.columns(3)
with col1:
        st.write(' ')
with col2:
        st.title("Satelite Analysis 🛰️")
with col3:
        st.write(' ')
   
 #config: sidebar setting
st.sidebar.image("assets\logo2.png")
st.sidebar.markdown("# Satelite Analysis 🛰️")



#config: body
col1, col2, col3 = st.columns([1,1,3])
with col1:
        file_n,path_n = get_dir("data\Pastis\source")
        file     = st.selectbox("Load Sentinal-2 Image", path_n)
        button_0 = st.button('Run Segmentation Analysis')
with col2:
        image,s1,s2,s3,s4,s5 = npy_to_img(file,5)
        
        fig, ax = plt.subplots(2,3,figsize = (10,10))
        ax[0,0].imshow(image)
        ax[0,0].tick_params(axis='x', colors='white')
        ax[0,0].tick_params(axis='y', colors='white') 
        ax[0,1].imshow(s1)
        ax[0,1].tick_params(axis='x', colors='white')
        ax[0,1].tick_params(axis='y', colors='white') 
        ax[0,2].imshow(s2)
        ax[0,2].tick_params(axis='x', colors='white')
        ax[0,2].tick_params(axis='y', colors='white') 
        ax[1,0].imshow(s3)
        ax[1,0].tick_params(axis='x', colors='white')
        ax[1,0].tick_params(axis='y', colors='white') 
        ax[1,1].imshow(s4)
        ax[1,1].tick_params(axis='x', colors='white')
        ax[1,1].tick_params(axis='y', colors='white') 
        ax[1,2].imshow(s5)
        ax[1,2].tick_params(axis='x', colors='white')
        ax[1,2].tick_params(axis='y', colors='white') 
        fig.set_facecolor("#002B36")
        
    
        
        st.pyplot(fig)
with col3:
        Map = geemap.Map()
        esa = ee.ImageCollection("ESA/WorldCover/v100").first()
        esa_vis = {"bands": ["Map"]}
        Map.add_basemap("ESA WorldCover 2020 S2 FCC")
        Map.setCenter(29.0588, 76.0856, 5)
        Map.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
        layer = geemap.ee_tile_layer(esa, esa_vis, "ESA Land Cover")
        Map.split_map(layer,layer,add_close_button = True )
        Map.to_streamlit()
         
#config: Segmentation Result
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
        if button_0:
            cmap,label_names = cmap_agri()
            fig, ax = plt.subplots(figsize=(1,3)) 
            ax.matshow(np.stack([np.arange(0, 20) for _ in range(3)], axis=1), cmap = cmap)
            ax.set_yticks(ticks = range(20), labels=label_names , fontsize = 10)
            ax.tick_params(axis='y', colors='white') 
            ax.set_xticks(ticks=[])
            fig.set_facecolor("#002B36")
            st.pyplot(fig)
        else:
            st.write(' ')

with col2:
        path_t = "data/Pastis/annotation/TARGET_"
        key_a  = find_between(file,'_','.npy')
        path_t = path_t + key_a + ".npy"
        cmap,label_names = cmap_agri()
        if button_0:
            anno_t = np.load(path_t)
            data_B = anno_t[0,:,:]
            data_G = anno_t[1,:,:]
            data_R = anno_t[2,:,:]

            rgbArray = np.zeros((128,128,3))
            rgbArray[:, :, 0] = normalize_img(data_R)
            rgbArray[:, :, 1] = normalize_img(data_G)
            rgbArray[:, :, 2] = normalize_img(data_B)
            
            fig, ax = plt.subplots(figsize = (5,5))
           
            ax.matshow(rgbArray.astype(np.uint8),
                cmap=cmap,
                vmin=0,
                vmax=255)
            
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white') 
            fig.set_facecolor("#002B36")
            st.pyplot(fig)
        else:
            st.write(' ')

with col3:
        path_a = "data/Pastis/annotation/ParcelIDs_"
        key_a  = find_between(file,'_','.npy')
        path_a = path_a + key_a + ".npy"
        if button_0:
            anno = np.load(path_a)
            anno = normalize_img(anno)
            fig, ax = plt.subplots(figsize = (5,5))
            ax.imshow(image)
            ax.pcolormesh(anno,cmap ='magma',alpha= 0.5)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white') 
            fig.set_facecolor("#002B36")
            st.pyplot(fig)
        else:
            st.write(' ')
    
with col4:
        path_z = "data/Pastis/annotation/ZONES_"
        key_a  = find_between(file,'_','.npy')
        path_z = path_z + key_a + ".npy"
        cmap,label_names = cmap_agri()
        
        if button_0:
            anno_z = np.load(path_z)
            anno_z = normalize_img(anno_z)
            anno_z[anno_z < 50] = 0
            anno_z[(anno_z>50) & (anno_z<150)] = 90
            anno_z[(anno_z>150) & (anno_z<190)] = 174
            anno_z[(anno_z>190) & (anno_z<220)] = 212
            anno_z[(anno_z>220)] = 255
            fig, ax = plt.subplots(figsize = (5,5))
            ax.imshow(image)
            ax.pcolormesh(anno_z,cmap ='magma',alpha= 0.5)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white') 
            fig.set_facecolor("#002B36")
            st.pyplot(fig)
        else:
            st.write(' ')
    
with col5:
        if button_0:
            cmap,label_names = cmap_agri()
            fig, ax = plt.subplots(figsize=(1,3)) 
            ax.matshow(np.stack([np.arange(0, 20) for _ in range(3)], axis=1), cmap = cmap)
            ax.set_yticks(ticks = range(20), labels=label_names , fontsize = 10)
            ax.tick_params(axis='y', colors='white') 
            ax.set_xticks(ticks=[])
            fig.set_facecolor("#002B36")
            st.pyplot(fig)
        else:
            st.write(' ')
