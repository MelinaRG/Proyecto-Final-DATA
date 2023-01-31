import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    host="dpg-cf3enqun6mplnpe950v0-a.oregon-postgres.render.com",
    database="olist",
    user="olist",
    password="IHCRtcefMFbJIjUMXuUMtcIfpTAEo5d1"
)

# Creación del cursor
cur = conn.cursor()

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('product_category_name_translation')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE product_category_name_translation (
            product_category_name_id SERIAL,
            product_category_name VARCHAR(255) NOT NULL,
            product_category_name_english VARCHAR(255) NOT NULL,
            PRIMARY KEY(product_category_name_id)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")    
cur.execute("""
 ALTER TABLE product_category_name_translation ADD UNIQUE (product_category_name)
 """)
# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('geolocation')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE geolocation (
            zip_code_prefix VARCHAR(15) NOT NULL,
            region_name VARCHAR(100) NOT NULL,
            id_state INTEGER NOT NULL,
            state_sigla VARCHAR(20) NOT NULL,
            state_name VARCHAR(100) NOT NULL,
            city VARCHAR(100) NOT NULL,
            localizador VARCHAR(100),
            latitud_city DECIMAL,
            longitud_city DECIMAL,
            latitud_state DECIMAL,
            longitud_state DECIMAL,
            PRIMARY KEY(zip_code_prefix)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('marketing_qualified_leads')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE marketing_qualified_leads (
            mql_id VARCHAR(255) NOT NULL,
            first_contact_date DATE NOT NULL,
            origin VARCHAR(255),
            PRIMARY KEY(mql_id)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe") 
    
# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('olist_sellers')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE olist_sellers (
            seller_id VARCHAR(255) NOT NULL,
            seller_zip_code_prefix VARCHAR(15),
            PRIMARY KEY(seller_id),
            FOREIGN KEY(seller_zip_code_prefix) REFERENCES geolocation(zip_code_prefix)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")    

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('closed_deals')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE closed_deals (
            closed_id SERIAL,
            mql_id VARCHAR(255) NOT NULL,
            seller_id VARCHAR(255) NOT NULL,
            won_date DATE NOT NULL,
            business_segment VARCHAR(255),
            lead_type VARCHAR(255),
            PRIMARY KEY(closed_id),
            FOREIGN KEY (mql_id) REFERENCES marketing_qualified_leads(mql_id),
            FOREIGN KEY (seller_id) REFERENCES olist_sellers(seller_id)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")

cur.execute("""
    SELECT to_regclass('customers')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE customers (
            customer_id	 VARCHAR(255) NOT NULL,
            customer_unique_id VARCHAR(255) NOT NULL,
            customer_zip_code_prefix VARCHAR(15) NOT NULL,
            PRIMARY KEY(customer_id),
            FOREIGN KEY (customer_zip_code_prefix) REFERENCES geolocation(zip_code_prefix)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('orders')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE orders (
            order_id VARCHAR(255) NOT NULL,
            customer_id VARCHAR(255) NOT NULL,
            order_status VARCHAR(255) NOT NULL,
            order_purchase_timestamp DATE NOT NULL,
            order_approved_at DATE,
            order_delivered_carrier_date DATE,
            order_delivered_customer_date DATE,
            order_estimated_delivery_date DATE NOT NULL,
            total_order_cost DECIMAL,
            PRIMARY KEY(order_id),
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")   

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('order_payments')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE order_payments (
            payment_id SERIAL,
            order_id VARCHAR(255) NOT NULL,
            payment_type VARCHAR(255) NOT NULL,
            payment_installments INTEGER NOT NULL,
            payment_value DECIMAL NOT NULL,
            PRIMARY KEY(payment_id),
            FOREIGN KEY(order_id) REFERENCES orders(order_id)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")    

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('order_reviews')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE order_reviews (
            review_unique_id SERIAL,
            review_id VARCHAR(255) NOT NULL,
            order_id VARCHAR(255) NOT NULL,
            review_score INTEGER NOT NULL,
            review_comment_title VARCHAR(255),
            review_comment_message VARCHAR(255),
            review_creation_date DATE NOT NULL,
            review_answer_timestamp DATE NOT NULL,
            PRIMARY KEY(review_unique_id),
            FOREIGN KEY(order_id) REFERENCES orders(order_id)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")    

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('products')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE products (
            product_id VARCHAR(255) NOT NULL,
            product_category_name VARCHAR(255),
            product_photos_qty INTEGER,
            PRIMARY KEY(product_id),
            FOREIGN KEY(product_category_name) REFERENCES product_category_name_translation(product_category_name)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")    

# Verifica si la tabla existe
cur.execute("""
    SELECT to_regclass('order_items')
""")

if cur.fetchone()[0] is None:
    # Creación de la tabla
    cur.execute("""
        CREATE TABLE order_items (
            order_unique_id SERIAL,
            order_id VARCHAR(255) NOT NULL,
            order_item_id INTEGER NOT NULL,
            product_id VARCHAR(255) NOT NULL,
            seller_id VARCHAR(255) NOT NULL,
            shipping_limit_date DATE NOT NULL,
            price DECIMAL NOT NULL,
            freight_value DECIMAL NOT NULL,
            PRIMARY KEY(order_unique_id),
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id),
            FOREIGN KEY(seller_id) REFERENCES olist_sellers(seller_id)
        )
    """)
    conn.commit()
    print("Tabla creada con éxito")
else:
    print("La tabla ya existe")    

# Cierre de la conexión
cur.close()
conn.close()
