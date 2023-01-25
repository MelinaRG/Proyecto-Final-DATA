import pandas as pd
import numpy as np
import datetime as dt
from sqlalchemy import create_engine
import time

product_cat_name=pd.read_csv("Datasets/product_category_name_translation.csv")


#Obtiene el tiempo actual
start_time = time.time()


#Product Category Name Translation

def etl_product_cat(product_cat_name):
    product_cat_name=product_cat_name.append({"product_category_name" : "pc_gamer" , "product_category_name_english" : "pc_gamer"} , ignore_index=True)
    product_cat_name=product_cat_name.append({"product_category_name" : "portateis_cozinha_e_preparadores_de_alimentos" , "product_category_name_english" : "kitchen_and_food_preparation_racks"} , ignore_index=True)

    product_cat_name["product_category_name"]=product_cat_name["product_category_name"].str.replace("_"," ")
    product_cat_name["product_category_name_english"]=product_cat_name["product_category_name_english"].str.replace("_"," ")

    engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

    product_cat_name.to_sql('product_category_name_translation', engine, if_exists='append', index=False)

    print('product_cat_name load')

    engine.dispose()