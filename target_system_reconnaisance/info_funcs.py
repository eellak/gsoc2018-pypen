"""

"""

import psutil
import nmap
import json


def get_procs():
    """
    Calls psutil.process_iter() to get information regarding the running processes of the system
    :return processes: list, processes with the following fields: 'pid', 'name', 'username'
    """

    processes = psutil.process_iter(attrs=['pid', 'name', 'username'])
    for proc in processes:
        print(proc)

    return processes


def port_state(host, port):
    """
    Get a specific port state (open, closed) for a given host
    :param host: str, target host address
    :param port: str or int, port number to check on target host
    :return: 0 if closed, 1 if open, None if error occured
    """

    # make sure port is of type 'str'
    port = str(port) if type(port) != str else port

    nmap_scan = nmap.PortScanner()

    try:
        nmap_scan.scan(host, port)

    except Exception as e:
        print(e)

        return None

    if host in nmap_scan.all_hosts():
        state = nmap_scan[host]['tcp'][int(port)]['state']
        print(" -> " + host + " tcp/" + port + " " + state)

        return 0 if state == 'closed' else 1

    else:
        print('Host ' + host + ' not found')

        return None


def os_info(host):
    """
    Host discovery ("ping") methods except for TCP Connect
    :param host: str, host url or host's ip address
    :return:
    """

    nmap_scan = nmap.PortScanner()
    # TODO: '--privileged' option not working, nmap commands should be executed as root
    # Nmap requires root permissions for everything except:
    # TCP Connect scan (-sT)
    # Reverse-DNS name resolution
    # Host discovery ("ping") methods except for TCP Connect (-PS)
    # Service and Application Version Detection (-sV)
    # Most Nmap Scripting Engine (NSE) scripts

    nmap_scan.scan(host, arguments='-PS')

    print(json.dumps(nmap_scan[host], indent=3, sort_keys=True))


if __name__ == "__main__":
    # port_state('192.168.10.170', '80')
    os_info('104.17.22.202')  # test www.in.gr
