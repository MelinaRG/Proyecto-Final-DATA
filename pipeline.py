import pandas as pd
import numpy as np
import datetime as dt
from sqlalchemy import create_engine

#df11=pd.read_csv("Datasets/product_category_name_translation.csv")

#df11=df11.append({"product_category_name" : "pc_gamer" , "product_category_name_english" : "pc_gamer"} , ignore_index=True)
#df11=df11.append({"product_category_name" : "portateis_cozinha_e_preparadores_de_alimentos" , "product_category_name_english" : "kitchen and food preparation racks"} , ignore_index=True)

#engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

#df11.to_sql('product_category_name_translation', engine, if_exists='append', index=False)

#engine.dispose()


#df9=pd.read_csv("Datasets/olist_products_dataset.csv")

#df9.drop(columns=["product_name_lenght","product_description_lenght","product_weight_g","product_length_cm","product_height_cm","product_width_cm"],axis=1,inplace=True)

#df9["product_photos_qty"].fillna(0.0,inplace=True)

#engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

#df9.to_sql('products', engine, if_exists='append', index=False)

#engine.dispose()


#df1=pd.read_csv("Datasets/olist_closed_deals_dataset.csv")

#df1.drop(columns=["sdr_id","sr_id","lead_behaviour_profile","has_company","has_gtin","average_stock","business_type","declared_product_catalog_size","declared_monthly_revenue"],axis=1,inplace=True)

#df1["won_date"]=pd.to_datetime(df1["won_date"],format="%Y-%m-%d %H:%M:%S")

#df1.fillna("SIN DATO",inplace=True)

#engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

#df1.to_sql('closed_deals', engine, if_exists='append', index=False)

#engine.dispose()


#df4=pd.read_csv("Datasets/olist_marketing_qualified_leads_dataset.csv")

#df4.drop(columns=["landing_page_id"],axis=1,inplace=True)

#df4["first_contact_date"]=pd.to_datetime(df4["first_contact_date"],format="%Y-%m-%d %H:%M:%S")

#df4.fillna("SIN DATO",inplace=True)

#engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

#df4.to_sql('marketing_qualified_leads', engine, if_exists='append', index=False)


#df10=pd.read_csv("Datasets/olist_sellers_dataset.csv",dtype={"seller_zip_code_prefix": str})

#df10.drop(columns=["seller_city","seller_state"],axis=1,inplace=True)

#df10['seller_zip_code_prefix'] = df10['seller_zip_code_prefix'].astype('string')

#engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

#df10.to_sql('marketing_qualified_leads', engine, if_exists='append', index=False)

