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

out = open('passwords.log', 'w')

data = str(subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])).split('\\n')

profiles = [(i.split(":")[1][1:-1])[0:len(i.split(":")[1][1:-1])-1] for i in data if languages[lan][0] in i]

for i in profiles:
    results = str(subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])).split('\\n')
    results = [(b.split(":")[1][1:-1])[0:len(b.split(":")[1][1:-1])-1] for b in results if languages[lan][1] in b]
    try:
        print("{:<30}|  {:<}".format(i, results[0]))
        out.write("{:<30}|  {:<}".format(i, results[0]))
    except IndexError:
        print("{:<30}|  {:<}".format(i, ""))
        out.write("{:<30}|  {:<}".format(i, ""))
    out.write('\n')
out.close()
input()
