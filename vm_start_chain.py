
"""EE 250L Lab 04 Starter Code
Run vm_sub.py in a separate terminal on your VM."""

from multiprocessing.sharedctypes import Value
import paho.mqtt.client as mqtt
import time


"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    time.sleep(1)
    client.subscribe("sarandi/pong") #subscribes to ping 

    client.message_callback_add("sarandi/pong", on_message_from_pong) #to receive and print message from pong and publish new message to pong

    client.publish("sarandi/ping", 13) #initial message with a value of 13


def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_pong(client, userdata, message): 
   print("Custom callback  - Pong: "+(message.payload.decode()))
   value= int(message.payload.decode()) + 1
   time.sleep(2)
   client.publish("sarandi/ping", f"{value}") #publish new value 
   print("Publishing ping value")

if __name__ == '__main__':
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_message = on_message

    client.on_connect = on_connect


    client.connect(host="172.20.10.4", port=1883, keepalive=60) #IP address of Rpi
    
    time.sleep(1)
    client.loop_forever()
