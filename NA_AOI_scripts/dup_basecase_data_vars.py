# create NA_AOI_surfdata.nc

import netCDF4 as nc
import numpy as np
from pyproj import Transformer
#import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import pandas as pd
import sys, os
import csv

from datetime import datetime

# Get current date
current_date = datetime.now()
# Format date to mmddyyyy
formatted_date = current_date.strftime('%y%m%d')

def main():
    args = sys.argv[1:]
    # Check the number of arguments
    # Check the number of arguments
    if len(sys.argv) != 7  or sys.argv[1] == '--help':  
    # sys.argv includes the script name as the first argument
        print("Example use: # python3 dup_basecase_data.py ${NTimes} ${input_data_path} ${input_data} ${output_data_path} ${output_data} ")
        print(" <NTimes>: Number of duplication in the new dataset")
        print(" <input_data_path>: path to the base_data_file")
        print(" <input_data>: the name of the base_data_file")
        print(" <output_data_path>:  output directory to store the data file")
        print(" <output_data>:  the name of the new data")
        print(" <vars>: list of variables")
        print(" The code increases the specific variables in the basecase data file by the Ntimes")      
        exit(0)
    
    NTimes = int(args[0])
    input_file_path = args[1]
    input_file = args[2]
    output_file_path = args[3]
    output_file = args[4]
    vars_file = args[5]


    # get the variable list
    # Specify the path to your CSV file
    # csv_file_path = 'path_to_your_csv_file.csv' 

    variable_names = []

    # Read the CSV file and store variable names into a list
    with open(vars_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            for item in row:
                variable_names.append(item)
    
    print(variable_names)

    # read in the netcdf file

    source = input_file_path + '/' + input_file
    src = nc.Dataset(source, 'r')

    dest = output_file_path + '/' + vars_file + '_' +output_file
    os.system('rm '+ dest)

    # get the dimensions and variables
    src_dims = [dim for dim in src.dimensions]
    src_vars = [var for var in src.variables]

    # create new netcdf file and write data to it
    dst = nc.Dataset(dest, 'w', format='NETCDF4')

    # Create new variables
    dst_vars = {}

    if 'surfdata' in input_file:

        # Copy the global attributes from the source to the target
        for name in src.ncattrs():
            dst.setncattr(name, src.getncattr(name))

        # Copy the dimensions from the source to the target
        for name, dimension in src.dimensions.items():
            if name != 'gridcell':
                dst.createDimension(
                    name, (len(dimension) if not dimension.isunlimited() else None))
            else:
                # Update the 'ni' dimension by NTimes
                ni = dst.createDimension('gridcell', NTimes * (len(dimension)))

        count = 0 # record how may 2D layers have been processed 
        
        # Copy the variables from the source to the target
        for name, variable in src.variables.items():

            if (len(variable.dimensions) == 0 or variable.dimensions[-1] != 'gridcell'):
                '''x = dst.createVariable(name, variable.datatype, variable.dimensions)   
                print(name, variable.dimensions)
                # Copy variable attributes
                dst[name].setncatts(src[name].__dict__)
                # Copy the data
                dst[name][...] = src[name][...]'''            

            else:
                if len(variable.dimensions) == 1:
                    '''dst_var = dst.createVariable(name, variable.datatype, ('gridcell',))   
                    print(name, dst[name].dimensions)
                    #dst[name][:] = src[name][domain_idx]
                    data = src.variables[name][:]
                    
                    #dst_data = np.repeat(data, NTimes, axis=src.variables[var].dimensions.index('ni'))
                    dst_data = np.copy(data)
                    for i in range(NTimes - 1):
                        dst_data = np.concatenate((dst_data, data), axis = src.variables[name].dimensions.index('gridcell'))
                    
                    #dst_var = dst.createVariable(var, src.variables[var].datatype, src.variables[var].dimensions)
                    #dst_var = dst.createVariable(name, src.variables[name].datatype, src.variables[name].dimensions)
                    
                    dst_var[:] = dst_data
                    dst_vars[name] = dst_var
                    print(name, dst_data.shape, dst_vars[name].dimensions)'''


                if len(variable.dimensions) == 2:
                    '''dst_var = dst.createVariable(name, variable.datatype, variable.dimensions[:-1]+('gridcell',))   
                    print(name, dst[name].dimensions)               
                    for index in range(variable.shape[0]):
                        # get all the source data (global)
                        #dst[name][index,:] = src[name][index][domain_idx]

                        data = src.variables[name][:]
                        #dst_data = np.repeat(data, NTimes, axis=src.variables[var].dimensions.index('ni'))
                        dst_data = np.copy(data)
                        for i in range(NTimes - 1):
                            dst_data = np.concatenate((dst_data, data), axis = src.variables[name].dimensions.index('gridcell'))
                        
                        #dst_var = dst.createVariable(var, src.variables[var].datatype, src.variables[var].dimensions)
                        #dst_var = dst.createVariable(name, src.variables[name].datatype, src.variables[name].dimensions)
                        
                        dst_var[:] = dst_data
                        dst_vars[name] = dst_var
                        print(name, dst_data.shape, dst_vars[name].dimensions)

                        count = count +1'''

                if (len(variable.dimensions) == 3 and (name in variable_names)):
                    dst_var = dst.createVariable(name, variable.datatype, variable.dimensions[:-1]+('gridcell',))   
                    print(name, dst[name].dimensions)   
                    for index1 in range(variable.shape[0]):
                        for index2 in range(variable.shape[1]):
                            # get all the source data (global)
                            #dst[name][index1,index2,:] = src[name][index1][index2][domain_idx]

                            data = src.variables[name][:]
                            #dst_data = np.repeat(data, NTimes, axis=src.variables[var].dimensions.index('ni'))
                            dst_data = np.copy(data)
                            for i in range(NTimes - 1):
                                dst_data = np.concatenate((dst_data, data), axis = src.variables[name].dimensions.index('gridcell'))
                            
                            #dst_var = dst.createVariable(var, src.variables[var].datatype, src.variables[var].dimensions)
                            #dst_var = dst.createVariable(name, src.variables[name].datatype, src.variables[name].dimensions)
                            
                            dst_var[:] = dst_data
                            dst_vars[name] = dst_var
                            print(name, dst_data.shape, dst_vars[name].dimensions)

                        print('finished layer#: ' + str(index1))    
                        count = count + variable.shape[1]

                        # Copy variable attributes (except _FillValue)
                        attrs = dict(src[name].__dict__)
                        attrs.pop('_FillValue', None)
                        dst[name].setncatts(attrs)

            if count > 50:
                dst.close()   # output the variable into a file to save memory

                dst = nc.Dataset(dest, 'a')

                count = 0
            
            print(count)

    else: # for domain and forcing data
        
        print("procesing "+ source)

        # Copy the global attributes from the source to the target
        for name in src.ncattrs():
            dst.setncattr(name, src.getncattr(name))

        # Copy the dimensions from the source to the target
        for name, dimension in src.dimensions.items():
            if name != 'ni':
                dst.createDimension(
                    name, (len(dimension) if not dimension.isunlimited() else None))
            else:
                # Update the 'ni' dimension by NTimes
                dst.createDimension('ni', NTimes * (len(dimension)))
                print(dst.dimensions)

        # Copy the variables from the source to the target
        for name, variable in src.variables.items():
            if (len(variable.dimensions) == 0 or variable.dimensions[-1] != 'ni'):
                dst_var = dst.createVariable(name, src.variables[name].datatype, src.variables[name].dimensions)
                dst_var[:] = src.variables[name][:]
                dst_vars[name] = dst_var
            else:
                dst_var = dst.createVariable(name, variable.datatype, variable.dimensions[:-1]+('ni',))

                print(name, dst[name].dimensions)
                data = src.variables[name][:]

                dst_data = np.copy(data)
                for i in range(NTimes - 1):
                    dst_data = np.concatenate((dst_data, data), axis = src.variables[name].dimensions.index('ni'))

                dst_var[:] = dst_data
                dst_vars[name] = dst_var
                print(name, dst_data.shape, dst_vars[name].dimensions)


        # copy variable attributes
        for name in dst_vars:
            for attr in src.variables[name].ncattrs():
                setattr(dst_vars[name], attr, getattr(src.variables[name], attr))

    # close both files
    src.close()
    dst.close()

if __name__ == '__main__':
    main()
