import network
import socket
import urequests as requests
import machine,utime
import secrets
led = machine.Pin(2, machine.Pin.OUT)  # GPIO 2 est utilisé pour contrôler la LED

#---------------------------------------Wifi Connection-------------------------------------------
#Wifi connection: setting the identifier and the password to the wifi connection
SSID= secrets.SSID_1				#Kot_1
PASSWORD= secrets.PASSWORD_1		#HEPL_2

# Configuration du serveur TCP et UDP
TCP_SERVER_IP = "192.168.1.26"
TCP_SERVER_PORT = 5000
UDP_SERVER_IP = "192.168.1.26"
UDP_SERVER_PORT = 5070

wlan = network.WLAN(network.STA_IF)
#Enabeling the wlan
wlan.active(True)
print("Wifi On, Status:",wlan.status())
wlan.connect(SSID, PASSWORD) #wlan.connect("secrets.SSID", "secrets.PASSWORD")
print("Waiting for connection with ",SSID)
#Loop while the wifi connection isn't establissed
while not wlan.isconnected():
    #
    led.value(1)	#Led off
    utime.sleep(1)	#Wait for 1 second
    led.value(0)	#Led on
    utime.sleep(1)
    #Checking the connection, if connection jus
    try:
        print("...")
        if wlan.isconnected():
            print("Wifi connection made with ",SSID)
            break
    #If the connection isn't working then re-trying after 1 second
    except:
        print("Wifi connection couldn't be made!, Re-trying...")
        wlan.connect(SSID, PASSWORD)
        pass
#Re-check the connection 
print("Wifi connection made with ",SSID)
#Show the actual connection features
print("IP Adresse informations: ",wlan.ifconfig())

led.value(0)  # Allume la LED

# Configuration du socket TCP
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_address = (TCP_SERVER_IP, TCP_SERVER_PORT)
tcp_sock.connect(tcp_address)

# Configuration du socket UDP
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_address = (UDP_SERVER_IP, UDP_SERVER_PORT)

data_to_send = 0

while True:
    # Envoi des données via TCP
    tcp_sock.send("{}".format(data_to_send))
    print("Données envoyées via TCP: {}".format(data_to_send))
    
    # Envoi des données via UDP
    udp_sock.sendto("{}".format(data_to_send), udp_address)
    print("Données envoyées via UDP: {}".format(data_to_send))
    
    data_to_send += 1
    utime.sleep(1.2)  # Attendre une seconde entre chaque envoi
    if (data_to_send==1000):
        data_to_send=0
