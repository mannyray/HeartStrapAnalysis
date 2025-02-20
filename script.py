from openant.easy.node import Node
from openant.devices import ANTPLUS_NETWORK_KEY
from openant.devices.heart_rate import HeartRate, HeartRateData
import time

# Script based on https://github.com/Tigge/openant/blob/master/examples/heart_rate.py

def current_milli_time():
    return round(time.time() * 1000)


# strap frequency is 4.06 hz which is expected to be thus about every 246ms
# the number is not exactly every 246 but sometimes slightly varies
communication_expecation = 246

previous_time = None
total_communications = 0
skipped_communications = 0
start_time = 0
log_line = 0

def main(device_id=0):
    node = Node()
    
    node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)

    device = HeartRate(node, device_id=device_id)

    def on_found():
        global start_time
        print(f"Device {device} found and receiving")
        start_time = current_milli_time()


    def on_device_data(page: int, page_name: str, data):
        global previous_time
        global total_communications
        global skipped_communications
        global start_time
        global log_line
        current_time = current_milli_time()
        if previous_time is not None:
            time_difference = current_time - previous_time
            communications_count_during_difference = round(float(time_difference)/float(communication_expecation))
            if( communications_count_during_difference != 1):
                skipped_communications = skipped_communications + (communications_count_during_difference-1)
        total_communications = total_communications + 1
        
        previous_time = current_milli_time()
        #if isinstance(data, HeartRateData):
        #    print(f"Heart rate update {data.heart_rate} bpm")
        print(str(log_line)+": "+str(data))
        log_line = log_line+1
        time_since_start = round(float(current_time - start_time)/1000.0,3)
        expected_communications =round( time_since_start/(float(communication_expecation)/1000.0))
        print(f"{log_line}: Running for {time_since_start} seconds with {expected_communications} expected communications. Skipped communications: {skipped_communications}. Recieved communications: {total_communications}.")
        log_line = log_line+1
        print()

    
    device.on_found = on_found
    device.on_device_data = on_device_data

    try:
        print(f"Starting {device}, press Ctrl-C to finish")
        node.start()
    except KeyboardInterrupt:
        print("Closing ANT+ device...")
    finally:
        device.close_channel()
        node.stop()


if __name__ == "__main__":
    main()
