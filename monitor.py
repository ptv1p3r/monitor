import serial
import time
import serial.tools.list_ports

ARDUINO = "/dev/ttyUSB0"
BAUDRATE = 9600
TIMEOUT = 1
arduinoConection = None
realpower = 0.0

# ports = list(serial.tools.list_ports.comports())
# for p in ports:
# 	print p.description + p.device

# abertura de porta serie
try:
	arduinoConection = serial.Serial(ARDUINO, BAUDRATE, timeout=TIMEOUT)
	print "Ligacao com Arduino em [ %s ] com sucesso\t" % arduinoConection.name
	time.sleep(1.8)  # estabiliza a ligacao
except:
	print "Ligacao com Arduino em [ %s ] nao efetuada\t" % arduinoConection.name

try:
	if arduinoConection.isOpen():  # ligacao aberta

		while arduinoConection.in_waiting:
			time.sleep(2)
			arduinoData = arduinoConection.readline()
			# arduinoData = arduinoConection.readline()

			pieces = arduinoData.split("\t")
			realpower = pieces[0]
			apparentPower = pieces[1]

			# print "realPower: " + realpower + " Apparent Power: " + apparentPower
			print(arduinoData)

		arduinoConection.close

except KeyboardInterrupt:  # captura termino ctrl+c
	arduinoConection.close
	print "Ligacao com Arduino em [ %s ] terminada com sucesso\t" % arduinoConection.name

