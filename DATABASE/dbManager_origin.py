from datetime import datetime
import pymysql

host = "10.200.37.130"   # ip address of server

def init_program_info():

    host = "192.168.0.6"
    user = "user"
    password = "1234"
    db = "capstone"

    con = pymysql.connect(host, user, password, db, port=3307)
    cur = con.cursor()

    #현재 날짜 program_info가 있는지 확인
    for i in range(1,4):
        sql = "select exists(select * from community_program_info where date=CURDATE() and program_id = "+str(i)+")"
        cur.execute(sql)
        row = cur.fetchone()
        if row[0] == 0:
            sql = "insert into community_program_info(program_id, date, used_time, num_users) values("+str(i)+",CURDATE(),0,0)"
            cur.execute(sql)
            
    con.commit()
    con.close()
    

def addTime(game_type,time):
    
    host = "192.168.0.6"
    user = "user"
    password = "1234"
    db = "capstone"
    
    con = pymysql.connect(host, user, password, db, port=3307)
    cur = con.cursor()

    #db에 있는 현재 시간을 가져옴
    sql1="select used_time from community_program_info where program_id="+str(game_type)+" and date=CURDATE()"
    cur.execute(sql1)
##    con.commit()
    
    row=cur.fetchone()

    #사용시간을 더해 db에 업데이트한다
    sql2="update community_program_info set used_time="+str(row[0]+time)+" where program_id="+str(game_type)+" and date=CURDATE()"
    cur.execute(sql2)
    con.commit()
    con.close()


def addNumUser(game_type,new_user):
    
    host = "192.168.0.6"
    user = "user"
    password = "1234"
    db = "imake"
    
    con = pymysql.connect(host, user, password, db, port=3307)
    cur = con.cursor()

    #db에 있는 현재 총 사용자수를 가져옴
    sql1="select num_users from community_program_info where program_id="+str(game_type)+" and date=CURDATE()"
    cur.execute(sql1)
    row=cur.fetchone()

    #사용자 수를 더해 db에 업데이트한다
    sql2="update community_program_info set num_users="+ str(row[0]+new_user)+" where program_id="+str(game_type)+" and date=CURDATE()"
    cur.execute(sql2)
    con.commit()
    con.close()

def addScore(game_type, score, url):
    
    host = "192.168.0.6"
    user = "user"
    password = "1234"
    db = "capstone"
     
    con = pymysql.connect(host, user, password, db, port=3307)
    cur = con.cursor()

    #사용자 추가
    sql1="insert into community_user (program_id, score, date) values ("+str(game_type)+","+str(score)+",CURDATE())"
    cur.execute(sql1)
    con.commit()
    con.close()
    

