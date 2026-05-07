import socket
import sys
import os
import urllib.request
import json
import errno
#это пизда или нармалды?
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return 'open'
        elif result == errno.ECONNREFUSED:
            return 'closed'
        else:
            return 'filtered'
    except Exception:
        return 'filtered'

def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,lat,lon,query"
        req = urllib.request.urlopen(url, timeout=5)
        data = json.loads(req.read().decode())
        if data.get('status') == 'success':
            return {
                'ip': data.get('query', ip),
                'country': data.get('country', 'Unknown'),
                'region': data.get('regionName', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown'),
                'lat': data.get('lat', 0),
                'lon': data.get('lon', 0)
            }
        else:
            return None
    except Exception:
        return None

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

def show_banner():
    print(r"""
 _____     ___  ___  ___  ______ 
|_   _|    |  \/  | / _ \ | ___ \
  | |______| .  . |/ /_\ \| |_/ /
  | |______| |\/| ||  _  ||  __/ 
  | |      | |  | || | | || |    
  \_/      \_|  |_/\_| |_/\_|    
""")
    print("Channel: @MetallPunk\n")

def wait_for_menu():
    print("\n[0] - Main menu")
    input()

def main():
    while True:
        clear_screen()
        show_banner()
        print("[1] Scan basic ports")
        print("[2] Scan custom port")
        print("[3] Information about IP")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            ip = input("Enter IP address: ").strip()
            if not is_valid_ip(ip):
                continue
#я педик
            ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,5555,5900,6379,8080,8443]
            print(f"\nScanning {ip}...\n")

            for port in ports:
                status = scan_port(ip, port)
                if status == 'open':
                    print(f"{port}/tcp {GREEN}open{RESET}")
                elif status == 'closed':
                    print(f"{port}/tcp {RED}closed{RESET}")
                else:
                    print(f"{port}/tcp {YELLOW}filtered{RESET}")

            wait_for_menu()

        elif choice == "2":
            ip = input("Enter IP address: ").strip()
            if not is_valid_ip(ip):
                continue

            port_input = input("Enter port: ").strip()
            if not port_input.isdigit():
                continue

            port = int(port_input)
            if port < 1 or port > 65535:
                continue

            status = scan_port(ip, port)
            print(f"\nScanning {ip}:{port}...\n")

            if status == 'open':
                print(f"{port}/tcp {GREEN}open{RESET}")
            elif status == 'closed':
                print(f"{port}/tcp {RED}closed{RESET}")
            else:
                print(f"{port}/tcp {YELLOW}filtered{RESET}")

            wait_for_menu()

        elif choice == "3":
            ip = input("Enter IP address: ").strip()
            if not is_valid_ip(ip):
                continue

            print(f"\nGetting information for {ip}...\n")
            info = get_ip_info(ip)

            if info:
                print("IP INFORMATION\n")
                print(f"IP: {info['ip']}")
                print(f"Country: {info['country']}")
                print(f"Region: {info['region']}")
                print(f"City: {info['city']}")
                print(f"ISP: {info['isp']}")
                print(f"\nMap: https://maps.google.com/?q={info['lat']},{info['lon']}")
            else:
                print("Failed to get IP information")

            wait_for_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(0)
    except Exception:
        sys.exit(1)