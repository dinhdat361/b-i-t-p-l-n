# Online Retail BI Dashboard

Project BI phân tích dữ liệu bán lẻ từ bộ dữ liệu `Online Retail`. Dữ liệu được xử lý bằng Python ETL, nạp vào PostgreSQL theo mô hình sao, sau đó mở dashboard có sẵn bằng Power BI.

## 1. Tổng quan

Project gồm 3 phần chính:

- **ETL**: đọc file CSV, làm sạch dữ liệu, tạo bảng dimension và fact.
- **Database**: lưu dữ liệu vào PostgreSQL theo mô hình star schema.
- **Power BI**: mở file dashboard `Project.pbix` và refresh dữ liệu từ PostgreSQL.

## 2. Công nghệ sử dụng

- Python 3.10+
- Pandas
- SQLAlchemy
- psycopg2
- PostgreSQL
- Power BI Desktop

## 3. Cấu trúc thư mục

```text
.
+-- README.md
+-- Document/
|   +-- BI_group 17.pdf
+-- Source Code/
    +-- data/
    |   +-- Online Retail.csv
    +-- ETL/
    |   +-- ETL.py
    |   +-- test.py
    +-- PBIX/
    |   +-- Project.pbix
    |   +-- page1.png
    |   +-- page2.png
    |   +-- page3.png
    +-- SQL/
        +-- SQL_BI.sql
```

Trong đó:

- `Source Code/data/Online Retail.csv`: file dữ liệu đầu vào.
- `Source Code/ETL/ETL.py`: file ETL chính.
- `Source Code/ETL/test.py`: file thử nghiệm.
- `Source Code/PBIX/Project.pbix`: file dashboard Power BI.
- `Source Code/PBIX/page1.png`, `page2.png`, `page3.png`: ảnh tham khảo các trang dashboard.
- `Document/BI_group 17.pdf`: file báo cáo project.
- `Source Code/SQL/SQL_BI.sql`: file SQL tham khảo. Khi chạy `ETL.py`, script đã tự tạo bảng và quan hệ nên không bắt buộc chạy file SQL này.

## 4. Thông tin kết nối database

Thông tin kết nối đang được cấu hình trong `Source Code/ETL/ETL.py`:

```python
USER = 'postgres'
PASSWORD = '123456'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'ecommerce_dw'
```

Database chính của project là:

```text
ecommerce_dw
```

Nếu PostgreSQL trên máy bạn dùng user, password hoặc port khác, hãy sửa lại các biến trong `ETL.py` trước khi chạy.

## 5. Mô hình dữ liệu

Sau khi chạy ETL, PostgreSQL sẽ có 5 bảng:

```text
dim_customer
dim_product
dim_time
dim_region
fact_orders
```

Quan hệ giữa các bảng:

```text
dim_customer.customer_key  1 --> *  fact_orders.customer_key
dim_product.product_key    1 --> *  fact_orders.product_key
dim_time.time_key          1 --> *  fact_orders.time_key
dim_region.region_key      1 --> *  fact_orders.region_key
```

Ý nghĩa bảng:

- `dim_customer`: thông tin khách hàng và quốc gia.
- `dim_product`: thông tin sản phẩm.
- `dim_time`: thông tin ngày, tháng, quý, năm.
- `dim_region`: thông tin quốc gia và nhóm khu vực.
- `fact_orders`: dữ liệu giao dịch, số lượng, đơn giá và doanh thu.

## 6. Cài thư viện Python

Mở terminal tại thư mục gốc project:

```powershell
cd "D:\nam 4\BI\Bài tập lớn\bài tập lớn"
```

Cài các thư viện cần thiết:

```powershell
pip install pandas sqlalchemy psycopg2-binary
```

Nếu máy có nhiều phiên bản Python, có thể dùng:

```powershell
python -m pip install pandas sqlalchemy psycopg2-binary
```

## 7. Tạo database PostgreSQL

Cần tạo database trước khi chạy ETL.

### Cách 1: Tạo bằng pgAdmin

1. Mở **pgAdmin**.
2. Kết nối tới PostgreSQL local.
3. Chuột phải vào **Databases**.
4. Chọn **Create > Database...**.
5. Nhập tên database:

```text
ecommerce_dw
```

6. Bấm **Save**.

### Cách 2: Tạo bằng psql

Mở SQL Shell hoặc terminal PostgreSQL rồi chạy:

```sql
CREATE DATABASE ecommerce_dw;
```

Kiểm tra database:

```sql
\l
```

## 8. Chạy ETL

Từ thư mục gốc project, chạy:

```powershell
python "Source Code\ETL\ETL.py"
```

Nếu chạy thành công, terminal sẽ hiện:

```text
--- Dang doc du lieu ---
--- Dang lam sach va bien doi du lieu ---
--- Dang nap du lieu vao Database ---
--- Dang anh xa khoa ngoai cho bang Fact ---
--- Dang nap bang fact_orders vao PostgreSQL ---
ETL hoan tat thanh cong!
```

Script sẽ tự động:

- đọc file `Source Code/data/Online Retail.csv`;
- lọc các dòng có `Quantity <= 0` hoặc `UnitPrice <= 0`;
- loại dòng thiếu `InvoiceDate` hoặc `Country`;
- điền `CustomerID` bị thiếu bằng dạng `Country_Guest`;
- tạo cột `Revenue = Quantity * UnitPrice`;
- tạo bảng dimension và fact;
- thêm primary key và foreign key để các bảng có quan hệ.

## 9. Kiểm tra dữ liệu sau khi ETL

Trong pgAdmin hoặc công cụ SQL khác, kết nối tới database:

```text
ecommerce_dw
```

Chạy thử:

```sql
SELECT COUNT(*) FROM fact_orders;
SELECT COUNT(*) FROM dim_customer;
SELECT COUNT(*) FROM dim_product;
SELECT COUNT(*) FROM dim_time;
SELECT COUNT(*) FROM dim_region;
```

Kiểm tra quan hệ khóa ngoại:

```sql
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_name = 'fact_orders';
```

Kết quả đúng sẽ có 4 foreign key từ `fact_orders` sang `dim_customer`, `dim_product`, `dim_time`, `dim_region`.

## 10. Mở dashboard Power BI

Sau khi tạo database và chạy ETL thành công:

1. Mở **Power BI Desktop**.
2. Chọn **File > Open report > Browse reports**.
3. Mở file:

```text
Source Code/PBIX/Project.pbix
```

4. Nếu Power BI hỏi quyền kết nối database, chọn PostgreSQL local.
5. Nếu cần sửa nguồn dữ liệu, vào **File > Options and settings > Data source settings**.
6. Chọn nguồn PostgreSQL rồi bấm **Change Source...**.
7. Đặt thông tin kết nối:

```text
Server: localhost
Database: ecommerce_dw
```

8. Bấm **Home > Refresh** để tải dữ liệu từ PostgreSQL.

Nếu file `Project.pbix` vẫn còn dashboard và kết nối đúng database, các biểu đồ sẽ hiển thị sau khi refresh.

## 11. Nếu Power BI không hiển thị dữ liệu

Kiểm tra theo thứ tự:

- PostgreSQL đang chạy chưa.
- Database `ecommerce_dw` đã được tạo chưa.
- Đã chạy `python "Source Code\ETL\ETL.py"` thành công chưa.
- Trong Power BI, source có đúng `Server: localhost` và `Database: ecommerce_dw` chưa.
- Credentials trong **Data source settings** có đúng chưa.
- Đã bấm **Home > Refresh** chưa.

Nếu mở PBIX mà vẫn không thấy dữ liệu, có thể do Power BI đang lưu source cũ. Khi đó vào:

```text
File > Options and settings > Data source settings
```

Sau đó sửa lại source PostgreSQL về:

```text
Server: localhost
Database: ecommerce_dw
```

## 12. Lỗi thường gặp

### Không tìm thấy file CSV

Hãy chạy script từ thư mục gốc project:

```powershell
python "Source Code\ETL\ETL.py"
```

### Không kết nối được PostgreSQL

Kiểm tra:

- PostgreSQL service đã chạy chưa.
- Database `ecommerce_dw` đã được tạo chưa.
- `USER`, `PASSWORD`, `HOST`, `PORT` trong `ETL.py` có đúng không.
- Port PostgreSQL mặc định thường là `5432`.

### ERD không hiện quan hệ

Sau khi chạy ETL, refresh lại schema trong pgAdmin hoặc công cụ database. Nếu vẫn chưa hiện, đóng mở lại tab ERD/schema vì một số công cụ cache metadata cũ.

## 13. Thứ tự chạy nhanh

```powershell
cd "D:\nam 4\BI\Bài tập lớn\bài tập lớn"
pip install pandas sqlalchemy psycopg2-binary
python "Source Code\ETL\ETL.py"
```

Sau đó mở:

```text
Source Code/PBIX/Project.pbix
```

và bấm **Refresh** trong Power BI.
