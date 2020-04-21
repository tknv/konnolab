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

try:
    net_connect = netmiko.ConnectHandler(**an_ap)
except netmiko.NetMikoAuthenticationException:
    print("Authentication failed when connecting to %s. Proceeding next" % an_ap['ip'])
except netmiko.NetMikoTimeoutException:
    print("Attempting connection time out to %s. Proceeding next" % an_ap['ip'])
else:
    net_connect.enable()
    output = net_connect.send_command('show version')
    print(output)
    cmds = ['self', 'logging on', 'logging console debugging', 'commit write memory']
    # net_connect.send_command_expect(cmds)
    for cmd in cmds:
        print(cmd)
        net_connect.send_command(cmd, expect_string="#")