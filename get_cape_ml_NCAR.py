import numpy as np
import xarray as xr
import pandas as pd
from datetime import date
import calendar

url_part1 = 'https://rda.ucar.edu/thredds/dodsC/files/g/ds608.0/3HRLY/'
cape_str = 'Convective_available_potential_energy_layer_between_two_pressure_difference_from_ground_layer'

#year = 2017
for year in range(1984, 2017):
    urls = []
    for month in range(1, 13):
        for start in [1, 10, 20]:
            start_date = date(year, month, start)
            if start == 1:
                end_date = date(year, month, start + 8)
            elif start == 10:
                end_date = date(year, month, start + 9)
            elif start == 20:
                last_day_of_month = calendar.monthrange(year, month)[1]
                end_date = date(year, month, last_day_of_month)

            url_last = start_date.strftime('%Y%m_%d') + end_date.strftime('%d')
            url = url_part1 + str(year) + '/NARRpbl_' + url_last + '.tar'
            urls.append(url)

    print('Opening NCAR data')
    url = urls[0]
    print(url)
    ds = xr.open_dataset(urls[0])
    da = ds[cape_str]

    for url in urls[1:]: 
        print(url)
        ds = xr.open_dataset(url)
        da1 = ds[cape_str]
        da = xr.concat([da, da1], dim='time')

    da = da.squeeze().drop(['layer_between_two_pressure_difference_from_ground_layer1', 'reftime'])
    da.name = 'cape_ml'

    ds_land = xr.open_dataset('land.nc')

    da = da.assign_coords(lon=(('y', 'x'), ds_land.lon.data))
    da = da.assign_coords(lat=(('y', 'x'), ds_land.lat.data))

    comp = dict(zlib=True, complevel=5)
    da.encoding.update(comp)

    filename = 'cape_ml.' + str(year) + '.nc'
    print(filename)
    da.to_netcdf(filename)
    print(len(da.time))
