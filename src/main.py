import argparse
import getpass
import sys

from communication import ApiCaller, PayloadCommunication
from payload import ProgramRunner


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

    # Get authentication
    if not comms.login(args.email, password):
        print("Errore nel login")
        exit(1)

    # Run the payload
    stdin, stdout = runner.run()

    if stdout is None or stdin is None:
        print("Errore nell'avvio del payload.")
        exit(1)

    # Comunica l'avvio del payload


if __name__ == '__main__':
    main()
