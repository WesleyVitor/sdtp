import struct
import array
import socket

###########################
## CONSTANTES
###########################

# Flags segundo a RFC do TCP
TH_FIN = 0x01 # Finalize
TH_SYN = 0x02 # Synchronize
TH_RST = 0x04 # Reset
TH_PUSH= 0x08 # Push (NAO USADA)
TH_ACK = 0x10 # Acknowledgment
TH_URG = 0x20 # Urgent (NAO USADA)

# Constantes usadas pelo protocolo
IP           = "127.0.0.1" # IP do servidor
PORTA        = 21020       # Porta de conexao com o servidor
MSS          = 255         # Maximo tamanho do payload (\f$2^8-1\f$)
MAXSDTP      = 10 + MSS    # Tamanho do cabecalho + MSS
LOREMSIZE    = 6328        # Total de bytes do arquivo a ser enviado
ALPHA        = 0.125       # Valor inicial do \f$\alpha\f$
BETA         = 0.25        # Valor inicial do \f$\beta\f$
ESTIMATEDRTT = 250         # RTT estimado inicial (ms)
DEVRTT       = 0           # Desvio do RTT estimado inicial (ms)



###########################
## FUNCOES
###########################

# calculo do checksum
def compute_checksum(packet):
    if len(packet) % 2 != 0:
        packet += b'\0'
    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff


# Funcao que cria um pacote SDTP
def sdtphdr(seqnum,  # Numero de sequencia
            acknum,  # Numero de confirmacao
            datalen, # Tamanho dos dados no segmento
            flags,   # Campo de flags
            window  # Tamanho da janela
            #checksum = 0 # Soma de verificacao (sera calculada)
            ):
        
        # criando o pacote
        packet = struct.pack(
            'HHBBHH', # representacao do tamanho de cada campo
            seqnum,   # H - 16 bits
            acknum,   # H - 16 bits
            datalen,  # B - 8 bits
            flags,    # B - 8 bits
            window,   # H - 16 bits
            0 # checksum # H - 16 bits
            # NOTE: o checksum sera inicialmente zero, depois calculado
        )
    
        # adicionando (concatenando) o valor calculado do checksum
        packet = packet[:8] + struct.pack('H', compute_checksum(packet))

        return packet


# cria uma funcao que aguarda no socket 's' por 't' milissegundos
def recvtimeout(s, t):
    # convertendo de milissegundo para segundo
    s.settimeout(t/1000)
    
    try:
        # Recebendo o pacote do servidor com sucesso
        p, addr = s.recvfrom(MAXSDTP)
    
        # TODO: ver se precisa tratar o erro -1 (erro de recepcao)
    except socket.timeout:
        # Pacote perdido por timeout
        return -2
    
    # retornando o pacote recebido
    return p       
class Pacote:
    def __init__(self, seqnum=0,acknum=0,datalen=0,flags=0,window=0,checksum=0) -> None:
        self.seqnum = seqnum
        self.acknum = acknum
        self.datalen = datalen
        self.flags = flags
        self.window = window
        self.checksum = checksum

def create_object_pacote(p):
    seqnum = struct.unpack("H", p[0:2])
    acknum = struct.unpack("H", p[2:4])
    datalen = p[4]
    flags = p[5]
    window = struct.unpack("H", p[6:8])
    checksum = struct.unpack("!H", p[8:10])

    return Pacote(seqnum,acknum,datalen,flags,window,checksum)
# imprime o pacote
def print_packet(p:Pacote):
    print("Imprimindo o pacote:")
    print("\tseqnum: %d" % p.seqnum)
    print("\tacknum: %d" % p.acknum)
    print("\tdatalen: %d" % p.datalen)
    print("\tflags: 0x%x" % p.flags)
    print("\twindow: %d" % p.window)
    print("\tchecksum: 0x%x" % p.checksum)


# references: 
# 1. https://kytta.medium.com/tcp-packets-from-scratch-in-python-3a63f0cd59fe
# 2. https://docs.python.org/3/library/struct.html

