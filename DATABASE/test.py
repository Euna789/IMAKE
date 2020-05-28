import dbManager as db

db.init_program_info()

gametype=3

time=777

num_user=1

score=150

img_url="new6"

db.addTime(gametype, time)

db.addNumUser(gametype,num_user)

db.addScore(gametype, score, img_url)

