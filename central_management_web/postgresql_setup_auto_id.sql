-- =====================================================
-- POSTGRESQL SETUP SCRIPT (AUTO INCREMENT ID)
-- Hệ thống quản lý trung tâm đào tạo
-- ID tự động tăng: 1, 2, 3, 4... (VARCHAR)
-- =====================================================

-- Xóa bảng nếu tồn tại (theo thứ tự dependency)
DROP TABLE IF EXISTS Feedback CASCADE;
DROP TABLE IF EXISTS Attendance CASCADE;
DROP TABLE IF EXISTS Enrollments CASCADE;
DROP TABLE IF EXISTS Schedule CASCADE;
DROP TABLE IF EXISTS Class CASCADE;
DROP TABLE IF EXISTS Teacher CASCADE;
DROP TABLE IF EXISTS HocVien CASCADE;
DROP TABLE IF EXISTS NhanVien CASCADE;

-- Xóa sequences nếu tồn tại
DROP SEQUENCE IF EXISTS nhanvien_id_seq CASCADE;
DROP SEQUENCE IF EXISTS teacher_id_seq CASCADE;
DROP SEQUENCE IF EXISTS hocvien_id_seq CASCADE;
DROP SEQUENCE IF EXISTS class_id_seq CASCADE;
DROP SEQUENCE IF EXISTS schedule_id_seq CASCADE;
DROP SEQUENCE IF EXISTS attendance_id_seq CASCADE;
DROP SEQUENCE IF EXISTS feedback_id_seq CASCADE;

-- =====================================================
-- TẠO SEQUENCES
-- =====================================================

CREATE SEQUENCE nhanvien_id_seq START 1;
CREATE SEQUENCE teacher_id_seq START 1;
CREATE SEQUENCE hocvien_id_seq START 1;
CREATE SEQUENCE class_id_seq START 1;
CREATE SEQUENCE schedule_id_seq START 1;
CREATE SEQUENCE attendance_id_seq START 1;
CREATE SEQUENCE feedback_id_seq START 1;

-- =====================================================
-- TẠO TRIGGER FUNCTION
-- =====================================================

-- Function để cập nhật si_so khi thêm/xóa enrollment
CREATE OR REPLACE FUNCTION update_class_size()
RETURNS TRIGGER AS $$
DECLARE
    current_size INTEGER;
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Lấy si_so hiện tại của lớp
        SELECT si_so INTO current_size FROM Class WHERE class_id = NEW.class_id;
        
        -- Kiểm tra nếu si_so đã đạt tối đa
        IF current_size >= 30 THEN
            RAISE EXCEPTION 'Lớp học đã đạt sĩ số tối đa (30 học viên)';
        END IF;
        
        -- Tăng si_so khi thêm enrollment mới
        UPDATE Class 
        SET si_so = si_so + 1 
        WHERE class_id = NEW.class_id;
    ELSIF TG_OP = 'DELETE' THEN
        -- Giảm si_so khi xóa enrollment
        UPDATE Class 
        SET si_so = si_so - 1 
        WHERE class_id = OLD.class_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- TẠO TRIGGER
-- =====================================================

-- Trigger cho bảng Enrollments
DROP TRIGGER IF EXISTS trg_update_class_size ON Enrollments;
CREATE TRIGGER trg_update_class_size
    BEFORE INSERT OR DELETE ON Enrollments
    FOR EACH ROW
    EXECUTE FUNCTION update_class_size();

-- =====================================================
-- TẠO BẢNG
-- =====================================================

-- Bảng Nhân viên
CREATE TABLE NhanVien (
    ma_nv VARCHAR(8) NOT NULL PRIMARY KEY DEFAULT nextval('nhanvien_id_seq')::text,
    full_name VARCHAR(40) NOT NULL,
    gender VARCHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40),
    sdt VARCHAR(15),
    address VARCHAR(30) ,
    CONSTRAINT chk_nhanvien_email CHECK (email LIKE '%@%')
);

-- Bảng Giáo viên
CREATE TABLE Teacher (
    teacher_id VARCHAR(8) NOT NULL PRIMARY KEY DEFAULT nextval('teacher_id_seq')::text,
    full_name VARCHAR(40) NOT NULL,
    gender VARCHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    birth_day DATE ,
    email VARCHAR(40) ,
    sdt VARCHAR(15) ,
    address VARCHAR(30) ,
    CONSTRAINT chk_teacher_email CHECK (email LIKE '%@%')
);

-- Bảng Học viên
CREATE TABLE HocVien (
    student_id VARCHAR(8) NOT NULL PRIMARY KEY DEFAULT nextval('hocvien_id_seq')::text,
    full_name VARCHAR(40) NOT NULL,
    gender VARCHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40) ,
    sdt VARCHAR(15),
    address VARCHAR(30),
    CONSTRAINT chk_hocvien_email CHECK (email LIKE '%@%')
);

-- Bảng Lớp học
CREATE TABLE Class (
    class_id VARCHAR(8) NOT NULL PRIMARY KEY DEFAULT nextval('class_id_seq')::text,
    class_name VARCHAR(40) NOT NULL,
    class_type VARCHAR(1) NOT NULL CHECK (class_type IN ('O', 'F')), -- O: Online, F: Offline
    room VARCHAR(15) NOT NULL,
    khai_giang_date DATE NOT NULL,
    ket_thuc_date DATE NOT NULL,
    si_so INTEGER NOT NULL DEFAULT 0 ,
    price INTEGER NOT NULL CHECK (price >= 0),
    ma_nv VARCHAR(8) REFERENCES NhanVien(ma_nv) NOT NULL,
    teacher_id VARCHAR(8) REFERENCES Teacher(teacher_id) NOT  NULL,
    CONSTRAINT chk_class_dates CHECK (ket_thuc_date > khai_giang_date)
);

-- Bảng Lịch học
CREATE TABLE Schedule (
    id_schedule VARCHAR(8) NOT NULL PRIMARY KEY DEFAULT nextval('schedule_id_seq')::text,
    class_id VARCHAR(8) NOT NULL REFERENCES Class(class_id) ON DELETE CASCADE,
    day VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CONSTRAINT chk_schedule_time CHECK (end_time > start_time)
);

-- Bảng Đăng ký học (với composite key)
CREATE TABLE Enrollments (
    student_id VARCHAR(8) NOT NULL REFERENCES HocVien(student_id) ON DELETE CASCADE,
    class_id VARCHAR(8) NOT NULL REFERENCES Class(class_id) ON DELETE CASCADE,
    enrollment_date DATE NOT NULL,
    minitest1 FLOAT CHECK (minitest1 >= 0 AND minitest1 <= 10 AND minitest1 % 0.5 = 0),
    minitest2 FLOAT CHECK (minitest2 >= 0 AND minitest2 <= 10 AND minitest2 % 0.5 = 0),
    minitest3 FLOAT CHECK (minitest3 >= 0 AND minitest3 <= 10 AND minitest3 % 0.5 = 0),
    minitest4 FLOAT CHECK (minitest4 >= 0 AND minitest4 <= 10 AND minitest4 % 0.5 = 0),
    midterm FLOAT CHECK (midterm >= 0 AND midterm <= 10 AND midterm % 0.5 = 0),
    final FLOAT CHECK (final >= 0 AND final <= 10 AND final % 0.5 = 0),
    PRIMARY KEY (student_id, class_id)
);

-- Bảng Điểm danh
CREATE TABLE Attendance (
    id_attend VARCHAR(8) NOT NULL PRIMARY KEY DEFAULT nextval('attendance_id_seq')::text,
    student_id VARCHAR(8) NOT NULL REFERENCES HocVien(student_id) ON DELETE CASCADE,
    class_id VARCHAR(8) NOT NULL REFERENCES Class(class_id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    status VARCHAR(15) NOT NULL CHECK (status IN ('Absent', 'Present'))
);

-- Bảng Feedback
CREATE TABLE Feedback (
    id_feedback VARCHAR(8) NOT NULL PRIMARY KEY DEFAULT nextval('feedback_id_seq')::text,
    student_id VARCHAR(8) NOT NULL REFERENCES HocVien(student_id) ON DELETE CASCADE,
    class_id VARCHAR(8) NOT NULL REFERENCES Class(class_id) ON DELETE CASCADE,
    teacher_id VARCHAR(8) REFERENCES Teacher(teacher_id) ON DELETE SET NULL,
    class_rate REAL CHECK (class_rate >= 1 AND class_rate <= 5),
    teacher_rate REAL CHECK (teacher_rate >= 1 AND teacher_rate <= 5)
);

-- =====================================================
-- TẠO INDEX
-- =====================================================

-- Index cho performance
-- CREATE INDEX idx_schedule_class_id ON Schedule(class_id);
-- CREATE INDEX idx_enrollment_student_id ON Enrollments(student_id);
-- CREATE INDEX idx_enrollment_class_id ON Enrollments(class_id);
-- CREATE INDEX idx_attendance_student_id ON Attendance(student_id);
-- CREATE INDEX idx_attendance_class_id ON Attendance(class_id);
-- CREATE INDEX idx_attendance_date ON Attendance(attendance_date);
-- CREATE INDEX idx_feedback_student_id ON Feedback(student_id);
-- CREATE INDEX idx_feedback_class_id ON Feedback(class_id);
-- CREATE INDEX idx_feedback_teacher_id ON Feedback(teacher_id);
-- CREATE INDEX idx_class_ma_nv ON Class(ma_nv);
-- CREATE INDEX idx_class_teacher_id ON Class(teacher_id);

-- =====================================================
-- THÊM DỮ LIỆU MẪU
-- =====================================================

-- Nhân viên (ID sẽ tự động: 1, 2, 3...)
INSERT INTO NhanVien (full_name, gender, birth_day, email, sdt, address) VALUES
('Nguyễn Văn An', 'M', '1985-05-15', 'nva@example.com', '0901234567', '123 Đường ABC, TP.HCM'),
('Trần Thị Bình', 'F', '1988-08-20', 'ttb@example.com', '0907654321', '456 Đường XYZ, TP.HCM'),
('Lê Văn Cường', 'M', '1987-03-12', 'lvc.nv@example.com', '0908888888', '789 Đường DEF, TP.HCM');

-- Giáo viên (ID sẽ tự động: 1, 2, 3, 4...)
INSERT INTO Teacher (full_name, gender, birth_day, email, sdt, address) VALUES
('Lê Văn Cường', 'M', '1980-03-10', 'lvc@example.com', '0912345678', '789 Đường DEF, TP.HCM'),
('Phạm Thị Dung', 'F', '1982-07-25', 'ptd@example.com', '0923456789', '321 Đường GHI, TP.HCM'),
('Hoàng Minh Tuấn', 'M', '1979-11-08', 'hmt@example.com', '0934567890', '654 Đường JKL, TP.HCM'),
('Nguyễn Thị Lan', 'F', '1983-09-15', 'ntl@example.com', '0945678901', '987 Đường MNO, TP.HCM');

-- Học viên (ID sẽ tự động: 1, 2, 3, 4, 5, 6...)
INSERT INTO HocVien (full_name, gender, birth_day, email, sdt, address) VALUES
('Hoàng Văn Em', 'M', '2006-01-15', 'hve@example.com', '0934567890', '654 Đường JKL, TP.HCM'),
('Vũ Thị Phương', 'F', '2004-12-05', 'vtp@example.com', '0945678901', '987 Đường MNO, TP.HCM'),
('Đỗ Văn Giang', 'M', '2005-06-18', 'dvg@example.com', '0956789012', '147 Đường PQR, TP.HCM'),
('Trần Thị Hoa', 'F', '2005-08-22', 'tth@example.com', '0967890123', '258 Đường STU, TP.HCM'),
('Nguyễn Văn Khoa', 'M', '2005-04-30', 'nvk@example.com', '0978901234', '369 Đường VWX, TP.HCM'),
('Lê Thị Mai', 'F', '2003-02-14', 'ltm@example.com', '0989012345', '741 Đường YZ, TP.HCM');

-- Lớp học (ID sẽ tự động: 1, 2, 3, 4...)
INSERT INTO Class (ma_nv, teacher_id, class_name, class_type, room, khai_giang_date, ket_thuc_date, si_so, price) VALUES
('1', '1', 'Toán 12 O', 'O', 'P101', '2024-01-1', '2024-04-01', 30, 2000000),
('2', '2', 'Toán 12 E', 'F', 'P102', '2024-02-01', '2024-05-01', 25, 3000000),
('3', '3', 'Toán 12 E', 'F', 'P103', '2024-03-01', '2024-06-01', 20, 3000000),
('1', '4', 'Toán 12 O', 'O', 'P104', '2024-04-01', '2024-07-01', 25, 4000000);

-- Lịch học (ID sẽ tự động: 1, 2, 3, 4...)
INSERT INTO Schedule (class_id, day, start_time, end_time) VALUES
('1', 'Thứ 2, 4, 6', '19:00:00', '21:00:00'),
('2', 'Thứ 3, 5, 7', '18:30:00', '20:30:00'),
('3', 'Thứ 2, 4, 6', '14:00:00', '16:00:00'),
('4', 'Thứ 3, 5, 7', '08:00:00', '10:00:00');

-- Đăng ký học (với điểm số mẫu)
INSERT INTO Enrollments (student_id, class_id, enrollment_date, minitest1, minitest2, minitest3, minitest4, midterm, final) VALUES
('1', '1', '2024-01-10', 8.5, 7.0, 9.0, 8.0, 8.0, 8.5),
('2', '1', '2024-01-12', 9.0, 8.5, 8.5, 9.5, 8.0, 9.0),
('3', '2', '2024-01-25', 7.5, 8.0, 7.0, 8.5, 7.0, 8.0),
('4', '2', '2024-01-26', 8.5, 8.5, 8.5, 9.0, 8.5, 8.5),
('5', '3', '2024-02-20', 9.5, 8.0, 9.5, 9.0, 9.5, 9.5),
('6', '3', '2024-02-21', 7.5, 8.0, 8.0, 8.5, 8.5, 8.5),
('1', '4', '2024-03-25', 8.5, 9.0, 8.5, 8.5, 8.5, 8.5),
('4', '4', '2024-03-26', 9.5, 9.0, 10, 9.5, 9.5, 9.5);

-- Điểm danh (ID sẽ tự động: 1, 2, 3, 4...)
INSERT INTO Attendance (student_id, class_id, attendance_date, status) VALUES
('1', '1', '2024-01-15', 'Present'),
('2', '1', '2024-01-15', 'Present'),
('3', '2', '2024-02-01', 'Present'),
('4', '2', '2024-02-01', 'Absent'),
('5', '3', '2024-03-01', 'Present'),
('6', '3', '2024-03-01', 'Absent'),
('1', '4', '2024-04-01', 'Present'),
('4', '4', '2024-04-01', 'Present');

-- Feedback (ID sẽ tự động: 1, 2, 3, 4...)
INSERT INTO Feedback (student_id, class_id, teacher_id, class_rate, teacher_rate) VALUES
('1', '1', '1', 4.5, 4.8),
('2', '1', '1', 4.7, 4.9),
('3', '2', '2', 4.2, 4.6),
('4', '2', '2', 4.8, 4.9),
('5', '3', '3', 4.9, 5.0),
('6', '3', '3', 4.3, 4.5),
('1', '4', '4', 4.6, 4.7),
('4', '4', '4', 4.8, 4.9);

-- =====================================================
-- THỐNG KÊ DỮ LIỆU
-- =====================================================

-- Hiển thị số lượng records trong mỗi bảng
SELECT 'Nhân viên' as bang, COUNT(*) as so_luong FROM NhanVien
UNION ALL
SELECT 'Giáo viên', COUNT(*) FROM Teacher
UNION ALL
SELECT 'Học viên', COUNT(*) FROM HocVien
UNION ALL
SELECT 'Lớp học', COUNT(*) FROM Class
UNION ALL
SELECT 'Lịch học', COUNT(*) FROM Schedule
UNION ALL
SELECT 'Đăng ký', COUNT(*) FROM Enrollments
UNION ALL
SELECT 'Điểm danh', COUNT(*) FROM Attendance
UNION ALL
SELECT 'Feedback', COUNT(*) FROM Feedback;

-- =====================================================
-- DEMO THÊM DỮ LIỆU MỚI
-- =====================================================

-- Ví dụ: Thêm học viên mới (ID sẽ tự động là 7)
INSERT INTO HocVien (full_name, gender, birth_day, email, sdt, address) VALUES
('Nguyễn Thị Lan Anh', 'F', '2000-03-20', 'ntla@example.com', '0999888777', '123 Đường Mới, TP.HCM');

-- Ví dụ: Thêm giáo viên mới (ID sẽ tự động là 5)
INSERT INTO Teacher (full_name, gender, birth_day, email, sdt, address) VALUES
('Trần Văn Đức', 'M', '1985-12-10', 'tvd@example.com', '0988777666', '456 Đường Mới, TP.HCM');

-- Kiểm tra ID mới được tạo
SELECT 'Học viên mới nhất' as loai, student_id, full_name FROM HocVien ORDER BY student_id::integer DESC LIMIT 1
UNION ALL
SELECT 'Giáo viên mới nhất', teacher_id, full_name FROM Teacher ORDER BY teacher_id::integer DESC LIMIT 1;

-- =====================================================
-- HOÀN THÀNH
-- =====================================================
SELECT '✅ Database với Auto-Increment ID đã được tạo thành công!' as thong_bao;
SELECT '📝 Khi thêm mới, chỉ cần INSERT không cần chỉ định ID!' as ghi_chu; 