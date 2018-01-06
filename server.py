# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web

import dbconn
dbconn.register_dsn("host=localhost dbname=examdb user=examdbo password=pass")


class BaseReqHandler(tornado.web.RequestHandler):

    def db_cursor(self, autocommit=True):
        return dbconn.SimpleDataCursor(autocommit=autocommit)
    

class MainHandler(BaseReqHandler):
    def get(self):
        self.render("1homepage.html",title="主页")

class StudentHandler(BaseReqHandler):
    def get(self):
        with self.db_cursor() as cur:
            sql = '''
            SELECT sc.stu_sn, s.name as stu_name, c.name as cou_name, t.name as tea_name, 
            sc.week, sc.section, sc.place, sc.cou_sn
            FROM schedule as sc
            INNER JOIN student as s ON sc.stu_sn = s.sn
            INNER JOIN course as c  ON sc.cou_sn = c.sn
            INNER JOIN teacher as t  ON sc.tea_sn = t.sn
            ORDER BY stu_sn, tea_sn, cou_sn;
            '''
            cur.execute(sql)
            items = cur.fetchall()
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render("3student2.html",title="学生页面", items=items)

class TeacherHandler(BaseReqHandler):
    def get(self):
        with self.db_cursor() as cur:
            sql = '''
            SELECT  t.name as tea_name,sc.stu_sn, c.name as cou_name, s.name as stu_name, 
            sc.week, sc.section, sc.place, sc.cou_sn 
            FROM schedule as sc
            INNER JOIN student as s ON sc.stu_sn = s.sn
            INNER JOIN course as c  ON sc.cou_sn = c.sn
            INNER JOIN teacher as t  ON sc.tea_sn = t.sn
            ORDER BY stu_sn, tea_sn, cou_sn;
            '''
            cur.execute(sql)
            items = cur.fetchall()
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render("5teacher2.html",title="教师页面", items=items)

class ScheduleHandler(BaseReqHandler):
    def get(self):
        with self.db_cursor() as cur:
            sql = '''
            SELECT sc.stu_sn, sc.tea_sn, sc.cou_sn, c.name as cou_name, t.name as tea_name,s.name as stu_name,
            sc.week, sc.section, sc.place 
            FROM schedule as sc
            INNER JOIN student as s ON sc.stu_sn = s.sn
            INNER JOIN course as c  ON sc.cou_sn = c.sn
            INNER JOIN teacher as t  ON sc.tea_sn = t.sn
            ORDER BY stu_sn, tea_sn, cou_sn;
            '''
            cur.execute(sql)
            items = cur.fetchall()
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.render("6schedule.html",title="排课信息", items=items) 


class CourseAddHandler(BaseReqHandler):
    def post(self):
        stu_sn  = int(self.get_argument("stu_sn"))
        tea_sn  = int(self.get_argument("tea_sn"))
        cou_sn  = int(self.get_argument("cou_sn"))
        week    = self.get_argument("week")
        section = int(self.get_argument("section"))
        place   = self.get_argument("place")
        
        with self.db_cursor() as cur:
            sql = '''INSERT INTO schedule 
            (stu_sn, tea_sn, cou_sn, week, section, place)  VALUES( %s, %s, %s, %s, %s, %s);'''
            cur.execute(sql, (stu_sn, tea_sn, cou_sn, week, section, place))
            cur.commit()
        
        self.set_header("Content-Type", "text/html; charset=UTF-8") 
        self.redirect("/schedule")

class CourseDelHandler(BaseReqHandler):
    def get(self, stu_sn,tea_sn ,cou_sn):
        stu_sn = int(stu_sn)
        tea_sn = int(tea_sn)
        cou_sn = int(cou_sn)
        
        with self.db_cursor() as cur:
            sql = '''
            DELETE FROM schedule 
                WHERE stu_sn= %s AND cou_sn= %s AND tea_sn= %s'''
            cur.execute(sql, (stu_sn, cou_sn, tea_sn))
            cur.commit()

        self.set_header("Content-Type", "text/html; charset=UTF-8")
        self.redirect("/schedule")

class CourseEditHandler(BaseReqHandler):
    def get(self, stu_sn, tea_sn, cou_sn):
        stu_sn  = int(stu_sn)
        tea_sn  = int(tea_sn)
        cou_sn  = int(cou_sn)
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        with self.db_cursor() as cur:
            sql = '''
            SELECT week,section,place FROM schedule
                WHERE stu_sn= %s AND cou_sn= %s AND tea_sn= %s'''
            cur.execute(sql, (stu_sn, cou_sn, tea_sn))
            row = cur.fetchone()
            if row:
                self.render("7schedule_edit.html", stu_sn=stu_sn, tea_sn=tea_sn, 
                    cou_sn=cou_sn, week=row[0],section=row[1],place=row[2])
            else:
                self.write('Not FOUND!')
    
    def post(self, stu_sn, cou_sn, tea_sn):
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        tea_sn = int(tea_sn)
        week=self.get_argument("week")
        section = int(self.get_argument("section"))
        place   = self.get_argument("place")
        self.set_header("Content-Type", "text/html; charset=UTF-8")
        with self.db_cursor() as cur:
            sql = '''
            UPDATE schedule SET week=%s,section=%s,place=%s
                WHERE stu_sn= %s AND cou_sn= %s AND tea_sn= %s'''
            cur.execute(sql, (week,section,place,stu_sn, cou_sn,tea_sn))
            cur.commit()
        self.redirect("/schedule")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/student",  StudentHandler),
    (r"/teacher",  TeacherHandler),
    (r"/schedule", ScheduleHandler),
    (r"/course.add", CourseAddHandler),
    (r"/course.del/([0-9]+)/([0-9]+)/([0-9]+)", CourseDelHandler),
    (r"/course.edit/([0-9]+)/([0-9]+)/([0-9]+)", CourseEditHandler)
], debug=True)


if __name__ == "__main__":
    application.listen(8888)
    server = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(lambda: None, 500, server).start()
    server.start()

