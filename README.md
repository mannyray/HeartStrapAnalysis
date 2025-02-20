# HeartStrapAnalysis

This repository is meant to a be a quick tool to test your ANT+ based heart strap and its communications. An ANT+ USB device picks up the communication signal from the heartstrap which, once put on a persons chest and activated, emits broadcast data at a frequency of about four times a second.
<center>
<figure>
<img src="assets/strap_usb.jpeg" width=75%>
<figcaption> Garmin HRM Pro strap and USB ANT+ device </figcaption>
</figure>
</center>

 Here we use the [openant](https://github.com/Tigge/openant/tree/master) python based library to assist in picking up the signals from the strap in the USB ANT+ device.
 
 ## Experiment setup:
 
 When running `python3 script.py`, the code will connect to the strap and print the strap broadcast summary:
 
 ```
1310: HeartRateData(page_specific=6083328, beat_time=24.015625, beat_count=250, heart_rate=62, operating_time=623064, manufacturer_id_lsb=1, serial_number=52701, previous_heart_beat_time=23.2060546875, battery_percentage=255)
1311: Running for 390.839 seconds with 1589 expected communications. Skipped communications: 932. Recieved communications: 656.

1312: HeartRateData(page_specific=6295552, beat_time=24.84765625, beat_count=251, heart_rate=63, operating_time=623064, manufacturer_id_lsb=1, serial_number=52701, previous_heart_beat_time=24.015625, battery_percentage=255)
1313: Running for 391.086 seconds with 1590 expected communications. Skipped communications: 932. Recieved communications: 657.

1314: HeartRateData(page_specific=6295552, beat_time=24.84765625, beat_count=251, heart_rate=63, operating_time=623064, manufacturer_id_lsb=1, serial_number=52701, previous_heart_beat_time=24.015625, battery_percentage=255)
1315: Running for 391.578 seconds with 1592 expected communications. Skipped communications: 933. Recieved communications: 658.

1316: HeartRateData(page_specific=6513664, beat_time=25.5908203125, beat_count=252, heart_rate=64, operating_time=623064, manufacturer_id_lsb=1, serial_number=52701, previous_heart_beat_time=24.84765625, battery_percentage=255)
1317: Running for 391.824 seconds with 1593 expected communications. Skipped communications: 933. Recieved communications: 659.
```

The lines are organized in groups of two by communication event from the strap. Lines `1310` and `1311` are for `beat_count=250` while `1312`, `1313` and `1314`,`1315` are for `beat_count=251` and the last two lines are for `beat_count=251`. An identical beat count (as in the case of `beatcount=251`) means that the strap communicated the same data as there was no new heart beat so it just sends the same data at the rate of about four times a second.

We observe that for line `1311` and `1313` we have that `Skipped communications: 932` is static meaning that there was no skipped communication. However, for line `1315` it is now `Skipped communications: 933.` Furtheremore, the difference between `Running for X seconds` between `1311` and `1313` is `391.086 - 390.839 = 247` milliseconds which is the expected difference for a four times a second communication rate. However, between `1315` and `1313` it is `391.578 - 391.086 = 492` millseconds. which means there was a skip of communications from the strap which explains the jump by one in `Skipped communications: 933.`

The `1593 expected communications` in `Running for 391.824 seconds with 1593 expected communications` is computed by the total run time of the experiment (`391.824`) divided by the expected frequency of communication which is every `246` milliseconds (`4.06Hz`). The expected communication number with respect to `Skipped communications: 933` allows us to compute that we have a `933/1593` skip rate which is about `59%` rate. `59%` of our packets are dropped.

## Old battery vs New battery

Running the experiment via `python3 script.py`, as explained in previous section, for an old battery after running the code for `594` seconds I obtained a skip rate of 58%:

```
2045: Running for 594.011 seconds with 2415 expected communications. Skipped communications: 1390. Recieved communications: 1023.
```

More than half of the packets being dropped is concerning as it could lead to missing out on the latest heart beat data right when it happens. This was the motivation behind this repository and purchasing a new battery and seeing if with a new battery we experience the same issue. When I connected the heart strap to my watch I was told that the battery status of the heart strap was OK, but the battery was a couple of years old (albeit used lightly).
 
 
## Script Setup and Run

Tested on a mac.

```
mkdir env
python3 -m venv env
source env/bin/activate       
python3 -m pip install openant
python3 -m pip install pyusb
python3 -m pip install libusb
brew install libusb
python3 script.py
```
