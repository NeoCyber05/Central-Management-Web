-- =====================================================
-- POSTGRESQL SETUP SCRIPT
-- Hệ thống quản lý trung tâm đào tạo
-- =====================================================

-- Xóa bảng nếu tồn tại (theo thứ tự dependency)
DROP TABLE IF EXISTS core_feedback CASCADE;
DROP TABLE IF EXISTS core_attendance CASCADE;
DROP TABLE IF EXISTS core_enrollment CASCADE;
DROP TABLE IF EXISTS core_schedule CASCADE;
DROP TABLE IF EXISTS core_class CASCADE;
DROP TABLE IF EXISTS core_teacher CASCADE;
DROP TABLE IF EXISTS core_hocvien CASCADE;
DROP TABLE IF EXISTS core_nhanvien CASCADE;

-- =====================================================
-- TẠO BẢNG
-- =====================================================

-- Bảng Nhân viên
CREATE TABLE core_nhanvien (
    ma_nv VARCHAR(8) NOT NULL PRIMARY KEY,
    full_name VARCHAR(40) NOT NULL,
    gender VARCHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    sdt VARCHAR(15) NOT NULL,
    address VARCHAR(30) NOT NULL,
    CONSTRAINT chk_nhanvien_email CHECK (email LIKE '%@%')
);

-- Bảng Giáo viên
CREATE TABLE core_teacher (
    teacher_id VARCHAR(8) NOT NULL PRIMARY KEY,
    full_name VARCHAR(40) NOT NULL,
    gender VARCHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    sdt VARCHAR(15) NOT NULL,
    address VARCHAR(30) NOT NULL,
    CONSTRAINT chk_teacher_email CHECK (email LIKE '%@%')
);

-- Bảng Học viên
CREATE TABLE core_hocvien (
    student_id VARCHAR(8) NOT NULL PRIMARY KEY,
    full_name VARCHAR(40) NOT NULL,
    gender VARCHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    sdt VARCHAR(15) NOT NULL,
    address VARCHAR(30) NOT NULL,
    CONSTRAINT chk_hocvien_email CHECK (email LIKE '%@%')
);

-- Bảng Lớp học
CREATE TABLE core_class (
    class_id VARCHAR(8) NOT NULL PRIMARY KEY,
    class_name VARCHAR(40) NOT NULL,
    class_type VARCHAR(1) NOT NULL CHECK (class_type IN ('O', 'F')), -- O: Online, F: Offline
    room VARCHAR(15) NOT NULL,
    khai_giang_date DATE NOT NULL,
    ket_thuc_date DATE NOT NULL,
    si_so INTEGER NOT NULL CHECK (si_so > 0),
    price INTEGER NOT NULL CHECK (price >= 0),
    ma_nv VARCHAR(8) REFERENCES core_nhanvien(ma_nv) ON DELETE SET NULL,
    teacher_id VARCHAR(8) REFERENCES core_teacher(teacher_id) ON DELETE SET NULL,
    CONSTRAINT chk_class_dates CHECK (ket_thuc_date > khai_giang_date)
);

-- Bảng Lịch học
CREATE TABLE core_schedule (
    id_schedule VARCHAR(8) NOT NULL PRIMARY KEY,
    class_id VARCHAR(8) NOT NULL REFERENCES core_class(class_id) ON DELETE CASCADE,
    day VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CONSTRAINT chk_schedule_time CHECK (end_time > start_time)
);

-- Bảng Đăng ký học (với composite key)
CREATE TABLE core_enrollment (
    student_id VARCHAR(8) NOT NULL REFERENCES core_hocvien(student_id) ON DELETE CASCADE,
    class_id VARCHAR(8) NOT NULL REFERENCES core_class(class_id) ON DELETE CASCADE,
    enrollment_date DATE NOT NULL,
    minitest1 REAL CHECK (minitest1 >= 0 AND minitest1 <= 10),
    minitest2 REAL CHECK (minitest2 >= 0 AND minitest2 <= 10),
    minitest3 REAL CHECK (minitest3 >= 0 AND minitest3 <= 10),
    minitest4 REAL CHECK (minitest4 >= 0 AND minitest4 <= 10),
    midterm REAL CHECK (midterm >= 0 AND midterm <= 10),
    final REAL CHECK (final >= 0 AND final <= 10),
    PRIMARY KEY (student_id, class_id)
);

-- Bảng Điểm danh
CREATE TABLE core_attendance (
    id_attend VARCHAR(8) NOT NULL PRIMARY KEY,
    student_id VARCHAR(8) NOT NULL REFERENCES core_hocvien(student_id) ON DELETE CASCADE,
    class_id VARCHAR(8) NOT NULL REFERENCES core_class(class_id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    status VARCHAR(15) NOT NULL CHECK (status IN ('Có mặt', 'Vắng', 'Trễ', 'Có phép'))
);

-- Bảng Feedback
CREATE TABLE core_feedback (
    id_feedback VARCHAR(8) NOT NULL PRIMARY KEY,
    student_id VARCHAR(8) NOT NULL REFERENCES core_hocvien(student_id) ON DELETE CASCADE,
    class_id VARCHAR(8) NOT NULL REFERENCES core_class(class_id) ON DELETE CASCADE,
    teacher_id VARCHAR(8) REFERENCES core_teacher(teacher_id) ON DELETE SET NULL,
    class_rate REAL CHECK (class_rate >= 1 AND class_rate <= 5),
    teacher_rate REAL CHECK (teacher_rate >= 1 AND teacher_rate <= 5)
);

-- =====================================================
-- TẠO INDEX
-- =====================================================

-- Index cho performance
CREATE INDEX idx_schedule_class_id ON core_schedule(class_id);
CREATE INDEX idx_enrollment_student_id ON core_enrollment(student_id);
CREATE INDEX idx_enrollment_class_id ON core_enrollment(class_id);
CREATE INDEX idx_attendance_student_id ON core_attendance(student_id);
CREATE INDEX idx_attendance_class_id ON core_attendance(class_id);
CREATE INDEX idx_attendance_date ON core_attendance(attendance_date);
CREATE INDEX idx_feedback_student_id ON core_feedback(student_id);
CREATE INDEX idx_feedback_class_id ON core_feedback(class_id);
CREATE INDEX idx_feedback_teacher_id ON core_feedback(teacher_id);
CREATE INDEX idx_class_ma_nv ON core_class(ma_nv);
CREATE INDEX idx_class_teacher_id ON core_class(teacher_id);

-- =====================================================
-- THÊM DỮ LIỆU MẪU
-- =====================================================

-- Nhân viên
INSERT INTO core_nhanvien (ma_nv, full_name, gender, birth_day, email, sdt, address) VALUES
('NV001', 'Nguyễn Văn An', 'M', '1985-05-15', 'nva@example.com', '0901234567', '123 Đường ABC, TP.HCM'),
('NV002', 'Trần Thị Bình', 'F', '1988-08-20', 'ttb@example.com', '0907654321', '456 Đường XYZ, TP.HCM'),
('NV003', 'Lê Văn Cường', 'M', '1987-03-12', 'lvc.nv@example.com', '0908888888', '789 Đường DEF, TP.HCM');

-- Giáo viên
INSERT INTO core_teacher (teacher_id, full_name, gender, birth_day, email, sdt, address) VALUES
('GV001', 'Lê Văn Cường', 'M', '1980-03-10', 'lvc@example.com', '0912345678', '789 Đường DEF, TP.HCM'),
('GV002', 'Phạm Thị Dung', 'F', '1982-07-25', 'ptd@example.com', '0923456789', '321 Đường GHI, TP.HCM'),
('GV003', 'Hoàng Minh Tuấn', 'M', '1979-11-08', 'hmt@example.com', '0934567890', '654 Đường JKL, TP.HCM'),
('GV004', 'Nguyễn Thị Lan', 'F', '1983-09-15', 'ntl@example.com', '0945678901', '987 Đường MNO, TP.HCM');

-- Học viên
INSERT INTO core_hocvien (student_id, full_name, gender, birth_day, email, sdt, address) VALUES
('HV001', 'Hoàng Văn Em', 'M', '2000-01-15', 'hve@example.com', '0934567890', '654 Đường JKL, TP.HCM'),
('HV002', 'Vũ Thị Phương', 'F', '1999-12-05', 'vtp@example.com', '0945678901', '987 Đường MNO, TP.HCM'),
('HV003', 'Đỗ Văn Giang', 'M', '2001-06-18', 'dvg@example.com', '0956789012', '147 Đường PQR, TP.HCM'),
('HV004', 'Trần Thị Hoa', 'F', '2000-08-22', 'tth@example.com', '0967890123', '258 Đường STU, TP.HCM'),
('HV005', 'Nguyễn Văn Khoa', 'M', '1998-04-30', 'nvk@example.com', '0978901234', '369 Đường VWX, TP.HCM'),
('HV006', 'Lê Thị Mai', 'F', '2001-02-14', 'ltm@example.com', '0989012345', '741 Đường YZ, TP.HCM');

-- Lớp học
INSERT INTO core_class (class_id, ma_nv, teacher_id, class_name, class_type, room, khai_giang_date, ket_thuc_date, si_so, price) VALUES
('LOP001', 'NV001', 'GV001', 'Lập trình Python cơ bản', 'O', 'ONLINE', '2024-01-15', '2024-04-15', 30, 2000000),
('LOP002', 'NV002', 'GV002', 'Web Development với Django', 'F', 'P101', '2024-02-01', '2024-05-01', 25, 3000000),
('LOP003', 'NV003', 'GV003', 'Data Science với Python', 'F', 'P102', '2024-03-01', '2024-06-01', 20, 3500000),
('LOP004', 'NV001', 'GV004', 'Machine Learning cơ bản', 'O', 'ONLINE', '2024-04-01', '2024-07-01', 25, 4000000);

-- Lịch học
INSERT INTO core_schedule (id_schedule, class_id, day, start_time, end_time) VALUES
('LH001', 'LOP001', 'Thứ 2, 4, 6', '19:00:00', '21:00:00'),
('LH002', 'LOP002', 'Thứ 3, 5, 7', '18:30:00', '20:30:00'),
('LH003', 'LOP003', 'Thứ 2, 4', '14:00:00', '17:00:00'),
('LH004', 'LOP004', 'Chủ nhật', '08:00:00', '12:00:00');

-- Đăng ký học (với điểm số mẫu)
INSERT INTO core_enrollment (student_id, class_id, enrollment_date, minitest1, minitest2, minitest3, minitest4, midterm, final) VALUES
('HV001', 'LOP001', '2024-01-10', 8.5, 7.8, 9.0, 8.2, 8.0, 8.5),
('HV002', 'LOP001', '2024-01-12', 9.0, 8.5, 8.8, 9.2, 8.8, 9.0),
('HV003', 'LOP002', '2024-01-25', 7.5, 8.0, 7.8, 8.3, 7.9, 8.1),
('HV004', 'LOP002', '2024-01-26', 8.2, 8.7, 8.5, 8.9, 8.6, 8.8),
('HV005', 'LOP003', '2024-02-20', 9.2, 8.8, 9.5, 9.0, 9.1, 9.3),
('HV006', 'LOP003', '2024-02-21', 7.8, 8.2, 8.0, 8.5, 8.1, 8.3),
('HV001', 'LOP004', '2024-03-25', 8.8, 9.0, 8.5, 8.7, 8.8, 8.9),
('HV004', 'LOP004', '2024-03-26', 9.5, 9.2, 9.8, 9.3, 9.4, 9.6);

-- Điểm danh
INSERT INTO core_attendance (id_attend, student_id, class_id, attendance_date, status) VALUES
('DD001', 'HV001', 'LOP001', '2024-01-15', 'Có mặt'),
('DD002', 'HV002', 'LOP001', '2024-01-15', 'Có mặt'),
('DD003', 'HV003', 'LOP002', '2024-02-01', 'Có mặt'),
('DD004', 'HV004', 'LOP002', '2024-02-01', 'Trễ'),
('DD005', 'HV005', 'LOP003', '2024-03-01', 'Có mặt'),
('DD006', 'HV006', 'LOP003', '2024-03-01', 'Vắng'),
('DD007', 'HV001', 'LOP004', '2024-04-01', 'Có mặt'),
('DD008', 'HV004', 'LOP004', '2024-04-01', 'Có mặt');

-- Feedback
INSERT INTO core_feedback (id_feedback, student_id, class_id, teacher_id, class_rate, teacher_rate) VALUES
('FB001', 'HV001', 'LOP001', 'GV001', 4.5, 4.8),
('FB002', 'HV002', 'LOP001', 'GV001', 4.7, 4.9),
('FB003', 'HV003', 'LOP002', 'GV002', 4.2, 4.6),
('FB004', 'HV004', 'LOP002', 'GV002', 4.8, 4.9),
('FB005', 'HV005', 'LOP003', 'GV003', 4.9, 5.0),
('FB006', 'HV006', 'LOP003', 'GV003', 4.3, 4.5),
('FB007', 'HV001', 'LOP004', 'GV004', 4.6, 4.7),
('FB008', 'HV004', 'LOP004', 'GV004', 4.8, 4.9);

-- =====================================================
-- THỐNG KÊ DỮ LIỆU
-- =====================================================

-- Hiển thị số lượng records trong mỗi bảng
SELECT 'Nhân viên' as bang, COUNT(*) as so_luong FROM core_nhanvien
UNION ALL
SELECT 'Giáo viên', COUNT(*) FROM core_teacher
UNION ALL
SELECT 'Học viên', COUNT(*) FROM core_hocvien
UNION ALL
SELECT 'Lớp học', COUNT(*) FROM core_class
UNION ALL
SELECT 'Lịch học', COUNT(*) FROM core_schedule
UNION ALL
SELECT 'Đăng ký', COUNT(*) FROM core_enrollment
UNION ALL
SELECT 'Điểm danh', COUNT(*) FROM core_attendance
UNION ALL
SELECT 'Feedback', COUNT(*) FROM core_feedback;

-- =====================================================
-- HOÀN THÀNH
-- =====================================================
SELECT '✅ Database đã được tạo và import dữ liệu mẫu thành công!' as thong_bao; 