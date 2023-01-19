import pandas as pd
import numpy as np
import datetime as dt
from sqlalchemy import create_engine
import time

# Obtiene el tiempo actual
start_time = time.time()


df11=pd.read_csv("Datasets/product_category_name_translation.csv")

df11=df11.append({"product_category_name" : "pc_gamer" , "product_category_name_english" : "pc_gamer"} , ignore_index=True)
df11=df11.append({"product_category_name" : "portateis_cozinha_e_preparadores_de_alimentos" , "product_category_name_english" : "kitchen_and_food_preparation_racks"} , ignore_index=True)

df11["product_category_name"]=df11["product_category_name"].str.replace("_"," ")
df11["product_category_name_english"]=df11["product_category_name_english"].str.replace("_"," ")

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df11.to_sql('product_category_name_translation', engine, if_exists='append', index=False)

print('df11 cargada')


geo=pd.read_csv("Datasets_auxiliares/pipeline_geo.csv", dtype= {'zip_code_prefix': str})

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

geo.to_sql('geolocation', engine, if_exists='append', index=False)

print('geo cargada')


df4=pd.read_csv("Datasets/olist_marketing_qualified_leads_dataset.csv")

df4.drop(columns=["landing_page_id"],axis=1,inplace=True)

df4["first_contact_date"]=pd.to_datetime(df4["first_contact_date"],format="%Y-%m-%d %H:%M:%S")

df4.fillna("SIN DATO",inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df4.to_sql('marketing_qualified_leads', engine, if_exists='append', index=False)

print('df4 cargada')


df1=pd.read_csv("Datasets/olist_closed_deals_dataset.csv")
df10=pd.read_csv("Datasets/olist_sellers_dataset.csv",dtype={"seller_zip_code_prefix": str})

df10.drop(columns=["seller_city","seller_state"],axis=1,inplace=True)

mergeauxiliar=pd.merge(left=df10,right=df1,how="outer",on="seller_id")
df10=mergeauxiliar.iloc[:,0:2]

df10['seller_zip_code_prefix'] = df10['seller_zip_code_prefix'].astype('string')

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df10.to_sql('olist_sellers', engine, if_exists='append', index=False)

print('df10 cargada')


df1=pd.read_csv("Datasets/olist_closed_deals_dataset.csv")

df1.drop(columns=["sdr_id","sr_id","lead_behaviour_profile","has_company","has_gtin","average_stock","business_type","declared_product_catalog_size","declared_monthly_revenue"],axis=1,inplace=True)

df1["won_date"]=pd.to_datetime(df1["won_date"],format="%Y-%m-%d %H:%M:%S")

df1.fillna("SIN DATO",inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df1.to_sql('closed_deals', engine, if_exists='append', index=False)

print('df1 cargada')


df2=pd.read_csv("Datasets/olist_customers_dataset.csv",dtype={"customer_zip_code_prefix": str})

df2.drop(columns=["customer_city","customer_state"],axis=1,inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df2.to_sql('customers', engine, if_exists='append', index=False)

print('df2 cargada')

df8=pd.read_csv("Datasets/olist_orders_dataset.csv")

df8["order_purchase_timestamp"]=pd.to_datetime(df8["order_purchase_timestamp"],format="%Y-%m-%d %H:%M:%S")
df8["order_approved_at"]=pd.to_datetime(df8["order_approved_at"],format="%Y-%m-%d %H:%M:%S")
df8["order_delivered_carrier_date"]=pd.to_datetime(df8["order_delivered_carrier_date"],format="%Y-%m-%d %H:%M:%S")
df8["order_delivered_customer_date"]=pd.to_datetime(df8["order_delivered_customer_date"],format="%Y-%m-%d %H:%M:%S")
df8["order_estimated_delivery_date"]=pd.to_datetime(df8["order_estimated_delivery_date"],format="%Y-%m-%d %H:%M:%S")

df8['difference_days1'] = df8['order_approved_at'] - df8['order_purchase_timestamp']
df8['difference_days2'] = df8['order_delivered_carrier_date'] - df8['order_approved_at']
df8['difference_days3'] = df8['order_delivered_customer_date'] - df8['order_approved_at']
df8['difference_days4'] = df8['order_delivered_customer_date'] - df8['order_delivered_carrier_date']
df8['difference_days5'] = df8['order_estimated_delivery_date'] - df8['order_delivered_customer_date']

df8["order_approved_at_new"]=df8["order_purchase_timestamp"]+(df8["order_delivered_carrier_date"]-df8["order_purchase_timestamp"])/2

df8.loc[(df8["difference_days2"]<pd.Timedelta(0)) & (df8["difference_days3"]<pd.Timedelta(0)),"order_approved_at"]=df8.loc[(df8["difference_days2"]<pd.Timedelta(0)) & (df8["difference_days3"]<pd.Timedelta(0)),"order_approved_at_new"]

df8["order_delivered_carrier_date_new"]=df8["order_approved_at"]+(df8["order_delivered_customer_date"]-df8["order_approved_at"])/2

df8.loc[df8["difference_days2"]<pd.Timedelta(0),"order_delivered_carrier_date"]=df8.loc[df8["difference_days2"]<pd.Timedelta(0),"order_delivered_carrier_date_new"]

df8["order_delivered_carrier_date_new"]=df8["order_approved_at"]+(df8["order_delivered_customer_date"]-df8["order_approved_at"])/2

df8.loc[df8["difference_days4"]<pd.Timedelta(0),"order_delivered_carrier_date"]=df8.loc[df8["difference_days4"]<pd.Timedelta(0),"order_delivered_carrier_date_new"]

df8["order_delivered_carrier_date_new"]=df8["order_approved_at"]+(df8["order_delivered_customer_date"]-df8["order_approved_at"])/2
df8.loc[(df8["order_status"]=="delivered") & (df8["order_delivered_carrier_date"].isnull()),"order_delivered_carrier_date"]=df8.loc[(df8["order_status"]=="delivered") & (df8["order_delivered_carrier_date"].isnull()),"order_delivered_carrier_date_new"]

df8.loc[(df8["order_status"]=="delivered") & (df8["order_delivered_carrier_date"].isnull()),"order_status"]="approved"

df8["order_approved_at_new"]=df8["order_purchase_timestamp"]+(df8["order_delivered_carrier_date"]-df8["order_purchase_timestamp"])/2
df8.loc[(df8["order_status"]=="delivered") & (df8["order_approved_at"].isnull()),"order_approved_at"]=df8.loc[(df8["order_status"]=="delivered") & (df8["order_approved_at"].isnull()),"order_approved_at_new"]

df8.loc[(df8["order_status"]=="delivered")&(df8["order_delivered_customer_date"].isnull()),"order_status"]="shipped"

df8.drop(columns=["difference_days1","difference_days2","difference_days3","difference_days4","difference_days5","order_approved_at_new","order_delivered_carrier_date_new"],inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df8.to_sql('orders', engine, if_exists='append', index=False)

print('df8 cargada')


df6=pd.read_csv("Datasets/olist_order_payments_dataset.csv")

df6.drop(columns=["payment_sequential"],axis= 1, inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df6.to_sql('order_payments', engine, if_exists='append', index=False)

print('df6 cargada')


df7=pd.read_csv("Datasets/olist_order_reviews_dataset.csv")

df7["review_creation_date"]=pd.to_datetime(df7["review_creation_date"],format="%Y-%m-%d %H:%M:%S")
df7["review_answer_timestamp"]=pd.to_datetime(df7["review_answer_timestamp"],format="%Y-%m-%d %H:%M:%S")

df7["review_comment_title"].fillna("SIN TITULO",inplace=True)
df7["review_comment_message"].fillna("SIN COMENTARIOS",inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df7.to_sql('order_reviews', engine, if_exists='append', index=False)

print('df7 cargada')


df9=pd.read_csv("Datasets/olist_products_dataset.csv")

df9.drop(columns=["product_name_lenght","product_description_lenght","product_weight_g","product_length_cm","product_height_cm","product_width_cm"],axis=1,inplace=True)

df9["product_photos_qty"].fillna(0.0,inplace=True)
df9["product_photos_qty"] = df9["product_photos_qty"] .astype("int")
df9["product_category_name"]=df9["product_category_name"].str.replace("_"," ")

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df9.to_sql('products', engine, if_exists='append', index=False)

print('df9 cargada')


df5=pd.read_csv("Datasets/olist_order_items_dataset.csv")

df5["shipping_limit_date"]=pd.to_datetime(df5["shipping_limit_date"],format="%Y-%m-%d %H:%M:%S")

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

df5.to_sql('order_items', engine, if_exists='append', index=False)

print('df5 cargada')

engine.dispose()

# Obtiene el tiempo final
end_time = time.time()

# Calcula el tiempo de ejecución total
total_time = end_time - start_time

# Convierte el tiempo de ejecución total a minutos y segundos
minutes, seconds = divmod(total_time, 60)

# Imprime el tiempo de ejecución total en minutos y segundos
print("Tiempo de ejecución total: {:.0f} minutos y {:.2f} segundos".format(minutes, seconds))