import sqlite3
from datetime import datetime

def init_program_info():
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    #현재 날짜 program_info가 있는지 확인
    sql="select exists(select * from program_info where date=?)"
    cur.execute(sql,(datetime.today().strftime("%Y-%m-%d"),))
    row=cur.fetchone()
    if row[0]==0:
        for i in range(1,4):
            sql="insert into program_info values (?,?,0,0)"
            cur.execute(sql,(i,datetime.today().strftime("%Y-%m-%d"),))
    con.commit()
    con.close()
    

def addTime(game_type,time):
    con = sqlite3.connect("test.db")
    cur=con.cursor()

    #db에 있는 현재 시간을 가져옴
    sql1="select used_time from program_info where program_id=? and date=?"
    cur.execute(sql1,(game_type,datetime.today().strftime("%Y-%m-%d"),))
    con.commit()
    row=cur.fetchone()

    #사용시간을 더해 db에 업데이트한다
    sql2="update program_info set used_time=? where program_id=? and date=?"
    cur.execute(sql2,(row[0]+time,game_type,datetime.today().strftime("%Y-%m-%d"),))
    con.commit()
    con.close()


def addNumUser(game_type,user):
    con=sqlite3.connect("test.db")
    cur=con.cursor()

    #db에 있는 현재 총 사용자수를 가져옴
    sql1="select num_users from program_info where program_id=? and date=?"
    cur.execute(sql1,(game_type,datetime.today().strftime("%Y-%m-%d"),))
    row=cur.fetchone()

    #사용자 수를 더해 db에 업데이트한다
    sql2="update program_info set num_users=? where program_id=? and date=?"
    cur.execute(sql2,(row[0]+user,game_type,datetime.today().strftime("%Y-%m-%d"),))
    con.commit()
    con.close()

def addScore(game_type, score, url):
    con=sqlite3.connect("test.db")
    cur=con.cursor()

    #사용자 추가
    sql1="insert into user (program_id, score,date) values (?,?,?)"
    cur.execute(sql1,(game_type,score,datetime.today().strftime("%Y-%m-%d"),))
    con.commit()
    con.close()
    

