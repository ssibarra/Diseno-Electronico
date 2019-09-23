import socket
import struct
import pymysql

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
        print(tot_data)
        print(addr[0])
        print(addr[1])

        sql = "INSERT INTO Arriving_Data (ipsource, port, message)  VALUES (%s, %s, %s);"

        try:
            cursor.execute(sql, (addr[0], addr[1], tot_data))
            # Commit your changes in the database
            conn.commit()
            print('Sent')
        except:
            # Rollback in case there is any error
            conn.rollback()
            print('Error')


main()
