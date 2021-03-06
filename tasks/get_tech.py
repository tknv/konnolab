import os
import sys
import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

an_ap = {
    'device_type': 'extreme_wing_ssh',
    'ip': sys.argv[1],
    'port': sys.argv[2],
    'username': sys.argv[3],
    'password': sys.argv[4],
}
tftp_host = sys.argv[5]
timestamp = sys.argv[6]

try:
    net_connect = netmiko.ConnectHandler(an_ap)
except netmiko.NetMikoAuthenticationException:
    print("Authentication failed when connecting to %s. Proceeding next" % an_ap['ip'])
except netmiko.NetMikoTimeoutException:
    print("Attempting connection time out to %s. Proceeding next" % an_ap['ip'])
else:
    net_connect.enable()
    find_hostname = net_connect.find_prompt()
    hostname = find_hostname.replace("#","") # expected does not change prompt setting
    cmd = 'service copy techsupport tftp://{}/{}-{}.tgz'.format(tftp_host, hostname, timestamp)
    print('Get techsupport by:{}'.format(cmd))
    output = net_connect.send_command(cmd)
    print(output)