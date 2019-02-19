import md5
import random
from datetime import datetime

topics = ["home/kitchen/light/on",
    "home/kitchen/light/off",
    "home/livingroom/light/off",
    "home/livingroom/light/on",
    "home/bathroom/light/off",
    "home/bathroom/light/on",
    "home/livingroom/tv/consumption",
    "home/livingroom/temperature",
    "home/kitchen/temperature",
    "home/bathroom/temperature",
    "home/door/kitchen/status",
    "home/door/livingroom/status",
    "home/door/bathroom/status",
    "home/door/status",
    "home/livingroom/switch1/on",
    "home/livingroom/switch2/on",
    "home/livingroom/switch3/on",
    "home/livingroom/switch4/on",
    "home/livingroom/switch5/on",
    "home/livingroom/switch7/on",
    "home/livingroom/switch8/on",
    "home/livingroom/switch9/on",
    "home/livingroom/switch10/on",
    "home/livingroom/switch11/on",
    "home/livingroom/switch12/on",
    "home/livingroom/switch13/on",
    "home/livingroom/switch1/off",
    "home/livingroom/switch2/off",
    "home/livingroom/switch3/off",
    "home/livingroom/switch4/off",
    "home/livingroom/switch5/off",
    "home/livingroom/switch6/off",
    "home/livingroom/switch7/off",
    "home/livingroom/switch8/off",
    "home/livingroom/switch9/off",
    "home/livingroom/switch10/off",
    "home/livingroom/switch11/off",
    "home/livingroom/switch12/off",
    "home/livingroom/switch13/off"
    ]

time_format = "%y-%j %H:%M:%S.%f"
csv_filename = "mqtt.csv"
server_url = "iot.eclipse.org"
# server_url = "localhost"

def microseconds():
    return datetime.now().strftime(time_format)

def calculate_timedelta(t1):
    dt = datetime.strptime(t1, time_format)
    s = str(datetime.now() - dt)
    return s[s.rfind(':')+1:].replace('.', ',')

def my_hash(data):
    r = 0
    for i in xrange(len(data)-1, -1, -1):
        r += ord(data[i]) ** i
    return r % 0xFFFFFFFF

def rand_string(length):
    A = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    r = ""
    for i in xrange(0, length):
        r += A[random.randint(0, len(A)-1)]
    return r

def apply_P(x, P):
    y = 0
    for i in xrange(0, len(P)-1):
        y += P[i] * x ** i
    return y
