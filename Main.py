import pexpect
from netmiko import ConnectHandler

# ------------ MENU FUNCTION ------------
def main_menu():
    
    while True:  # Infinite loop for the menu for a better experience
        print("\n=== Menu ===")
        print("1. Run SSH Task")
        print("2. Run Telnet Task")
        print("3. Exit")
        
        user_option = input("Enter your choice: ") # Takes the users input

        # Execute based on user's choice
        if user_option == '1':
            SSH_Config()  # Calls the SSH function
        elif user_option == '2':
            Telnet_Config()  # Calls the Telnet function
        elif user_option == '3':
            print("Exiting the program")
            exit()  # Exits the program
        else:
            print("Invalid choice. Please try again.")  # Will send the user back to the menu if there is an error
            main_menu()

# ------------ SSH FUNCTION ------------
def SSH_Config():
    
    # Device details and credentials
    ip_address = '192.168.56.101'
    username = 'prne'
    password = 'cisco123!'
    password_enable = 'class123!'

    # Spawn SSH session with pexpect 
    session = pexpect.spawn(f'ssh {username}@{ip_address}', encoding='utf-8', timeout=20)
    
    # Wait for password prompt or timeout
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    # Checks if there was an error in creating the session
    if result != 0:
        print('--- FAILURE! creating session for:', ip_address)
        exit()  # Exit if there is an error with the system

    # Send the login password
    session.sendline(password)
    
    result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

    # Checks if the password entry was successful
    if result != 0:
        print('--- FAILURE! entering password:', password)
        exit()  # Exit if there is an error

    # Enters enable mode
    session.sendline('enable')
    
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    # Send enable mode password
    session.sendline(password_enable)
    
    # Wait for privileged prompt
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

    # Enter configuration mode
    session.sendline('configure terminal')
    
    # Wait for configuration mode prompt
    result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    # Change the hostname of the device to 'R1'
    session.sendline('hostname R1')
    
    # Wait for confirmation of the hostname change
    result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])

    # Exit configuration mode and the SSH session
    session.sendline('exit')  # Exit configuration mode
    session.sendline('exit')  # Close the session
    session.close()

    print("Saving running configuration...")
    
    # Save the running configuration to a file
    Save_running_config(ip_address, username, password, "ssh_running_config.txt")

# ------------ TELNET FUNCTION ------------
def Telnet_Config():
    
    # Device details and credentials
    ip_address = '192.168.56.101'
    username = 'cisco'
    password = 'cisco123!'

    # Spawn Telnet session using pexpect to automate interactions
    session = pexpect.spawn(f'telnet {ip_address}', encoding='utf-8', timeout=20)
    
    # Wait for username prompt
    result = session.expect(['Username:', pexpect.TIMEOUT])

    # Check if there was an error in creating the session
    if result != 0:
        print('--- FAILURE! creating session for:', ip_address)
        exit()  # Exit if there's an error

    # Send the username
    session.sendline(username)
    
    # Wait for password prompt
    result = session.expect(['Password:', pexpect.TIMEOUT])

    # Send the password
    session.sendline(password)
    
    # Wait for the privileged prompt ('#')
    result = session.expect(['#', pexpect.TIMEOUT])

    # Exit the Telnet session
    session.sendline('quit')  # Quit Telnet session
    session.close()

    # Save the running configuration to a file
    Save_running_config(ip_address, username, password, "telnet_running_config.txt")

# ------------ SAVE FUNCTION ------------
def Save_running_config(ip_address, username, password, filename):
    
    # Gets device details
    device = {
        'device_type': 'cisco_ios', 
        'host': ip_address,
        'username': username,
        'password': password,
    }

    # Gets a SSH connection using netmiko
    connection = ConnectHandler(**device)
    
    # Gets the running configuration of the device
    running_config = connection.send_command('show running-config')

    # Save the configuration locally
    with open(filename, 'w') as config_file:
        config_file.write(running_config)

    # Close the SSH connection
    connection.disconnect()

if __name__ == "__main__":
    main_menu()