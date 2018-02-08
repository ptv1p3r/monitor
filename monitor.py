import serial
import mysql.connector
import time
# from time import time, gmtime, strftime
from datetime import datetime
import serial.tools.list_ports

ARDUINO = "/dev/ttyUSB0"
BAUDRATE = 9600
TIMEOUT = 1
arduinoConection = None
realPower = 0.0

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

# abertura de porta serie
try:
	arduinoConection = serial.Serial(ARDUINO, BAUDRATE, timeout=TIMEOUT)
	print "Ligacao com Arduino em [ %s ] com sucesso\t" % arduinoConection.name
	time.sleep(1.8)  # estabiliza a ligacao
except:
	print "Ligacao com Arduino em [ %s ] nao efetuada\t" % arduinoConection.name

try:
	if arduinoConection.isOpen():  # ligacao aberta

		conn = mysql.connector.Connect(host='127.0.0.1', user='monitor', password='monitor', database='monitor')
		c = conn.cursor()

		while arduinoConection.in_waiting:
			arduinoData = arduinoConection.readline()

			pieces = arduinoData.split("\t")

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

			c.execute(addReading, dataReading)

			conn.commit()

			print(arduinoData)
			time.sleep(5)  # tempo de espera 5 segundos

		arduinoConection.close
		c.close()
		conn.close()

except KeyboardInterrupt:  # captura termino ctrl+c
	arduinoConection.close
	print "Ligacao com Arduino em [ %s ] terminada com sucesso\t" % arduinoConection.name

