import threading
from queue import Queue

# Création de la file pour l'historique des commandes
command_history = Queue()
command_history_lock = threading.Lock()
