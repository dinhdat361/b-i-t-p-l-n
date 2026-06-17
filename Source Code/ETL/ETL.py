from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

USER = 'postgres'
PASSWORD = '123456'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'ecommerce_dw'

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / 'data' / 'Online Retail.csv'

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

print("--- Dang doc du lieu ---")
if not CSV_PATH.exists():
    raise FileNotFoundError(f"Khong tim thay file du lieu: {CSV_PATH}")

df = pd.read_csv(CSV_PATH, encoding='ISO-8859-1')

print("--- Dang lam sach va bien doi du lieu ---")

df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].copy()
df = df.dropna(subset=['InvoiceDate', 'Country'])

df['CustomerID'] = df['CustomerID'].fillna(df['Country'] + '_Guest')
df['CustomerID'] = df['CustomerID'].astype(str)

df['StockCode'] = df['StockCode'].astype(str)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Revenue'] = df['Quantity'] * df['UnitPrice']

dim_customer_df = (
    df[['CustomerID', 'Country']]
    .drop_duplicates(subset=['CustomerID'], keep='last')
    .reset_index(drop=True)
)
dim_customer_df.insert(0, 'customer_key', range(1, len(dim_customer_df) + 1))

dim_product_df = (
    df[['StockCode', 'Description']]
    .drop_duplicates(subset=['StockCode'], keep='last')
    .reset_index(drop=True)
)
dim_product_df['Description'] = dim_product_df['Description'].fillna('No Description')
dim_product_df.insert(0, 'product_key', range(1, len(dim_product_df) + 1))

dim_time_df = pd.DataFrame({'InvoiceDate': df['InvoiceDate'].dt.normalize().unique()})
dim_time_df['TimeKey'] = dim_time_df['InvoiceDate'].dt.strftime('%Y%m%d').astype(int)
dim_time_df['Day'] = dim_time_df['InvoiceDate'].dt.day
dim_time_df['Month'] = dim_time_df['InvoiceDate'].dt.month
dim_time_df['Quarter'] = dim_time_df['InvoiceDate'].dt.quarter
dim_time_df['Year'] = dim_time_df['InvoiceDate'].dt.year

dim_region_df = df[['Country']].drop_duplicates().reset_index(drop=True)
region_map = {
    'United Kingdom': 'UK',
    'Germany': 'Europe',
    'France': 'Europe',
    'EIRE': 'Europe',
    'Norway': 'Europe',
    'Australia': 'Oceania',
    'USA': 'North America',
    'Canada': 'North America',
}
dim_region_df['region_group'] = dim_region_df['Country'].map(region_map).fillna('Other International')
dim_region_df.insert(0, 'region_key', range(1, len(dim_region_df) + 1))
print("--- Dang nap du lieu vao Database ---")

with engine.begin() as conn:
    for table_name in ['fact_orders', 'dim_region', 'dim_time', 'dim_product', 'dim_customer']:
        conn.execute(text(f'DROP TABLE IF EXISTS {table_name} CASCADE'))

dim_customer_df.columns = ['customer_key', 'customer_id', 'country']
dim_product_df.columns = ['product_key', 'stock_code', 'description']
dim_time_df.columns = ['invoice_date', 'time_key', 'day', 'month', 'quarter', 'year']
dim_region_df.columns = ['region_key', 'country', 'region_group']

dim_customer_df.to_sql('dim_customer', engine, if_exists='replace', index=False)
dim_product_df.to_sql('dim_product', engine, if_exists='replace', index=False)
dim_time_df.to_sql('dim_time', engine, if_exists='replace', index=False)
dim_region_df.to_sql('dim_region', engine, if_exists='replace', index=False)

with engine.begin() as conn:
    conn.execute(text('ALTER TABLE dim_customer ADD CONSTRAINT dim_customer_pk PRIMARY KEY (customer_key)'))
    conn.execute(text('ALTER TABLE dim_product ADD CONSTRAINT dim_product_pk PRIMARY KEY (product_key)'))
    conn.execute(text('ALTER TABLE dim_time ADD CONSTRAINT dim_time_pk PRIMARY KEY (time_key)'))
    conn.execute(text('ALTER TABLE dim_region ADD CONSTRAINT dim_region_pk PRIMARY KEY (region_key)'))

print("--- Dang anh xa khoa ngoai cho bang Fact ---")

db_cust = pd.read_sql('SELECT customer_key, customer_id FROM dim_customer', engine)
db_prod = pd.read_sql('SELECT product_key, stock_code FROM dim_product', engine)
db_reg = pd.read_sql('SELECT region_key, country FROM dim_region', engine)

db_cust['customer_id'] = db_cust['customer_id'].astype(str)
db_prod['stock_code'] = db_prod['stock_code'].astype(str)

df = df.merge(db_cust, left_on='CustomerID', right_on='customer_id', how='left')
df = df.merge(db_prod, left_on='StockCode', right_on='stock_code', how='left')
df = df.merge(db_reg, left_on='Country', right_on='country', how='left')

df['time_key'] = df['InvoiceDate'].dt.strftime('%Y%m%d').astype(int)

fact_orders_df = df[
    [
        'InvoiceNo',
        'customer_key',
        'product_key',
        'time_key',
        'region_key',
        'Quantity',
        'UnitPrice',
        'Revenue',
    ]
].copy()

fact_orders_df.columns = [
    'invoice_no',
    'customer_key',
    'product_key',
    'time_key',
    'region_key',
    'quantity',
    'unit_price',
    'revenue',
]

print("--- Dang nap bang fact_orders vao PostgreSQL ---")
fact_orders_df.to_sql('fact_orders', engine, if_exists='replace', index=False)

with engine.begin() as conn:
    conn.execute(text('ALTER TABLE fact_orders ADD CONSTRAINT fact_orders_customer_fk FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)'))
    conn.execute(text('ALTER TABLE fact_orders ADD CONSTRAINT fact_orders_product_fk FOREIGN KEY (product_key) REFERENCES dim_product(product_key)'))
    conn.execute(text('ALTER TABLE fact_orders ADD CONSTRAINT fact_orders_time_fk FOREIGN KEY (time_key) REFERENCES dim_time(time_key)'))
    conn.execute(text('ALTER TABLE fact_orders ADD CONSTRAINT fact_orders_region_fk FOREIGN KEY (region_key) REFERENCES dim_region(region_key)'))

print("ETL hoan tat thanh cong!")










