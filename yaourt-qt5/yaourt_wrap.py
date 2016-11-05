import subprocess
import os

def yaourt_update(aur=1, forceRepoDown=1):
    command = []
    command.append('yaourt')
    if forceRepoDown:
        command.append('-Syyu')
    else:
        command.append('-Syu')
    if aur:
        command.append('--aur')

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    open('temp.txt', 'w').close()
    for line in iter(proc.stdout.readline, b''):
        if 'Foreign packages:' in str(line):
            fpkline = str(line).replace("b'",'').replace("'",'').replace('\\\\','').replace(': /',': ').replace(': |',': ').replace(': -',': ').replace('\\r','\n').replace('\\n','\n').encode()
            print(fpkline.decode())
            # print(str(line).replace("b'",'').replace("'",'').replace('\\\\','').replace(': /',': -').replace(': |',': -').replace('\\n','').split('\\r'))
        else:
            tempfr = open('temp.txt')
            if str(line) != tempfr.read():
                tempfr.close()
                tempf = open('temp.txt', 'w')
                tempf.write(str(line))
                tempf.close()
                print(line.decode().rstrip())
            tempfr.close()
            # print(line.decode().rstrip())
    print('System up to date')
    os.remove('temp.txt')

    # while proc.poll() is None:
    #     line = proc.stdout.readline()
    #     print(line.decode().rstrip())


yaourt_update(forceRepoDown=0)
