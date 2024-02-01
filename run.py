from spectra_strike.welcome import  *
from spectra_strike.utils.nmap_scanner  import *
from spectra_strike.scanners.directory_scanner import dirbust
from spectra_strike.scanners.subdomain_scanner import sdenum
from spectra_strike.scanners.ftp_scanner import ftp_scan

def main():
    print_banner()
    args = get_args()
    host = args.host
    ip=args.ip
    subdomain_wordlist_path = args.subdomainwordlist
    directory_wordlist_path = args.directorywordlist
    recursion_depth = args.recursive

    # Now you can use target_host, subdomain_wordlist_path, directory_wordlist_path, and recursion_depth in your script
    print(f"Scanning {ip} using:")
    print(f" - Subdomain wordlist: {subdomain_wordlist_path}")
    print(f" - Directory wordlist: {directory_wordlist_path}")
    print(f" - Recursion depth: {recursion_depth}")

    scanner = NmapScanner()
    subdomain_wordlist=get_wordlist(subdomain_wordlist_path)
    directory_wordlist=get_wordlist(directory_wordlist_path)
    scanner.scan_host(ip)
    hostname=scanner.get_hostname(ip)
    if host is None or host == "":
        host = hostname if hostname else ip
    results=scanner.get_scan_results(ip)
    if 443 in results:

        subdomains=sdenum(host, subdomain_wordlist, True)
        dirbust(host, directory_wordlist, recursion_depth,True)
        for s in subdomains:
            dirbust(s, directory_wordlist, recursion_depth,True)
    if 80 in results:
        print("**********************************************")
        print("****************HTTP**************************")
        subdomains=sdenum(host, subdomain_wordlist, False)
        dirbust(host, directory_wordlist, recursion_depth,False)
        for s in subdomains:
            dirbust(s, directory_wordlist, recursion_depth,False)
    if 20 in results:
        ftp_scan(host)

    print("Finished")


def get_wordlist(file_path):
    return open(file_path).read().splitlines()



if __name__ == "__main__":
    main()
