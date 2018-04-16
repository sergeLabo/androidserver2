#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


import os, sys
import subprocess
from time import time, sleep
import threading
import json
import ast
from Queue import Queue

# install_twisted_rector must be called before importing
# and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol, Factory

import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

from tools import datagram_decode, get_ip_address

QUEUE = Queue()


class MyMulticastSender(DatagramProtocol):
    """Envoi en continu a 1 fps 
    a tous les joueurs de l'IP de ce serveur .
    """

    def __init__(self, config):

        self.config = config
        self.multi_ip = self.config.get('network', 'multi_ip')
        self.multi_port = int(self.config.get('network', 'multi_port'))
        self.multi_addr = self.multi_ip, self.multi_port
        
        self.tempo = time()
        self.count = 0
        self.ip_server = get_ip_address()

        print("Envoi en multicast sur", self.multi_ip,
                                        self.multi_port)

    def startProtocol(self):
        """Called after protocol has started listening."""

        # Set the TTL>1 so multicast will cross router hops:
        # https://www.rap.prd.fr/pdf/technologie_multicast.pdf

        # preconise TTL = 1
        self.transport.setTTL(1)

        # Join a specific multicast group:
        self.transport.joinGroup(self.multi_ip)

        # Boucle infinie pour envoi continu a tous les joueurs
        self.send_loop_thread()

    def ip_msg(self):
        """Retourne msg encode avec l'ip serveur"""

        ip = {"ip": self.ip_server}
        ip_enc = json.dumps(ip).encode("utf-8")

        return ip_enc

    def send_loop(self):
        """{'ip': '192.168.1.17'}"""

        ip = self.ip_msg()
        msg = ("ip"+ str(ip)).encode("utf-8")
        addr = self.multi_ip, self.multi_port
        
        while 1:
            sleep(1)
            try:
                self.transport.write(msg, addr)
            except OSError as e:
                if e.errno == 101:
                    print("Network is unreachable")

    def send_loop_thread(self):
        thread_s = threading.Thread(target=self.send_loop)
        thread_s.start()


class MyTcpServer(Protocol):
    """Reception de chaque joueur en TCP."""

    def __init__(self, factory):
        
        print("MyTcpServer un client connecte")
        self.factory = factory
        self.create_user()
        self.tempo = time()

    def create_user(self):
        """Impossible d'avoir 2 user identiques"""

        self.user = "TCP" + str(int(10000* time()))[-8:]
        print("Un user cree: ", self.user)

    def connectionMade(self):
        self.addr = self.transport.client
        print("Une connexion etablie par le client {}".format(self.addr))

    def connectionLost(self, reason):
        print("Connection lost, reason:", reason)
        print("Connexion fermee avec le client {}".format(self.addr))

    def dataReceived(self, data):
        """ TODO: rajouter decode sorting"""
        
        global QUEUE
        
        if data:
            print("data", data)
            QUEUE.put(data)


class MyTcpServerFactory(Factory):
    """self ici sera self.factory dans les objets MyTcpServer."""

    def __init__(self):
        """L'objet gestion du jeu est construit ici.
        Il est accessible dans MyTcpServer avec self.factory.game
        """
        
        # Serveur
        self.numProtocols = 1
        print("Serveur twisted reception TCP lance\n")

    def buildProtocol(self, addr):
        print("Nombre de protocol dans factory", self.numProtocols)

        # le self permet l'acces a self.factory dans MyTcpServer
        return MyTcpServer(self)    


class MainScreen(Screen):
    """Ecran principal"""

    info = StringProperty()
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.display_info_thread()
        print("Initialisation de MainScreen ok")

    def display_info(self):
        
        global QUEUE
        
        while 1:
            sleep(0.02)
            try:
                data = QUEUE.get(block=False, timeout=0.001)
                print("data dans queue", data)
                self.info = data.decode("utf-8")
            except:
                data = None
                
    def display_info_thread(self):
        thread_d = threading.Thread(target=self.display_info)
        thread_d.start()

    
SCREENS = { 0: (MainScreen, "Main")}


class AndroidServerApp(App):
    
    def build(self):
        """Execute en premier apres run()"""

        # Creation des ecrans
        self.screen_manager = ScreenManager()
        for i in range(len(SCREENS)):
            self.screen_manager.add_widget(SCREENS[i][0](name=SCREENS[i][1]))

        return self.screen_manager

    def on_start(self):
        """Execute apres build()"""
        
       ## Receive
        tcp_port = int(self.config.get('network', 'tcp_port'))
        reactor.listenTCP(tcp_port, MyTcpServerFactory())

        ## Send: je reçois aussi ce que j'envoie
        multi_port = int(self.config.get('network', 'multi_port'))
        reactor.listenMulticast(multi_port,
                                MyMulticastSender(self.config),
                                listenMultiple=True)
        
    def build_config(self, config):
        """Si le fichier *.ini n'existe pas,
        il est cree avec ces valeurs par defaut.
        Si il manque seulement des lignes, il ne fait rien !
        """

        config.setdefaults('network',
                            { 'multi_ip': '224.0.0.11',
                              'multi_port': '18888',
                              'tcp_port': '8000',
                              'freq': '1'})

        config.setdefaults('kivy',
                            { 'log_level': 'debug',
                              'log_name': 'androidserver_%y-%m-%d_%_.txt',
                              'log_dir': '/toto',
                              'log_enable': '1'})

        config.setdefaults('postproc',
                            { 'double_tap_time': 250,
                              'double_tap_distance': 20})

    def build_settings(self, settings):
        """Construit l'interface de l'ecran Options,
        pour  le serveur seul, Kivy est par defaut,
        appele par app.open_settings() dans .kv
        """

        data =  """[{"type": "title", "title":"Reseau"},
                            {  "type":    "numeric",
                                "title":   "Frequence",
                                "desc":    "Frequence entre 1 et 60 Hz",
                                "section": "network", 
                                "key":     "freq"},
                             
                    {"type": "title", "title":"Reseau"},
                            {   "type":    "string",
                                "title":   "IP Multicast",
                                "desc":    "IP Multicast",
                                "section": "network", 
                                "key":     "multi_ip"},
                                
                    {"type": "title", "title":"Reseau"},
                            {   "type":    "numeric",
                                "title":   "Port Multicast",
                                "desc":    "Port Multicast",
                                "section": "network", 
                                "key":     "multi_port"},
                                
                    {"type": "title", "title":"Reseau"},
                            {   "type":    "numeric",
                                "title":   "TCP Port",
                                "desc":    "TCP Port",
                                "section": "network", 
                                "key":     "tcp_port"}
                    ]
                """

        # self.config est le config de build_config
        settings.add_json_panel('AndroidServer', self.config, data=data)

    def on_config_change(self, config, section, key, value):
        """Si modification des options, fonction appelee automatiquement
        """

        freq = int(self.config.get('network', 'freq'))
        menu = self.screen_manager.get_screen("Main")

        if config is self.config:
            token = (section, key)

            # If frequency change
            if token == ('network', 'freq'):
                # TODO recalcul tempo
                print("Nouvelle frequence", freq)

    def go_mainscreen(self):
        """Retour au menu principal depuis les autres ecrans."""

        #if touch.is_double_tap:
        self.screen_manager.current = ("Main")

    def do_quit(self):

        print("Je quitte proprement")

        # Kivy
        AndroidServerApp.get_running_app().stop()

        # Extinction de tout
        os._exit(0)


if __name__ == "__main__":
    AndroidServerApp().run()
