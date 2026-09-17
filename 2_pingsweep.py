import subprocess
import datetime

# result = subprocess.run(["ping", "-n", "3", "-w" , "10000" ,"8.8.8.8"])

def write(x):
    with open("project2_res/ip_out.txt", "a") as file:
        file.write(f"\n{x}")

def diagnose(ping_result):
    if ping_result.returncode == 0:
        return "Success"
    elif "could not find host" in ping_result.stdout or "Ping request could not find host" in ping_result.stdout:
        return "DNS resolution failed"
    elif "Destination host unreachable" in ping_result.stdout:
        return "Unreachable (router refused)"
    elif "Request timed out" in ping_result.stdout:
        return "Timeout"
    else:
        return "Failed (unknown reason)"





secs = input("Enter Timeout(in seconds) : ")
time = int(secs) * 1000

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("project2_res/ip_out.txt", "a") as file:
    file.write(f"\n\n--- New Scan: {current_time} ---")

with open("project2_res/ip_list.txt", "r") as file:
        for line in file:
            ip = line.strip()
            if ip:
                print(f"\n=== Pinging : {ip} ===\n")
                result = subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(ip ," :: Success", result.returncode)
                    write(f"{ip} :: Success")
                    # write(f"{ip} :: Success {result.returncode}")
                    # print(result.stdout)
                
                elif "Request timed out" in result.stdout:
                    print(f"{ip} :: Timeout")
                    deep_result = subprocess.run(["ping", "-n", "4", ip, "-w", str(time)], capture_output=True, text=True, timeout=40)
                    if deep_result.returncode == 0:
                        print(f"{ip} :: deep scan success")
                        write(f"{ip} :: Success (deep scan)")
                    else:
                        status = diagnose(deep_result)
                        print(f"{ip} :: {status}")
                        write(f"{ip} :: {status}")
                
                else:
                    status2 = diagnose(result)
                    print(f"{ip} :: {status2}")
                    write(f"{ip} :: {status2}")

            else:
                continue