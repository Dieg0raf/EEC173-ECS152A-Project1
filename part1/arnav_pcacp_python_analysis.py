#print ("hello world")
#````````````````````
#dpkt example 2
# #!/usr/bin/env python

# import dpkt

# f = open('test.pcap')
# pcap = dpkt.pcap.Reader(f)

# for ts, buf in pcap:
#  eth = dpkt.ethernet.Ethernet(buf)
#  ip = eth.data
#  tcp = ip.data

#  if tcp.dport == 80 and len(tcp.data) > 0:
#  http = dpkt.http.Request(tcp.data)
#  print http.uri

# f.close()
#`````````````````````````````````````````
# import dpkt
# # common ports from my example
# known_ports_protocol = {
#     80: 'HTTP',
#     443: 'QUIC',
#     5353: 'MDNS',
#     53: 'DNS',
#     # for now i will include the other protocols in the other category
# }

# #create a function to open our pcap file

# def pcap_reader(pcap_file):
#     protocol_count = {}

#     with open(pcap_file,'rb') as f:
#         pcap = dpkt.pcap.Reader(f)

#         for ts, buf in pcap:
#             eth = dpkt.ethernet.Ethernet(buf)
#             ip = eth.data
#             tcp = ip.data
#             # desitination and source ports
#             dst_port = ip.dport
#             src_port = ip.sport

#             protocol_common = known_ports_protocol.get(dst_port) or known_ports_protocol.get(src_port)

#             if protocol_common is None:
#                 protocol_common = 'Other'
            
#             protocol_count[protocol_common] = protocol_count.get(protocol_common,0)+1
    
#     return protocol_count
#            this is my code for part 1a where I want to find the number of protocols and what protocols are being used is it correct
##```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

import dpkt
import socket
from datetime import datetime
# common ports from my example
known_ports_protocol = {
    80: 'HTTP',
    443: 'QUIC',
    5353: 'MDNS',
    53: 'DNS',
    # for now i will include the other protocols in the other category
}

#create a function to open our pcap file
# chat GPT says my code is correct just I need to add the checks if ip.data is TCP or UDP
#adding those checks

def pcap_reader_protocol(pcap_file):
    protocol_count = {}

    with open(pcap_file,'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            protocol_common = 'Other'
            # this check is what my original code was missing since i was assuming it will always be tcp
            if isinstance(ip,dpkt.ip6.IP6):
                if isinstance(ip.data,dpkt.tcp.TCP):
                    tcp = ip.data
                    protocol_common = known_ports_protocol.get(tcp.dport) or known_ports_protocol.get(tcp.sport)
                if isinstance(ip.data,dpkt.udp.UDP):
                    udp = ip.data
                    protocol_common = known_ports_protocol.get(udp.dport) or known_ports_protocol.get(udp.sport)   
           
            protocol_count[protocol_common] = protocol_count.get(protocol_common,0)+1
    
    return protocol_count

def pcap_http_https(pcap_file):
    http_count = 0
    https_count = 0

    with open(pcap_file,'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data 
            if isinstance(ip,dpkt.ip6.IP6):
                if isinstance(ip.data,dpkt.tcp.TCP):
                    tcp = ip.data
                    if tcp.dport == 80 and len(tcp.data) > 0:
                        #http = dpkt.http.Request(tcp.data)
                        http_count +=1
                    elif tcp.dport == 443 and len(tcp.data) > 0: #assuming https is 443 port
                        #http = dpkt.http.Request(tcp.data)
                        https_count +=1
    
    print("Http count",http_count)
    print("Https count",https_count)
    
    return http_count + https_count

## creating a new function to get the ipaddress and how long it took
## for this part I asked chat gpt how to convert the ip address we get from wireshark to a human readble format
## chat gpt gave me the socket methot from the dpkt library

def ip_reader(pcap_file):
    ## array to store all the ips and their times
    dest_ip = []
    ip_time = []

    with open(pcap_file,'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        for ts,buf in pcap:

            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data 

            if isinstance(ip,dpkt.ip.IP):#was taking ip4 instead of ip6
                #socket idea from chatgpt
                dest_ip_curr = socket.inet_ntoa(ip.dst)
                ip_time_curr = datetime.fromtimestamp(ts)

                dest_ip.append(dest_ip_curr)
                ip_time.append(ip_time_curr)
    ## error here was that i needed to take fstring
    ## coming from c and cpp language i often miss such stuff
    for dest_ip_curr in dest_ip:
        print(f"Destination IP {dest_ip_curr}")
    for ip_time_curr in ip_time:
        print(f"Time taken {ip_time_curr}")
    
    return 0

## so to find out what browser we used we can extract it from the http information partuclarly user agent

def pcap_browser(pcap_file):
    # print("test we are being called")
    http_count = 0
    # https_count = 0

    with open(pcap_file,'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data 
            if isinstance(ip,dpkt.ip6.IP6):
                if isinstance(ip.data,dpkt.tcp.TCP):
                    tcp = ip.data
                    if (tcp.dport == 80 and len(tcp.data)>0):
                        #try block is from chat gpt
                        http_count +=1
                        # print("Http is working here")
                        try:
                            http = dpkt.http.Request(tcp.data)
                            browser = http.headers.get('user-agent','Unknown')
                            #print(f"Browser: {browser}")

                        except(dpkt.dpkt.NeedData,dpkt.dpkt.UnpackError):
                            print("We are not getting the packet")
                            continue
    
    return browser,http_count     


if __name__ == "__main__":
    result = pcap_reader_protocol(r"C:\Users\arnav\Documents\arnav_google_ping.pcap")
    print("Protocol Counts:", result)

    http_https_total = pcap_http_https(r"C:\Users\arnav\Documents\arnav_example.pcap")
    print("Total HTTP and HTTPS packets:", http_https_total)   

    result_date_time = ip_reader(r"C:\Users\arnav\Documents\arnav_example.pcap") 

    # to find the browser
    result_browser = pcap_browser(r"C:\Users\arnav\Documents\arnav_example.pcap")
    print("Browser type and number of times called: ",result_browser)

