#!/usr/bin/env python2.7

import os
import time
import datetime
import MySQLdb

global c
global db
def getCPUtemperature():
    t_cpu = os.popen('vcgencmd measure_temp').readline()
    t_cpu = t_cpu.replace("temp=","").replace("'C\n","")
    return(t_cpu)

def insert_to_db():
    temperatur = (getCPUtemperature())
    zeit = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
    datum = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
    print (temperatur + " - " + zeit + " - " + datum)
    sql =  "INSERT INTO TAB_CPU (TValue, T_Date, T_Time) VALUES (%s, %s, %s)" 
    try:
        c.execute(sql,( str(temperatur) , str(datum), str(zeit)))
        db.commit()
    except:
        db.rollback()
    #db.close()

def read_from_db():
    try:
        #c.execute("SELECT * FROM TAB_CPU WHERE ID = (SELCET MAX(ID) FROM TAB_CPU)")
        c.execute("SELECT * FROM TAB_CPU ORDER BY ID DESC LIMIT 1")      
        result = c.fetchall()
        if result is not None:
             print ('CPU temperature: ' , result[0][1], '| time: ' , result[0][3], ' | datum: ' , result[0][2])
    except:
        print ("read error")
    
def main():
    while 1:
        insert_to_db()
        read_from_db()
        time.sleep(10)
    
        
if __name__ == '__main__':
    try:
        db = MySQLdb.connect("localhost","root","test","DB_CPU")
        c= db.cursor()
    except:
        print ("Keine Verbindung zum Server...")
             
    try:
      main()
    except KeyboardInterrupt:
      print ("bye bye...")
      pass    
        
  
