import argparse
import getpass
import sys
import time

from communication import PayloadCommunication
from payload import ProgramRunner
from src.sysInfo import SystemInfo

def on_error(e, func):
    print(f"Errore nell'avvio: {e}")
    func.notify_payload_start()
    func.notify_payload_end()
    exit(1)



def main():
    parser = argparse.ArgumentParser(description='Esegui il payload.')
    parser.add_argument('payload_path', help='Il percorso del payload da avviare.')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help(sys.stdout)
        sys.exit(1)

    # Richiesta della password all'utente
    email = input('Inserisci l\'email: ')
    password = getpass.getpass('Inserisci la password: ')
    resourceId = input('Inserisci l\'id dell\'assignment: ')

    runner = ProgramRunner(args.payload_path)
    comms = PayloadCommunication(email=email, resource_id=resourceId)

    sys_info = SystemInfo()
    sys_info.get_all_resources()

    # Get authentication
    if not comms.login(password):
        exit(1)

    # Recupera la risorsa assegnata
    if not sys_info.select_resource_byname(comms.get_resource()):
        print("Errore nel recuperare la risorsa assegnata.")
        comms.notify_payload_start()
        comms.notify_payload_end()
        exit(1)

    # Comunica l'avvio del payload
    try:
        comms.notify_payload_start()
    except Exception as e:
        on_error(e, comms)

    # Run the payload
    print("Starting Task...")
    try:
        stdin, stdout = runner.run()

        while True:
            if stdout is not None:
                output = stdout.readline()
                if output == '':
                    break
                if output:
                    print(output.strip())
            else:
                print("Errore durante esecuzione.")
                break


            time.sleep(0.1)

        if stdout is None or stdin is None:
            print("Errore nell'avvio del payload.")
            comms.notify_payload_end()
            exit(1)

    except Exception as e:
        print(f"Errore nell'avvio del payload: {e}")
        comms.notify_payload_end()
        exit(1)



if __name__ == '__main__':
    main()
