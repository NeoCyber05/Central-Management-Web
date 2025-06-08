





--- 


-- Tạo bảng nhan_vien
CREATE TABLE nhan_vien (
    nv_id SERIAL PRIMARY KEY,
    full_name VARCHAR(40) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40) NOT NULL,
    sdt VARCHAR(15) NOT NULL,
    address VARCHAR(30) NOT NULL
);

-- Tạo bảng teacher
CREATE TABLE teacher (
    teacher_id SERIAL PRIMARY KEY,
    full_name VARCHAR(40) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40) NOT NULL,
    sdt VARCHAR(15) NOT NULL,
    address VARCHAR(30) NOT NULL,
    trinh_do VARCHAR(10) DEFAULT 'Cử nhân' CHECK (trinh_do IN ('Cử nhân', 'Thạc Sĩ', 'Tiến Sĩ'))
);

-- Tạo bảng hoc_vien
CREATE TABLE hoc_vien (
    student_id SERIAL PRIMARY KEY,
    full_name VARCHAR(40) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    birth_day DATE NOT NULL,
    email VARCHAR(40) NOT NULL,
    sdt VARCHAR(15) NOT NULL,
    address VARCHAR(30) NOT NULL
);

-- Tạo bảng class_type
CREATE TABLE class_type (
    type_id SERIAL PRIMARY KEY,
    describe TEXT NOT NULL,
    code CHAR(1) UNIQUE NOT NULL
);

-- Tạo bảng clazz
CREATE TABLE clazz (
    class_id SERIAL PRIMARY KEY,
    nv_id INTEGER NOT NULL REFERENCES nhan_vien(nv_id) ON DELETE RESTRICT,
    teacher_id INTEGER NOT NULL REFERENCES teacher(teacher_id) ON DELETE RESTRICT,
    type_id INTEGER NOT NULL REFERENCES class_type(type_id) ON DELETE RESTRICT,
    class_name VARCHAR(40) NOT NULL,
    room VARCHAR(15) NOT NULL,
    khai_giang DATE NOT NULL,
    ket_thuc DATE NOT NULL,
    si_so INTEGER DEFAULT 0 NOT NULL,
    price INTEGER NOT NULL
);

-- Tạo bảng schedule
CREATE TABLE schedule (
    id_schedule SERIAL PRIMARY KEY,
    class_id INTEGER UNIQUE NOT NULL REFERENCES clazz(class_id) ON DELETE CASCADE,
    day VARCHAR(2)[] CHECK (array_length(day, 1) = 3),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

-- Tạo bảng enrollments
CREATE TABLE enrollments (
    student_id INTEGER NOT NULL REFERENCES hoc_vien(student_id) ON DELETE CASCADE,
    class_id INTEGER NOT NULL REFERENCES clazz(class_id) ON DELETE CASCADE,
    enrollment_date DATE NOT NULL,
    minitest1 DECIMAL(4,2) CHECK (minitest1 >= 0 AND minitest1 <= 10),
    minitest2 DECIMAL(4,2) CHECK (minitest2 >= 0 AND minitest2 <= 10),
    minitest3 DECIMAL(4,2) CHECK (minitest3 >= 0 AND minitest3 <= 10),
    minitest4 DECIMAL(4,2) CHECK (minitest4 >= 0 AND minitest4 <= 10),
    midterm DECIMAL(4,2) CHECK (midterm >= 0 AND midterm <= 10),
    final DECIMAL(4,2) CHECK (final >= 0 AND final <= 10),
    PRIMARY KEY (student_id, class_id)
);

-- Tạo bảng attendance
CREATE TABLE attendance (
    id_attend SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES hoc_vien(student_id) ON DELETE CASCADE,
    class_id INTEGER NOT NULL REFERENCES clazz(class_id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    status VARCHAR(15) CHECK (status IN ('Absent', 'Present'))
);

-- Tạo bảng feedback
CREATE TABLE feedback (
    id_feedback SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES hoc_vien(student_id) ON DELETE RESTRICT,
    class_id INTEGER NOT NULL REFERENCES clazz(class_id) ON DELETE RESTRICT,
    teacher_id INTEGER NOT NULL REFERENCES teacher(teacher_id) ON DELETE RESTRICT,
    class_rate DECIMAL(4,2) CHECK (class_rate >= 1 AND class_rate <= 10),
    teacher_rate DECIMAL(4,2) CHECK (teacher_rate >= 1 AND teacher_rate <= 10)
);







ALTER TABLE schedule
ADD CONSTRAINT days_valid CHECK (
    array_length(day, 1) = 3
    AND days <@ ARRAY['2','3','4','5','6','7','CN']
);


ALTER TABLE schedule
ADD CONSTRAINT check_time_2h
CHECK (end_time = start_time + INTERVAL '2 hours');