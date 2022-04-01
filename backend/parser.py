import pandas as pd
import geopandas
from sqlalchemy import inspect, create_engine, MetaData, Table, Column, Date, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from datetime import datetime

from utils.GeoUtils import deg2num

engine = create_engine('postgresql://postgres:docker@localhost:25433/climatlas', pool_recycle=3600)

date_parser = lambda x: datetime.strptime(x, '%Y%m%d')

source_dataframe = pd.read_csv(
  '../data/temp_moyen_2m_test_2.txt', sep=" ", skiprows=40,
  names=['date', 'lat', 'lon', 'temp'],
  parse_dates=['date'],
  date_parser=date_parser
)

# For each zoom level
for zoom_level in range(11, 17):
  # Get the corresponding tile for each measure
  generic_level_df = source_dataframe.copy()
  generic_level_df['tile_x'] = generic_level_df.apply(lambda row: deg2num(row.lat, row.lon, zoom_level)[0], axis=1)
  generic_level_df['tile_y'] = generic_level_df.apply(lambda row: deg2num(row.lat, row.lon, zoom_level)[1], axis=1)
  generic_level_df = generic_level_df.groupby(['date', 'tile_x', 'tile_y']).agg({ 'temp': ['min', 'max', 'mean'] })
  generic_level_df = generic_level_df.reset_index()

  for time_scale in ['D', 'W', 'M', 'Y']:
    table_name = "z{}_{}".format(zoom_level, time_scale)
    generic_level_df.resample(time_scale, on='date')
    generic_level_df.agg(['mean', 'min', 'max'])
    # Create the corresponding data frame
    scaled_data_frame = generic_level_df.copy()
    # Aggregate the statistics
    scaled_data_frame = scaled_data_frame.agg(['min','max','mean'])

    RECALCULER LAT LONG DEPUIS LES TILES PUIS SUPPRIMER LES TILES

    gdf = geopandas.GeoDataFrame(
      scaled_data_frame, geometry=geopandas.points_from_xy(
        scaled_data_frame.lat, scaled_data_frame.lon
      )
    )
    del gdf['lat']
    del gdf['lon']

    gdf.to_postgis(table_name, engine, if_exists='replace')
