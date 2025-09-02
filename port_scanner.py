import socket
import termcolor
import threading
import time
from datetime import datetime

# Global variables for managing the thread

open_ports = []  # stores the port which ae open
closed_ports = []  # stores the port whichh are closed
threads = []  # keeps tracks of all threds
max_threads = 50  # Limit concurrent threads
scan_start_time = None  # remembers the starting time


def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(5)  # Add timeout to prevent hanging
        result = sock.connect_ex(
            (ipaddress, port)
        )  # connect_ex returns 0 if it is successful and error numbers if it fails

        if result == 0:
            try:
                service = socket.getservbyport(
                    port, "tcp"
                )  # tries to identify what service is runnijng
            except:
                service = "unknown"
            with threading.Lock():  # Prevent race condition like modifying same list at same time
                open_ports.append((port, service))
        else:
            with threading.Lock():
                closed_ports.append(port)
        sock.close()
    except Exception:
        with threading.Lock():
            closed_ports.append(port)


def scan(target, ports):
    print(
        termcolor.colored(
            f"\nStarting scan for {target} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "green",
        )
    )

    global scan_start_time  # specifying that we r trying to use the global one
    scan_start_time = time.time()  # gets the current time from the computer

    for port in range(1, ports + 1):
        # Wait if we have too many active threads
        while (
            threading.active_count() > max_threads
        ):  # threading.active_count() counts how many scanning processes are currently running
            time.sleep(0.01)

        # Create and start a new thread for each port
        thread = threading.Thread(target=scan_port, args=(target, port))
        thread.daemon = True  # safety feature to stop the runing threads if the main program stops or scanner stops
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()  # tells thta  to wait for all the threads to finish before continuing

    display_results(target, ports)


def display_results(target, ports):
    scan_duration = (
        time.time() - scan_start_time
    )  # current time with the  time when it started

    print(termcolor.colored(f"\nScan results for {target}:", "blue", attrs=["bold"]))
    print(termcolor.colored("=" * 50, "blue"))

    if open_ports:
        print(
            termcolor.colored(
                f"Found {len(open_ports)} open " "ports out of {ports} scanned:",
                "green",
            )
        )
        for port, service in sorted(open_ports):
            print(
                termcolor.colored(
                    f"[+] Port {port} is open - Service: {service}", "green"
                )
            )
    else:
        print(termcolor.colored("No open ports found.", "red"))

    print(
        termcolor.colored(
            f"\nScan completed in {scan_duration:.2f} seconds", "yellow"
        )  #:-signal to follow instruction, .2- decimal after 2 digit,f-means fixed point notaion (decimal number)
    )  #:-signal to follow instruction, .2- decimal after 2 digit,f-means fixed point notaion (decimal number)

    print(termcolor.colored("=" * 50, "blue"))


def banner():
    print(
        termcolor.colored(
            r"""
        ____             _    ____                                  
        |  _ \ ___  _ __ | |_ / ___|  ___ __ _ _ __  _ __   ___ _ __ 
        | |_) / _ \|  __\| __|\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
        |  __/ (_) | |   | |_  ___) | (_| (_| | | | | | | |  __/ |   
        |_|   \___/|_|    \__||____/ \___\__,_|_| |_|_| |_|\___|_|   
        """,
            "cyan",
        )
    )
    print(termcolor.colored("            Python Port Scanner by Md Mohsin", "magenta"))
    print(termcolor.colored("=" * 55, "cyan"))


# Main execution
# if __name__ == "__main__":
def run_port_scanner():

    banner()

    targets = input(
        termcolor.colored(
            "\n[*] Enter IP address(es) to"
            " scan (separate multiple targets with ','): ",
            "yellow",
        )
    )

    ports = int(
        input(
            termcolor.colored(
                "[*] Enter how many ports to scan (e.g., 1000): ", "yellow"
            )
        )
    )

    if "," in targets:
        print(termcolor.colored("\n Scanning Multiple Targets", "red", attrs=["bold"]))
        for ip in targets.split(","):
            # Reset results for each target
            open_ports.clear()
            closed_ports.clear()
            threads.clear()

            scan(ip.strip(), ports)
    else:
        scan(targets, ports)
