import pexpect
from netmiko import ConnectHandler

# Define variables
ip_address = '192.168.56.101'
username = 'prne'
password = 'cisco123!'
password_enable = 'class123!'

# Create the SSH session
session = pexpect.spawn('ssh ' + username + '@' + ip_address,
 encoding='utf-8', timeout=20)
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if exists then display error and exit
if result != 0:
 print('--- FAILURE! creating session for: ', ip_address)
 exit()

# Session expecting password, enter details
session.sendline(password)
result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
 print('--- FAILURE! entering password: ', password)
 exit()

 # Enter enable mode
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
 print('--- Failure! entering enable mode')
 exit()
# Send enable password details
session.sendline(password_enable)
result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
 print('--- Failure! entering enable mode after sending password')
 exit()

 # Enter configuration mode
session.sendline('configure terminal')
result = session.expect([r'.\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
 print('--- Failure! entering config mode')
 exit()

# Change the hostname to R1
session.sendline('hostname R1')
result = session.expect([r'R1\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
# Check for error, if exists then display error and exit
if result != 0:
 print('--- Failure! setting hostname')

# Exit config mode
session.sendline('exit')
# Exit enable mode
session.sendline('exit')



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

# Terminate SSH session
session.close()

