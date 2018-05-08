from zipfile import ZipFile
import redis
import csv
import os

def parse(zip_filename, folder_location):
    redis_conn = redis.Redis()
    redis_conn.flushdb()
    
    file1 = ""

    with ZipFile(zip_filename, 'r') as zip:
        file1 = zip.namelist()[0]
        zip.extractall(folder_location)
    #print "file1 = ", file1

    with open(folder_location+file1) as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            prev_close = float(row['PREVCLOSE'])
            
            if prev_close == 0:
                prev_close = (float(row['OPEN']) + float(row['LOW']) + float(row['HIGH']) + float(row['CLOSE']))/4
            
            redis_conn.hmset("scrip:'"+row["SC_NAME"].strip()+"'", {'code':row['SC_CODE'],'open':row['OPEN'], 'high':row['HIGH'], 'low':row['LOW'],'close':row['CLOSE'] , 'variation': round( ((float(row["CLOSE"]) - float(row["OPEN"]) ) * 100 / prev_close ),2)   }) 
               
if __name__ == "__main__":
    parse("/home/ubuntu/web_app/EQ080518_CSV.ZIP", "/home/ubuntu/web_app/")