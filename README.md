# androidserver2
Python server on android, on local network. Used in a futur funny game.

Made with twisted

L'application s'appelle Android_Server_2

### Apk build fails
Debian 9.2 64 bits en avril 2018
Voir 
VirtualBox 5.1.30
buildozer-0.34
kivy-1.10.0
twisted
cython-0.25.2 and cython-0.23

* [Installation de debian](https://ressources.labomedia.org/debian_installation_configuration)
* [VirtualBox](https://ressources.labomedia.org/debian_installation_configuration#virtualbox)
* [Installation de kivy buildozer twisted](https://ressources.labomedia.org/kivy_buildozer_avec_python_2.7)

#### Buildozer fails with incremental
See https://stackoverflow.com/questions/49707807/buildozer-with-twisted-fails-because-it-cannot-find-incremental

#### Log
##### log_0.71.txt
requirements=incremental

pas de dossier incremental obtenu

##### log_0.72.txt
requirements=incremental,kivy

incremental installé dans python2.7

##### log_0.73.txt
requirements=incremental,kivy,twisted

erreur avec incremental

##### log_0.74.txt
requirements=kivy,twisted

mais accents dans main.py, erreur chargement apk sur android

##### log_0.75.txt
requirements=kivy,twisted

mais sans accents dans main.py, apk valide et fonctionnel

### Test possible

Avec [TCPclient](https://github.com/sergeLabo/TCPclient)

Application Android qui envoie des nombre incrémentés

### Bugs connus
Ce projet est une recherche pour créer un serveur TCP sur Android.
Beaucoup de choses sont brutes de décoffrage.

La fréquence ne sert à rien.

La récupération de l'IP local est fausse.
