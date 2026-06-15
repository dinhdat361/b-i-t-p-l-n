CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    country VARCHAR(100)
);

-- 2. Tạo bảng chiều Sản phẩm
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    stock_code VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);

-- 3. Tạo bảng chiều Thời gian
CREATE TABLE dim_time (
    time_key INT PRIMARY KEY, -- Định dạng YYYYMMDD
    invoice_date DATE,
    day INT,
    month INT,
    quarter INT,
    year INT
);

-- 4. Tạo bảng chiều Vùng miền 
CREATE TABLE dim_region (
    region_key SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    region_group VARCHAR(100) NOT NULL
);

CREATE TABLE fact_orders (
   fact_id SERIAL PRIMARY KEY, 
   invoice_no VARCHAR(50),
   customer_key INT,
   product_key INT,
   time_key INT,
   region_key INT,
   quantity INT,
   unit_price DECIMAL(10,2),
   revenue DECIMAL(12,2),
   FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key) ON DELETE CASCADE,
   FOREIGN KEY (product_key) REFERENCES dim_product(product_key) ON DELETE CASCADE,
   FOREIGN KEY (time_key) REFERENCES dim_time(time_key) ON DELETE CASCADE,
   FOREIGN KEY (region_key) REFERENCES dim_region(region_key) ON DELETE CASCADE
);

SELECT COUNT(*) AS total_guest_orders
FROM fact_orders f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
WHERE c.customer_id LIKE '%_Guest';
