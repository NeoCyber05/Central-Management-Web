-- Dữ liệu mẫu cho hệ thống quản lý trung tâm đào tạo

-- Nhân viên
INSERT OR IGNORE INTO core_nhanvien (ma_nv, full_name, gender, birth_day, email, sdt, address) VALUES
('NV001', 'Nguyễn Văn An', 'M', '1985-05-15', 'nva@example.com', '0901234567', '123 Đường ABC, TP.HCM'),
('NV002', 'Trần Thị Bình', 'F', '1988-08-20', 'ttb@example.com', '0907654321', '456 Đường XYZ, TP.HCM');

-- Giáo viên
INSERT OR IGNORE INTO core_teacher (teacher_id, full_name, gender, birth_day, email, sdt, address) VALUES
('GV001', 'Lê Văn Cường', 'M', '1980-03-10', 'lvc@example.com', '0912345678', '789 Đường DEF, TP.HCM'),
('GV002', 'Phạm Thị Dung', 'F', '1982-07-25', 'ptd@example.com', '0923456789', '321 Đường GHI, TP.HCM');

-- Học viên
INSERT OR IGNORE INTO core_hocvien (student_id, full_name, gender, birth_day, email, sdt, address) VALUES
('HV001', 'Hoàng Văn Em', 'M', '2000-01-15', 'hve@example.com', '0934567890', '654 Đường JKL, TP.HCM'),
('HV002', 'Vũ Thị Phương', 'F', '1999-12-05', 'vtp@example.com', '0945678901', '987 Đường MNO, TP.HCM'),
('HV003', 'Đỗ Văn Giang', 'M', '2001-06-18', 'dvg@example.com', '0956789012', '147 Đường PQR, TP.HCM');

-- Lớp học
INSERT OR IGNORE INTO core_class (class_id, MaNV, teacher_id, class_name, class_type, room, khai_giang_date, ket_thuc_date, si_so, price) VALUES
('LOP001', 'NV001', 'GV001', 'Lập trình Python cơ bản', 'O', 'ONLINE', '2024-01-15', '2024-04-15', 30, 2000000),
('LOP002', 'NV002', 'GV002', 'Web Development với Django', 'F', 'P101', '2024-02-01', '2024-05-01', 25, 3000000);

-- Lịch học
INSERT OR IGNORE INTO core_schedule (id_schedule, class_id, day, start_time, end_time) VALUES
('LH001', 'LOP001', 'Thứ 2, 4, 6', '19:00:00', '21:00:00'),
('LH002', 'LOP002', 'Thứ 3, 5, 7', '18:30:00', '20:30:00');

-- Đăng ký học (với điểm số mẫu)
INSERT OR IGNORE INTO core_enrollment (student_id, class_id, enrollment_date, minitest1, minitest2, minitest3, minitest4, midterm, final) VALUES
('HV001', 'LOP001', '2024-01-10', 8.5, 7.8, 9.0, 8.2, 8.0, 8.5),
('HV002', 'LOP001', '2024-01-12', 9.0, 8.5, 8.8, 9.2, 8.8, 9.0),
('HV003', 'LOP002', '2024-01-25', 7.5, 8.0, 7.8, 8.3, 7.9, 8.1);

-- Điểm danh
INSERT OR IGNORE INTO core_attendance (id_attend, student_id, class_id, attendance_date, status) VALUES
('DD001', 'HV001', 'LOP001', '2024-01-15', 'Có mặt'),
('DD002', 'HV002', 'LOP001', '2024-01-15', 'Có mặt'),
('DD003', 'HV003', 'LOP002', '2024-02-01', 'Có mặt');

-- Feedback
INSERT OR IGNORE INTO core_feedback (id_feedback, student_id, class_id, teacher_id, class_rate, teacher_rate) VALUES
('FB001', 'HV001', 'LOP001', 'GV001', 4.5, 4.8),
('FB002', 'HV002', 'LOP001', 'GV001', 4.7, 4.9),
('FB003', 'HV003', 'LOP002', 'GV002', 4.2, 4.6); 