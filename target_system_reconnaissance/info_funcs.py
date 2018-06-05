"""
This module contains system information gathering functions
"""

import psutil
import nmap
import json
import socket
from subprocess import run, PIPE
import os


def get_procs(verbose=False):
    """
    Calls psutil.process_iter() to get information regarding the running processes of the system
    :param verbose: print results
    :return processes: list, processes with the following fields: 'pid', 'name', 'username'
    """

    processes = psutil.process_iter(attrs=['pid', 'name', 'username'])

    if verbose:
        print(processes)

    return processes


def port_state(host, port, verbose=False):
    """
    Get a specific port state (open, closed) for a given host
    :param host: str, target host address
    :param port: str or int, port number to check on target host
    :param verbose: print results
    :return: 0 if closed, 1 if open, None if error occurred
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
        if verbose:
            print(" -> " + host + " tcp/" + port + " " + state)

        return 0 if state == 'closed' else 1

    else:
        print('Host ' + host + ' not import osfound')

        return None


def os_info(host, verbose=False):
    """
    Host discovery ("ping") methods except for TCP Connect
    :param host: str, host url or host's ip address
    :param verbose: print results
    :return: JSON (dict) object, including various system info regarding os, the device and open ports
    """

    nmap_scan = nmap.PortScanner()
    # script execution must be followed by sudo "$(which python)"
    # Nmap requires root permissions for everything except:
    # TCP Connect scan (-sT)
    # Reverse-DNS name resolution
    # Host discovery ("ping") methods except for TCP Connect (-PS)
    # Service and Application Version Detection (-sV)
    # Most Nmap Scripting Engine (NSE) scripts

    nmap_scan.scan(host, arguments='-O')

    if host in nmap_scan.all_hosts():
        if verbose:
            print(json.dumps(nmap_scan[host], indent=3, sort_keys=True))

        return nmap_scan[host]

    else:
        print('Host ' + host + ' not found')

        return None


def socket_info(host, port=None, verbose=False):
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
    :param verbose: print results
    :return: JSON (dict) object, including the following info: family, type, proto, canonname, sockaddr
    """

    result = {}

    try:
        for res in socket.getaddrinfo(host, port):
            result[len(result)] = {k: v for k, v in zip(['family',
                                                         'type',
                                                         'proto',
                                                         'canonname',

                                                         'sockaddr'], res)}
        if verbose:
            print(json.dumps(result, indent=3, sort_keys=True))

        return result

    except socket.gaierror:
        print('Host ' + host + ' not found')

        return None


def file_info(ext, directory=None, verbose=False):
    """
    Get information (os.stat) for files of a specific type (extension), in a specific directory. If the directory is not
    specified, the file search begins from root
    :param ext: str, file extension, optional
    :param directory: str, directory of interest, optional
    :param verbose: print results
    :return: JSON (dict) object, including the following info: 'st_mode', 'st_ino', 'st_dev', 'st_nlink', 'st_uid',
                                                                'st_gid', 'st_size', 'st_atime', 'st_mtime', 'st_ctime'
    """
    files_stat = {}

    # if a directory has not been set, start walking from root
    if not directory:
        directory = '/'

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                files_stat[os.path.join(root, file)] = {k: v for k, v in zip(['st_mode',
                                                                              'st_ino',
                                                                              'st_dev',
                                                                              'st_nlink',
                                                                              'st_uid',
                                                                              'st_gid',
                                                                              'st_size',
                                                                              'st_atime',
                                                                              'st_mtime',
                                                                              'st_ctime'],
                                                                             os.stat(os.path.join(root, file)))}
    if verbose:
        print(json.dumps(files_stat, indent=3, sort_keys=True))

    return files_stat


def pipe_info(pid, verbose=False):
    """
    :param pid: str or int, process id
    :param verbose: print results
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

    if verbose:
        print(json.dumps(output, indent=3, sort_keys=True))

    return output


if __name__ == "__main__":
    # test a function here
    exit()
