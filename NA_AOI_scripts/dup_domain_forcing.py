
# python3 dup_domain.py ${NTimes} ${input_domain_path} ${input_domain} ${output_domain_path} ${output_domain}

# basecase nc file duplication 
import numpy as np
import sys 
import os

import netCDF4 as nc

def main():

    args = sys.argv[1:]
    # Check the number of arguments
    if len(sys.argv) != 6  or sys.argv[1] == '--help':  
    # sys.argv includes the script name as the first argument
        print("Example use: # python3 dup_domain.py ${NTimes} ${input_domain_path} ${input_domain} ${output_domain_path} ${output_domain} ")
        print(" <NTimes>: Number of duplication in the new dataset")
        print(" <input_domain_path>: path to the base_domain_file")
        print(" <input_domain>: the name of the base_domain_file")
        print(" <output_domain_path>:  output directory to store the domain file")
        print(" <output_domain>:  the name of the new domain")
        print(" The code increases the domain file by the Ntimes")      
        exit(0)
        
    NTimes = int(args[0])
    input_domain_path = args[1]
    input_domain = args[2]
    output_domain_path = args[3]
    output_domain = args[4]

    # read in the netcdf file

    source = input_domain_path + '/' + input_domain
    src = nc.Dataset(source, 'r')

    dest = output_domain_path + '/' + output_domain
    os.system('rm '+ dest)

    # get the dimensions and variables
    src_dims = [dim for dim in src.dimensions]
    src_vars = [var for var in src.variables]

    # create new netcdf file and write data to it
    dst = nc.Dataset(dest, 'w', format='NETCDF4')

    # copy global attributes
    for attr in src.ncattrs():
        setattr(dst, attr, getattr(src, attr))

    # create new dimensions
    dst_dims = {}
    for dim in src_dims:
        if dim == "ni":
            dst_size = len(src.dimensions[dim]) * NTimes
            dst_dims[dim] = dst_size
        else:
            dst_dims[dim] = len(src.dimensions[dim])

    for dim in dst_dims:
        dst.createDimension(dim, dst_dims[dim])

    # Create new variables
    dst_vars = {}
    for var in src_vars:
        if 'ni' in src.variables[var].dimensions:
            data = src.variables[var][:]
            #dst_data = np.repeat(data, NTimes, axis=src.variables[var].dimensions.index('ni'))
            dst_data = np.copy(data)
            for i in range(NTimes - 1):
                dst_data = np.concatenate((dst_data, data), axis = src.variables[var].dimensions.index('ni'))
            
            #dst_var = dst.createVariable(var, src.variables[var].datatype, src.variables[var].dimensions)
            dst_var = dst.createVariable(var, src.variables[var].datatype, src.variables[var].dimensions)
            
            dst_var[:] = dst_data
            dst_vars[var] = dst_var
            print(var, dst_data.shape)
        else:
            dst_var = dst.createVariable(var, src.variables[var].datatype, src.variables[var].dimensions)
            dst_var[:] = src.variables[var][:]
            dst_vars[var] = dst_var

    # copy variable attributes
    for var in dst_vars:
        for attr in src.variables[var].ncattrs():
            setattr(dst_vars[var], attr, getattr(src.variables[var], attr))

    # close both files
    src.close()
    dst.close()

if __name__ == '__main__':
    main()

