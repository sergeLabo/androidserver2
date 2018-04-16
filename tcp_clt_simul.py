#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket
from time import sleep


class LabTcpClient:
    """Envoi et réception sur le même socket en TCP.
    Toutes les méthodes sont sans try.
    """

    def __init__(self, ip, port, buffer_size=1024):

        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.server_address = (ip, port)
        self.data = None
        self.sock = None
        self.create_socket()

    def create_socket(self):
        """Création du socket sans try, et avec connexion."""

        while not self.sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect_sock()
            print("    Création du socket client {}".format(self.server_address))
            sleep(0.1)

    def connect_sock(self):
        """Connexion de la socket, si ok retoune 1 sinon None"""

        try:
            self.sock.connect(self.server_address)
            print("    Client connecté")
            return 1
        except:
            print("    Connexion impossible du client sur {}".
                  format(self.server_address))
            return None

    def send(self, msg):
        """Envoi d'un message, avec send, msg doit être encodé avant."""

        # Création d'un socket si besoin
        if not self.sock:
            self.create_socket()

        # Envoi
        try:
            self.sock.send(msg)
        except:
            print("Envoi raté: {}".format(msg))
            # Nouvelle création d'une socket
            self.sock.close()
            self.sock = None

    def reconnect(self):
        """Reconnexion."""

        self.sock = None
        self.create_socket()

    def close_sock(self):
        """Fermeture de la socket."""

        try:
            self.sock.close()
            print("Socket client fermée")
        except:
            print("La socket client est déjà close")

        self.sock = None

    def listen(self):
        """Retourne les data brutes reçues."""

        raw_data = None

        raw_data = self.sock.recv(self.buffer_size)

        return raw_data


if __name__ == "__main__":
    
    import sys

    ip = "192.168.1.4"
    port = 8000

    clt = LabTcpClient(ip, port)
    
    for num in range(20000):
        print(num)
        text = "abcdefghij " + str(num)
        clt.send(text.encode("utf-8"))

        sleep(1)
        
    clt.close_sock()
