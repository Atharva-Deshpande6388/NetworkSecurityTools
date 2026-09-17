#Project 1: IP address validator & subnet calculator

def ip_validator(formatip):

    if (len(formatip) == 4):
        for x in formatip:
            if not x.isdigit():
                print("Incorrect IP format (CONTAIN ALPHABETS INSTEAD OF NUMBERS)")
                return False

        for i in range(0,4):
            if not (0 <= int(formatip[i]) <= 255) :
                print("invalid ip format", formatip, " --> ", formatip[i])
                break
                
        else:
            return True
    else:
        print("incorrect ip address")


def subnet_validator(formatsub):
    if(len(formatsub) != 4):
        print("Incorrect subnet format")
        return False
    
    for x in formatsub:
        if not x.isdigit():
            print("Incorrect subnet format (CONTAIN ALPHABETS INSTEAD OF NUMBERS)")
            return False

    subnet_values = [int(x) for x in formatsub]
    validsub = [255,254,252,248,240,224,192,128,0]
    ended = False

    for value in subnet_values:
        if value not in validsub:
            print("incorrect subnet", formatsub, " --> ", value)
            return False
        if ended and (value != 0):
            print("incorrect subnet", formatsub, " --> ", value)
            return False
        if value != 255:
            ended = True
    return True



ipaddr = input("Enter IP address : ")
subnet = input("Enter subnet(format: 255.255.255.255) : ")

formatip = ipaddr.split(".")
print(formatip)

formatsub = subnet.split(".")
print(formatsub)


ip = False
sub = False
ip = ip_validator(formatip)
sub = subnet_validator(formatsub)   



if (ip == True) and (sub == True):
    print("Valid IP and Subnet")
    if (formatsub == ['255', '255', '255', '255']):
        print("No usable host range.")
    else:
        network_addr, broadcast_addr = [], []
        for b in range(4):
            ip_part = int(formatip[b])
            mask_part = int(formatsub[b])
            netpart = ip_part & mask_part
            network_addr.append(str(netpart))
            broad_part = netpart + (255-mask_part)
            broadcast_addr.append(str(broad_part))
        str_network = ".".join(network_addr)
        str_broadcast = ".".join(broadcast_addr)
        print("Network Address:   ", str_network)
        print("Broadcast Address: ", str_broadcast)
        first_host = network_addr[0:3] + [str(int(network_addr[3])+1)]
        last_host = broadcast_addr[0:3] + [str(int(broadcast_addr[3])-1)]
        print("First Usable Host:", ".".join(first_host))
        print("Last Usable Host:", ".".join(last_host))
else:
    print("Invalid IP or Subnet")