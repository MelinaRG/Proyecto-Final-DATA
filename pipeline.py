import pandas as pd
import numpy as np
import datetime as dt
from sqlalchemy import create_engine
import time

# Obtiene el tiempo actual
start_time = time.time()


product_cat_name=pd.read_csv("Datasets/product_category_name_translation.csv")

product_cat_name=product_cat_name.append({"product_category_name" : "pc_gamer" , "product_category_name_english" : "pc_gamer"} , ignore_index=True)
product_cat_name=product_cat_name.append({"product_category_name" : "portateis_cozinha_e_preparadores_de_alimentos" , "product_category_name_english" : "kitchen_and_food_preparation_racks"} , ignore_index=True)

product_cat_name["product_category_name"]=product_cat_name["product_category_name"].str.replace("_"," ")
product_cat_name["product_category_name_english"]=product_cat_name["product_category_name_english"].str.replace("_"," ")

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

product_cat_name.to_sql('product_category_name_translation', engine, if_exists='append', index=False)

print('product_cat_name load')


geolocation=pd.read_csv("Datasets_auxiliares/pipeline_geolocation.csv", dtype= {'zip_code_prefix': str})

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

geolocation.to_sql('geolocationlocation', engine, if_exists='append', index=False)

print('geolocation load')


marketing=pd.read_csv("Datasets/olist_marketing_qualified_leads_dataset.csv")

marketing.drop(columns=["landing_page_id"],axis=1,inplace=True)

marketing["first_contact_date"]=pd.to_datetime(marketing["first_contact_date"],format="%Y-%m-%d %H:%M:%S")

marketing.fillna("SIN DATO",inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

marketing.to_sql('marketing_qualified_leads', engine, if_exists='append', index=False)

print('marketing load')


closed_deals=pd.read_csv("Datasets/olist_closed_deals_dataset.csv")
sellers=pd.read_csv("Datasets/olist_sellers_dataset.csv",dtype={"seller_zip_code_prefix": str})

sellers.drop(columns=["seller_city","seller_state"],axis=1,inplace=True)

mergeauxiliar=pd.merge(left=sellers,right=closed_deals,how="outer",on="seller_id")
sellers=mergeauxiliar.iloc[:,0:2]

sellers['seller_zip_code_prefix'] = sellers['seller_zip_code_prefix'].astype('string')

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

sellers.to_sql('olist_sellers', engine, if_exists='append', index=False)

print('sellers load')


closed_deals=pd.read_csv("Datasets/olist_closed_deals_dataset.csv")

closed_deals.drop(columns=["sdr_id","sr_id","lead_behaviour_profile","has_company","has_gtin","average_stock","business_type","declared_product_catalog_size","declared_monthly_revenue"],axis=1,inplace=True)

closed_deals["won_date"]=pd.to_datetime(closed_deals["won_date"],format="%Y-%m-%d %H:%M:%S")

closed_deals.fillna("SIN DATO",inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

closed_deals.to_sql('closed_deals', engine, if_exists='append', index=False)

print('closed_deals load')


customers=pd.read_csv("Datasets/olist_customers_dataset.csv",dtype={"customer_zip_code_prefix": str})

customers.drop(columns=["customer_city","customer_state"],axis=1,inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

customers.to_sql('customers', engine, if_exists='append', index=False)

print('customers load')

orders=pd.read_csv("Datasets/olist_orders_dataset.csv")

orders["order_purchase_timestamp"]=pd.to_datetime(orders["order_purchase_timestamp"],format="%Y-%m-%d %H:%M:%S")
orders["order_approved_at"]=pd.to_datetime(orders["order_approved_at"],format="%Y-%m-%d %H:%M:%S")
orders["order_delivered_carrier_date"]=pd.to_datetime(orders["order_delivered_carrier_date"],format="%Y-%m-%d %H:%M:%S")
orders["order_delivered_customer_date"]=pd.to_datetime(orders["order_delivered_customer_date"],format="%Y-%m-%d %H:%M:%S")
orders["order_estimated_delivery_date"]=pd.to_datetime(orders["order_estimated_delivery_date"],format="%Y-%m-%d %H:%M:%S")

orders['difference_days1'] = orders['order_approved_at'] - orders['order_purchase_timestamp']
orders['difference_days2'] = orders['order_delivered_carrier_date'] - orders['order_approved_at']
orders['difference_days3'] = orders['order_delivered_customer_date'] - orders['order_approved_at']
orders['difference_days4'] = orders['order_delivered_customer_date'] - orders['order_delivered_carrier_date']
orders['difference_days5'] = orders['order_estimated_delivery_date'] - orders['order_delivered_customer_date']

orders["order_approved_at_new"]=orders["order_purchase_timestamp"]+(orders["order_delivered_carrier_date"]-orders["order_purchase_timestamp"])/2

orders.loc[(orders["difference_days2"]<pd.Timedelta(0)) & (orders["difference_days3"]<pd.Timedelta(0)),"order_approved_at"]=orders.loc[(orders["difference_days2"]<pd.Timedelta(0)) & (orders["difference_days3"]<pd.Timedelta(0)),"order_approved_at_new"]

orders["order_delivered_carrier_date_new"]=orders["order_approved_at"]+(orders["order_delivered_customer_date"]-orders["order_approved_at"])/2

orders.loc[orders["difference_days2"]<pd.Timedelta(0),"order_delivered_carrier_date"]=orders.loc[orders["difference_days2"]<pd.Timedelta(0),"order_delivered_carrier_date_new"]

orders["order_delivered_carrier_date_new"]=orders["order_approved_at"]+(orders["order_delivered_customer_date"]-orders["order_approved_at"])/2

orders.loc[orders["difference_days4"]<pd.Timedelta(0),"order_delivered_carrier_date"]=orders.loc[orders["difference_days4"]<pd.Timedelta(0),"order_delivered_carrier_date_new"]

orders["order_delivered_carrier_date_new"]=orders["order_approved_at"]+(orders["order_delivered_customer_date"]-orders["order_approved_at"])/2
orders.loc[(orders["order_status"]=="delivered") & (orders["order_delivered_carrier_date"].isnull()),"order_delivered_carrier_date"]=orders.loc[(orders["order_status"]=="delivered") & (orders["order_delivered_carrier_date"].isnull()),"order_delivered_carrier_date_new"]

orders.loc[(orders["order_status"]=="delivered") & (orders["order_delivered_carrier_date"].isnull()),"order_status"]="approved"

orders["order_approved_at_new"]=orders["order_purchase_timestamp"]+(orders["order_delivered_carrier_date"]-orders["order_purchase_timestamp"])/2
orders.loc[(orders["order_status"]=="delivered") & (orders["order_approved_at"].isnull()),"order_approved_at"]=orders.loc[(orders["order_status"]=="delivered") & (orders["order_approved_at"].isnull()),"order_approved_at_new"]

orders.loc[(orders["order_status"]=="delivered")&(orders["order_delivered_customer_date"].isnull()),"order_status"]="shipped"

orders.drop(columns=["difference_days1","difference_days2","difference_days3","difference_days4","difference_days5","order_approved_at_new","order_delivered_carrier_date_new"],inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

orders.to_sql('orders', engine, if_exists='append', index=False)

print('orders load')


payments=pd.read_csv("Datasets/olist_order_payments_dataset.csv")

payments.drop(columns=["payment_sequential"],axis= 1, inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

payments.to_sql('order_payments', engine, if_exists='append', index=False)

print('payments load')


reviews=pd.read_csv("Datasets/olist_order_reviews_dataset.csv")

reviews["review_creation_date"]=pd.to_datetime(reviews["review_creation_date"],format="%Y-%m-%d %H:%M:%S")
reviews["review_answer_timestamp"]=pd.to_datetime(reviews["review_answer_timestamp"],format="%Y-%m-%d %H:%M:%S")

reviews["review_comment_title"].fillna("SIN TITULO",inplace=True)
reviews["review_comment_message"].fillna("SIN COMENTARIOS",inplace=True)

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

reviews.to_sql('order_reviews', engine, if_exists='append', index=False)

print('reviews load')


products=pd.read_csv("Datasets/olist_products_dataset.csv")

products.drop(columns=["product_name_lenght","product_description_lenght","product_weight_g","product_length_cm","product_height_cm","product_width_cm"],axis=1,inplace=True)

products["product_photos_qty"].fillna(0.0,inplace=True)
products["product_photos_qty"] = products["product_photos_qty"] .astype("int")
products["product_category_name"]=products["product_category_name"].str.replace("_"," ")

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

products.to_sql('products', engine, if_exists='append', index=False)

print('products load')


items=pd.read_csv("Datasets/olist_order_items_dataset.csv")

items["shipping_limit_date"]=pd.to_datetime(items["shipping_limit_date"],format="%Y-%m-%d %H:%M:%S")

engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

items.to_sql('order_items', engine, if_exists='append', index=False)

print('items load')

engine.dispose()

# Obtiene el tiempo final
end_time = time.time()

# Calcula el tiempo de ejecución total
total_time = end_time - start_time

# Convierte el tiempo de ejecución total a minutos y segundos
minutes, seconds = divmod(total_time, 60)

# Imprime el tiempo de ejecución total en minutos y segundos
print("Tiempo de ejecución total: {:.0f} minutos y {:.2f} segundos".format(minutes, seconds))