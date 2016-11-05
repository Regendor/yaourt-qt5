import subprocess


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
    for line in iter(proc.stdout.readline, b''):
        print(line.decode().rstrip())

    # while proc.poll() is None:
    #     line = proc.stdout.readline()
    #     print(line.decode().rstrip())


yaourt_update(forceRepoDown=0)
