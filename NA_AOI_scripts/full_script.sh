#!/bin/bash

# set up global variables

export kiloCraft=/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/

export NA_inputGEN_path=${kiloCraft}/NA_inputGEN/

export NA_domain_path=${kiloCraft}/Daymet_NA_1D/
export NA_domain=domain.lnd.Daymet_NA.1km.1d.c240521.nc

export AOI_case_name=NApoint5
export AOI_case_date=$(date +'%y%m%d')
export EXPID=${AOI_case_name}

export script_path=${kiloCraft}/NA_cases_data/${AOI_case_name}/scripts/
export output_path=${kiloCraft}/NA_cases_data/${AOI_case_name}/domain_surfdata/
export forcing_output_path=${kiloCraft}/NA_cases_data/${AOI_case_name}/forcing/

export NA_surfdata_path="/gpfs/wolf2/cades/cli185/proj-shared/wangd/kiloCraft/NA_cases_data/NADaymet/"
export NA_surfdata="NADaymet_surfdata.Daymet_NA.1km.1d.c240327.nc"

mkdir ${output_path}
mkdir ${forcing_output_path}

# after the changes in the ${AOI_case_name}_subdomain.py
# create gridID file
source ${script_path}/gridID_creation.sh

# create domain file
source ${script_path}/domain_creation.sh

# create surfdata
sbatch ${script_path}/surfdata_creation.sbatch

# create forcing
sbatch ${script_path}/forcing_creation.sbatch
