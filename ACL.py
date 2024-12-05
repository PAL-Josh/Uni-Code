from netmiko import ConnectHandler

# Device details
device = {
    'device_type': 'cisco_ios',  # Update based on device type
    'ip': '192.168.1.1',         # Replace with actual IP
    'username': 'admin',
    'password': 'password123',
}

# ACL command
acl_main_commands = [
    'ip access-list extended ', # try and get this working
    'permit tcp any any eq 80',
    'permit tcp any any eq 443',
    'deny ip any any',
]

# IPsec Commands
ipsec_commands = [
    'crypto isakmp policy 10',
    'encryption aes 256',
    'hash sha',
    'authentication pre-share',
    'group 2',
    'crypto isakmp key MY_SECRET_KEY address 0.0.0.0',
    'crypto ipsec transform-set TRANS_SET_NAME esp-aes 256 esp-sha-hmac',
    'crypto map MAP_NAME 10 ipsec-isakmp',
    'set peer 192.168.1.2',
    'set transform-set TRANS_SET_NAME',
    'match address ACL_NAME',
]

# Connect and configure
try:
    connection = ConnectHandler(**device)
    
    # Configure ACL
    acl_output = connection.send_config_set(acl_main_commands)
    print("ACL Configuration Output:\n", acl_output)
    
    # Configure IPsec
    ipsec_output = connection.send_config_set(ipsec_commands)
    print("IPsec Configuration Output:\n", ipsec_output)
    
    connection.disconnect()
except Exception as e:
    print(f"An error occurred: {e}")