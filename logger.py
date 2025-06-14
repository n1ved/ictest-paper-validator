class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printwarn(provider,content):
    print(bcolors.WARNING + "[" + provider + "] "+ bcolors.ENDC + content)

def printinfo(provider,content):
    print(bcolors.OKBLUE + "[" + provider + "] "+ bcolors.ENDC + content)

def printsuccess(provider,content):
    print(bcolors.OKGREEN + "[" + provider + "] "+ bcolors.ENDC + content)

def printfail(provider,content):
    print(bcolors.FAIL + "[" + provider + "] "+ bcolors.ENDC + content)
