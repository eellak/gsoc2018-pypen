"""
This modules runs various information gathering functions for  a target system
"""

import json
import configparser
import os

# custom modules import
from info_funcs import get_procs, os_info, socket_info, file_info, pipe_info

params = configparser.ConfigParser()
params.read('params.ini')

def save(data, fname):
    out_file = open(fname, 'w')
    try:
        json.dump(data, out_file)

        return fname + ' saved'

    except Exception as e:
        print(str(e) + ' - File: ' + fname)

        return None


def main():

    print('Target Reconnaissance')

    host, port, ext, directory = None, None, None, None

    # if target host address and other needed info is not provided in the params.ini file (which is the recommended way
    # of using this module), it needs to be entered via command prompt
    if not params['FIELDS']['host'] or not params['FIELDS']['ext']:
        print('Parameters file not configured, enter target info below')
        host = input('Enter target host address: ')
        port = input('Enter target port (optional): ')
        ext = input('Enter extension of file types to get info about: ')
        directory = input('Enter directory for files search (optional): ')

        # host and file extension info are necessary for this module to run
        if not host or not ext:
            print('Insufficient target info provided. Exiting...')
            exit()

    else:
        host, port, ext, directory = params['FIELDS'].values()
        print('Parameters file configured\nTarget scan initiated')

    if not os.path.exists(params['IO']['results']):
        os.makedirs(params['IO']['results'])

    # process scan
    processes = get_procs()
    if save(processes, params['IO']['processes']):
        print('processes scan ok')

    else:
        print('processes scan failed')

    # os info
    if save(os_info(host), params['IO']['results'] + params['IO']['os']):
        print('os scan ok')

    else:
        print('os scan failed')

    # socket info
    if save(socket_info(host, port), params['IO']['results'] + params['IO']['sockets']):
        print('sockets scan ok')

    else:
        print('sockets scan failed')

    # files info
    if save(file_info(ext, directory), params['IO']['results'] + params['IO']['files']):
        print('files scan ok')

    else:
        print('files scan failed')

    # pipe info per process
    print('Pipe information gathering started, this will take some time...')
    if not os.path.exists(params['IO']['results'] + params['IO']['pipes_results']):
        os.makedirs(params['IO']['results'] + params['IO']['pipes_results'])

    for proc in processes.keys():
        fname = params['IO']['pipes_results'] + 'process' + str(proc) + '.json'
        save(pipe_info(proc, port), params['IO']['results'] + fname)


if __name__ == "__main__":
    main()

