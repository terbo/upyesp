# upyesp 0.2.5
simple scripts for small systems

This is a networking/cli developmental playground.

Recently a few ESP-07's showed up on my doorstep, and I figured
I'd try to integrate them into my continous Sigmon experiments.

Born were these scripts, which I aim to use to create a sort of
ad-hoc non-hemogenous sensor network with various functions, and
an integrated control facility.

# Install

Copy all the scripts to a blank ESP's /lib directory, excluding
the boot.py & main.py files. Edit default settings in the cfg.py
file. Boot and enjoy.

# What do

In the cfg.py file is defined the ESPConfig object, which is
instantiated in the main.py. These settings are saved by default
in /etc/esp.json, and define several startup conditions:

Wifi AP/STA/Monitor, Telnet/WebREPL, MQTT, UART dupterm,
GSM (Sim800L), LCD (i2c OLED). Todo: Leds (ws8211x), SD Card, GPS,
NTP Time

MQTT (not working) has a few commands enabled for remote queries
and commands. Still troubleshooting memory problems, even with
umqtt frozen in the firmware.

There are several convienence commands added to the REPL like ls, cat,
head, ifconfig, uptime, date, status, and pp (pretty print). Also
importable are wget, wifiscan, and geolocate (with free google apikey).

The OLED supports basic scrolling output, thats about it.
Also, the GSM support is preliminary while I work on a better
UART interface, and wait for another sim card.

Incorporated are ideas and some code from various sources, including
the original microtelnetserver, micropython upyphone, micropython forums,
and a few other sources.

Finally the beginnings of a promiscious sniffer are in mon.py, taken from
mzaklharo's fork of micropython. I've simplified the code in the callback
to send just the binary packet, and can process some fields on the esp
itself - but not all, and processing the same packet on pc yields variable
results. Maybe endianess, but thinking of adding pcap in someway. We'll see.


Have fun.
