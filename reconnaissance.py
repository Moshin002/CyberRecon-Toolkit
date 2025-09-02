import subprocess
import socket


def domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def run_email_scraper(url):
    print("\n[+] Running Email Scraper...\n")
    # Pass the target URL to your scraper
    subprocess.run(["python", "email_scraper.py"], input=f"{url}\n".encode())


def run_port_scanner(ip, ports):
    print("\n[+] Running Port Scanner...\n")
    # Pass the IP and ports to your scanner
    user_input = f"{ip}\n{ports}\n"
    subprocess.run(["python", "port_scanner.py"], input=user_input.encode())


def main():
    print("=== ReconSuite: Combined Email + Port Recon Tool ===")

    target_url = input("[*] Enter target URL (e.g. https://example.com): ")
    target_domain = target_url.split("//")[-1].split("/")[0]

    # 1. Run Email Scraper
    run_email_scraper(target_url)

    # 2. Resolve Domain -> IP
    ip = domain_to_ip(target_domain)
    if not ip:
        print("[-] Could not resolve domain to IP. Skipping port scan.")
        return

    # 3. Run Port Scanner
    ports = int(input("[*] Enter how many ports to scan (e.g., 1000): "))
    run_port_scanner(ip, ports)


if __name__ == "__main__":
    main()
