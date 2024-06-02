#!/bin/bash

export kiloCraft='/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/'

export NA_inputGEN_path=${kiloCraft}/NA_inputGEN/

export NA_domain_path=${kiloCraft}/Daymet_NA_1D/

export NA_domain="domain.lnd.Daymet_NA.1km.1d.c240521.nc"

export output_path=${kiloCraft}/NA_cases_data/NADaymet1M/domain_surfdata/

export AOI_case_name='NADaymet1M'

# create gridIDs 

cd ${NA_inputGEN_path} 

echo ${NA_domain_path}  ${output_path}  ${AOI_case_name}

python3 NADaymet_subdomain.py  ${NA_domain_path}  ${output_path}  ${AOI_case_name}

