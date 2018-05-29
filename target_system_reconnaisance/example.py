"""
example code https://www.mediafire.com/folder/f0sp7xj666apz/HackingWithPython%206%20-%20NMAP%20Scanner
print port state for a given host
"""
import optparse
import nmap



def nmapScan(tgtHost, tgtPort):
    nScan = nmap.PortScanner()
    nScan.scan(tgtHost, tgtPort)
    state = nScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print(" [*] " + tgtHost + " tcp/" + tgtPort + " " + state)


def Main():
    parser = optparse.OptionParser('usage %prog ' + \
                                   '-H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', \
                      help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', \
                      help='specify target port[s] seperated by comma')
    (options, args) = parser.parse_args()
    if (options.tgtHost == None) | (options.tgtPort == None):
        print(parser.usage)
        exit(0)
    else:
        tgtHost = options.tgtHost
        tgtPorts = str(options.tgtPort).split(',')

    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)


if __name__ == '__main__':
    Main()
