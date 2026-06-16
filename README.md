# Online Retail BI Dashboard

Project BI phân tích dữ liệu bán lẻ `Online Retail` bằng quy trình ETL, lưu vào PostgreSQL và trực quan hóa trên Power BI.

## Tổng quan

Repo này gồm 3 phần chính:

1. **ETL**: làm sạch dữ liệu CSV, tạo bảng chiều và bảng fact.
2. **Database**: tạo schema dạng sao trong PostgreSQL.
3. **Dashboard**: phân tích doanh số, sản phẩm và địa lý bằng Power BI.

## Công nghệ sử dụng

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Power BI

## Dữ liệu đầu vào

- File dữ liệu: `Source Code/data/Online Retail.csv`
- Báo cáo tham khảo: `Document/BI_group 17.pdf`

## Cấu trúc thư mục

```text
Source Code/
├── ETL/
│   └── ETL.py
├── SQL/
│   └── SQL_BI.sql
├── PBIX/
│   ├── Project.pbix
│   ├── page1.png
│   ├── page2.png
│   └── page3.png
└── data/
    └── Online Retail.csv
Document/
└── BI_group 17.pdf
```

## Mô hình dữ liệu

ETL tạo các bảng sau:

- `dim_customer`
- `dim_product`
- `dim_time`
- `dim_region`
- `fact_orders`

## Xử lý dữ liệu

Luồng ETL trong `Source Code/ETL/ETL.py` thực hiện:

- đọc file CSV với encoding `ISO-8859-1`
- loại bỏ bản ghi có `Quantity <= 0` hoặc `UnitPrice <= 0`
- bỏ dòng thiếu `InvoiceDate` hoặc `Country`
- điền `CustomerID` bị thiếu bằng dạng `Country_Guest`
- chuyển `InvoiceDate` sang kiểu ngày giờ
- tính trường `Revenue = Quantity * UnitPrice`
- tạo bảng chiều và bảng fact
- nạp dữ liệu vào PostgreSQL database `ecommerce_dw_ver1`

## Cách chạy

### 1. Cài thư viện Python

```bash
pip install pandas sqlalchemy psycopg2-binary
```

### 2. Tạo PostgreSQL database

Tạo database có tên:

```text
ecommerce_dw_ver1
```

### 3. Cập nhật thông tin kết nối

Mở `Source Code/ETL/ETL.py` và kiểm tra:

```python
USER = 'postgres'
PASSWORD = '123456'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'ecommerce_dw_ver1'
```

### 4. Chạy ETL

```bash
python "Source Code/ETL/ETL.py"
```

### 5. Mở dashboard Power BI

Mở file:

```text
Source Code/PBIX/Project.pbix
```

## Dashboard

### Sales Performance

![Sales Performance](Source%20Code/PBIX/page1.png)

### Product Performance

![Product Performance](Source%20Code/PBIX/page2.png)

### Geographic Analysis

![Geographic Analysis](Source%20Code/PBIX/page3.png)

## Ghi chú

- File `SQL/SQL_BI.sql` dùng để tạo schema bảng trong PostgreSQL.
- Một số tên cột, công thức và bảng được tối ưu theo mục tiêu phân tích doanh thu.

