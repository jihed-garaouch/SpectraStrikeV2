#############################################################################


from ftplib import FTP


import os





def download_files(host):
    i = 0
    try:
        items = []
        f_ftp = FTP(str(host), timeout=5)
        f_ftp.login('anonymous', 'anonymous@test.com')
        # here need to add if  ftp failed print("cannot connect anonmosly to ftp
        f_ftp.retrlines('LIST', items.append)
        items = map(str.split, items)
        directories = [item.pop() for item in items if item[0][0] == 'd']

        file_names = f_ftp.nlst()

        if file_names:
            os.makedirs('tmp/{}'.format(host))

        for file_name in file_names:
            if file_name not in directories:
                local_file = os.path.normpath('tmp/{}/{}'.format(host, file_name))
                if os.path.exists(local_file):
                    local_file = os.path.join('{}.{}'.format(local_file, i))
                    i += 1
                with open(local_file, 'wb') as d_file:
                    f_ftp.retrbinary('RETR {}'.format(file_name), d_file.write)

        for directory in directories:
            if not os.path.exists('tmp/{}/{}'.format(host, directory)):
                os.makedirs('tmp/{}/{}'.format(host, directory))
            download_files_recursive(f_ftp, directory, host, directory)
    except:
        return


def download_files_recursive(r_ftp, r_dir, host, directory):
    r_ftp.cwd(r_dir)
    items = []
    r_ftp.retrlines('LIST', items.append)
    items = map(str.split, items)
    directories = [item.pop() for item in items if item[0][0] == 'd']

    file_names = r_ftp.nlst()

    for file_name in file_names:
        if file_name not in directories:
            local_file = os.path.normpath('tmp/{}/{}/{}'.format(host, directory, file_name))
            with open(local_file, 'wb') as d_file:
                r_ftp.retrbinary('RETR {}'.format(file_name), d_file.write)

    for directory in directories:
        if not os.path.exists('tmp/{}/{}'.format(host, directory)):
            os.makedirs('tmp/{}/{}'.format(host, directory))
        download_files_recursive(r_ftp, directory, host, directory)
        r_ftp.cwd('..')


# Function to clear the screen
def clear_screen():
        os.system('clear')


def ftp_scan(host):
    download_files(host)
