import os
import webbrowser
from os.path import expanduser
import datetime
import kismet_debian_submit_gnusa

file = open(expanduser("~") + '/Desktop/HERE.txt', 'w')
file.write("It worked!\n" + str(datetime.datetime.now()))
file.close()

sudoPassword = 'PASSWORD_USER_DEBIAN'
wlan = 'wlo1'
command = 'sudo ifconfig ' + wlan + ' down && sudo iwconfig ' + wlan + ' mode monitor && sudo iwconfig ' + wlan
print(command)
#os.system("gnome-terminal -e 'bash -c \""+ (sudoPassword, command) +";bash\"'")
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
print(p)

command = 'sudo kismet'
#os.system("gnome-terminal -e 'bash -c \""+ (sudoPassword, command) +";bash\"'")
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

#command="sudo kismet"
#os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")


webbrowser.open('http://localhost:2051', new=2)

exec(open('kismet_debian_submit_gnusa.py').read())


