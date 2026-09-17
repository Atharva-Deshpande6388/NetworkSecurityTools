import socket
import os
import time
import errno
import datetime


os.makedirs("project3_res", exist_ok=True)
def read_ports(p):
    ports = []
    with open(p, "r") as file:
        for line in file:
            cleaned = line.strip()
            if cleaned.isdigit():
                ports.append(int(cleaned))
            elif cleaned:
                print(f"skipping individual port entry: {cleaned}")
    return ports


def write(x):
    with open("project3_res/scan_results.txt", "a") as file:
        file.write(f"{x}\n")


def list_scan(a):
    start_time = time.time()

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    open_ports = []
    closed_ports = []
    write(
        f"\n\n--- New Scan: {current_time} ---\n"
        f"Scan Type: List Scan\n"
        f"Target: {ip}\n\n"
    )
    for port in a:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            result = sock.connect_ex((ip, port))
            error_name = errno.errorcode.get(result)
            if result == 0:
                print(port, "--> OPEN")
                # print(port, " --> ", result)
                write(f"{port} --> OPEN")
                open_ports.append(port)
            else:
                print(port, "--> closed/filtered(OS):",result, error_name, os.strerror(result)) #debug
                write(f"{port} --> CLOSED/FILTERED, WSAcode: {result}, {error_name}")
                closed_ports.append(port)
                # print(port, "--> closed/filtered:", result, error_name)
        # sock.close()
    end_time = time.time()
    total_time_taken = end_time - start_time
    print(f"Time taken: {total_time_taken:.4f} seconds")
    write(f"\nOPEN PORTS: {open_ports} : {len(open_ports)}\nCLOSED PORTS: {closed_ports} : {len(closed_ports)}\n\nTime taken: {total_time_taken:.4f} seconds\n")

def range_scan(x, y):
    start_time = time.time()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    open_ports = []
    closed_ports = []
    
    write(
        f"\n\n--- New Scan: {current_time} ---\n"
        f"Scan Type: Ranged Scan\n"
        f"Target: {ip}\n\n"
    )

    for i in range(x,y):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((ip, i))
            error_name = errno.errorcode.get(result)
            if result == 0:
                print(i, "--> OPEN")
                write(f"{i} --> OPEN")
                # print(port, " --> ", result)
                open_ports.append(i)
            else:
                print(i, "--> closed/filtered(OS):", result, error_name, os.strerror(result)) #debug
                write(f"{i} --> CLOSED/FILTERED, WSAcode: {result}, {error_name}")
                closed_ports.append(i)
                # print(i, "--> closed/filtered:", result, error_name)
    end_time = time.time()
    total_time_taken = end_time - start_time
    print(open_ports)
    print(f"Time taken: {total_time_taken:.4f} seconds")
    write(f"\nOPEN PORTS: {open_ports} : {len(open_ports)}\nCLOSED PORTS: {closed_ports} : {len(closed_ports)}\n\nTime taken: {total_time_taken:.4f} seconds\n")



ip = input("Enter url : ")
choice = input("1. List Scan,\n2. Range Scan\nYour Choice(1/2): ")

try:
    if choice == "1":
        path = input("Enter path: ")
        ports = read_ports(path)
        list_scan(ports)
    elif choice == "2":
        Rs = input("Start: ")
        Re = input("End : ")
        print(f"Scanning port from {Rs} to {Re}")
        range_scan(int(Rs),int(Re))
    else:
        print("Invalid value...")

except socket.gaierror as e:
    print("DNS resolution failed", e)