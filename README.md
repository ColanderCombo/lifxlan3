# lifxlan

**lifxlan** is a Python module for locally controlling LIFX devices (such as lightbulbs) over a LAN. 

## How to Install

`sudo pip install lifxlan`

Or you can install from source with:

`sudo python setup.py install`

## Run

See the `examples` folder for example scripts that use **lifxlan**.  

## Overview

You can do several things with this library:

* Control LIFX devices using the high-level API (see the `examples` folder).
* Build your own high-level API on top of the low-level networking messages.
* Build virtual LIFX devices in software (think adapters for Philips Hue bulbs, Wemo, etc).

<!---
That's right, you can also use the low-level networking library to create messages that LIFX *devices* send to *clients*, effectively simulating a LIFX device in software. That means you can write a software program that looks and acts like a LIFX device, but is really converting SetColor and/or SetPower messages into API calls for other RGB lightbulbs or on/off devices, like Philips Hue bulbs and Wemos.

TL;DR: Theoretically, you can use this library to write proxy programs that let you view and control your Hue lights and Wemos through the LIFX app! Whoa!
-->
#### High-Level API:

* **lifxlan.py** - Provides the LifxLAN API, and low-level API for sending broadcast LIFX packets to the LAN.
* **device.py** - Provides the Device API, and low-level API for sending unicast LIFX packets to a Device.
* **light.py** - Provides the Light API. Subclass of Device.

##### LifxLAN API

```
# power = "on"/"off", True/False, 0/1, or 0/65535
# color = list of HSBK values: [hue (0-65535), saturation (0-65535), brightness (0-65535), Kelvin (2500-9000)]
# duration = transition time in seconds
# rapid = True/False. If True, don't wait for device response before proceeding, just send multiple packets and move on

get_lights()											# returns list of Light objects
set_power_all_lights(power, [duration], [rapid])		# set power for all lights on LAN
set_color_all_lights_color(color, [duration], [rapid])	# set color for all lights on LAN
get_power_all_lights()									# returns dict of Light, power pairs
get_color_all_lights()									# returns dict of Light, color pairs

```

##### Device API

```
# label = string, 32 char max
# power = "on"/"off", True/False, 0/1, or 0/65535
# rapid = True/False. If True, don't wait for device response before proceeding, just send multiple packets and move on

set_label(label)			
set_power(power, [rapid])			 
get_mac_addr()
get_service()						# returns int, 1 = UDP
get_port()							
get_label()			
get_power()							# returns 0 for off, 65535 for on
get_host_firmware_tuple()			# returns (build_timestamp (in nanoseconds), version)
get_host_firmware_build_timestamp()
get_host_firmware_version()
get_wifi_info_tuple()				# returns (wifi_signal_mw, wifi_tx_bytes, wifi_rx_bytes)
get_wifi_signal_mw()
get_wifi_tx_bytes()
get_wifi_rx_bytes()			
get_wifi_firmware_tuple()			# returns (build_timestamp (in nanoseconds), version)
get_wifi_firmware_build_timestamp()	
get_wifi_firmware_version()
get_version_tuple()					# returns (vendor, product, version)
get_vendor()
get_product()
get_version()
get_info_tuple()					# returns (time (current timestamp in ns), uptime (in ns), downtime (in ns, +/- 5 seconds))
get_time()
get_uptime()
get_downtime()
```

##### Light API

The Light API provides everything in the Device API, as well as:

```
# power = power = "on"/"off", True/False, 0/1, or 0/65535
# color = HSBK list of values: [hue (0-65535), saturation (0-65535), brightness (0-65535), Kelvin (2500-9000)]
# duration = transition time in seconds
# rapid = True/False. If True, don't wait for device response before proceeding, just send multiple packets and move on

set_power(power, [duration], [rapid])	
set_color(color, [duration], [rapid])									
get_power()								# returns 0 or 65535
get_color()								# returns color (HSBK list)
```


#### LIFX LAN Protocol:

The LIFX LAN protocol is officially documented [here](https://github.com/LIFX/lifx-protocol-docs). In lifxlan, you can see the underlying stream of packets being sent and received at any time by initializing the LifxLAN object with the verbose flag set: `lifx = LifxLAN(verbose = True)`. (Ssee `examples/verbose_lan.py`.)

The files that deal with LIFX packet construction and representation are:

* **message.py** -  Defines the message fields and the basic packet structure.
* **msgtypes.py** - Provides subclasses for each LIFX message type, along with their payload constructors.
* **unpack.py** - Creates a LIFX message object from a string of binary data (crucial for receiving messages).

Happy hacking!