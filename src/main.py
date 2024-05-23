import argparse
import getpass
import sys

from communication import ApiCaller, PayloadCommunication
from payload import ProgramRunner
from src.sysInfo import SystemInfo


def main():
    parser = argparse.ArgumentParser(description='Esegui un payload e fai una chiamata API.')
    parser.add_argument('payload_path', help='Il percorso del payload da avviare.')
    parser.add_argument('email', help='L\'email da utilizzare per la chiamata API.')
    args = parser.parse_args()

    if len(sys.argv) < 3:
        parser.print_help(sys.stdout)
        sys.exit(1)

    # Richiesta della password all'utente
    password = getpass.getpass('Inserisci la password: ')

    runner = ProgramRunner(args.payload_path)
    comms = PayloadCommunication()
    sys_info = SystemInfo()
    sys_info.get_all_resources()

    # Get authentication
    if not comms.login(args.email, password):
        print("Errore nel login")
        exit(1)

    # Recupera la risorsa assegnata
    if not sys_info.select_resource_byname(comms.get_resource(args.email)):
        print("Errore nel recuperare la risorsa assegnata.")
        comms.notify_payload_start()
        comms.notify_payload_end()
        exit(1)

    # Comunica l'avvio del payload
    comms.notify_payload_start()

    # Run the payload
    print("Starting Task...")
    stdin, stdout = runner.run()

    if stdout is None or stdin is None:
        print("Errore nell'avvio del payload.")
        exit(1)


if __name__ == '__main__':
    main()
