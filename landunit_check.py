import netCDF4 as nc
import numpy as np

source_file = 'MOF21points_surfdata.Daymet_NA.1km.1d.c240523.nc'
# open the 1D domain data
src = nc.Dataset(source_file, 'a', format='NETCDF4')

sand_pct= src['PCT_SAND'][...]
clay_pct= src['PCT_CLAY'][...]
nat_pft_pct=src['PCT_NAT_PFT'][...]

natveg_pct=src['PCT_NATVEG'][...]
crop_pct=src['PCT_CROP'][...]
wetland_pct=src['PCT_WETLAND'][...]
lake_pct=src['PCT_LAKE'][...]
glacier_pct=src['PCT_GLACIER'][...]
urban_pct=src['PCT_URBAN'][...]

wt_lunit= natveg_pct+lake_pct+sum(urban_pct) + wetland_pct+glacier_pct+crop_pct

lake_pct_n=lake_pct/wt_lunit * 100
natveg_pct_n=natveg_pct/wt_lunit * 100
urban_pct_n=np.zeros((3,21), dtype=np.float64)
urban_pct_n[0]=urban_pct[0]/wt_lunit * 100
urban_pct_n[1]=urban_pct[1]/wt_lunit * 100
urban_pct_n[2]=urban_pct[2]/wt_lunit * 100
wetland_pct_n= wetland_pct/wt_lunit * 100
glacier_pct_n=glacier_pct/wt_lunit * 100
crop_pct_n   =crop_pct/wt_lunit * 100

wt_lunit_n = natveg_pct_n+lake_pct_n+sum(urban_pct_n) + wetland_pct_n+glacier_pct_n+crop_pct_n

src['PCT_NATVEG'][...]=natveg_pct_n
src['PCT_CROP'][...]=crop_pct_n
src['PCT_WETLAND'][...]=wetland_pct_n
src['PCT_LAKE'][...]=lake_pct_n
src['PCT_GLACIER'][...]=glacier_pct_n
src['PCT_URBAN'][...]=urban_pct_n

src.close()
