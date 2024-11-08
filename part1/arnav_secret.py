## we want to find out the secrets in file 1
## we can make use of the same code from part a but instead here search for some key words like password, secret , token
import dpkt
import socket
from datetime import datetime

def pcap_detective(pcap_file):
    secrets = []
    f = open(pcap_file,'rb')
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
       # print("test1")
        if isinstance(ip,dpkt.ip6.IP6):
            #print("test2")
            #print("we get tcp")
            if isinstance(ip.data,dpkt.tcp.TCP) and isinstance(eth.data, dpkt.ip6.IP6):
                tcp = ip.data
                if(tcp.dport==80 or tcp.sport==80):
                    try:
                        #print("we are in the tcp try block")
                        http = dpkt.http.Request(tcp.data)
                        if'secret' in http.headers:
                         my_secret = http.headers['secret']
                         secrets.append(my_secret)
                         #print(f"secret: {my_secret}")
                    except(dpkt.dpkt.NeedData,dpkt.dpkt.UnpackError):
                        continue
    
    return secrets

## now we wnat to compare file 2 and file 3 and find the difference 
def difference_finder(pcap_file_1,pcap_file_2):
    f = open(pcap_file_1,'rb')
    k = open(pcap_file_2,'rb')
    list1 = []
    list2 = []
    pcap1 = dpkt.pcap.Reader(f)
    pcap2 = dpkt.pcap.Reader(k)

    for ts1, buf1 in pcap1:
        eth1 = dpkt.ethernet.Ethernet(buf1)
        ip1 = eth1.data
        # print("test1")
        if isinstance(ip1,dpkt.ip.IP):
            if isinstance(ip1.data,dpkt.icmp.ICMP): # use icmp not tcp
                # dpkt example @ https://dpkt.readthedocs.io/en/latest/print_icmp.html
                # learnt how to use 
                # print("test 2")
                icmp1 = ip1.data
                #print(socket.inet_ntoa(ip1.src))
                addy1 = socket.inet_ntoa(ip1.src)
                list1.append(addy1)
                #print(not_frag,more_frag,frag_offset)
    
    for ts2, buf2 in pcap2:
        eth2 = dpkt.ethernet.Ethernet(buf2)
        ip2 = eth2.data
        # print("test1")
        if isinstance(ip1,dpkt.ip.IP):
            if isinstance(ip1.data,dpkt.icmp.ICMP): # use icmp not tcp
                # dpkt example @ https://dpkt.readthedocs.io/en/latest/print_icmp.html
                # learnt how to use 
                # print("test 2")
                icmp2 = ip2.data
                #print(socket.inet_ntoa(ip1.src))
                addy2 = socket.inet_ntoa(ip2.src)
                list2.append(addy2)
                #print(not_frag,more_frag,frag_offset)
    
    return list1,list2

# def differencefinder_mylists(list1,list2):
#     final_list = []
#     for i in range(len(list1)):
#         for j in range(len(list2)):
#             if(list1[i]!=list2[j]):
#                 #print(f"The different sources are as follows file1 is {list1[i]} and for file2 is {list2[j]}")
#                 final_list.append(list1[i])
#                 final_list.append(list2[j])
#                 # print(f"Difference number {i} \n")
#                 # print(final_list)
#     return final_list
                


# what exactly is the difference we are looking for my manually searching the wire shark files i was able to see that the ip addresses are different
    

if __name__ == "__main__":
    # bond_007 = pcap_detective(r"C:\Users\arnav\Desktop\EEC173\ass1_1.pcap")
    # print("The secret is ",bond_007)

    comp = difference_finder(r"C:\Users\arnav\Desktop\EEC173\ass1_2.pcap",r"C:\Users\arnav\Desktop\EEC173\ass1_3.pcap")
    print(f"The Ip addreses for file 2 \n are {comp[0]}")
    print("\n")
    print(f"The Ip addreses for file 3 \n are {comp[1]}")
    print(" \n We can clearly spot the difference all the addresses are different")
    print()
    # print("/n the highlighted difference")
    # comp2 = differencefinder_mylists(comp[0],comp[1])
    # print(f"The different values are {comp2}")
    

