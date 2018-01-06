-- ===班级表
DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student (
    sn       INTEGER,     --序号
    no       VARCHAR(10), --班级号
    name     TEXT,        --班级
    --enrolled DATE,        --入学时间
    PRIMARY KEY(sn)
);

-- 给sn创建一个自增序号
CREATE SEQUENCE seq_student_sn 
    START 10000 INCREMENT 1 OWNED BY student.sn;
ALTER TABLE student ALTER sn 
    SET DEFAULT nextval('seq_student_sn');
-- 班级号唯一
CREATE UNIQUE INDEX idx_student_no ON student(no);

-- === 教师表
DROP TABLE IF EXISTS teacher;
CREATE TABLE IF NOT EXISTS teacher  (
    sn       INTEGER,     --序号
    no       VARCHAR(10), --教师号
    name     TEXT,        --教师姓名
    PRIMARY KEY(sn)
);
CREATE SEQUENCE seq_teacher_sn 
    START 10000 INCREMENT 1 OWNED BY teacher.sn;
ALTER TABLE teacher ALTER sn 
    SET DEFAULT nextval('seq_teacher_sn');
CREATE UNIQUE INDEX idx_teacher_no ON teacher(no);

-- === 课程表
DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course  (
    sn       INTEGER,     --序号
    no       VARCHAR(10), --课程号
    name     TEXT,        --课程名称
    PRIMARY KEY(sn)
);
CREATE SEQUENCE seq_course_sn 
    START 10000 INCREMENT 1 OWNED BY course.sn;
ALTER TABLE course ALTER sn 
    SET DEFAULT nextval('seq_course_sn');
CREATE UNIQUE INDEX idx_course_no ON course(no);

-- === 排课信息表
DROP TABLE IF EXISTS schedule;
CREATE TABLE IF NOT EXISTS schedule  (
    stu_sn  INTEGER,     -- 班级序号
    cou_sn  INTEGER,     -- 课程序号
    tea_sn  INTEGER,     -- 教师序号
    week    TEXT,        -- 周
    section INTEGER,     -- 节次
    place   TEXT,        -- 地点
    PRIMARY KEY(stu_sn,tea_sn,cou_sn)
);

ALTER TABLE schedule 
    ADD CONSTRAINT stu_sn_fk FOREIGN KEY (stu_sn) REFERENCES student(sn);
ALTER TABLE schedule 
    ADD CONSTRAINT cou_sn_fk FOREIGN KEY (cou_sn) REFERENCES course(sn);
ALTER TABLE schedule 
    ADD CONSTRAINT tea_sn_fk FOREIGN KEY (tea_sn) REFERENCES teacher(sn);

