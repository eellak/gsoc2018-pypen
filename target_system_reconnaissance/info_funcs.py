#!/usr/bin/env python3
"""
This module contains system information gathering functions

File name: info_funcs.py
Author: Konstantinos Christos Liosis
Date created: 4/6/2018
Python Version: 3.6.0
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

    processes = list(psutil.process_iter(attrs=['pid', 'name', 'username']))

    if verbose:
        print(processes)

    return {proc.info['pid']: [proc.info['name'], proc.info['username']] for proc in processes}


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
import os
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


def socket_info(verbose=False):
    """
    Use of the 'ss' bash command for socket information
    :param host: str, address
    :param port: str or int, port number
    :param verbose: print results
    :return: JSON (dict) object, including the following info: family, type, proto, canonname, sockaddr
    """
    result = run(['ss',
                  'state',
                  'listening'], stdout=PIPE)

    output = {}

    for line in [x for x in result.stdout.decode('utf-8').split('\n')[:-1] if '::' not in x]:
        output[len(output)] = {k: v for k, v in zip(['Netid',
                                                     'Recv-Q',
                                                     'Send-Q',
                                                     'Local Address',
                                                     'Local Address Port',
                                                     'Peer Address',
                                                     'Peer Address Port'], line.replace(':', ' ').split())}

    if verbose:
        print(json.dumps(output, indent=3, sort_keys=True))

    return output


def file_info(ext, directory=None, verbose=False):
    # TODO:
    # possible extension would be the discovery of a directories with valuable files for later exploitation with
    # ransomware

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


def pipe_info(pid=None, verbose=False):
    """
    :param pid: str or int, process id
    :param verbose: print results
    :return: JSON (dict) object, including the following info: COMMAND, PID, USER, FD, TYPE, DEVICE, SIZE/OFF, NODE, NAME
    """

    result = run('lsof',
                 stdout=PIPE)

    # if pid is defined, find pipes for this specific process, otherwise find all pipes
    if pid:
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
