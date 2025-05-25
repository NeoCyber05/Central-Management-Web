# 🐘 Hướng dẫn Setup PostgreSQL

## 📋 Yêu cầu
- PostgreSQL 12+ đã cài đặt
- psql command line tool
- Quyền tạo database

## 🚀 Cách 1: Tạo database mới hoàn toàn

### Bước 1: Tạo database
```bash
# Đăng nhập PostgreSQL
psql -U postgres

# Tạo database mới
CREATE DATABASE central_management_db;

# Tạo user (tùy chọn)
CREATE USER django_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE central_management_db TO django_user;

# Thoát psql
\q
```

### Bước 2: Import schema và dữ liệu
```bash
# Import file SQL hoàn chỉnh
psql -U postgres -d central_management_db -f postgresql_setup.sql

# Hoặc với user tự tạo
psql -U django_user -d central_management_db -f postgresql_setup.sql
```

## 🔄 Cách 2: Reset database hiện có

```bash
# Backup trước khi reset (khuyến khích)
pg_dump -U postgres central_management_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Import lại schema mới
psql -U postgres -d central_management_db -f postgresql_setup.sql
```

## ⚙️ Cấu hình Django settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'central_management_db',
        'USER': 'django_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📊 Kiểm tra sau khi import

```sql
-- Kết nối database
psql -U postgres -d central_management_db

-- Kiểm tra các bảng
\dt

-- Kiểm tra dữ liệu
SELECT 'Nhân viên' as bang, COUNT(*) as so_luong FROM core_nhanvien
UNION ALL
SELECT 'Giáo viên', COUNT(*) FROM core_teacher
UNION ALL
SELECT 'Học viên', COUNT(*) FROM core_hocvien
UNION ALL
SELECT 'Lớp học', COUNT(*) FROM core_class;
```

## 🔒 Các ràng buộc đã được thêm

### Check Constraints:
- **Gender**: Chỉ cho phép 'M' hoặc 'F'
- **Email**: Phải chứa ký tự '@'
- **Điểm số**: Từ 0-10 cho tất cả loại điểm
- **Đánh giá**: Từ 1-5 cho class_rate và teacher_rate
- **Sĩ số**: Phải > 0
- **Học phí**: Phải >= 0
- **Ngày**: ket_thuc_date > khai_giang_date
- **Thời gian**: end_time > start_time
- **Trạng thái điểm danh**: 'Có mặt', 'Vắng', 'Trễ', 'Có phép'

### Foreign Key Constraints:
- **ON DELETE CASCADE**: Xóa dữ liệu liên quan khi xóa parent
- **ON DELETE SET NULL**: Set NULL khi xóa parent (cho optional relationships)

### Indexes:
- Tất cả foreign keys đều có index
- Index cho các trường thường query (attendance_date, etc.)

## 🎯 Dữ liệu mẫu bao gồm:
- **3 Nhân viên**
- **4 Giáo viên**
- **6 Học viên**
- **4 Lớp học**
- **4 Lịch học**
- **8 Đăng ký học** (với điểm số đầy đủ)
- **8 Điểm danh**
- **8 Feedback**

## 🛠️ Troubleshooting

### Lỗi permission:
```bash
# Cấp quyền cho user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_user;
```

### Lỗi encoding:
```bash
# Tạo database với UTF8
CREATE DATABASE central_management_db 
WITH ENCODING 'UTF8' 
LC_COLLATE='en_US.UTF-8' 
LC_CTYPE='en_US.UTF-8';
```

### Reset hoàn toàn:
```bash
# Xóa và tạo lại database
DROP DATABASE IF EXISTS central_management_db;
CREATE DATABASE central_management_db;
psql -U postgres -d central_management_db -f postgresql_setup.sql
``` 