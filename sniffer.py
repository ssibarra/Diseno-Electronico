import socket
import pymysql
import datetime

host = "desingrds.ci0brdruazre.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "desingdata"
user = "Administrator"
password = "Administrator"

connection = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
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
        tot_data, addr = sock.recvfrom(1024)
        tot_data = str(tot_data)
        print(tot_data)
        nWeeks = tot_data[8:12]
        days = tot_data[12]
        time = tot_data[13:18]
        lat = tot_data[18:21] + "." + tot_data[21:26]
        lon = tot_data[26:30] + "." + tot_data[30:35]
        # Escoger el unixtime que le funcione a su instancia
        # unixtime = (int(nWeeks)*604800)+(int(days)*86400)+int(time)-(5*3600)+315957600
        unixtime = ((int(nWeeks)-7)*604800)+((int(days)+1)*86400)+int(time)-(5*3600)+315957600
        realtime = datetime.datetime.fromtimestamp(unixtime).strftime('%Y%m%d%H%M%S')
        print(realtime)

        send = "INSERT INTO `gpsdata`(`id`, `latitude`, `longitude`, `date`) VALUES (DEFAULT, %s, %s, %s);"

        try:
            cursor.execute(send, (lat, lon, realtime))
            # Commit your changes in the database
            connection.commit()
            print('Sent')
        except:
            # Rollback in case there is any error
            connection.rollback()
            print('Error')


main()
