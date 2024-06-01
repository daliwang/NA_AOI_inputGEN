# create NADaymet_subdomain

import netCDF4 as nc
import numpy as np

from datetime import datetime

# Get current date
current_date = datetime.now()
# Format date to mmddyyyy
formatted_date = current_date.strftime('%y%m%d')

AOI='NADaymet1M'

# save to the 1D domain file
AOI_gridID = str(AOI)+'_gridID.c'+ formatted_date + '.nc'
AOIgridID_start = 0
AOIgridID_end = 1000000
dst = nc.Dataset(AOI_gridID, 'w', format='NETCDF4')

source_file = 'domain.lnd.Daymet_NA.1km.1d.c240521.nc'
# open the 1D domain data
src = nc.Dataset(source_file, 'r', format='NETCDF4')

# read gridID
NA_gridID = src.variables['gridID'][:]

AOI_gridID_arr = NA_gridID[0][AOIgridID_start:AOIgridID_end].copy()

print(AOI_gridID_arr.shape)

# create the gridIDs, lon, and lat variable
ni_dim = dst.createDimension('ni', AOI_gridID_arr.size)
nj_dim = dst.createDimension('nj', 1)

gridID_var = dst.createVariable('gridID', np.int32, ('nj','ni'), zlib=True, complevel=5)
gridID_var.long_name = 'gridId in the NA domain'
gridID_var.decription = "start from #0 at the upper left corner of the domain, covering all land and ocean gridcells" 
dst.variables['gridID'][...] = AOI_gridID_arr
dst.title = 'First 1M land gridcells in the NA Daymet domain'

src.close()
dst.close()

