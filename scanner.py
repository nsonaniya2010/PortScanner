import socket
import argparse
from multiprocessing.dummy import Pool as ThreadPool
from itertools import repeat
import termcolor
import sys
import requests

arg_parse = argparse.ArgumentParser()

arg_parse.add_argument('-l', '--list', help="List file in which PreProd domains are there.", required=True)
arg_parse.add_argument('-r', '--range', help="Port range you want to scan seperated by -(hyphen)", required=True)
args = arg_parse.parse_args()


def logo():
    return """
______               _    _____                                        
| ___ \             | |  /  ___|                                       
| |_/ / ___   _ __ | |_ \ `--.   ___   __ _  _ __   _ __    ___  _ __ 
|  __/ / _ \ | '__|| __| `--. \ / __| / _` || '_ \ | '_ \  / _ \| '__|
| |   | (_) || |   | |_ /\__/ /| (__ | (_| || | | || | | ||  __/| |   
\_|    \___/ |_|    \__|\____/  \___| \__,_||_| |_||_| |_| \___||_|RedBus  


"""


def getIpFromList(l):
    hostlst = set()
    with open(l, 'rt') as f:
        for i in f.readlines():
            if i.strip() != '':
                hostlst.add(i.strip())

    return hostlst


def portscan(target, port):
    s = socket.socket()
    tar = socket.gethostbyname(target)
    s.settimeout(1)
    try:
        con = s.connect((tar, port))
        if con == None:
            if not str(requests.get('http://' + target + ':' + str(port)).status_code).startswith('5'):
                if str(requests.get('http://' + target + ':' + str(port)).content).endswith("Connection reset by peer'))"):
                    print(termcolor.colored("Port Open: " + str(port), color='blue', attrs=['bold']))
    except:
        pass


if __name__ == '__main__':
    try:
        print(termcolor.colored(logo(), color='red', attrs=['bold']))
        rang = args.range
        lst = args.list
        print(termcolor.colored("Getting IP's from list:\n", color='red', attrs=['bold']))
        hosts = getIpFromList(lst)
        l0, l1 = rang.split('-')

        ports = list()

        for i in range(int(l0), int(l1)):
            ports.append(i)

        print(termcolor.colored("All set, going to scan for ports.\n", color='red', attrs=['bold']))
        for host in hosts:
            theads = ThreadPool(100)
            print(termcolor.colored("Scanning " + host + " for open ports.\n", color='green', attrs=['bold']))
            theads.starmap(portscan, zip(repeat(host), ports))
            print('\n')
            theads.close()
            theads.join()
    except KeyboardInterrupt:
        print("Keyboard Intruppt. Exiting...")
        sys.exit(1)