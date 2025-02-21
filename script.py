from openant.easy.node import Node
from openant.easy.channel import Channel
from openant.devices import ANTPLUS_NETWORK_KEY
from openant.devices.heart_rate import HeartRate, HeartRateData
import time

# Script based on https://github.com/Tigge/openant/blob/master/examples/heart_rate.py

def current_milli_time():
    return round(time.time() * 1000)


previous_time = None

def main(device_id=0):
    node = Node()
    
    node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)

    def on_update(data: list):
        global counter
        counter = counter + 1
        
    def on_device_data2(data):
        global previous_time
        current_time = current_milli_time()
        if previous_time is not None:
            time_difference = current_time - previous_time
            print(time_difference)
        previous_time = current_time

    
    channel = node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)

    # setup callbacks
    channel.on_broadcast_data = on_device_data2
    channel.on_burst_data = on_device_data2

    # setup slave channel
    channel.set_period(8070)
    channel.set_search_timeout(12)
    channel.set_rf_freq(57)
    channel.set_id(0, 120, 0)





    try:
        channel.open()
        node.start()
    except KeyboardInterrupt:
        print("Closing ANT+ device...")
    finally:
        node.stop()


if __name__ == "__main__":
    main()
