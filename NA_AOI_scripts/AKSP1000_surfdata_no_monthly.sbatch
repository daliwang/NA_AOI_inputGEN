#!/bin/bash
#SBATCH -A CLI185
#SBATCH -J s_nomonthly_10x100
#SBATCH -p batch_ccsi
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH --mem=1000GB


module load python/3.11-anaconda3
source activate /ccsopen/home/wangd/compEnv

# set up global variables

export kiloCraft=/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/
export NA_inputGEN_path=${kiloCraft}/NA_inputGEN/

AOI_case_date=$(date +'%y%m%d')

NTimes=100
BASEID=AKSPx10
EXPID=${BASEID}x${NTimes}
AOI_case_name=${EXPID}

refcase_root=${kiloCraft}/NA_cases_data/${BASEID}/
case_root=${kiloCraft}/NA_cases_data/${AOI_case_name}/

script_path=${refcase_root}/scripts/

input_domain_path=${refcase_root}/domain_surfdata/
input_domain=${BASEID}_domain.lnd.Daymet_NA.1km.1d.c240524.nc

input_surfdata_path=${refcase_root}/domain_surfdata/
input_surfdata=${BASEID}_surfdata.Daymet_NA.1km.1d.c240524.nc

input_forcing_path=${refcase_root}/forcing/

output_domain_path=${case_root}/domain_surfdata/
output_surfdata_path=${output_domain_path}
output_forcing_path=${case_root}/forcing/

#mkdir ${case_root}
#mkdir ${output_domain_path}
#mkdir ${output_forcing_path}
#mkdir ${case_root}/scripts

output_domain=${EXPID}_domain.lnd.Daymet_NA.1km.1d.c240524.nc
output_surfdata=NoMonthly_${EXPID}_surfdata.Daymet_NA.1km.1d.c240524.nc
#vars="TKCV"

cd ${case_root}/scripts
#cp ${refcase_root}/scripts/* .

# duplicate the domain and surfdata files

#python3 dup_basecase_data.py ${NTimes} ${input_domain_path} ${input_domain} ${output_domain_path} ${output_domain}
python3 dup_basecase_data_no_monthly.py ${NTimes} ${input_surfdata_path} ${input_surfdata} ${output_surfdata_path} ${output_surfdata} >> surfdup_no_monthly.log.${AOI_case_date}

#for file in ${input_forcing_path}/*clmforc*.nc
#do
#  input_forcing=$(basename $file)
#  echo "python3 dup_basecase_data.py" ${NTimes} ${input_forcing_path} ${input_forcing} ${output_forcing_path} ${input_forcing} >> forcingdup.log.${AOI_case_date}
#  python3 dup_basecase_data.py ${NTimes} ${input_forcing_path} ${input_forcing} ${output_forcing_path} ${input_forcing}
#done


