import MySQLdb as pydb

conn = pydb.connect("localhost","root","","flaskprojectdb")

cursor = conn.cursor()

def insertdata(userid,uname,phno,logid,sessionid,date,time,predictval):
    q = "INSERT INTO useran VALUES('"+userid+"','"+uname+"','"+phno+"');"
    u = "INSERT INTO userlog VALUES('"+logid+"','"+sessionid+"','"+str(date)+"','"+str(time)+"','"+str(predictval)+"','"+userid+"');"
    cursor.execute(q)
    cursor.execute(u)
    conn.commit()
    return [cursor.rowcount]

# insertdata("user1764","user4468","3548474468","log4643","88tiuf5b","13/07/2006","23:25:46",43245.87778)
