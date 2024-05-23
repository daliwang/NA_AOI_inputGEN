# create NA_AOI_domain.nc

import netCDF4 as nc
import numpy as np
from pyproj import Transformer
#import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import pandas as pd
import sys, os

from datetime import datetime

# Get current date
current_date = datetime.now()
# Format date to mmddyyyy
formatted_date = current_date.strftime('%y%m%d')

# An input csv file that contains the locations of land gridcells in Daymet domain;
# 1:  land gridcell ID
# 2:  xc, yc (lon, lat) of land gridcell center 
# 3:  xc_LCC,yc_LCC (x,y) location in LLC projection

# output 1D AOIdomain.nc that can be used to generate 1D AOIsurfdata.nc and 1D AOIforcing.nc 

def read_gridcells(file_name):
    try:
        df = pd.read_csv(file_name, sep=",")
    except pd.errors.ParserError:
        df = pd.read_csv(file_name, sep=" ")
    return df

def find_nearest_points(listA, listB):
    tree = cKDTree(np.array(listB))
    _, indices = tree.query(listA, k=1)
    return indices

def main():

    args = sys.argv[1:]
    # Check the number of arguments
    if len(sys.argv) != 4  or sys.argv[1] == '--help':  # sys.argv includes the script name as the first argument
        print("Example use: python NA_AOI_domainGEN.py <input_path> <output_path> <AOI_points_file>")
        print(" <input_path>: path to the 1D source data directory")
        print(" <output_path>:  path for the 1D AOI output data directory")
        print(" <AOI_points_file>:  <AOI>_gridID.csv or <AOI>_xcyc.csv or <AOI>_xcyc_lcc.csv")
        print(" The code uses NA domain to generation 1D AOI domain.nc")      
        exit(0)
    
    input_path = args[0]
    output_path = args[1]
    AOI_gridcell_file = args[2]
    '''

    input_path = "./AKSP_info/"
    output_path = "./temp"
    #AOI_gridcell_file = 'AKSP_gridID.csv'
    AOI_gridcell_file = 'AKSP_xcyc.csv'
    AOI_gridcell_file = 'AKSP_xcyc_lcc.csv'
    #AOI_gridcell_file = 'MOF21points_xcyc.csv' 
    AOI=AOI_gridcell_file.split("_")[0]
    '''
    AOI=AOI_gridcell_file.split("_")[0]
    AOI_gridcell_file = input_path + AOI_gridcell_file    

    if AOI_gridcell_file.endswith('gridID.csv'):
        user_option = 1
    if AOI_gridcell_file.endswith('xcyc.csv'):
        user_option = 2
    if AOI_gridcell_file.endswith('xcyc_lcc.csv'):
        user_option = 3

    # save to the 1D domain file
    AOIdomain = str(AOI)+'_domain.lnd.Daymet_NA.1km.1d.c'+ formatted_date + '.nc'

    # check if file exists then delete it
    if os.path.exists(AOIdomain):
        os.remove(AOIdomain)

    source_file = 'domain.lnd.Daymet_NA.1km.1d.nc'
    dst = nc.Dataset(AOIdomain, 'w', format='NETCDF4')

    # open the 1D domain data
    src = nc.Dataset(source_file, 'r', format='NETCDF4')

    # 3) Open a csv file to read a list of points (y, x)
    #df = read_gridcells(AOI_gridcell_file)  

    if user_option == 1: # gridID is used directly
        #AOI_gridcell_file = AOI+'_gridID.csv'  # user provided gridcell IDs
        df = pd.read_csv(AOI_gridcell_file, sep=",", skiprows=1, names = ['gridID'])
        #read gridIds
        AOI_points = list(df['gridID'])
        #AOI_points = list(mygridIDs)

        # read gridIDs
        NA_gridIDs = src.variables['gridID'][:]
        NA_gridcell_list = list(NA_gridIDs)
        print(NA_gridcell_list[0:5])

        domain_idx = np.where(np.in1d(NA_gridcell_list, AOI_points))[0]

        NA_gridcell_arr = np.array(NA_gridIDs)
        AOI_points_arr = np.array(AOI_points)

    if user_option == 2: # use lat lon coordinates
        #AOI_gridcell_file = AOI+'_xcyc.csv'  # user provided gridcell csv file  (xc, yc) (lon, lat)
        df = pd.read_csv(AOI_gridcell_file, sep=",", skiprows=1, names = ['xc', 'yc'], engine='python')

        #read in x, y coordinate (lon, lat)
        AOI_points = list(zip(df['xc'], df['yc']))
        #AOI_points = list(zip(myxc, myyc))
        
        # read yc, xc (y, x)
        NA_yc = src.variables['yc'][:]
        NA_xc = src.variables['xc'][:]
        # create list for all land gridcell (lat, lon)
        NA_gridcell_list = list(zip(NA_xc, NA_yc))
 
        # find the xc, yc boundary
        NA_xc_max, NA_xc_min = np.max(NA_xc), np.min(NA_xc)
        NA_yc_max, NA_yc_min = np.max(NA_yc), np.min(NA_yc)

        #check the boundaries
        for i, pt in enumerate(AOI_points):
            pt_x, pt_y = pt
            #print (pt_x, NA_xc_min, NA_xc_min.shape)
            if pt_x > NA_xc_max or pt_x < NA_xc_min or pt_y > NA_yc_max or pt_y < NA_yc_min:
                AOI_points.remove(pt)
                print(f"point {i} ({pt_x},{pt_y}) is out of Daymet domain and is removed")


        AOI_points_arr = np.array(AOI_points)
        print("AOI_points_arr", AOI_points_arr[0:5], "shape", AOI_points_arr.shape)
        NA_gridcell_arr = np.squeeze(np.array(NA_gridcell_list)).transpose()    
        print("NA_gridcell_arr", NA_gridcell_arr[0:5], "shape", NA_gridcell_arr.shape)

        tree = cKDTree(NA_gridcell_arr)
        _, domain_idx = tree.query(AOI_points_arr, k=1)

    if user_option == 3: # xc_LCC and yc_LCC is used directly
        #AOI_gridcell_file = AOI+'_XYLCC.csv'  # user provided gridcell csv file  (xc_LCC, yc_LCC) 
        df = pd.read_csv(AOI_gridcell_file, sep=",", skiprows=1, names = ['xc_LCC', 'yc_LCC'], engine='python')

        #read in x, y coordinate (in LCC projection)
        AOI_points = list(zip(df['xc_LCC'], df['yc_LCC']))
        #AOI_points = list(zip(myxc_lcc, myyc_lcc))

        # read yc_LCC, xc_LCC (y, x in LCC)
        NA_yc_LCC = src.variables['yc_LCC'][:]
        NA_xc_LCC = src.variables['xc_LCC'][:]

        # create list for all land gridcell (lat, lon)
        NA_gridcell_list = list(zip(NA_xc_LCC, NA_yc_LCC))


        # find the xc, yc boundary
        NA_xc_LCC_max, NA_xc_LCC_min = np.max(NA_xc_LCC), np.min(NA_xc_LCC)
        NA_yc_LCC_max, NA_yc_LCC_min = np.max(NA_yc_LCC), np.min(NA_yc_LCC)

        #check the boundaries
        for i, pt in enumerate(AOI_points):
            pt_x, pt_y = pt
            #print (pt_x, NA_xc_LCC_min, NA_xc_LCC_min.shape)
            if pt_x > NA_xc_LCC_max or pt_x < NA_xc_LCC_min or pt_y > NA_yc_LCC_max or pt_y < NA_yc_LCC_min:
                AOI_points.remove(pt)
                print(f"point {i} ({pt_x},{pt_y}) is out of Daymet domain and is removed")

        AOI_points_arr = np.array(AOI_points)
        print("AOI_points_arr", AOI_points_arr[0:5], "shape", AOI_points_arr.shape)
        NA_gridcell_arr = np.squeeze(np.array(NA_gridcell_list)).transpose()    
        print("NA_gridcell_arr", NA_gridcell_arr[0:5], "shape", NA_gridcell_arr.shape)

        tree = cKDTree(NA_gridcell_arr)
        _, domain_idx = tree.query(AOI_points_arr, k=1)

    AOI_mask = np.isin(NA_gridcell_arr, AOI_points_arr)

    #domain_idx = np.sort(domain_idx).squeeze()

    print("gridID_idx", domain_idx.shape, domain_idx[0:20])
    
    #if not user_option==1:
    #    np.savetxt("AOI_gridId.csv", src['gridID'][...,domain_idx], delimiter=",", fmt='%d\n')

    # Copy the global attributes from the source to the target
    for name in src.ncattrs():
        dst.setncattr(name, src.getncattr(name))

    # Copy the dimensions from the source to the target
    for name, dimension in src.dimensions.items():
        if name != 'ni':
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))
        else:
            # Update the 'ni' dimension with the length of the list
            #dst.dimensions['ni'].set_length(len(AOI_points))
            ni = dst.createDimension("ni", len(AOI_points))

    # Copy the variables from the source to the target
    for name, variable in src.variables.items():
        if (name == 'lon' or name == 'lat'): continue

        x = dst.createVariable(name, variable.datatype, variable.dimensions)   
        print(name, variable.dimensions)
        
        if (name != 'lambert_conformal_conic'):
            if (variable.dimensions[-1] != 'ni'):
                dst[name][...] = src[name][...]
            elif (len(variable.dimensions) == 2):
                dst[name][...] = src[name][:,domain_idx]
            elif (len(variable.dimensions) == 3):
                d0 = variable.shape[0]
                d1 = variable.shape[1]
                d2 = variable.shape[2]
                '''for index1 in range(variable.shape[0]):
                    # get all the source data (global)
                    source = src[name][index1, :, :]
                    aoi_data = source[:,domain_idx]
                    dst[name][index1,...] =aoi_data
                    print("finished layer: "+ str(index1))'''
                print("reading source data")
                source_data = src[name][...]
                print("subsetting source data"+str(source_data.shape))                
                #data_arr = np.copy(source_data[...,AOI_mask]).reshape(d0,d1,ni)   

                source_data = np.reshape(source_data, (d0, d2))  # reshape source_data into (4,ni)
                #AOI_data = np.copy(source_data[..., AOI_mask])  # mask out the source data with AOI_mask
    
                # put the masked result into an array of (m,1, AOI_points)
                data_arr = np.empty((d0, d1, len(AOI_points)))
                for i in range(d0):
                    AOI_data = np.copy(source_data[i, domain_idx])  # mask out the source data with AOI_mask  
                    data_arr[i, 0, :] = AOI_data[:]

                print("putting back data into netcdf"+ str(data_arr.shape))
                dst[name][...] = data_arr


# Copy the variable attributes
        for attr_name in variable.ncattrs():
            dst[name].setncattr(attr_name, variable.getncattr(attr_name))

    dst.title = '1D domain for '+ AOI +', generated on ' +formatted_date + ' with ' + source_file
       
    # Close the source netCDF file
    src.close()

    # Save the target netCDF file
    dst.close()

    print("Domain generation has done")

if __name__ == '__main__':
    main()

