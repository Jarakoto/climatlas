import pandas as pd
import geopandas
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine('postgresql://postgres:docker@localhost:25433/climatlas', pool_recycle=3600)

date_parser = lambda x: datetime.strptime(x, '%Y%m%d')

df = pd.read_csv(
  '../data/temp_moyen_2m_test.txt', sep=" ", skiprows=40,
  names=['date', 'lat', 'lon', 'temp'],
  parse_dates=['date'],
  date_parser=date_parser
)
df['id'] = df['lat'].astype(str) + df['lon'].astype(str)
gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lat, df.lon))
del gdf['lat']
del gdf['lon']

gdf.to_postgis('temperatures', engine)
