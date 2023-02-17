
"""EE 250L Lab 04 Starter Code
Run vm_sub.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time


"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("sarandi/ping") #subscribes to ping / initial chain 
    

    client.message_callback_add("sarandi/ping", on_message_from_ping)  #to receive and print message and publish new message to pong
    


def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_ping(client, userdata, message): 
   print("Custom callback  - Ping: "+message.payload.decode())

   message = int(message.payload.decode()) + 1

   time.sleep(2)

   client.publish("sarandi/pong", f"{message}") #may be a string value instead of an int 

   print("Publishing pong value")




if __name__ == '__main__':
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_message = on_message

    client.on_connect = on_connect


    client.connect(host="172.20.10.4", port=1883, keepalive=60) #IP address of RPi


    #client.loop_start()
    time.sleep(1)


    client.loop_forever()