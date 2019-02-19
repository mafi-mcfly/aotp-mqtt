import paho.mqtt.client as mqtt
from time import sleep
from random import randint
import json
import sys
import common


AP = lambda x, P: common.apply_P(x, P)

def make_message_m():
    H = {}
    n_t = {}
    p = common.rand_string(2)
    P = []
    for i in xrange(0, randint(3,6)):
        P.append(randint(0,10))
    for t in common.topics:
        H_t = []
        s = common.rand_string(2)
        n = randint(4, 8)
        n_t[t] = n
        H_t.append(common.my_hash(s))
        for x in xrange(1, n):
            H_t.append(common.my_hash(str(H_t[x-1])) * AP(x, P))
        H[t] = H_t

    M = {}
    for t in H:
        M[t] = H[t][-1]
    return (p, M, P, H, n_t)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_message = on_message
url = sys.argv[1] if len(sys.argv) == 2 else common.server_url
client.connect(url, 1883, 60)

print common.microseconds(), "starting bootstrap"
p, M, P, H, n_t = make_message_m()
m = {'p': p, 'M': M, 'P': P, 'n_t': n_t}
client.publish("hsos/aotp/bootstrap", json.dumps(m))
print common.microseconds(), "bootstrap message sent"
sleep(3)

for i in xrange(1, 200):
    x = randint(0, len(common.topics)-1)
    t = common.topics[x]
    n = n_t[t]
    if n == 1:
        print t, "has no more hashes"
        p, M, P, H, n_t = make_message_m()
        m = {'p': p, 'M': M, 'P': P, 'n_t': n_t}
        client.publish("hsos/aotp/bootstrap", json.dumps(m))
    else:
        topic = p + "/" + str(H[t][n-2])
        print i, t, ">", topic
        client.publish(topic, common.microseconds())
        n_t[t] -= 1
    sleep(5)
client.publish("hsos/aotp/finish", "")
client.disconnect()
