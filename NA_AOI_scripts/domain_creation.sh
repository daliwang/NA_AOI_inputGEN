# Domain data generation

#!/bin/bash

#kiloCraft='/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/'

#NA_inputGEN_path=${kiloCraft}/NA_inputGEN/

#export NA_domain_path=${kiloCraft}/Daymet_NA_1D/

#export NA_domain="domain.lnd.Daymet_NA.1km.1d.c240521.nc"

#export AOI_case_name="NApoint5"
#output_path=${kiloCraft}/NA_cases_data/${AOI_case_name}/domain_surfdata/

cd ${NA_inputGEN_path}
 
# create gridIDs 
#echo ${NA_domain_path}  ${output_path}  ${AOI_case_name}
#python3 NADaymet_subdomain.py  ${NA_domain_path}  ${output_path}  ${AOI_case_name}

# create domain files

AOI_gridID_file=${AOI_case_name}_gridID.c${AOI_case_date}.nc
#AOI_gridfile_path=${kiloCraft}/NA_cases_data/${AOI_case_name}/domain_surfdata/
#AOI_domain_output_path=${kiloCraft}/NA_cases_data/${AOI_case_name}/domain_surfdata/
AOI_gridfile_path=${output_path}
AOI_domain_output_path=${output_path}

echo "python3 NA_AOI_domainGENv2.py" ${AOI_gridfile_path} ${AOI_domain_output_path} ${AOI_gridID_file}
python3 NA_AOI_domainGENv2.py ${AOI_gridfile_path} ${AOI_domain_output_path} ${AOI_gridID_file}


# surfdata generation

#python3 /gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_inputGEN/NA_AOI_surfdataGEN.py /gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/Daymet_NA_1D/ surfdata.Daymet_NA.1km.1d.c240327.nc /gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_cases_data/ /gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_cases_data/MOF21points/ MOF21points_domain.lnd.Daymet_NA.1km.1d.c240522.nc

# we use batch job to create the surfdata, which will take around 2 hours. 
# command sbatch surfdata_generation.sbatch

