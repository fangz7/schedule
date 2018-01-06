DELETE FROM schedule;
DELETE FROM course;
DELETE FROM student;
DELETE FROM teacher;

INSERT INTO student (sn, no, name)  VALUES
    (101, 'S001',  '信息01'),
    (102, 'S002',  '信息02'), 
    (103, 'S003',  '土地01'),
    (104, 'S004',  '土地02');

INSERT INTO teacher (sn, no, name)  VALUES 
    (101, 't001',  '陈老师'), 
    (102, 't002',  '赵老师'),
    (103, 't003',  '高老师');

INSERT INTO course (sn, no, name)  VALUES 
    (101, 'C01',  '高数'), 
    (102, 'C02',  '外语'),
    (103, 'C03',  '线代');


INSERT INTO schedule (stu_sn,tea_sn,cou_sn,week,section,place)  VALUES 
    (102, 101, 101, '一',2,'a401'), 
    (103, 102, 102, '二',1,'b412'),
    (103, 103, 103, '三',3,'c309'),
    (101, 102, 102, '三',3,'a103');


    
