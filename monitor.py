import serial
import mysql.connector
import time
from datetime import datetime
import serial.tools.list_ports
import os

ARDUINO = "/dev/ttyUSB0"
BAUDRATE = 9600
TIMEOUT = 1
arduinoConn = None
logfile = "monitor.log"

# ports = list(serial.tools.list_ports.comports())
# for p in ports:
# 	print p.description + p.device

# conn = mysql.connector.Connect(host='127.0.0.1', user='monitor', password='monitor', database='monitor')
# c = conn.cursor()
#
# c.execute("SELECT * from readings")
# row = c.fetchone()
# print row[4]
# c.close()


def logWrite(strMessage):
	if os.path.exists(logfile):
		append_write = 'a'
	else:
		append_write = 'w'
	log = open(logfile, append_write)
	log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + " " + strMessage + '\n')
	log.close()


# abertura de porta serie
try:
	arduinoConn = serial.Serial(ARDUINO, BAUDRATE, timeout=TIMEOUT)
	logWrite("Ligacao com Arduino em [ %s ] com sucesso" % arduinoConn.name)
	time.sleep(1.8)  # estabiliza a ligacao
except Exception:
	logWrite("Ligacao com Arduino em [ %s ] nao efetuada" % arduinoConn.name)

try:
	if arduinoConn.isOpen():  # ligacao aberta

		dbConn = mysql.connector.Connect(host='127.0.0.1', user='monitor', password='monitor', database='monitor')  # ligacao a bd
		dbCursor = dbConn.cursor()  # abre um cursor

		while arduinoConn.in_waiting:
			arduinoData = arduinoConn.readline()  # le linha inteira do buffer

			pieces = arduinoData.split("\t")

			# Estrutura de cada leitura
			timestamps = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
			node = 1
			ct = 1
			realPower = float(pieces[0][pieces[0].index(":")+1:])
			apparentPower = float(pieces[1][pieces[1].index(":")+1:])
			supplyVoltage = float(pieces[2][pieces[2].index(":")+1:])
			irms = float(pieces[3][pieces[3].index(":")+1:])
			powerFactor = float(pieces[4][pieces[4].index(":")+1:])

			addReading = ("INSERT INTO readings "
							"(timestamp, node, ct, rpower, apower, svoltage, irms, pfactor) "
							"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
			dataReading = (timestamps, node, ct, realPower, apparentPower, supplyVoltage, irms, powerFactor)

			dbCursor.execute(addReading, dataReading)
			dbConn.commit()

			# print(arduinoData)
			time.sleep(5)  # tempo de espera 5 segundos

		arduinoConn.close
		dbCursor.close()  # fecha cursor
		dbConn.close()  # fecha ligacao a base de dados

except KeyboardInterrupt:  # captura termino ctrl+c
	if arduinoConn.isOpen():
		arduinoConn.close
	logWrite("Ligacao com Arduino em [ %s ] terminada com sucesso" % arduinoConn.name)
