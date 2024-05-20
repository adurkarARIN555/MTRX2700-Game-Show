from serial.tools import list_ports

port = list(list_ports.comports())     # Gets a list of all of the ports

for p in port:                         # Loops through all of the ports and prints out the device name of each port in use
    print(p.device)
