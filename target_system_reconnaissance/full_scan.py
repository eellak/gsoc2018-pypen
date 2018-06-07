"""

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

if __name__ == "__main__":
    print('Target Reconnaissance')

    host, port, ext, directory = None, None, None, None

    if not (params['FIELDS']['host'] or params['FIELDS']['ext']):
        print('Parameters file not configured, enter target info below')
        host = input('Enter target host address: ')
        port = input('Enter target port (optional): ')
        ext = input('Enter extension of file types to get info about: ')
        directory = input('Enter directory for files search (optional): ')

        if host or ext is None:
            print('Insufficient target info provided. Exiting...')
            exit()

    else:
        host, port, ext, directory = params['FIELDS'].values()
        print('Parameters file configured\nTarget scan initiated')

        # process scan
        processes = get_procs()
        if save(processes, params['IO']['processes']):
            print('processes scan ok')
        else:
            print('processes scan failed')

        # os info
        if save(os_info(host), params['IO']['os']):
            print('os scan ok')
        else:
            print('os scan failed')

        # socket info
        if save(socket_info(host, port), params['IO']['sockets']):
            print('sockets scan ok')
        else:
            print('sockets scan failed')

        # files info
        if save(file_info(ext, directory), params['IO']['files']):
            print('files scan ok')
        else:
            print('files scan failed')

        # pipe info per process
        if not os.path.exists('pipes_info'):
            os.makedirs('pipes_info')

        for proc in processes.keys():
            fname = 'proccess_info/process' + str(proc) + '.json'
            save(pipe_info(proc, port), fname)