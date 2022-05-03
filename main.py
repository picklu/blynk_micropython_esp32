import random
from dht import DHT11
from machine import Pin
from BlynkLib import Blynk
from BlynkTimer import Timer


led = Pin(4, Pin.OUT)
sensor = DHT11(Pin(14))

timer = Timer()
blynk = Blynk(BLYNK_AUTH_TOKEN)


def measure_sensor(retry=3):
    while retry >= 0:
        try:
            sensor.measure()
            break
        except:
            retry = retry - 1
            print(".", end="")
    print()


@timer.register(vpin_num=0, interval=5, run_once=False)
def read_temperature(vpin_num):
    measure_sensor()
    t = sensor.temperature()
    print(f"[WRITE_VIRTUAL_WRITE] Pin: V{vpin_num} t: '{t}'")
    blynk.virtual_write(vpin_num, t)


@timer.register(vpin_num=1, interval=5, run_once=False)
def read_humidity(vpin_num):
    measure_sensor()
    h = sensor.humidity()
    print(f"[VIRTUAL_WRITE] Pin: V{vpin_num} h: '{h}'")
    blynk.virtual_write(vpin_num, h)


@blynk.on("V*")
def blynk_handle_vpins(vpin_num, value):
    print(f"[VIRTUAL_READ] Pin: V{vpin_num} value: {value}")
    if vpin_num == "2":
        led.value(int(value[0]))
    

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    print("Updating V2 value from the server...")
    blynk.sync_virtual(2)

@blynk.on("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')


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
