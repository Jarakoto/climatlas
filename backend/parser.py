import pandas as pd
import geopandas
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine('postgresql://postgres:docker@localhost:25433/climatlas', pool_recycle=3600)

date_parser = lambda x: datetime.strptime(x, '%Y%m%d')

source_dataframe = pd.read_csv(
  '../data/temp_moyen_2m_test.txt', sep=" ", skiprows=40,
  names=['date', 'lat', 'lon', 'temp'],
  parse_dates=['date'],
  date_parser=date_parser
)
source_dataframe['id'] = source_dataframe['lat'].astype(str) + source_dataframe['lon'].astype(str)

# For each zoom level
for zoom_level in range(11, 17):
  for time_scale in ['D', 'W', 'M', 'Y']:
    # Create the corresponding data frame
      scaled_data_frame = 
    
  

gdf = geopandas.GeoDataFrame(source_dataframe, geometry=geopandas.points_from_xy(source_dataframe.lat, source_dataframe.lon))
del gdf['lat']
del gdf['lon']

gdf.to_postgis('temperatures', engine)
