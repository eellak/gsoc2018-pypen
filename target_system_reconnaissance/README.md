# Target System Reconnaissance & Information gathering

A set of functions have been developed in order to get useful information for a target system such as open ports, OS info etc.

## How to use

### Setup

You will need to install the necessary python packages through executing  
`pip install -r requirements.txt`

and [NMAP](https://nmap.org/download.html) through
`sudo apt-get install nmap`

### Functions 
Inside the file `info_funcs.py` one can find the following functions:

* `get_procs(verbose=False)`  
Calls `psutil.process_iter()` method and returns running processes with the following fields: 'pid', 'name', 'username' in proper JSON format. `verbose` can be set to `True` if you want the results to be printed.

* `port_state(host, port, verbose=False)`  
Calls the `nmap.PortScanner()` method to scan a specific port of a specific host address and check whether it's open or closed. `verbose` can be set to `True` if you want the results to be printed.

* `os_info(host, verbose=False)`  
Calls the `nmap.PortScanner()` method with **-O** input argument to receive to OS info for the given host and returns the results in proper JSON format. `verbose` can be set to `True` if you want the results to be printed.  
**IMPORTANT NOTE**: You have to run this function as `sudo` (or any python script that contains this function). Since `PYTHONPATH` may change when you use `sudo`, you can try this trick:
`sudo "$(which python)" myscript.py`

* `socket_info(host, port=None, verbose=False)`  
Calls the `ss` command. Returns the following info: Netid, Recv-Q, Send-Q, Local Address, Local Address Port, Peer Address, Peer Address Port in proper JSON format. `verbose` can be set to `True` if you want the results to be printed.

* `file_info(ext, directory=None, verbose=False)`  
Calls the `os.stat()` method on files with the defined extenstion `ext`, found in the defined directory (if omitted, the search begins from the root directory) and returns the following info per file: 'st_mode', 'st_ino', 'st_dev', 'st_nlink', 'st_uid', 'st_gid', 'st_size', 'st_atime', 'st_mtime', 'st_ctime' in proper JSON format. `verbose` can be set to `True` if you want the results to be printed.

* `pipe_info(pid, verbose=False)`  
Calls the `lsof` commands to find open pipes for a given process (if pid is defined, otherwise find all open pipes) and returns the following info: COMMAND, PID, USER, FD, TYPE, DEVICE, SIZE/OFF, NODE, NAME in proper JSON format. `verbose` can be set to `True` if you want the results to be printed.

There's also the `full_scan.py` script, that runs almost all of the above. To use this, you'll either have to fill in *FIELDS* section in the `params.ini` file or you'll provide them via command prompt. For further info you can check the code.

### Backchannel functionality
Our assumption is that we already have access to a target system. That's why we have created the `snitch` exectuable (with the use of PyInstaller), which runs the client part of our backchannel, executes the `full_scan.py` script and send the retrieved info to the server (attacker).
The server must be running, by executing the `snitch_server.py` module (definition of *server* and *port* options is necessary)

### Disclaimer

*The purpose of this library is educational, for Penetration Testing and Ethical Hacking and under no circumstances for malicious actions. It's use will comply to all current data protection legislation.*