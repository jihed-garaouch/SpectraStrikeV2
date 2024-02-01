
import argparse
def print_banner():
    banner = """
███████████    █████████   ███████████     █████████  ██████████    ██████████ █████       █████       █████ █████       ██████████       █████                ██████████     █████████  
░░███░░░░░███  ███░░░░░███ ░░███░░░░░███   ███░░░░░███░░███░░░░░█   ░░███░░░░░█░░███       ░░███       ░░███ ░░███       ░░███░░░░░█     ███░░░███             ░░███░░░░███   ███░░░░░███ 
 ░███    ░███ ░███    ░███  ░███    ░███  ███     ░░░  ░███  █ ░     ░███  █ ░  ░███        ░███        ░███  ░███        ░███  █ ░     ███   ░░███ █████ █████ ░███   ░░███ ░███    ░███ 
 ░██████████  ░███████████  ░██████████  ░███          ░██████       ░██████    ░███        ░███        ░███  ░███        ░██████      ░███    ░███░░███ ░░███  ░███    ░███ ░███████████ 
 ░███░░░░░███ ░███░░░░░███  ░███░░░░░███ ░███    █████ ░███░░█       ░███░░█    ░███        ░███        ░███  ░███        ░███░░█      ░███    ░███ ░░░█████░   ░███    ░███ ░███░░░░░███ 
 ░███    ░███ ░███    ░███  ░███    ░███ ░░███  ░░███  ░███ ░   █    ░███ ░   █ ░███      █ ░███      █ ░███  ░███      █ ░███ ░   █   ░░███   ███   ███░░░███  ░███    ███  ░███    ░███ 
 ███████████  █████   █████ █████   █████ ░░█████████  ██████████    ██████████ ███████████ ███████████ █████ ███████████ ██████████    ░░░█████░   █████ █████ ██████████   █████   █████
░░░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░   ░░░░░   ░░░░░░░░░  ░░░░░░░░░░    ░░░░░░░░░░ ░░░░░░░░░░░ ░░░░░░░░░░░ ░░░░░ ░░░░░░░░░░░ ░░░░░░░░░░       ░░░░░░   ░░░░░ ░░░░░ ░░░░░░░░░░   ░░░░░   ░░░░░ 
    """
    print(banner)
def get_args():
    parser = argparse.ArgumentParser(description="SpectraStrike Scanner")
    parser.add_argument("-ho", "--host", help="Target host")
    parser.add_argument("-ip", "--ip", help="Target ip", required=True)
    parser.add_argument("-sw", "--subdomainwordlist", default="./wordlist/subdomains.txt", help="Path to the subdomain wordlist file")
    parser.add_argument("-dw", "--directorywordlist", default="./wordlist/directory", help="Path to the directory wordlist file")
    parser.add_argument("-r", "--recursive", type=int, default=1, help="Recursion depth")
    args = parser.parse_args()
    return args


