# androidserver2
Python server on android, on local network. Used in a futur funny game.

L'application s'appelle Android_Server_2

### Apk build fails

Debian 9.2 64 bits en avril 2018
Voir 
VirtualBox 5.1.30
buildozer
kivy
twisted
python 2.7

* [Installation de debian](https://ressources.labomedia.org/debian_installation_configuration)
* [VirtualBox](https://ressources.labomedia.org/debian_installation_configuration#virtualbox)
* [Installation de kivy buildozer twisted](https://ressources.labomedia.org/kivy_buildozer_avec_python_2.7)

#### Buildozer fails with incremental

See https://stackoverflow.com/questions/49707807/buildozer-with-twisted-fails-because-it-cannot-find-incremental

#### Log

####" log_0.71.txt
requirements=incremental

pas de dossier incremental obtenu

####" log_0.72.txt
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

mais sans accents dans main.py

apk valide et fonctionnel
