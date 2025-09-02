import termcolor
from port_scanner import run_port_scanner
from email_scraper import run_email_scraper


def main():
    while True:
        print(
            termcolor.colored("\n=== CyberSecurity Toolkit ===", "cyan", attrs=["bold"])
        )
        print("1. Port Scanner")
        print("2. Email & URL Scraper")
        print("3. Exit")

        choice = input(termcolor.colored("\nChoose an option: ", "yellow"))

        if choice == "1":
            run_port_scanner()
            input(
                termcolor.colored("\nPress Enter to return to main menu...", "yellow")
            )

        elif choice == "2":
            run_email_scraper()
            input(
                termcolor.colored("\nPress Enter to return to main menu...", "yellow")
            )

        elif choice == "3":
            print(termcolor.colored("Exiting Toolkit. Goodbye!", "red"))
            break

        else:
            print(termcolor.colored("Invalid choice, try again!", "red"))


if __name__ == "__main__":
    main()
