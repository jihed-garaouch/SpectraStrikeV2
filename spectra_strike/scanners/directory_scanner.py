import requests
import sys
from threading import Thread, Lock
from queue import Queue
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def generate_subdirectories(base, directories):
    return [f"{base}/{subdir}" for subdir in directories]

def scan_directories(host, max_depth, directories, ssl, q, discovered_directories, list_lock):
    while True:
        try:
            directory, current_depth = q.get()
            protocol = 'https' if ssl else 'http'
            url = f"{protocol}://{host}/{directory}"
            if(ssl ==True ):
                response=requests.get(url, verify=False)
            else:
                response=requests.get(url)
        except requests.ConnectionError:
            pass
        except KeyboardInterrupt:
            sys.exit('^C')
        except Exception as e:
            pass
        else:
            if response.status_code != 404:
                print(f'Discovered directory: {url}')
                with list_lock:
                    discovered_directories.append(url)
                    if current_depth < max_depth:
                        for subdir in generate_subdirectories(directory, directories):
                            q.put((subdir, current_depth + 1))
        finally:
            q.task_done()

def main(host, threads, directories, max_depth, ssl):
    q = Queue()
    list_lock = Lock()
    discovered_directories = []
    print(f'Performing directory busting on {host}...\nPress CTRL-C to cancel.\nThis might take a while. Looking for directories in {host}...')
    try:
        for directory in directories:
            q.put((directory, 0))
        for _ in range(threads):
            worker = Thread(target=scan_directories, args=(host, max_depth, directories, ssl, q, discovered_directories, list_lock))
            worker.daemon = True
            worker.start()
        q.join()
    except KeyboardInterrupt:
        sys.exit('^C\n')
    except Exception as e:
        print(f'Error: {e}')
    return discovered_directories

def dirbust(host, words, max_depth, ssl):
    threads = 8
    try:
        discovered_directories = main(host=host, threads=threads, directories=words, max_depth=max_depth, ssl=ssl)
        if discovered_directories:
            print(f'\nScan completed. {len(discovered_directories)} directory(ies) were discovered.\n')
        else:
            print(f'Scan completed. No directories were discovered.\n')
    except KeyboardInterrupt:
        sys.exit('^C\n')
    except Exception as e:
        print(f'Error: {e}')
