
import socket

# importando as constantes e funcoes de sdtp.py
from sdtp import *

# criando um socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def three_way_handshake():
    # criando um pacote SDTP
    pout = sdtphdr(0, 0, 0, TH_SYN, 0)
    pacote_pout = create_object_pacote(pout)
    # imprimindo o pacote
    print("Pacote enviado:")
    print_packet(pacote_pout)
    pin = -2
    while pin ==-2:
        # enviando o pacote SDTP para o servidor
        s.sendto(pout, (IP, PORTA))

        # # recebendo um pacote pelo socket 's' e aguardando 2 segundos
        pin = recvtimeout(s, 2000)
    
        if pin == -2:
            print("Erro de timeout - reenviar o pacote")
    pacote = create_object_pacote(pin)
    print("Pacote recebido:")
    print_packet(pacote)

    return pacote
def read_bytes_file(pacote3wayhandshake):
    
    #abrindo o arquivo
    with open('lorem_ipsum.txt','r') as file:

        line = file.read(MSS)
        seqnum = 0
        window = 0
        checksum = 0
        window = 0
        lido = MSS
        while True:
            # criando um pacote SDTP
            pout = sdtphdr(seqnum, 0, MSS, 0, window)
            pacote_pout = create_object_pacote(pout)
            # imprimindo o pacote
            print("Pacote enviado:")
            print_packet(pacote_pout)

            pin = -2
            pacote:Pacote = Pacote()
            while pin ==-2:
                # enviando o pacote SDTP para o servidor
                s.sendto(pout, (IP, PORTA))

                # # recebendo um pacote pelo socket 's' e aguardando 2 segundos
                pin = recvtimeout(s, 2000)
                
                
                if pin == -2:
                    print("Erro de timeout - reenviar o pacote")
                else: # Se Não for -2, então pin é um pacote
                    pacote = create_object_pacote(pin)
                    checksumPout = compute_checksum(pin)
                    if pacote.checksum[0] != checksumPout:
                        print("Pacote Corrompido - reenviar o pacote")
                        pin=-2
                        continue
            
            seqnum = seqnum + pacote.datalen
            window = window + pacote.window[0]
            lido = lido+pacote.acknum[0]
            if (LOREMSIZE - lido) < MSS:
                line = file.read(LOREMSIZE - lido)
            else:
                line = file.read(MSS)

            if not line:
                break
        print("Arquivo enviado com sucesso!")

pacote3wayhandshake:Pacote = three_way_handshake()
read_bytes_file(pacote3wayhandshake)



    





    


# references: 
# 1. https://wiki.python.org/moin/UdpCommunication

