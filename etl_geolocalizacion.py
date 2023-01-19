# Librerias
import pandas as pd
import numpy as np


""" # Api requests
import json
import requests

import geocoder """


""" # DUNCIONES NECESARIAS
# Funciones de latitud y longitud Geocoder
def find_latitud_geocoder(localizador):
    loc = geocoder.osm(localizador)
    return loc.lat

def find_longitud_geocoder(localizador):
    loc = geocoder.osm(localizador)
    return loc.lng """



# ETL
#Datasets
df_geo = pd.read_csv('./datasets/olist_geolocation_dataset.csv',dtype={'geolocation_zip_code_prefix': str})
df_sell = pd.read_csv('./datasets/olist_sellers_dataset.csv',dtype={'seller_zip_code_prefix': str})
df_cust = pd.read_csv('./datasets/olist_customers_dataset.csv',dtype={'customer_zip_code_prefix': str})
df_coord_estados = pd.read_csv('./datasets_auxiliares/cordenadas_estados.csv',sep=';')
df_coord_ciudades = pd.read_csv('./datasets_auxiliares/coordenadas.csv')
br_info = pd.read_csv('./datasets_auxiliares/br_info.csv')


# Renombre de columnas

df_geo.rename(columns={'geolocation_zip_code_prefix': 'zip_code_prefix','geolocation_city': 'city','geolocation_state': 'state'}, inplace=True)
df_sell.rename(columns={'seller_zip_code_prefix': 'zip_code_prefix', 'seller_city': 'city', 'seller_state': 'state'}, inplace=True)
df_cust.rename(columns={'customer_zip_code_prefix': 'zip_code_prefix', 'customer_city': 'city', 'customer_state': 'state'}, inplace=True)

# Concatención
# Concateno todos los datasets
df_concat = pd.concat([df_geo,df_sell[['zip_code_prefix','city','state']],df_cust[['zip_code_prefix','city','state']]],axis=0)

# PROCESAMIENTO
df_procesado = df_concat.groupby(by='zip_code_prefix', as_index=False).min()
df_procesado = df_procesado.merge(br_info, how='left', left_on='state', right_on='sigla')
# Renombre
df_procesado.rename(columns={'id': 'id_state', 'state':'state_sigla','nome':'state_name','nome_regiao':'region_name'}, inplace=True)
# Drop de sigla
df_procesado.drop(columns=['sigla'],inplace=True)
# Reordenado
df_procesado = df_procesado[['zip_code_prefix','region_name','id_state','state_sigla','state_name','city','geolocation_lat','geolocation_lng']]
# Añado columna localizador
df_procesado['localizador'] = df_procesado['city'] + ' ' + df_procesado['state_sigla'] + ', Brazil'
# Merge con coordenadas de city y estados
df_procesado = df_procesado.merge(df_coord_ciudades[['localizador','latitud','longitud']], on = 'localizador')
df_procesado = df_procesado.merge(df_coord_estados, how='left', left_on='state_sigla', right_on='uf')
# Renombre columnas
df_procesado.rename(columns={'latitud': 'latitud_city','longitud': 'longitud_city','latitude': 'latitud_state', 'longitude':'longitud_state'}, inplace=True)
# Elimino geolocation_latitude y geolocation_longitude y uf
df_final_procesado = df_procesado.drop(columns=['uf','geolocation_lat','geolocation_lng'])

# EXPORTACION CSV
df_final_procesado.to_csv('./datasets_auxiliares/pipeline_geo.csv', index=False)
