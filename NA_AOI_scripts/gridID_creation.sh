#!/bin/bash

#kiloCraft=/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/

#NA_inputGEN_path=${kiloCraft}/NA_inputGEN/

#NA_domain_path=${kiloCraft}/Daymet_NA_1D/

#NA_domain=domain.lnd.Daymet_NA.1km.1d.c240521.nc

#AOI_case_name=NApoint5

output_path=${kiloCraft}/NA_cases_data/${AOI_case_name}/domain_surfdata/

mkdir ${output_path}

# create gridIDs 
# NADaymet_subdomain.py in the NA_inputGEN contains the scirpt for 1M gridcell case
# we need to copy it to the current directory and change the start/end gridIDs
# for the 3M case (1,000,000:4,000,000)

echo ${NA_domain_path}  ${output_path}  ${AOI_case_name}

python3 ${AOI_case_name}_subdomain.py ${NA_domain_path}  ${output_path}  ${AOI_case_name}

