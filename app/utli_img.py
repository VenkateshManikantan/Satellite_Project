import numpy as np 
import matplotlib
from matplotlib.colors import ListedColormap
from matplotlib import patches
import cv2
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,)
from PIL import Image
from collections import defaultdict
import pandas as pd 

def normalize_img(img):
    """Function: Normalize an array.

    `Function to normalize a numpy array, to form the RGB image'

    Parameters
    ----------
    img : numpy array 
        numpy array of size 128 ,129 
    Returns
    -------
    output: Numpy array
        A normalized array as an output 
    """
    img = np.array(img)
    norm = (img - np.min(img)) / (np.max(img) - np.min(img))
    return (255*norm).astype(np.uint8)

def cmap_agri():
    """Function: CMAP
    CMAP specific to PASTIS labeling

    Parameters
    ----------
     
    Returns
    -------
    output: cmap
    output: Label names
         
    """
    label_names = [
    "Background",
    "Meadow",
    "Soft winter wheat",
    "Corn",
    "Winter barley",
    "Winter rapeseed",
    "Spring barley",
    "Sunflower",
    "Grapevine",
    "Beet",
    "Winter triticale",
    "Winter durum wheat",
    "Fruits,  vegetables, flowers",
    "Potatoes",
    "Leguminous fodder",
    "Soybeans",
    "Orchard",
    "Mixed cereal",
    "Sorghum",
    "Void label"]
    
    cm = matplotlib.cm.get_cmap('tab20')
    def_colors = cm.colors
    cus_colors = ['k'] + [def_colors[i] for i in range(1,20)]+['w']
    cmap = ListedColormap(colors = cus_colors, name='agri',N=21)
    return cmap,label_names

def npy_to_img(path,d_index):
    """Function: convert .npy tp img (BGR).

    `This is a test function, aim of the function is to extract one image of a purticular date
    index. and plot that image 

    Parameters
    ----------
    path : str
        Path towards a single .npy file.
    d_index : int
        Integer value from 0 to 41, each value is respect to a purticualar time frame 
    Returns
    -------
    img_a: Numpy array
        A resized numpy array holding the value of the image in BGR format 
    """
    
    data = np.load(path)
    data_B = data[d_index,0,:,:]
    data_G = data[d_index,1,:,:]
    data_R = data[d_index,2,:,:]

    data_B = np.reshape(data_B,(128,128))
    data_G = np.reshape(data_G,(128,128))
    data_R = np.reshape(data_R,(128,128))

    rgbArray = np.zeros((128,128,3))
    rgbArray[:, :, 0] = normalize_img(data_R)
    rgbArray[:, :, 1] = normalize_img(data_G)
    rgbArray[:, :, 2] = normalize_img(data_B)

    data_s1 = data[d_index,4,:,:]
    data_s1 = np.reshape(data_s1,(128,128))
    data_s2 = data[d_index,5,:,:]
    data_s2 = np.reshape(data_s2,(128,128))
    data_s3 = data[d_index,6,:,:]
    data_s3 = np.reshape(data_s3,(128,128))
    data_s4 = data[d_index,7,:,:]
    data_s4 = np.reshape(data_s4,(128,128))
    data_s5 = data[d_index,8,:,:]
    data_s5 = np.reshape(data_s5,(128,128))



    return rgbArray.astype(np.uint8),data_s1,data_s2,data_s3,data_s4,data_s5


def plot_pano_gt(pano_gt, ax, alpha=.5, plot_void=True):
    """Function: convert .npy tp img (BGR).

    `This is a test function, aim of the function is to extract one image of a purticular date
    index. and plot that image 

    Parameters
    ----------
    path : str
        Path towards a single .npy file.
    d_index : int
        Integer value from 0 to 41, each value is respect to a purticualar time frame 
    Returns
    -------
    img_a: Numpy array
        A resized numpy array holding the value of the image in BGR format 
    """

    cm = matplotlib.cm.get_cmap('tab20')
    def_colors = cm.colors
    cus_colors = ['k'] + [def_colors[i] for i in range(1,5)]+['w']
    cmap = ListedColormap(colors = cus_colors, name='agri',N=20)


    ground_truth_instances = pano_gt[:,:]
    grount_truth_semantic  = pano_gt[:,:]

    for inst_id in np.unique(ground_truth_instances):
        if inst_id==0:
            continue  
        mask = (ground_truth_instances==inst_id)
        try:
            c,h= cv2.findContours(mask.astype(int), cv2.RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE)
            u,cnt  = np.unique(grount_truth_semantic[mask], return_counts=True)
            cl = u if np.isscalar(u) else u[np.argmax(cnt)]
            
            if cl==19 and not plot_void: # Not showing predictions for Void objects
                continue
            
            color = cmap.colors[cl]
            for co in c[1::2]:
                poly = patches.Polygon(co[:,0,:], fill=True, alpha=alpha, linewidth=0, color=color)
                ax.add_patch(poly)
                poly = patches.Polygon(co[:,0,:], fill=False, alpha=.8, linewidth=4, color=color)
                ax.add_patch(poly)
        except ValueError as e:
            print(e)




def convert_rgb_to_names(rgb_tuple):
    """Function: CMAP
    CMAP specific to PASTIS labeling

    Parameters
    ----------
     
    Returns
    -------
    output: cmap
    output: Label names
    """     
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

def closest(colors,color):
    """Function: CMAP
    CMAP specific to PASTIS labeling

    Parameters
    ----------
     
    Returns
    -------
    output: cmap
    output: Label names
    """   
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance
            
def color_t(filepath):
    """Function: CMAP
    CMAP specific to PASTIS labeling

    Parameters
    ----------
     
    Returns
    -------
    output: cmap
    output: Label names
    """ 

    im = Image.open(filepath)
    by_color = defaultdict(int)
    for pixel in im.getdata():
        by_color[pixel] += 1
    
    rgb = []
    counts =[]

    for k,v in by_color.items():
        rgb.append(k)
        counts.append(v)
    
    

    test_df = pd.DataFrame(data= rgb ,columns=["red","green","blue"])
    test_df["counts"] = counts

    color = []
    for i in range(len(test_df)):
        col_val = convert_rgb_to_names([test_df["red"][i],test_df["green"][i],test_df["blue"][i]])
        color.append(col_val)
    
    test_df["color"] = color


    return test_df