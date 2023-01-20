# **Análisis Exploratorio de datos - Olist**

<img src='https://www.meta.com.br/wp-content/uploads/2022/05/Logo-Olist.png' width = 100px>
<br>
<br>

En el presente informe se resumen los puntos más importantes del EDA realizado para cada dataset disponible y que es fundamental para la elaboración de las transformaciones y el pipeline correspondiente que se deben aplicar previo a cargar los datos a un DataWarehouse.

Se utilizan `Notebooks.ipynb` para realizar los anális correspondientes a cada dataset

Navegar en los títulos del informe:

- [Insights del Análisis exploratorio de datos](#insights-del-análisis-exploratorio-de-datos)
- [Overview de los datos](#overview-de-los-datos)
- [Criterio de calidad de los datos](#criterio-de-calidad-de-los-datos)
- [Calidad de los datos - Transformaciones y acciones pertinentes](#calidad-de-los-datos---transformaciones-y-acciones-pertinentes)
- [Conclusiones](#conclusiones)

## Insights del Análisis exploratorio de datos

---

Los datasets que se proveen de olist los podemos agrupar según los datos con los que cuentan. Se definen los insights principales de cada anális y alguna observación en cuanto a la calidad de datos.

### Datasets de Ordenes de Compra

- **olist_orders_dataset**
  [Análisis EDA](./EDA/EDA_olist_orders_dataset_Julio.ipynb)

  En este dataset deberiamos:

  - Cambiar nombres de las columnas
  - Cambiar los tipos de datos de la columna 3 a la 7 por datetime
  - Analizar que todos los faltantes esten justificados
  - Corregir fecha entrega al fletero, en los 1359 registros que tienen fecha de aprobacion posterior
  - Corregir fecha de entrega al cliente, en los 23 registros que tienen fecha de entrega al fletero posterior

* **olist_order_items_dataset**
  [Análisis EDA](./EDA/EDA_olist_order_items_dataset_Emmanuel.ipynb)

  - Price: con una media casi en el tercer cuartil, vemos que la distribución de datos está concentrada dentro del primer cuartil. Hay valores outliers sin los cuales la distribución sería normal.

  - Freight_value: casi la totalidad de los datos están concentrados en el primer cuartil. Pasando el segundo cuartil, podría decirse que son todos datos outliers.

  ETL (recomendado):

  - Renombrar columnas.

- **olist_order_payments_dataset**
  [Análisis EDA](./EDA/EDA_olist_order_payments_dataset_Emmanuel.ipynb)

  - Payment type: dentro de los tipos de pago encontramos 5 alternativas.

  - Payment sequential: la mayor concentración de datos dentro se encuentra dentro del primer cuartil, mostrando incluso que tenemos muchos ouliers o valores fuera del rango principal.

  - Payment installment: la distribución posee un rango acotado (si tenemos en cuenta la cantidad de datos), mostrando algunos outliers que hacen ruido en la distribución.

  - Payment value: como los anteriores, la mayor concentración de datos está dentro del primer cuartil. Se evidencian pocos outliers, pero con valores muy extremos que disparan la distribución de datos.

  ETL (recomendado):

  - Renombrar columnas.
  - Agregar columna con valor total (installments \* value).
  - Traducir valores de payment_type.

- **olist_order_reviews_dataset**

  Lo prncipal que se observó es la cantidad elevada de nulos en las columnas de títulos y comentarios de las reviews que es de esperarse.

### Datasets de Productos

- **olist_products_dataset**
  [Análisis EDA](./EDA/EDA_olist_sellers-products-category_dataset_Issac.ipynb)

  - No tiene duplicados, si presenta nulos
  - Las columnas (product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm) presentan outliers pero no deben ser eliminados.
  - Eliminar las siguientes columnas (product_name_lenght, product_description_lenght) por ser irrelevantes

- **product_category_name_translation**
  [Análisis EDA](./EDA/EDA_olist_sellers-products-category_dataset_Issac.ipynb)

  - No presenta valores nulos ni duplicados.
  - Todo su contenido se debe usar.

### Datasets de Clientes y Vendedores

- **olist_sellers_dataset**
  [Análisis EDA](./EDA/EDA_olist_sellers-products-category_dataset_Issac.ipynb)

  - No presenta nulos ni duplicados.
  - Eliminar las columnas seller_city y seller_state por presentar incongruencias, es mejor usar geolocalicacion_city y geolocalicacion_state del dataset de olist_geolocation_dataset

- **olist_customers_dataset**
  [Análisis EDA](./EDA/EDA_olist_customers_dataset_Julio.ipynb)

  En este dataset se deberia:

  - Cambiar nombres de las columnas
  - Los duplicados en customer_unique_id es correcto porque un cliente puede tener varias compras
  - Dropear customer_city y customer_state, dejar solo zip_code y unirlo con el dataset de geolocalization.

  Ó bien:

  - Normalizar nombres de ciudades
  - En customer_state podriamos poner el nombre completo del Estado

### Datasets de Geolocalización

- **olist_geolocation_dataset**
  [Análisis EDA](./EDA/EDA_olist_geolocation_dataset_Nicolas.ipynb)

  Este dataset es cuenta con varios problemas relacionados la integridad y fiabilidad de los datos. Cuentra con los codigos postales de cada seguido del estado, ciudad, latitud y longitud. La mayoria de los inconvenientes están relacionados con:

  - Hay duplicados en zipcode. Deberían ser unicos ya que este dataset debería convertirse en una tabla de dimensiones del cual el resto de las tablas obtengan la información de localización a partir del zip code

  - Hay outliers en cuanto a los valores de latitud y longitud. No se confía en dichos valores por lo que debería obtenerse de otra fuente de datos. - Los nombres de las ciudades no son homogeneos entre sí ya que cuentan con una leve diferencia de tipeo a pesar de ser la misma ciudad

  Lo que se debe hacer es:

  - Renombrar ciertas columnas a criterio - Obtener de otra fuente de datos (APIs) más información sobre los estados de Brasil, la región, la latitud y longitud como centroides de cada estado y ciudad

  Se genera un notebook de procesado para obtener una tabla totalmente nueva de geolocalización con más información: [Procesado de Geolocalización](./Geolocalizacion_procesado.ipynb)

  Se utiliza la API Geocoder para traer las coordenadas de cada ciudad

  <a href='https://geocoder.readthedocs.io/'>
  <img src='https://geocoder.readthedocs.io/_static/geocoder.png' width = 50px>
  </a>

### Datasets de Marketing

- **olist_marketing_qualified_leads_dataset**
  [Análisis EDA](./EDA/EDA_olist_marketing_qualified_leads_dataset_Melina.ipynb)

  Analizar si vamos a utilizar algunas columnas de esta tabla o si la vamos a eliminar directamente, ya que no posee relacion con los KPIs planteados y el analisis que estamos realizando

- **olist_closed_deals_dataset**
  [Análisis EDA](./EDA/EDA_olist_closed_deals_dataset_Melina.ipynb)

  Analizar si vamos a utilizar algunas columnas de esta tabla o si la vamos a eliminar directamente, ya que no posee relacion con los KPIs planteados y el analisis que estamos realizando

## Overview de los datos

---

[:arrow_up_small:](#top) **_SUBIR_**

Se presenta una tabla resumen con un overview de los datos de cada dataset, entre ellos valores nulos, duplicados y outliers. Los datasets más comprometidos son los de geolocalización, reviews y ordenes en dichos aspectos.

| **Nro Tabla** | **Dataset**                                     | **Cantidad registros** | **Cantidad columnas** | **Valores nulos totales** | **Columnas con valores nulos** | **Valores nulos columna max** | **Valores nulos (Mayor %)** | **Registros duplicados** | **Registros duplicados (%)** | **Columnas con duplicados**          | **Duplicados columna** | **Registros duplicados (%)** |                                      **Columnas con Outliers**                                       |
| :-----------: | :---------------------------------------------- | :--------------------: | :-------------------: | :-----------------------: | :----------------------------: | :---------------------------: | :-------------------------: | :----------------------: | :--------------------------: | :----------------------------------- | :--------------------: | :--------------------------: | :--------------------------------------------------------------------------------------------------: |
|       1       | olist_closed_deals_dataset                      |          842           |          14           |           3.300           |               8                |              779              |           92,52%            |            0             |            0,00%             | -                                    |           0            |            0,00%             |                                                  -                                                   |
|       2       | olist_customers_dataset                         |         99.441         |           5           |             0             |               0                |               0               |            0,00%            |            0             |            0,00%             | 1)- customer_unique_id               |           0            |            0,00%             |                                                  -                                                   |
|       3       | olist_geolocation_dataset                       |       1.000.163        |           6           |             0             |               0                |               0               |            0,00%            |         261.831          |            26,18%            | 1)- geolocation_zip_code_prefix      |        981.148         |            98,10%            |                            geolocation_latitude<br>geolocation_longitude                             |
|       4       | olist_marketing_qualified_leads_dataset         |         8.000          |           4           |            60             |               1                |              60               |            0,75%            |            0             |            0,00%             | -                                    |           0            |            0,00%             |                                                  -                                                   |
|       5       | olist_order_items_dataset                       |        112.650         |           7           |             0             |               0                |               0               |            0,00%            |            0             |            0,00%             | 1)- order_id                         |           0            |            0,00%             |                               order_item_id<br>price<br>freight_value                                |
|       6       | olist_order_payments_dataset                    |        103.886         |           5           |             0             |               0                |               0               |            0,00%            |            0             |            0,00%             | 1)- order_id                         |           0            |            0,00%             |                     payment_secuential<br>payment_installments<br>payment_value                      |
|       7       | olist_order_reviews_dataset                     |         99.224         |           7           |          145.903          |               2                |            87.656             |           88,34%            |            0             |            0,00%             | 1)- review_id                        |          814           |            0,82%             |                                                  -                                                   |
|       8       | olist_orders_dataset                            |         99.441         |           8           |           4.908           |               3                |             2.965             |            2,98%            |            0             |            0,00%             | -                                    |           0            |            0,00%             |                                                  -                                                   |
|       9       | olist_products_dataset                          |         32.951         |           8           |           2.448           |               8                |              610              |            1,85%            |            0             |            0,00%             | -                                    |           0            |            0,00%             | product_photos_qty<br>product_weight_g<br>product_length_cm<br>product_height_cm<br>product_width_cm |
|      10       | olist_sellers_dataset                           |         3.095          |           4           |             0             |               0                |               0               |            0,00%            |            0             |            0,00%             | 1)- seller_city <br>2)- seller_state |           0            |            0,00%             |                                                  -                                                   |
|      11       | olist_product_category_name_translation_dataset |           71           |           2           |             0             |               0                |               0               |            0,00%            |            0             |            0,00%             | -                                    |           0            |            0,00%             |                                                  -                                                   |

## Criterio de calidad de los datos

---

[:arrow_up_small:](#top) **_SUBIR_**

Para decidir sobre las transformaciones pertinentes se tienen en cuenta los siguientes criterios definidos para evaluar la calidad de los datos de cada dataset.

|     **Icono**      | **Calidad de los datos** |                                                                                                                                                  **Referencia**                                                                                                                                                  |
| :----------------: | :----------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| :white_check_mark: |      Satisfactoria       |                                                         Los datos tienen muy buena calidad y hay que hacer nula o mínima cantidad de transformaciones como renombre de columnas, cambio de tipo de dato, tratamiento de nulos, dropeo de columnas, etc.                                                          |
|     :warning:      |        Aceptable         |                             Los datos tienen problemas que requieren algún criterio y toma de decisión en las transformaciones, como imputación de valores faltantes, creación de nuevas features, tratamiento de duplicados, tratamiento de outliers, correcciones en valores, etc.                             |
|        :x:         |         No buena         | El dataset requiere un tratamiento exhaustivo que lleva tiempo y criterio en la toma de decisiones, puede incluir falta de veracidad o confianza en registros, procesamientos arduos de variables, mergeo con fuentes externas (otros datasets, APIs) además de lo mencionado para datasets de calidad aceptable |

## Calidad de los datos - Transformaciones y acciones pertinentes

---

[:arrow_up_small:](#top) **_SUBIR_**

Se evaluan cada dataset y se consideran que los más comprometidos son los de geolocalización y ordenes por la cantidad de transformaciones y la rigurosidad que se tiene que tener para lograr luego analisis de buena calidad.

### **_Calidad de datos de cada dataset_**

| **Nro Tabla** | **Dataset**                                     | **Calidad de los datos** |
| :-----------: | :---------------------------------------------- | :----------------------: |
|       1       | olist_closed_deals_dataset                      |    :white_check_mark:    |
|       2       | olist_customers_dataset                         |    :white_check_mark:    |
|       3       | olist_geolocation_dataset                       |           :x:            |
|       4       | olist_marketing_qualified_leads_dataset         |    :white_check_mark:    |
|       5       | olist_order_items_dataset                       |    :white_check_mark:    |
|       6       | olist_order_payments_dataset                    |    :white_check_mark:    |
|       7       | olist_order_reviews_dataset                     |        :warning:         |
|       8       | olist_orders_dataset                            |           :x:            |
|       9       | olist_products_dataset                          |        :warning:         |
|      10       | olist_sellers_dataset                           |    :white_check_mark:    |
|      11       | olist_product_category_name_translation_dataset |    :white_check_mark:    |

### **_Transformaciones aplicadas_**

| **Nro Tabla** | **Dataset**                                     | **Transformaciones o acciones pertinentes**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :-----------: | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|       1       | olist_closed_deals_dataset                      | 1)- Cambiar tipo de dato de columna won_date a DATE. <br>2)- Completar nulos con SIN DATO.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|       2       | olist_customers_dataset                         | Sin transformaciones                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|       3       | olist_geolocation_dataset                       | 1)- Concatenar tabla de geolocalización, customers y sellers y eliminar duplicados de zipcode<br>2)- Traer datos de API de nombre de estado, región y coordenadas y jonearlo al dataset simplificado <br>3)- Dropear algunos valores nulos de los cuales la API no pudo traer las coordenadas                                                                                                                                                                                                                                                                                                                                                 |
|       4       | olist_marketing_qualified_leads_dataset         | 1)- Cambiar tipo de dato de columna first_contact_date a DATE. <br> 2)- Completar nulos con SIN DATO.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|       5       | olist_order_items_dataset                       | 1)- Cambiar tipo de dato de columna shipping_limit_date a DATE.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|       6       | olist_order_payments_dataset                    | 1)- Crear tabla auxiliar con columna total_order_cost .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|       7       | olist_order_reviews_dataset                     | 1)- Cambiar tipo de dato de las columnas review_creation_date y review_answer_timestamp a DATE. <br>2)- Llenar nulos de la columna review_comment_title con SIN TITULO. <br>3)- Llenar nulos de la columna review_comment_message con SIN COMENTARIOS.                                                                                                                                                                                                                                                                                                                                                                                        |
|       8       | olist_orders_dataset                            | 1)- Cambiar tipo de dato de las columnas order_purchase_timestamp,order_approved_at,order_delivered_carrier_date,order_delivered_customer_date y order_estimated_delivery_date a DATE .<br>2)- Modificamos las 4 primeras columnas mencionadas con tal que exista congruencia de tiempo entre estas. <br>3)- Completamos vacios de las 4 primeras columnas mencionadas en el punto 1) tomando como referencia las columnas adyacentes a estas. <br>4)- Modifcamos la columna order_status para que tengan congruencia con las 4 primeras columnas mencionadas en el punto 1). <br>5)- Unimos esta tabla conla tabla auxiliar tota_order_cost. |
|       9       | olist_products_dataset                          | 1)- Llenar vacíos de la columna product*photos_qty con 0.0 E <br> 2)- Cambiar tipo de dato de la columna product_photos_qty a INT. <br>3)- Reemplazar caracter "*" por espacio en la columna product_category_name .                                                                                                                                                                                                                                                                                                                                                                                                                          |
|      10       | olist_sellers_dataset                           | 1)- Agregar Seller_id faltantes del dataset olist_closed_deals_dataset. <br> 2)- Completar nulos de la columna seller_zip_code_prefix con SIN DATO.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|      11       | olist_product_category_name_translation_dataset | 1)- Agregar 2 registros faltantes que se encuentran en el dataset olist*products_dataset. <br> 2)- Reemplazar caracter "*" por espacio en todas las columnas del dataset                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

## Conclusiones

---

[:arrow_up_small:](#top) **_SUBIR_**

En el presente análisis se pudieron determinar la calidad de datos de las fuentes y dió un mejor panorama de qué utilizar y cómo para obtener mejores resultados en los análisis de bussiness y machine learning. Permitió plantear la ingeniería de datos necesaria de acuerdo a criterios e insights concluidos en el análisis, fundamental para poder obtener un buen producto final.
