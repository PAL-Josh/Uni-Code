import pexpect
from netmiko import ConnectHandler

# Define variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'

# Create telnet session
session = pexpect.spawn('telnet ' + ip_address, encoding='utf-8',timeout=20)
result = session.expect(['Username:', pexpect.TIMEOUT]) 

# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! creating session for: ', ip_address)
    exit() 

# Session is expecting username, enter details
session.sendline(username)
result = session.expect(['Password:', pexpect.TIMEOUT])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering username: ', username)
    exit()
# Session is expecting password, enter details
session.sendline(password)
result = session.expect(['#', pexpect.TIMEOUT])
# Check for error, if exists then display error and exit
if result != 0:
    print('--- FAILURE! entering password: ', password)
    exit()

def save_running_config(ip, username, password, filename):
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
    }

    # Establish SSH connection
    connection = ConnectHandler(**device)
    
    # Get running configuration
    running_config = connection.send_command('show running-config')
    
    # Save the configuration to a local file
    with open(filename, 'w') as config_file:
        config_file.write(running_config)
    
    # Close the connection
    connection.disconnect()

filename = "running_config.txt"

save_running_config(ip_address, username, password, filename)

# Terminate telnet to device and close session
session.sendline('quit')
session.close()
