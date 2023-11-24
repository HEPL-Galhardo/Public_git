# Import necessary modules
import network  # For WiFi connectivity
import socket   # For handling sockets (TCP and UDP)
import urequests as requests  # For making HTTP requests (not used in this code)
import machine  # For hardware-related operations
import utime    # For handling time-related operations
import secrets  # A custom module (not included here) for storing sensitive data

# Set up a pin for controlling an LED (GPIO 2 in this case)
led = machine.Pin(2, machine.Pin.OUT)

#---------------------------------------Wifi Connection-------------------------------------------

# Define WiFi credentials (SSID and PASSWORD) using secrets module
SSID = secrets.SSID_1        # SSID of the WiFi network
PASSWORD = secrets.PASSWORD_1    # Password for the WiFi network

# Define TCP and UDP server configurations
TCP_SERVER_IP = "192.168.1.26"  # IP address of TCP server
TCP_SERVER_PORT = 5000          # Port for TCP communication
UDP_SERVER_IP = "192.168.1.26"  # IP address of UDP server
UDP_SERVER_PORT = 5070          # Port for UDP communication

# Create a WLAN (Wireless Local Area Network) object
wlan = network.WLAN(network.STA_IF)

# Enable WLAN
wlan.active(True)
print("Wifi On, Status:", wlan.status())

# Connect to the WiFi network using the provided SSID and PASSWORD
wlan.connect(SSID, PASSWORD)
print("Waiting for connection with ", SSID)

# Loop until the WiFi connection is established
while not wlan.isconnected():
    # Blink LED to indicate attempts to connect
    led.value(1)   # LED off
    utime.sleep(1)   # Wait for 1 second
    led.value(0)   # LED on
    utime.sleep(1)
    
    try:
        print("...")
        if wlan.isconnected():
            print("Wifi connection made with ", SSID)
            break
    except:
        # If an exception occurs, retry connecting to WiFi
        print("Wifi connection couldn't be made! Retrying...")
        wlan.connect(SSID, PASSWORD)
        pass

# Re-check the connection
print("Wifi connection made with ", SSID)

# Display the actual connection information
print("IP Address information: ", wlan.ifconfig())

led.value(0)  # Turn on the LED to indicate successful connection

# Configure TCP socket
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
tcp_address = (TCP_SERVER_IP, TCP_SERVER_PORT)  # Define the address and port for TCP connection
tcp_sock.connect(tcp_address)  # Connect the TCP socket to the defined address

# Configure UDP socket
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
udp_address = (UDP_SERVER_IP, UDP_SERVER_PORT)  # Define the address and port for UDP connection

data_to_send = 0  # Initialize data to be sent

# Main loop for sending data via TCP and UDP
while True:
    # Send data via TCP
    tcp_sock.send("{}".format(data_to_send))  # Send data through the TCP socket
    print("Data sent via TCP: {}".format(data_to_send))
    
    # Send data via UDP
    udp_sock.sendto("{}".format(data_to_send), udp_address)  # Send data through the UDP socket
    print("Data sent via UDP: {}".format(data_to_send))
    
    # Increment data and reset after reaching 1000
    data_to_send += 1
    if data_to_send == 1000:
        data_to_send = 0
    
    utime.sleep(1.2)  # Wait for 1.2 seconds before sending the next data
        #To make the different tests change step by step to 0.1s to see UDP performance against TCP limitations
        # and further on to test UDP limitations.