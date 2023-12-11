#!/usr/bin/env python3

import os

local_top_dir = '/crunch/c0/NARR/3_hr_all/'
remote_top_dir = 'https://downloads.psl.noaa.gov/Datasets/NARR/monolevel/'

variable_list = ["acpcp", "air.2m", "apcp", "cape", "cin", "dpt.2m", "hlcy", "pres.sfc", "shum.2m", "uwnd.10m", "vwnd.10m"]
#year_range = range(2016, 2022)
year_range = range(2022, 2023)

for variable in variable_list:
    # check if directory exists locally
    local_dir = local_top_dir + variable + '/'
    if os.path.isdir(local_dir):
        print('Directory ' + local_dir + ' exists')
    for year in year_range:
        local_file = local_dir + variable + '.' + str(year) + '.nc'
        if os.path.isfile(local_file):
            print('File ' + local_file + ' exists')
            os.system('ls -lh ' + local_file)
#            if year==2016:
#                os.system('mv -n ' + local_file + ' ' + local_file + '.old-2022-08-23')
        else:
            print('File ' + local_file + ' is missing')
            remote_file = remote_top_dir + variable + '.' + str(year) + '.nc'
            os.system('curl ' + remote_file + ' -o ' + local_file)


