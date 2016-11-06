import subprocess
import os
import psutil


def Update(aur=1, forceRepoDown=1, noconfirm=1):
    command = []
    command.append('yaourt')
    if forceRepoDown:
        command.append('-Syyu')
    else:
        command.append('-Syu')
    if aur:
        command.append('--aur')
    if noconfirm:
        command.append('--noconfirm')

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    if os.path.exists('guitemp.txt'):
        os.remove('guitemp.txt')
    open('temp.txt', 'w').close()
    downloadcount = 0
    upgradecount = 0
    for line in iter(proc.stdout.readline, b''):
        if 'Packages' in str(line):
            packagenumber = int(str(line).split('(')[1].split(')')[0])
        if 'downloading' in str(line):
            if '.db' in str(line):
                pass
            else:
                downtemp = open('downtemp.txt', 'w')
                downloadcount += 1
                downtemp.write(str(downloadcount) + '/' + str(packagenumber))
                downtemp.close()
            if 'upgrading' in str(line):
                upgradecount += 1
                if downloadcount != packagenumber:
                    downtemp = open('downtemp.txt','w')
                    downloadcount = packagenumber
                    downtemp.write(str(downloadcount) + '/' + str(packagenumber))
                    downtemp.close()
                upgrtemp = open('guitemp.txt', 'w')
                upgrtemp.write(str(upgradecount) + '/' + str(packagenumber))
                upgrtemp.close()

        # if 'Foreign packages:' in str(line):
        #     fpkline = str(line).replace("b'",'').replace("'",'').replace('\\\\','').replace(': /',': ').replace(': |',': ').replace(': -',': ').replace('\\r','\n').replace('\\n','\n').encode()
        #     print(fpkline.decode())
        #     # print(str(line).replace("b'",'').replace("'",'').replace('\\\\','').replace(': /',': -').replace(': |',': -').replace('\\n','').split('\\r'))
        # else:
        tempfr = open('temp.txt')
        if str(line) != tempfr.read():
            tempfr.close()
            tempf = open('temp.txt', 'w')
            tempf.write(str(line))
            tempf.close()
            # if 'Foreign packages:' in str(line):
            #     guitempf = open('guitemp.txt', 'r')
            #     fdata = guitempf.read()
            #     guitempf.close()
            #     oldvalue = fdata.split('\n')[len(fdata.split('\n')) - 2].replace(' F', 'F')
            #     if 'Foreign packages:' in oldvalue:
            #         print(oldvalue)
            #         fnewdata = fdata.replace(oldvalue, line.decode())
            #         guitempf = open('guitemp.txt', 'w')
            #         guitempf.write(fnewdata)
            #         guitempf.close()
            #     else:
            #         guitempf = open('guitemp.txt', 'a+')
            #         guitempf.write(line.decode())
            #         guitempf.close()
            guitempf = open('guitemp.txt', 'a+')
            guitempf.write(line.decode())
            guitempf.close()
        tempfr.close()
        tempfr = open('temp.txt')
    if 'Foreign packages:' in tempfr.read():
        print('System up to date')
    if 'Error' in tempfr.read():
        print('System update failed.')
    tempfr.close()
    os.remove('temp.txt')
    if os.path.exists('downtemp.txt'):
        os.remove('downtemp.txt')
    if os.path.exists('upgrtemp.txt'):
        os.remove('upgrtemp.txt')

    # while proc.poll() is None:
    #     line = proc.stdout.readline()
    #     print(line.decode().rstrip())


def processVerification(pname):
    instance = 0
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == "python" and len(p.cmdline()) > 1 and pname in p.cmdline()[1]:
            instance += 1
            if instance > 1:
                return "running"
