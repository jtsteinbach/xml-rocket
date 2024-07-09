    ________        *
  *  \ v1.3 \-\-------*[=]=------_______
** *##[=]>   ) )    XML ROCKET   ))     )--
   * /      /-/------**[=]=------‾‾‾‾‾‾‾
    ‾‾‾‾‾‾‾‾     * *

Created By: https://jts.codes/


XML Rocket is a tool that sends XML files via TCP packets
to a target IP address. You can also spoof the sender IP
and MAC address, with the option to randomly generate the
port and/or MAC address.

You can also test if a host accepts XML data, before sending a payload.



!!! INSTALL requirements.txt BEFORE USING 
 
1. Extract xml_rocket-1.3.zip
2. Open Terminal/CMD Prompt in "xml_rocket" directory
3. Enter "pip install -r requirements.txt" into command line



COMMANDS:

    [TARGET IP] [PORT] -n
    [TARGET IP] [PORT] -d [DISGUISE IP] [PORT] [MAC ADDR]
    [TARGET IP] [PORT] -test [DISGUISE IP] [PORT] [MAC ADDR]

    -rp as [PORT] generates random port
    -rm as [MAC ADDR] generates random mac addr

 ex: 51.52.53.54 80 -d 10.0.2.10 80 -rm
