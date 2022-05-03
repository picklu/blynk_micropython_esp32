import random
from BlynkLib import Blynk
from BlynkTimer import Timer
from machine import Pin, ADC

timer = Timer()

led = Pin(4, Pin.OUT)
pot = ADC(Pin(36))
blynk = Blynk(BLYNK_AUTH_TOKEN)

def read_dht():
    t = random.random() * 50
    h = random.random() * 100
    blynk.virtual_write(0, t)
    blynk.virtual_write(1, h)


def read_potentiometer():
    pot_val = pot.read()
    print(f"Potentiometer reading is {pot_val}")
    blynk.virtual_write(3, pot_val)

@blynk.on("V*")
def blynk_handle_vpins(pin, value):
    print("V{} value: {}".format(pin, value))
    if pin == "2":
        led.value(int(value[0]))
    

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    print("Updating V2 value from the server...")
    blynk.sync_virtual(2)

@blynk.on("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')


timer.set_timeout(5, read_dht)
timer.set_timeout(5, read_potentiometer)


def runLoop():
    while True:
        blynk.run()
        timer.run()
        #machine.idle()

# Run blynk in the main thread
runLoop()

# You can also run blynk in a separate thread (ESP32 only)
#import _thread
#_thread.stack_size(5*1024)
#_thread.start_new_thread(runLoop, ())
