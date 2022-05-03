import random
from BlynkLib import Blynk
from BlynkTimer import Timer
from machine import Pin, ADC

timer = Timer()

led = Pin(4, Pin.OUT)
pot = ADC(Pin(36))
blynk = Blynk(BLYNK_AUTH_TOKEN)

@timer.register(vpin_num=0, interval=5, run_once=False)
def read_temperature(vpin_num):
    t = random.random() * 50
    print(f"[WRITE_VIRTUAL_WRITE] Pin: V{vpin_num} t: '{t}'")
    blynk.virtual_write(vpin_num, t)


@timer.register(vpin_num=1, interval=5, run_once=False)
def read_humidity(vpin_num):
    h = random.random() * 100
    print(f"[WRITE_VIRTUAL_WRITE] Pin: V{vpin_num} h: '{h}'")
    blynk.virtual_write(vpin_num, h)


@timer.register(vpin_num=3, interval=5, run_once=False)
def read_potentiometer(vpin_num):
    pot_val = pot.read()
    print(f"[WRITE_VIRTUAL_WRITE] Pin: V{vpin_num} Value: '{pot_val}'")
    blynk.virtual_write(vpin_num, pot_val)

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


# timer.set_timeout(5, read_dht)
# timer.set_timeout(5, read_potentiometer)


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
