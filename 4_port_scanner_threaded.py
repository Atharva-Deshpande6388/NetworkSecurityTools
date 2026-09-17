import socket
import os
import errno
from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import sys


def write(x):
    with open(file_path, "a") as file:
        file.write(f"{x}\n")

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        result = sock.connect_ex((ip, port))
        is_open = (result == 0)
        error_name = errno.errorcode.get(result)
        return(port, is_open, error_name, result)
try:
    try:
        ip = input("Enter IP address : ")
        start = int(input("Enter range for scanning ports\nFrom : "))
        end = int(input("To : "))
        choice = input("Do you want failed ports to be written in your Document?\n(y/n) : ")
        folder = input("Enter folder path : ")
        if not folder:
            raise ValueError("Folder path cannot be empty")
        file_path = os.path.join(folder, "port_results.txt")
        os.makedirs(folder, exist_ok=True)

        if choice not in ("y", "Y", "n", "N"):
            print("Invalid choice.")
            sys.exit()
            
    except ValueError as e:
        print("Invalid input: ",e)
        sys.exit()
    except OSError as e:
        print("Unable to create/access folder:", e)
        sys.exit()
    start_time = time.time()
    
    open_ports = []
    closed_ports = []

    with ThreadPoolExecutor(max_workers = 50) as executor:
        start_time = time.time()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = executor.map(check_port, range(start, end))
        write(
            f"\n\n--- New Scan: {current_time} ---\n"
            f"Range : {start} to {end}\n"
            f"Target: {ip}\n\n"
        )
        for port, is_open, error_name, result in results:
            print(port, is_open, error_name, result)
            if is_open:
                write(f"{port} -> OPEN : {result} \n")
                open_ports.append(port)
            else:
                if choice in ("y", "Y"):
                    write(
                        f"{port} -> CLOSED : "
                        f"ERROR NAME -> {error_name} : ERROR CODE {result}\n"
                    )

                closed_ports.append(port)
        end_time = time.time()
        total_time_taken = end_time - start_time
        print(f"Time taken: {total_time_taken:.4f} seconds")

    # ports = [10, 20, 22, 46, 80, 85]

    print("Open ports:", open_ports)
    write(f"Open ports: {open_ports}")
    print("Closed ports:", closed_ports)
    write(f"Closed ports: {closed_ports}")
    write(f"Time taken: {total_time_taken:.4f} seconds")

except socket.gaierror as e:
    end_time = time.time()
    total_time_taken = end_time - start_time
    print("DNS resolution failed", e)
    write(f"DNS resolution failed... {e} ...\nTime taken: {total_time_taken:.4f} seconds")
except KeyboardInterrupt as e:
    print("Scan interrupted by user ")
    write(f"Scan interrupted by user...\nTime taken: {total_time_taken:.4f} seconds")
except OSError as e:
    print("OS error occurred:", e)
    write(f"OS error occurred: {e}")