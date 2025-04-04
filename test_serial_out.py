import board
import busio
import digitalio
import time

uart = busio.UART(board.TX, board.RX, baudrate=115200)

#time.sleep(0.1)

#uart = busio.UART(board.A2, board.A3, baudrate=115200, timeout=0)

time.sleep(.1)

index = 0 
while True:
    sendstring = "Test depth " +str(index)

    print("Sending "+sendstring)
    
    uart.write(bytes(sendstring, "ascii"))

    index=index+1

    time.sleep(30)


