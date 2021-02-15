from os import popen
import subprocess
import locale

lan = locale.getdefaultlocale()[0][0:2].upper()

languages = {'DE':['alle Benutzer', 'inhalt'],
             'EN':['All User Profile', 'Key Content'],
             'ZH':['All User Profile', 'Key Content'],
             'RU':['All User Profile', 'Key Content'],
             'FR':['Profil Tous les utilisateurs', 'Contenu de la'],
             'ES':['Perfil de todos los usuarios', 'Contenido de la clave'],
             'HI':['All User Profile', 'Key Content']}

if not lan in languages:
    print('Language "'+lan+'" not implemented yet')
    input('press enter to continue')
    exit()

out = open('Data.log', 'w')

data = str(subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])).split('\\n')

profiles = [(i.split(":")[1][1:-1])[0:len(i.split(":")[1][1:-1])-1] for i in data if languages[lan][0] in i]

for i in profiles:
    try:
        results = str(subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])).split('\\n')
        results = [(b.split(":")[1][1:-1])[0:len(b.split(":")[1][1:-1])-1] for b in results if languages[lan][1] in b]
        try:
            print("{:<30}|  {:<}".format(i, results[0]))
            out.write("{:<30}|  {:<}".format(i, results[0]))
            
        except IndexError:
            print("{:<30}|  {:<}".format(i, ""))
            out.write("{:<30}|  {:<}".format(i, ""))
        out.write('\n')
        
    except subprocess.CalledProcessError:
        print("{:<30}|".format(i))
        out.write("{:<30}|\n".format(i))

print('\n\n\n')
out.write('\n\n\n')


#   ----------  Mac Adress  ----------
macA = popen('getmac').read()
print(macA)
out.write(macA+'\n')

print('\n\n\nPartitions:')
out.write('\n\n\nPartitions:')

#   ----------  Partitions  ----------
p = popen('wmic partition get name,size,type').read()
print(p)
out.write(p+'\n')

#   ---------- Installed programms ---
'''if input('Do you want to check all installed Programms? (Could take a while!) [J/N] ') == 'J':
    print('\n\n\nInstalled programms:')
    out.write('\n\n\nInstalled programms:')
    pr = popen('wmic product get name').read()
    print(pr)
    out.write(pr+'\n')

else:
    print('Not checked for installed programms')
    out.write('Not checked for installed programms\n')'''

# ---------- General Inforamtion -----
gIn = popen('systeminfo').read()
print(gIn)
out.write(gIn+'\n')

out.close()
input('\nDone')
