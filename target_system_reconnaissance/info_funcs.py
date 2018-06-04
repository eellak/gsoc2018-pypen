"""
This module contains system information gathering functions
"""

import psutil
import nmap
import json
import socket
from subprocess import run, PIPE


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
    :return: JSON (dict) object, including various system info regarding os, the device and open ports
    """

    nmap_scan = nmap.PortScanner()
    # TODO: '--privileged' option not working, nmap commands should be executed as root
    # Nmap requires root permissions for everything except:
    # TCP Connect scan (-sT)
    # Reverse-DNS name resolution
    # Host discovery ("ping") methods except for TCP Connect (-PS)
    # Service and Application Version Detection (-sV)
    # Most Nmap Scripting Engine (NSE) scripts

    nmap_scan.scan(host, arguments='-O')

    if host in nmap_scan.all_hosts():
        print(json.dumps(nmap_scan[host], indent=3, sort_keys=True))

        return nmap_scan[host]

    else:
        print('Host ' + host + ' not found')

        return None


def socket_info(host, port=None):
    """
    According to python docs:
    The function returns a list of 5-tuples with the following structure:
    (family, type, proto, canonname, sockaddr)
    In these tuples, family, type, proto are all integers and are meant to be passed to the socket() function.
    canonname will be a string representing the canonical name of the host if AI_CANONNAME is part of the flags
    argument; else canonname will be empty. sockaddr is a tuple describing a socket address, whose format depends
    on the returned family (a (address, port) 2-tuple for AF_INET, a (address, port, flow info, scope id) 4-tuple for
    AF_INET6), and is meant to be passed to the socket.connect() method.
    :param host: str, address
    :param port: str or int, port number
    :return: JSON (dict) object, including the following info: family, type, proto, canonname, sockaddr
    """

    result = {}

    try:
        for res in socket.getaddrinfo(host, port):
            result[len(result)] = {k: v for k, v in zip(['family', 'type', 'proto', 'canonname', 'sockaddr'], res)}

        print(json.dumps(result, indent=3, sort_keys=True))

        return result

    except socket.gaierror:
        print('Host ' + host + ' not found')

        return None


def file_info(ext, dir=None):
    # TODO
    """
    stat() for dir, ext
    If dir omitted, os.walk(‘/’)
    """
    raise NotImplementedError


def pipe_info(pid):
    """
    :param pid: str or int, process id
    :return: JSON (dict) object, including the following info: COMMAND, PID, USER, FD, TYPE, DEVICE, SIZE/OFF, NODE, NAME
    """

    result = run('lsof',
                 stdout=PIPE)

    result = run(['grep', str(pid)],
                 input=result.stdout,
                 stdout=PIPE)

    result = run(['grep', 'pipe'],
                 input=result.stdout,
                 stdout=PIPE)

    output = {}

    for line in result.stdout.decode('utf-8').split('\n')[:-1]:
        output[len(output)] = {k: v for k, v in zip(['COMMAND',
                                                     'PID',
                                                     'USER',
                                                     'FD',
                                                     'TYPE',
                                                     'DEVICE',
                                                     'SIZE/OFF',
                                                     'NODE',
                                                     'NAME'], line.split())}

    print(json.dumps(output, indent=3, sort_keys=True))

    return output


if __name__ == "__main__":
    # port_state('192.168.10.170', '80')
    # os_info('192.168.1.254')
    # socket_info('192.168.1.254')
    # pipe_info(6828)
    exit()