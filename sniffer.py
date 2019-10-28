import socket
import pymysql

host = "desingrds.ci0brdruazre.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "desingdata"
user = "Administrator"
password = "Administrator"

connection = pymysql.connect(
    host, user=user, port=port, passwd=password, db=dbname)
print('Server conected')
cursor = connection.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version : {0}".format(data))


def main():

    IP = '172.31.31.63'
    PORT = 5000
    # Creating the socket to lisent UDP packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))  # Config the IP and PORT
    print('Listening ' + IP + ':' + str(PORT) + ' ...')
    while True:
        # gpsdata220191026194530+110070-07479700000000
        tot_data, addr = sock.recvfrom(1024)
        tot_data = str(tot_data)
        tot_data = tot_data[2:(len(tot_data)-1)]
        db = tot_data[0:8]
        realtime = tot_data[8:22]
        lat = tot_data[22:25] + "." + tot_data[25:29]
        lon = tot_data[29:33] + "." + tot_data[33:37]
        rpm = tot_data[37:41]
        vel = tot_data[41:]
        if (db == 'gpsdata1'):
            send = "INSERT INTO `gpsdata1` (`id`, `latitude`, `longitude`, `date`, `rpm`, `speed`) VALUES (DEFAULT, %s, %s, %s, %s, %s);"
        elif (db == 'gpsdata2'):
            send = "INSERT INTO `gpsdata2` (`id`, `latitude`, `longitude`, `date`, `rpm`, `speed`) VALUES (DEFAULT, %s, %s, %s, %s, %s);"

        try:
            cursor.execute(send, (lat, lon, realtime, rpm, vel))
            # Commit your changes in the database
            connection.commit()
            print("Sent to " + db)
        except:
            # Rollback in case there is any error
            connection.rollback()
            print("Error sending to " + db)


main()
