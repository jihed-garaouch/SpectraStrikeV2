import requests
import sys
from threading import Thread, Lock
from queue import Queue
import warnings

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def scan_subdomains(domain, ssl, discovered_domains, list_lock, q):
    while True:
        try:
            subdomain = q.get()
            protocol = 'https' if ssl else 'http'
            url = f"{protocol}://{subdomain}.{domain}"
            if(ssl ==True ):
                requests.get(url, verify=False)
            else:
                requests.get(url)
        except requests.ConnectionError:
            pass
        except KeyboardInterrupt:
            sys.exit('^C')
        except Exception as e:
            pass
        else:
            print(f'Discovered subdomain: {url}')
            # Add the subdomain to the local list
            with list_lock:
                discovered_host = f"{subdomain}.{domain}"
                discovered_domains.append(discovered_host)
        finally:
            # Scanning of that subdomain complete
            q.task_done()

def run(domain, threads, subdomains, ssl, discovered_domains, list_lock):
    q = Queue()
    print(f'Performing subdomain enumeration on {domain}...\nPress CTRL-C to cancel.\nThis might take a while. Looking for subdomains in {domain}...')
    try:
        for subdomain in subdomains:
            q.put(subdomain)
        for _ in range(threads):
            worker = Thread(target=scan_subdomains, args=(domain, ssl, discovered_domains, list_lock, q))
            worker.daemon = True
            worker.start()
        q.join()  # Wait for all threads to complete
    except KeyboardInterrupt:
        sys.exit('^C')
    except Exception as e:
        print(f'Error: {e}')

def sdenum(domain, wordlist, ssl):
    threads = 8
    discovered_domains = []  # Local variable for discovered domains
    list_lock = Lock()  # Local lock for thread-safe operations on discovered_domains
    try:
        run(domain=domain, threads=threads, subdomains=wordlist, ssl=ssl, discovered_domains=discovered_domains, list_lock=list_lock)
        if discovered_domains:
            print(f'\nScan completed. {len(discovered_domains)} subdomain(s) were discovered.\n')
        else:
            print(f'Scan completed. No subdomains were discovered.\n')
        return discovered_domains
    except KeyboardInterrupt:
        sys.exit('^C')
    except Exception as e:
        print(f'Error: {e}')


