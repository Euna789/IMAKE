'''
    #3위안에 드는지 체크해서 winner테이블 수정
    #현재3위 안 점수를 가져옴
    sql="select score from winner where program_id=? and rank=1"
    cur.execute(sql,(game_type,))
    first=cur.fetchone()[0]
    sql="select score from winner where program_id=? and rank=2"
    cur.execute(sql,(game_type,))
    second=cur.fetchone()[0]
    sql="select score from winner where program_id=? and rank=3"
    cur.execute(sql,(game_type,))
    third=cur.fetchone()[0]
    con.commit()

#######################user id 알아내서 랭크에 넣기##########

    #나의 user_id알아냄
    sql3="select user_id from user where img_url=?"
    cur.execute(sql3,(url,))
    my_row=cur.fetchone()
    my_id=my_row[0]

    #1등비교
    if score>first:
        sql5="delete from winner where program_id=? and rank=3"
        cur.execute(sql5,(game_type,))
        sql6="update winner set rank=3 where program_id=? and rank=2"
        cur.execute(sql6,(game_type,))
        sql7="update winner set rank=2 where program_id=? and rank=1"
        cur.execute(sql7,(game_type,))
        sql4="insert into winner values (?,1,?,?)"
        cur.execute(sql4,(game_type,my_id,score))
        con.commit()
    elif score>second:
        sql5="delete from winner where program_id=? and rank=3"
        cur.execute(sql5,(game_type,))
        sql6="update winner set rank=3 where program_id=? and rank=2"
        cur.execute(sql6,(game_type,))
        sql4="insert into winner values (?,2,?,?)"
        cur.execute(sql4,(game_type,my_id,score))
        con.commit()
    elif score>third:
        sql5="delete from winner where program_id=? and rank=3"
        cur.execute(sql5,(game_type,))
        sql4="insert into winner values (?,3,?,?)"
        cur.execute(sql4,(game_type,my_id,score))
        con.commit()
    con.close()

def getScore(game_type,rank):
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    sql="select score from winner where program_id=? and rank=?"
    cur.execute(sql,(game_type,rank,))
    score=cur.fetchone()[0]
    con.commit()
    con.close()
    return score
    
def first_url(game_type):
    con=sqlite3.connect("test.db")
    cur=con.cursor()
    sql="select user_id from winner where program_id=? and rank=1"
    cur.execute(sql,(game_type,))
    user_id=cur.fetchone()[0]
    sql="select img_url from user where user_id=?"
    cur.execute(sql,(user_id,))
    url=cur.fetchone()[0]
    con.commit()
    con.close()
    return url

'''
