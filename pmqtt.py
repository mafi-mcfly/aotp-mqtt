import paho.mqtt.client as mqtt
import json
import sys
import common

p = None
M = None
P = None
n_t = None

msgCount = 0
run = True
csv = open(common.csv_filename, "a")

# Python seems to cache the strptime format. So this makes sense. :)
deobfuscation_start = common.microseconds()
deobfuscation_time = common.calculate_timedelta(deobfuscation_start)

def setup(payload, client):
    global p, M, P, n_t
    m = json.loads(payload)
    p = m['p']
    M = m['M']
    P = m['P']
    n_t = m['n_t']
    client.subscribe(p+"/#")
    # print "subscribed to prefix", p

def deobfuscated_topic(topic):
    tau = topic[len(p)+1:]
    for t in n_t:
        h = common.my_hash(str(tau)) * common.apply_P((n_t[t]-1), P)
        if h == M[t]:
            M[t] = long(tau)
            n_t[t] = (n_t[t]-1)
            return t
    return None

def on_connect(client, userdata, flags, rc):
    csv.write("mode;number;timestamp;topic;real_topic;delay;deobfuscation_time;endpoint\n")
    client.subscribe("hsos/#")

def on_message_pmqtt(client, userdata, msg):
    global msgCount, run, url
    if msg.topic == u"hsos/aotp/bootstrap":
        setup(msg.payload, client)
    if msg.topic == u"hsos/aotp/finish":
        run = False
    if msg.topic.startswith(p):
        deobfuscation_start = common.microseconds()
        topic = deobfuscated_topic(msg.topic)
        deobfuscation_time = common.calculate_timedelta(deobfuscation_start)
        if topic:
            csv.write("aotp;%d;%s;%s;%s;%s;%s;%s\n" % (msgCount, common.microseconds(), msg.topic, topic, common.calculate_timedelta(msg.payload), deobfuscation_time, url))
            msgCount += 1
        else:
            print "topic could not be deobfuscated"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message_pmqtt
url = sys.argv[1] if len(sys.argv) == 2 else common.server_url
client.connect(url, 1883, 60)

try:
    while run:
        client.loop()
    csv.close()
except KeyboardInterrupt:
    client.disconnect()
