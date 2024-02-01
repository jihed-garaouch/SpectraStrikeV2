import nmap
import sys
class NmapScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()

    def scan_host(self, host):
        try:
            print(f"Performing Nmap scan on {host}")
            self.nm.scan(hosts=host, arguments='--top-ports 1000 ')
            print(self.nm.command_line())
            print("Scan info:", self.nm.scaninfo())
        except nmap.PortScannerError:
            print("Nmap not found", sys.exc_info()[0])
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit(1)


    def get_scan_results(self, host):
        open_ports = {}
        try:
            # Ensure that the scan is complete and 'tcp' is in the results
            if self.nm.all_hosts() and 'tcp' in self.nm[host]:
                print(self.nm[host]['tcp'].keys())
                for port in self.nm[host]['tcp']:
                    if self.nm[host]['tcp'][port]['state'] == 'open':
                        open_ports[port] = self.nm[host]['tcp'][port]['name']
                        print(f"Open port: {port}/{self.nm[host]['tcp'][port]['name']}")
            else:
                print(f"No open TCP ports found or host not scanned: {host}")
            return open_ports
        except KeyError as e:
            print(f"Expected keys not found in scan results: {e}")
            return open_ports
    def get_hostname(self,host):
        return self.nm[host].hostname()