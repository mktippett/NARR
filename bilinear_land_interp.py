#!/usr/bin/env python3
import numpy as np
import xarray as xr
import pandas as pd
import xesmf as xe
import os

import pathlib

import warnings
warnings.filterwarnings("ignore")

# grid for the xesmf regridding
ds_out = xr.Dataset(
    {
        "lat": (["lat"], np.arange(0, 86 + 1, 1.0)),
        "lon": (["lon"], np.arange(148, 360 + 1, 1.0) - 360),
    }
)

#!curl https://downloads.psl.noaa.gov/Datasets/NARR/time_invariant/land.nc -o land.nc
ds_land = xr.open_dataset('land.nc')
ds_land['land'] = ds_land.land.squeeze('time')
print('Read land')

regridder_bilinear = xe.Regridder(ds_land, ds_out, 'bilinear')
land_1x1_bilinear = regridder_bilinear(ds_land.land)
mask = land_1x1_bilinear.where(land_1x1_bilinear < 0.5, 1)
mask = mask.where(land_1x1_bilinear >= 0.5, 0)
ds_out['mask'] = mask
regridder_bilinear = xe.Regridder(ds_land, ds_out, 'bilinear')

print('regridder done')

# the loopy version
in_top_dir = '/crunch/c0/NARR/3_hr_all/'
out_top_dir = '/crunch/c0/NARR/3_hr_land_1x1/'
#variable_list = ["acpcp", "apcp", "cape", "cin", "hlcy", "shum.2m", "uwnd.10m", "vwnd.10m", "cape_ml"]
variable_list = ["acpcp", "air.2m", "apcp", "cape", "cin", "dpt.2m", "hlcy", "pres.sfc", "shum.2m", "uwnd.10m", "vwnd.10m"]
for variable in variable_list:
    
    outdir = pathlib.Path(out_top_dir + variable + '/' )
    print(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

#    for year in range(1979, 2022):
    for year in range(2022, 2023):
        infile = in_top_dir + variable + '/' + variable + '.' + str(year) + '.nc'
        outfile = out_top_dir + variable + '/' + variable + '.' + str(year) + '.nc'

        if os.path.isfile(outfile):
            print(outfile + ' exists, skipping')
        else:
            print(infile, outfile)
            ds = xr.open_dataset(infile)
            
            # this is for the .2m variables
            variable0 = pathlib.Path(variable).stem
            da = regridder_bilinear(ds[variable0], keep_attrs=True)
            del da.attrs['grid_mapping']
        
            comp = dict(zlib=True)
            da.encoding.update(comp)
            da.to_netcdf(outfile)
            print(outfile)
