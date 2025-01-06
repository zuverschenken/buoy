import numpy as np
import pandas as pd
import xarray as xr

ds = xr.open_dataset("data/waves_2019-01-01.nc")
data_for_latlon_for_day = ds.sel(latitude=0.0000, longitude=0.0000, method="nearest")
max_height_on_day = data_for_latlon_for_day['hmax'].max()
wave_height = round(max_height_on_day.item(), 3)

print(f"The tallest wave registered at data collection point nearest lat: 0.0, lon: 0.0 on 2019-01-01 was {wave_height} meters tall")



