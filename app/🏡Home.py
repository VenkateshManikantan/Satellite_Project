"""
Discription: Web application to showcase a solution 
Date: 12/25/2022
License_info: Privatly Held 
"""

# UI libraries 
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_folium import folium_static
import folium


# Data libraries 
import pandas as pd 
import yaml
from yaml.loader import SafeLoader
import geopandas as gpd
import numpy as np 
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta  
from meteostat import Point, Daily
import matplotlib.pyplot as plt
import ee
import geemap.foliumap as geemap
import tempfile
import os
import uuid
from IPython.display import Image
import urllib.request
import plotly.express as px
import base64


# Custom Scripts libraries
from utli_img import npy_to_img 
from utli_img import normalize_img 
from utli_img import cmap_agri
from utli_img import color_t
from util_crop_img_ati import run_K_img_std
from util_file import get_dir
from util_file import find_between


__author__     = "Venkatesh Manikantan , Vishal Rajput"
__copyright__  = "Source code: Belongs to group KOKAR AI"
__credits__    = ["Venkatesh Manikantan"]
__license__    = "none"
__version__    = "0.1.0"
__maintainer__ = "TEAM"
__email__      = "venkateshvishwanath99@gmail.com"
__status__     = "Dev - Co Founder"



def add_bg_from_local(image_file):
    """Function: to embededd a background image to the UI.

    `Function takes in an image file and ebeddes in the CSS
    styly of the streamlit application'

    Parameters
    ----------
    image_file : string 
        path to the image file 
    Returns
    -------
    returns: int
        value 0 """
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

    return 0
   
st.set_page_config(layout="wide")
col0_1, col0_2, col0_3 = st.columns([3,1,3])
col1, col2, col3 = st.columns([1, 1, 1])
col1_1, col1_2, col1_3 = st.columns([1, 1, 1])

with open(r'E://streamlit_app//data//user_auth//user_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


with col1:
        st.write(' ')
with col2:
        name, authentication_status, username = authenticator.login('Log-in', 'main')
        if authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')
with col3:
        st.write(' ')

if authentication_status == None:
     add_bg_from_local(r'E:\streamlit_app\assets\background3.png')



if authentication_status == None:
    with col0_1:
            st.write(' ')
    with col0_2:
            st.image("assets\kokar_logo.png", use_column_width= True)
    with col0_3:
            st.write(' ')
   

with col1_1:
        st.write(' ')
with col1_2:
        with st.expander("Register"):
            if authentication_status == None:
                try:
                    if authenticator.register_user('Register user', preauthorization=False):
                        with open(r'E://streamlit_app//data//user_auth//user_config.yaml', 'w') as file:
                                yaml.dump(config, file, default_flow_style=False)
                        st.success('User registered successfully')
                except Exception as e:
                    st.error(e)
with col1_3:
        st.write(' ')
   

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if authentication_status:
    st.session_state['auth'] = True


if authentication_status:
    ee.Initialize()
    
    st.write(f'Welcome *{name}*')


    @st.cache(allow_output_mutation=True)
    def uploaded_file_to_gdf(data):
        _, file_extension = os.path.splitext(data.name)
        file_id = str(uuid.uuid4())
        file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

        with open(file_path, "wb") as file:
            file.write(data.getbuffer())

        if file_path.lower().endswith(".kml"):
            gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"
            gdf = gpd.read_file(file_path, driver="KML")
        else:
            gdf = gpd.read_file(file_path)
    
        area = gdf.to_crs(4328).area
        area = area*0.000001
        area = round(area, 2)
        length = int(gdf.to_crs(4328).length / 4)
        lat  = gdf['geometry'].centroid.x
        lat  = lat.values[0]
        lon  = gdf['geometry'].centroid.y
        lon  = lon.values[0]

        return gdf,area,lat,lon,length


    def app():
        

        st.sidebar.image("assets\logo2.png")
        st.sidebar.markdown("# Satelite Analysis 🛰️")
        
        
        
        st.title("Land Cover Monitor:")

        
        col1, col2 = st.columns([4, 1])
        with st.spinner('Loading...'):
            Map = geemap.Map(plugin_Draw = True, Draw_export=True,locate_control=True,
                    plugin_LatLngPopup=False)
            Map.add_basemap("ESA WorldCover 2020 S2 FCC")
            Map.add_basemap("ESA WorldCover 2020 S2 TCC")
            Map.add_basemap("HYBRID")

            esa = ee.ImageCollection("ESA/WorldCover/v100").first()
            esa_vis = {"bands": ["Map"]}


        esri = ee.ImageCollection(
                "projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m"
            ).mosaic()
        
        esri_vis = {
            "min": 1,
            "max": 10,
            "palette": [
                "#1A5BAB",
                "#358221",
                "#A7D282",
                "#87D19E",
                "#FFDB5C",
                "#EECFA8",
                "#ED022A",
                "#EDE9E4",
                "#F2FAFF",
                "#C8C8C8",
                        ],
            }


        markdown = """
            - [Dynamic World Land Cover](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1?hl=en)
            - [ESA Global Land Cover](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100)
            - [ESRI Global Land Cover](https://samapriya.github.io/awesome-gee-community-datasets/projects/esrilc2020)
            """

        with col2:

                longitude = st.number_input("Longitude", -180.0, 180.0, 77.1025)
                latitude = st.number_input("Latitude", -90.0, 90.0,28.644800 )
                zoom = st.number_input("Zoom", 0, 20, 11)
                
                Map.setCenter(longitude, latitude, zoom)

                start = st.date_input("Start Date for Dynamic World", datetime(2020, 1, 1))
                end = st.date_input("End Date for Dynamic World", datetime(2021, 1, 1))

                start_date = start.strftime("%Y-%m-%d")
                end_date = end.strftime("%Y-%m-%d")

                region = ee.Geometry.BBox(-179, -89, 179, 89)
                dw = geemap.dynamic_world(region, start_date, end_date, return_type="hillshade")

                layers = {
                "Dynamic World": geemap.ee_tile_layer(dw, {}, "Dynamic World Land Cover"),
                "ESA Land Cover": geemap.ee_tile_layer(esa, esa_vis, "ESA Land Cover"),
                "ESRI Land Cover": geemap.ee_tile_layer(esri, esri_vis, "ESRI Land Cover"),
                }

                options = list(layers.keys())
                left = st.selectbox("Select a left layer", options, index=2)
                right = st.selectbox("Select a right layer", options, index=2)

                left_layer = layers[left]
                right_layer = layers[right]

                Map.split_map(left_layer, right_layer,add_close_button = True )

                legend = st.selectbox("Select a legend", options, index=options.index(right))
                if legend == "Dynamic World":
                    Map.add_legend(
                    title="Dynamic World Land Cover",
                    builtin_legend="Dynamic_World",
                    )
                elif legend == "ESA Land Cover":
                    Map.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
                elif legend == "ESRI Land Cover":
                    Map.add_legend(title="ESRI Land Cover", builtin_legend="ESRI_LandCover")

                with st.expander("Data sources"):
                    st.markdown(markdown)
        
      
        def map_to_st():
            Map.to_streamlit(height=750)
            Map.extract_values_to_points("data/temp_data/test.csv")

        with col1:
                map_to_st()


        col3, col4, col5 = st.columns([1, 1, 2])

        with col3:
                uploaded_file = st.file_uploader("Upload ROI file", type=["geojson"])
                if uploaded_file is not None:
                    gdf,area,lon,lat,length = uploaded_file_to_gdf(uploaded_file)
                    if len(gdf) >1:
                        st.error(f"Please upload an  ROI with only one polygon, your AOI contains {len(gdf)} polygons.")
                    else:
                        st.session_state["roi"] = geemap.geopandas_to_ee(gdf, geodesic=False)
                        st.write("You have uploaded a GeoJSON file.")
                    
                    st.metric(label="Area in square Kilometers", value = area)
                    st.metric(label="lat", value = round(lat,2))
                    st.metric(label="lon", value = round(lon,2))
                    
        button_0 = st.button('Compute Analytics')

        with st.spinner('Computing...'):        
            
            with col4:
            
                if button_0:
                    lat = lat
                    lon = lon
                    length_1 = length

                    poi = ee.Geometry.Point(lon,lat)
                    roi = poi.buffer(length_1)
                    esri_1 = esri

                    url = esri_1.getThumbUrl({
                    'min': 1, 'max': 10, 'dimensions': 512, 'region': roi,
                    "palette": [
                        "#1A5BAB",
                        "#358221",
                        "#A7D282",
                        "#87D19E",
                        "#FFDB5C",
                        "#EECFA8",
                        "#ED022A",
                        "#EDE9E4",
                        "#F2FAFF",
                        "#C8C8C8",
                    ]})
                    


                    urllib.request.urlretrieve(url,"data/temp_data/test_1.jpg")

                    st.write("Region of Interest:")
                    st.image("data/temp_data/test_1.jpg")
                
                else:
                    st.write(' ')
            
            with col5:
                if button_0:
                    run_K_img_std("data/temp_data/test_1.jpg",20)
                    df_1 = color_t("data/temp_data/output_k.png")
                    
                    col_one_list   = df_1['color'].tolist()
                    col_one_list_2 = df_1['color'].tolist()

                    res = {col_one_list[i]: col_one_list_2[i] for i in range(len(col_one_list))}

                    fig = px.pie(df_1, values='counts', names='color',  color='color',title='Distribution of Land Segmentation',
                                color_discrete_map=res)
                    st.plotly_chart(fig)

            col6, col7, col8 = st.columns([1, 1, 1])
            
            with col6:
                if button_0:
                    today = datetime.today()
                    one_year = today - relativedelta(years = 5)
                    roi_point = Point(lat,lon)
                    data = Daily(roi_point, one_year, today)
                    data = data.fetch()
                    
                    if data.empty:
                        print('DataFrame is empty!')
                    
                    fig = px.line(data, x= data.index, y= ["tmax","tavg","tmin"],title='Air Temperature in °C')
                    fig.update_xaxes(
                        dtick="M1",
                        tickformat="%b\n%Y")
                    st.plotly_chart(fig, use_container_width=True)
            with col7:
                if button_0:
                    fig = px.line(data, x= data.index, y= ["wspd","wpgt"],title='Wind Speed and Gust in KM/H')
                    fig.update_xaxes(
                        dtick="M1",
                        tickformat="%b\n%Y")
                    st.plotly_chart(fig, use_container_width=True)
            with col8:
                if button_0:
                    fig = px.line(data, x= data.index, y= ["prcp"],title='Daily Precipitation Total in mm')
                    fig.update_xaxes(
                        dtick="M1",
                        tickformat="%b\n%Y")
                    st.plotly_chart(fig, use_container_width=True)
        
        
                    
        
        with st.sidebar:
            with st.expander("Reset Password"):
                try:
                    if authenticator.reset_password(username, 'Reset password'):
                        with open(r'E://streamlit_app//data//user_auth//user_config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        st.success('Password modified successfully')
                except Exception as e:
                    st.error(e)
            authenticator.logout('Logout', 'main')

    if __name__ == "__main__":
        app()

