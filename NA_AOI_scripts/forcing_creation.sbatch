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

date_string=$(date +'%y%m%d-%H%M')

EXPID="NADaymet1M"
NA_forcing_path="/gpfs/wolf2/cades/cli185/proj-shared/wangd/Forcing_2014/daymet4_1d/"

output_path=/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_cases_data/$EXPID/forcing/

AOI_file_path=/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_cases_data/${EXPID}/domain_surfdata/ 
AOI_points_file=${EXPID}_domain.lnd.Daymet_NA.1km.1d.c240601.nc


#if len(sys.argv) != 5  or sys.argv[1] == '--help':  # sys.argv includes the script name as the first argument
#    print("Example use: python AOI_forcingGEN.py <input_path> <output_path> <AOI_gridID_path> <AOI_points_file>")
#    print(" <input_path>: path to the 1D source data directory")
#    print(" <output_path>:  path for the 1D AOI forcing data directory")
#    print(" <AOI_gridID_path>:  path to the AOI_gridID_file")
#    print(" <AOI_gridID_file>:  <AOI>_gridID.csv or <AOI>_domain.nc")
#    print(" The code uses NA forcing to generation 1D AOI forcing")              
#    exit(0)
    
srun -n 1 python3 NA_AOI_forcingGEN.py ${NA_forcing_path} ${output_path} ${AOI_file_path} ${AOI_points_file} >& ${output_path}${EXPID}_forcinggen.log.${date_string}


