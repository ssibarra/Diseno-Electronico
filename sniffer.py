import socket
import struct
import pymysql
import datetime

host = "rdsdiseno.c37pqurbdepy.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "RDS_diseno"
user = "admin"
password = "diseno1234"

conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
print('Server conected')
cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version : {0}".format(data))


def main():

    IP = '192.168.1.65'
    PORT = 6000
    # Creating the socket to lisent UDP packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))  # Config the IP and PORT
    print('Listening ' + IP + ':' + str(PORT) + ' ...')
    while True:
        tot_data, addr = sock.recvfrom(1024)
        nWeeks = tot_data[6:10]
        days = tot_data[10]
        time = tot_data[11:16]
        lat = tot_data[16:24]
        lon = tot_data[24:33]
        # Escoger el unixtime que le funcione a su instancia
        # unixtime = (int(nWeeks)*604800)+(int(days)*86400)+int(time)-(5*3600)+315957600
        unixtime = ((int(nWeeks)-7)*604800)+((int(days)+1)
                                             * 86400)+int(time)-(5*3600)+315957600
        realtime = datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y%m%d%H%M%S')
        print(realtime)

        sql = "INSERT INTO Arriving_Data (ipsource, lat, lng, date)  VALUES (%s, %s, %s, %s);"

        try:
            cursor.execute(sql, (addr[0], lat, lon, realtime))
            # Commit your changes in the database
            conn.commit()
            print('Sent')
        except:
            # Rollback in case there is any error
            conn.rollback()
            print('Error')


main()
