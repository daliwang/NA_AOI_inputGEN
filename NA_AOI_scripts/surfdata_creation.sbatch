#!/bin/bash
#SBATCH -A CLI185
#SBATCH -J NADaymet1M_surfdataGEN
#SBATCH -p batch_ccsi
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH --mem=500GB


module load python/3.11-anaconda3
source activate /ccsopen/home/wangd/compEnv

cd /gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_inputGEN/


#Example use: python NA_AOI_surfdataGEN.py <input_path> <NA_surfdata> <output_path> <AOI_file_path>  <AOI_points_file>
# <input_path>: path to the 1D surfdata source data directory
# <NA_surfdata>: 1D NA_surfdata.nc
# <output_path>:  path for the 1D AOI surface data directory
# <AOI_file_path>:  path to the <AOI_points_files>
# <AOI_points_file>:  <AOI>_gridID.csv or <AOI>_domain.nc
# The code uses NA surfdata  to generation 1D AOI surfdata

date

EXPID="NADaymet1M"
NA_surfdata_path="/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/Daymet_NA_1D/"
NA_surfdata="surfdata.Daymet_NA.1km.1d.c240327.nc"

output_path=/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_cases_data/$EXPID/domain_surfdata/

AOI_file_path=/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_cases_data/${EXPID}/domain_surfdata/ 
AOI_points_file=${EXPID}_domain.lnd.Daymet_NA.1km.1d.c240601.nc

srun -n 1 python3 NA_AOI_surfdataGENv2.py ${NA_surfdata_path} ${NA_surfdata} ${output_path} ${AOI_file_path} ${AOI_points_file} >& ${output_path}${EXPID}_surfgen.log
