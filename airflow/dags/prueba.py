import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import today
#Defino diccionario de argumentos por default
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['meligriffo@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

product_cat_name=pd.read_csv("/mnt/c/Users/jpost/OneDrive/Escritorio/Final-Data/Proyecto-Final-DATA-1/airflow/dags/datasets/product_category_name_translation.csv")
#Product Category Name Translation

def etl_product_cat(product_cat_name):

    #extract
    product_cat_name=pd.read_csv("/mnt/c/Users/jpost/OneDrive/Escritorio/Final-Data/Proyecto-Final-DATA-1/airflow/dags/datasets/product_category_name_translation.csv")

    #transform
    product_cat_name=product_cat_name.append({"product_category_name" : "pc_gamer" , "product_category_name_english" : "pc_gamer"} , ignore_index=True)
    product_cat_name=product_cat_name.append({"product_category_name" : "portateis_cozinha_e_preparadores_de_alimentos" , "product_category_name_english" : "kitchen_and_food_preparation_racks"} , ignore_index=True)

    product_cat_name["product_category_name"]=product_cat_name["product_category_name"].str.replace("_"," ")
    product_cat_name["product_category_name_english"]=product_cat_name["product_category_name_english"].str.replace("_"," ")

    #load
    engine = create_engine('postgresql://olist:IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1@dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com:5432/olist')

    product_cat_name.to_sql('product_category_name_translation', engine, if_exists='append', index=False)

    print('product_cat_name load')

    engine.dispose()

def prueba_ok():
    print("prueba salio ok")


#Definimos DAG y tasks
with DAG(
    dag_id='first',
    default_args=default_args,
    description='Prueba primer DAG',
    schedule=timedelta(days=1),
    start_date=today().subtract(days=2),
    tags=['example'],
) as dag:
    etl_product_cat_task = PythonOperator(task_id="scrape", python_callable=etl_product_cat)
    prueba_ok_task = PythonOperator(task_id="process", python_callable=prueba_ok)
   
    etl_product_cat_task >> prueba_ok_task


if __name__ == '__main__':
    etl_product_cat(product_cat_name)
    prueba_ok
