# XML Rocket | Version 1.3 | Created By: jts.codes/
import socket
import random
import logging
import netifaces
import subprocess
import sys
from scapy.all import *
from colorama import Fore
from tkinter import Tk, filedialog


def send_spoofed_http_post(dest_ip, dest_port, source_ip, source_mac, source_port, xml_data):
        print(Fore.LIGHTBLACK_EX + "\nNOTE: Spamming requests may result in SYN packets being instantly dropped!")
        ether = Ether(src=source_mac, dst='ff:ff:ff:ff:ff:ff')
        ip = IP(src=source_ip, dst=dest_ip)
        tcp_syn = TCP(sport=source_port, dport=dest_port, flags='S', seq=random.randint(1000, 9000))
        syn_ack = srp1(ether / ip / tcp_syn, timeout=2, verbose=0)
        if syn_ack and TCP in syn_ack and syn_ack[TCP].flags == 'SA':
                ack = TCP(sport=source_port, dport=dest_port, flags='A', seq=tcp_syn.seq + 1, ack=syn_ack.seq + 1)
                sendp(ether / ip / ack, verbose=0)
                http_request = f"POST / HTTP/1.1\r\nHost: {dest_ip}\r\nContent-Type: application/xml\r\nContent-Length: {len(xml_data)}\r\n\r\n{xml_data}"
                psh_ack = TCP(sport=source_port, dport=dest_port, flags='PA', seq=tcp_syn.seq + 1, ack=syn_ack.seq + 1)
                raw = Raw(load=http_request)
                sendp(ether / ip / psh_ack / raw, verbose=0)
                print(Fore.LIGHTCYAN_EX + f"\nSpoofed HTTP POST request sent successfully.\nHost: {dest_ip}:{dest_port} accepts XML data from {source_ip}:{source_port}/{source_mac}!\n")
                if xml_data != "":
                        print(Fore.LIGHTBLACK_EX + f"XML File Data:\n\n{xml_data}")
        else:
                print(Fore.LIGHTRED_EX + f"\nFailed to complete TCP handshake.\nHost: {dest_ip}:{dest_port} does NOT accept XML data from {source_ip}:{source_port}/{source_mac}!\n")


def disguise_packet_send(dest_ip, dest_port, source_ip, source_port, source_mac):
        try:
                Tk().withdraw()
                file_path = filedialog.askopenfilename(title="Select an XML file", filetypes=[("XML files", "*.xml")])
                with open(file_path, 'r') as file:
                        xml_data = file.read()
                send_spoofed_http_post(dest_ip, dest_port, source_ip, source_mac, source_port, xml_data)
                core()
        except Exception as e:
                input("{r}[!] ERROR SENDING DISGUISED PACKET [!]\n   {lg}{e}\n\nPress ENTER to continue...".format(
                        r=Fore.LIGHTRED_EX, lg=Fore.WHITE, e=e))


def normal_packet_send(dest_ip, dest_port, source_ip, source_mac):
        try:
                source_port = dest_port
                Tk().withdraw()
                file_path = filedialog.askopenfilename(title="Select an XML file", filetypes=[("XML files", "*.xml")])
                with open(file_path, 'r') as file:
                        xml_data = file.read()
                send_spoofed_http_post(dest_ip, dest_port, source_ip, source_mac, source_port, xml_data)
                core()
        except Exception as e:
                input("{r}[!] ERROR SENDING PACKET [!]\n   {lg}{e}\n\nPress ENTER to continue...".format(
                        r=Fore.LIGHTRED_EX, lg=Fore.WHITE, e=e))


def get_default_ip():
        gateways = netifaces.gateways()
        default_gateway = gateways.get('default', {})
        interface = default_gateway.get(netifaces.AF_INET, [None])[1]
        if interface:
                addresses = netifaces.ifaddresses(interface)
                ip_info = addresses.get(netifaces.AF_INET, [{}])[0]
                return ip_info.get('addr', '127.0.0.1')
        return '127.0.0.1'


def get_mac_address():
        gateways = netifaces.gateways()
        default_gateway = gateways.get('default', {})
        interface = default_gateway.get(netifaces.AF_INET, [None])[1]
        if interface:
                addresses = netifaces.ifaddresses(interface)
                mac_info = addresses.get(netifaces.AF_LINK, [{}])[0]
                return mac_info.get('addr', '00:00:00:00:00:00')
        return '00:00:00:00:00:00'


def generate_random_mac():
        try:
                mac = [random.randint(0x00, 0xFF) for _ in range(6)]
                random_mac = ':'.join(f'{byte:02x}' for byte in mac)
                return random_mac
        except Exception as e:
                input("{r}[!] ERROR GENERATING MAC ADDRESS [!]\n   {lg}{e}\n\nPress ENTER to continue...".format(
                        r=Fore.LIGHTRED_EX, lg=Fore.WHITE, e=e))


def core():
        try:
                target = input("{r}Target: {w}".format(w=Fore.LIGHTWHITE_EX, r=Fore.LIGHTRED_EX))
                args = target.split()
                if args[2] == "-d":
                        dest_ip = str(args[0])
                        dest_port = int(args[1])
                        source_ip = str(args[3])
                        if args[4] == "-rp":
                                source_port = random.randint(1024, 65535)
                        else:
                                source_port = int(args[4])
                        if args[5] == "-rm":
                                source_mac = generate_random_mac()
                        else:
                                source_mac = args[5]
                        disguise_packet_send(dest_ip, dest_port, source_ip, source_port, source_mac)
                if args[2] == "-n":
                        dest_ip = str(args[0])
                        dest_port = int(args[1])
                        source_ip = get_default_ip()
                        source_mac = get_mac_address()
                        normal_packet_send(dest_ip, dest_port, source_ip, source_mac)
                if args[2] == "-test":
                        dest_ip = str(args[0])
                        dest_port = int(args[1])
                        source_ip = str(args[3])
                        if args[4] == "-rp":
                                source_port = random.randint(1024, 65535)
                        else:
                                source_port = int(args[4])
                        if args[5] == "-rm":
                                source_mac = generate_random_mac()
                        else:
                                source_mac = args[5]
                        send_spoofed_http_post(dest_ip, dest_port, source_ip, source_mac, source_port, xml_data="")
                        core()
        except KeyboardInterrupt:
                return core()
        except Exception as e:
                input("{r}[!] ERROR RUNNING COMMAND [!]\n   {lg}{e}\n\nPress ENTER to continue...".format(
                        r=Fore.LIGHTRED_EX, lg=Fore.WHITE, e=e))


print("\033[2J\033[H", end="", flush=True)
print("""

    {r}________        {y}*
  {y}*  {r}\\ {w}v1.3{r} \\-\\{w}-------{y}*{g}[=]{r}=------_______
{y}** *#{ly}#{g}[=]{r}>   ) )    {w}XML ROCKET{r}   ))     {r})--
   {y}* {r}/      /-/{w}------{y}**{g}[=]{r}=------‾‾‾‾‾‾‾
    {r}‾‾‾‾‾‾‾‾     {y}* *
  {lg}                               Creator: https://jts.codes/
{g}USAGE:

    {g}[TARGET IP] [PORT] -n
    [TARGET IP] [PORT] -d [DISGUISE IP] [PORT] [MAC ADDR]
    [TARGET IP] [PORT] -test [DISGUISE IP] [PORT] [MAC ADDR]

    -rp as [PORT] generates random port
    -rm as [MAC ADDR] generates random mac addr

 ex: 51.52.53.54 80 -d 10.0.2.10 80 -rm
	""".format(g=Fore.LIGHTBLACK_EX, r=Fore.LIGHTRED_EX, w=Fore.LIGHTWHITE_EX, lg=Fore.WHITE, y=Fore.YELLOW,
                   ly=Fore.LIGHTYELLOW_EX))

core()

