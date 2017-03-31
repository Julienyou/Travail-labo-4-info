Afin d'exécuter notre code sur un seul ordinateur, veuillez suivre les étapes suivantes :
Si vous souhaitez tester le code avec 2 ordinateurs, la seule différence est la suivante. Lors de l'exécution du point 3), il faut préciser l'adresse IP du serveur qui s'affiche lorsqu'on lance le serveur : "pyhton3 Chat_binome_1.py client 172.17....".

1) Allez dans votre terminal et rendez-vous dans le répertoire où se trouve le document.
2) Tapez "python3 Chat_binôme_2 server".
3) Ouvrez une nouvelle fenêtre qui vous servira de client et tapez "python3 Chat_binome_1 client". Avec un ordinateur Windows, il suffit d'écrire "python" au lieu de "python3".
4) Dans la fenêtre du client, il existe une multitude de commandes disponibles. Les voici :

/connect : Permet de se connecter au server. Grâce à cette action, votre pseudo est visible dans la liste des clients
et les autres chatteurs peuvent prendre contact avec vous. Afin de ne pas avoir deux fois le même pseudo dans la liste
 de clients, nous demandons aux personnes dont le nom figure déjà dans la liste d'encoder un nouveau pseudo.

/disconnect : Cette action permet d'arrêter toute action liée au chat sur son terminal, entre autre de s'enlever de
la liste des clients.

/quit : Permet de quitter la discussion avec un autre client.

/clients : Permet d'afficher la liste des clients connectés : par la suite, il est possible de joindre un des clients
en utilisant son nom avec la fonction join.

/join : Permet d'établir une liaison avec la personne souhaitée qui fait partie de le liste afin de communiquer. Pour
préciser avec qui vous voulez ouvrir la discussion, tapez "/join nom de la personne".

/send : Pour envoyer un msg, écrire "/send blablabla"

5) Pour établir la communication avec une autre personne connectée au serveur, il est nécessaire d'exécuter les
fonctions dans l'ordre suivant : Clients (pour savoir qui est connecté), /join pour joindre la personne souhaitée,
Send pour lui envoyer un message.

6) Une fois le dialogue terminé, il est important d'effectuer la fonction /quit afin de se retirer de la liste des
clients et ensuite la fonction /disconnect.

Description du protocole de communication : Nous utilisons le protocole UDP pour qu'un client puisse parler à un autre client et le protocole TCP pour que le client puisse communiquer avec le serveur.