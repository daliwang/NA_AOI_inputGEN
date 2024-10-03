import numpy as np
import pandas as pd
from netCDF4 import Dataset
from scipy.spatial import cKDTree

# Read the masked gridcells from the input file
def read_masked_gridcells(file_path):
    return pd.read_csv(file_path, skiprows=1, header=None, names=['lon', 'lat'])

# Load the NetCDF domain file
def load_netcdf_file(file_path):
    return Dataset(file_path, mode='r+')

# Find the nearest grid cell for given (lon, lat)
def find_nearest_gridcell(lon, lat, xc, yc):
    # Create a KDTree for efficient nearest neighbor search
    tree = cKDTree(np.column_stack((xc, yc)))
    dist, index = tree.query((lon, lat))
    return index

# Update Mask and Frac values in the domain dataset
def update_netcdf_mask_and_frac(nc_file, indices):
    # Update the mask and frac values for the identified indices
    nc_file.variables['mask'][0, indices] = 0
    nc_file.variables['frac'][0, indices] = 0.0

def main():
    # Path to the input files
    csv_file_path = 'masked_NAgridcell.txt'
    netcdf_file_path = 'NApoint5_domain.lnd.Daymet_NA.1km.1d.c240606.nc'
    
    # Read input data
    masked_gridcells = read_masked_gridcells(csv_file_path)
    
    # Load the NetCDF file
    nc_file = load_netcdf_file(netcdf_file_path)
    
    # Read the necessary variables
    xc = nc_file.variables['xc'][:].squeeze()
    yc = nc_file.variables['yc'][:].squeeze()
    print("xc", xc)
    print("yc", yc)

    # Loop over each (lon, lat) and find the nearest gridcell
    for index, row in masked_gridcells.iterrows():
        lon = row['lon']
        lat = row['lat']
        
        # Find the nearest grid cell index
        nearest_index = find_nearest_gridcell(lon, lat, xc, yc)
            
        print(f'Location of gridcell for lon={lon}, lat={lat} is index {nearest_index}')
        
        # Modify the mask and frac variables
        # Handle the case if nearest_index is valid
        if 0 <= nearest_index < len(nc_file.variables['mask'][:]):
            update_netcdf_mask_and_frac(nc_file, nearest_index)
    
    # Save the modified netcdf as a new file
    nc_file.close()
    '''
    # Re-open for writing to a new file
    with Dataset(netcdf_file_path, mode='r') as src:
        with Dataset(output_netcdf_file_path, mode='w', format='NETCDF4') as dst:
            # Copy dimensions
            for name, dimension in src.dimensions.items():
                dst.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
                
            # Copy variables
            for name, variable in src.variables.items():
                new_var = dst.createVariable(name, variable.datatype, variable.dimensions)
                dst[name][:] = src[name][:]
    
            # Now that we have the new structure, let's update the mask and frac variables
            for index, row in masked_gridcells.iterrows():
                lon = row['lon']
                lat = row['lat']
                nearest_index = find_nearest_gridcell(lon, lat, nc_file.variables['xc'][:], nc_file.variables['yc'][:])
                if 0 <= nearest_index < len(src.variables['mask'][:]):
                    dst.variables['mask'][nearest_index] = 0
                    dst.variables['frac'][nearest_index] = 0.0
                
    print(f'Modified NetCDF file has been saved as {output_netcdf_file_path}')
    '''
if __name__ == '__main__':
    main()
