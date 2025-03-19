import board
import busio
import digitalio
import time

#uart_sense = busio.UART(board.TX, board.RX, baudrate=9600)

#time.sleep(0.1)

uart = busio.UART(board.D2, board.D3, baudrate=115200, timeout=0)

time.sleep(.1)

index = 0 
while True:
    sendstring = "test: "+str(index)

    print("Sending "+sendstring)
    
    uart.write(bytes(sendstring, "ascii"))

    index=index+1

    time.sleep(5)


