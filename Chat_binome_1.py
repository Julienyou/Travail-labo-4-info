import socket
import sys
import threading
import subprocess
import json
import time

SERVERADDRESS = (socket.gethostname(), 6000)


class AdderServer:
    a = socket.getaddrinfo(*SERVERADDRESS)[1][4]
    ip, port = a[0], a[1]
    b = (ip, port)
    clients = {}
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        print('listen to', self.b, '\n')

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                self._handle(client, addr)
                client.close()
            except OSError:
                print('Erreur lors du traitement de la requête du client.', '\n')

    def _handle(self, client, addr):
        data = client.recv(64).decode()
        a = data.split(' ')
        listname = []
        for i in self.clients:
            listname.append(i)

        if a[0] == 'connect':
            if a[1] in listname:
                name = b'existing'
                client.send(name)
                pseudo = client.recv(1024).decode()
                while pseudo in listname:
                    client.send(name)
                    pseudo = client.recv(1024).decode()
                name = b'ok'
                client.send(name)
                self.clients[pseudo] = addr[0]
                print(pseudo , ' connecté')
            else:
                self.clients[a[1]] = addr[0]
                print(a[1] , ' connecté')
                #print(self.clients, '\n')
            return self.clients
        elif a[0] == 'clients':
            dicojson = json.dumps(self.clients).encode()
            client.send(dicojson)
        elif a[0] == 'disconnect':
            self.clients.pop(a[1])
            #print(self.clients, '\n')
            return self.clients
        else:
            pass


class AdderClient:
    def __init__(self, addr=socket.gethostname()):
        self.__serveraddr = (addr, 6000)
        self.__data = self.Who()
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind(('0.0.0.0', 5000))
        self.__s = s    
        
    def run(self):
        handlers = {
            '/disconnect': self._disconnect,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/clients': self._clients,
            '/connect': self._connect
        }

        self.__running = True
        self.__address = None
        threading.Thread(target=self._receive).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            command = line[:line.index(' ')]
            param = line[line.index(' ') + 1:].rstrip()
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except OSError:
                    print('Erreur lors de l\'exécution de la commande.')
            else:
                print('Commande inconnue:', command, '\n')
                
    def _help(self):
        
        hanlers = {
            '/disconnect': self._disconnect,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/clients': self._clients,
            '/connect': self._connect,
        }
        for command in handlers:
            print(command, '\n')
            
    def _connect(self):
        try:
            s = socket.socket()
            s.connect(self.__serveraddr)
            totalsent = 0
            msg = b'connect ' + self.__data.encode()
            while totalsent < len(msg):
                sent = s.send(msg[totalsent:])
                totalsent += sent
            existance = s.recv(1024)
            while existance == b'existing':
                    pseudo = input('Il y a déjà une personne ayant ce nom, veuillez entrer un pseudo:\n')
                    s.send(pseudo.encode())
                    existance = s.recv(1024)
            print('Connecté au serveur', '\n')
        except OSError:
            print("Connexion échouée.", '\n')

    def _disconnect(self):                    #quit everything
        try:
            s = socket.socket()
            s.connect(self.__serveraddr)
            totalsent = 0
            msg = b'disconnect ' + self.__data.encode()
            while totalsent < len(msg):
                sent = s.send(msg[totalsent:])
                totalsent += sent
            self.__running = False
            self.__address = None
            s.close()
            print('Déconnecté du serveur', '\n')
        except OSError:
            print('Déconnexion échouée.', '\n')

    def _quit(self):
        self.__address = None

    def _join(self, param):
        dico = self._client()
        ip = dico[param]
        if param != None and len(param) > 0:
            try:
                self.__address = (ip, 5000)
                print('Connecté à {}'.format(param), '\n')
            except OSError:
                print('Erreur lors de la jonction avec', param, '\n')

    def _send(self, param):
        if self.__address is not None:
            try:
                namedmessage = self.Who() + ": " + param
                message = namedmessage.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Erreur lors de l\'envoi du message.', '\n')

    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(512)
                print(data.decode(), '\n')
                sys.stdout.flush()
            except socket.timeout:
                pass
            except OSError:
                return

    def _clients(self):
        try:
            s = socket.socket()
            s.connect(self.__serveraddr)
            totalsent = 0
            msg = b'clients ' + self.__data.encode()
            while totalsent < len(msg):
                sent = s.send(msg[totalsent:])
                totalsent += sent
            print('Requête réussie\n')
            time.sleep(0.5)
            dico = json.loads(s.recv(512).decode())
            for name in dico:
                print(name, ': ', dico[name], '\n')
        except OSError:
            print('Requête échouée:','\n')

    def _client(self):
        try:
            s = socket.socket()
            s.connect(self.__serveraddr)
            totalsent = 0
            msg = b'clients ' + self.__data.encode()
            while totalsent < len(msg):
                sent = s.send(msg[totalsent:])
                totalsent += sent
            dico = json.loads(s.recv(512).decode())
            return dico
        except OSError:
            print('Requête échouée:','\n')

    def Who(self):
        proc = subprocess.Popen(['Whoami'], stdout=subprocess.PIPE,
                                universal_newlines=True)
        out, err = proc.communicate()
        if '\\' in str(out):                                        # the name is for example julien\julien
            spl = out.split('\\')                                   # we separate both names
            user = spl[0]                                           # and take the first one
        else:
            user = out

        return str(user)                                            # return found name


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        AdderServer().run()
    elif len(sys.argv) == 2 and sys.argv[1] == 'client':
        AdderClient().run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        AdderClient(sys.argv[2]).run()
