import pexpect
from netmiko import ConnectHandler
import sys


# ------------ MENU FUNCTION ------------
def main_menu():
    """Main menu for interactive selection."""
    while True:
        print("\n=== Menu ===")
        print("1. Run SSH Task")
        print("2. Run Telnet Task")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            ip, username, password = SSH_Config()  # Capture credentials from SSH task
            save_running_config(ip, username, password, "running_config_ssh.txt")  # Save config
        elif choice == '2':
            ip, username, password = Telnet_Config()  # Capture credentials from Telnet task
            save_running_config(ip, username, password, "running_config_telnet.txt")  # Save config
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.") 

# ------------ SSH FUNCTION ------------
def SSH_Config():
    """SSH configuration logic."""
    ip_address = '192.168.56.101'
    username = 'prne'
    password = 'cisco123!'
    password_enable = 'class123!'

    session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('--- FAILURE! creating session for:', ip_address)
        exit()

    session.sendline(password)
    result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

    if result != 0:
        print('--- FAILURE! entering password:', password)
        exit()

    session.sendline('enable')  # Entering enable mode
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    session.sendline(password_enable)  # Send enable password
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    session.sendline('configure terminal')  # Enter config mode
    result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    session.sendline('hostname R1')  # Change hostname to 'R1'
    result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    session.sendline('exit')  # Exit configuration mode
    session.sendline('exit')  # Close the session
    session.close()

    return ip_address, username, password  # Return credentials

# ------------ TELNET FUNCTION ------------
def Telnet_Config():
    """Telnet configuration logic."""
    ip_address = '192.168.56.101'
    username = 'cisco'
    password = 'cisco123!'

    session = pexpect.spawn(f'telnet {ip_address}', encoding='utf-8', timeout=20)
    result = session.expect(['Username:', pexpect.TIMEOUT])

    if result != 0:
        print('--- FAILURE! creating session for:', ip_address)
        exit()

    session.sendline(username)  # Enter username
    result = session.expect(['Password:', pexpect.TIMEOUT])

    session.sendline(password)  # Enter password
    result = session.expect(['#', pexpect.TIMEOUT])

    session.sendline('quit')  # Quit the session
    session.close()

    return ip_address, username, password  # Return credentials

# ------------ SAVE FUNCTION ------------
def save_running_config(ip_address, username, password, filename):
    """Save the running configuration of a device."""
    device = {
        'device_type': 'cisco_ios',  # Define the type of device
        'host': ip_address,
        'username': username,
        'password': password,
    }

    connection = ConnectHandler(**device)  # Establish SSH connection
    running_config = connection.send_command('show running-config')  # Get config

    with open(filename, 'w') as config_file:
        config_file.write(running_config)  # Save config to file

    connection.disconnect()  # Close the connection

if __name__ == "__main__":
    main_menu()
