import socket
import numpy as np
import matplotlib
matplotlib.use("TkAgg")   # Backend stabile per PyInstaller
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ================================
#  INPUT IP DA TASTIERA
# ================================
print("Inserisci l'indirizzo IP del WiFi_Terminal (es. 192.168.1.22):")
HOST = input("IP: ").strip()

PORT = 9000   # Porta TCP del bridge

# ================================
#  CONNESSIONE TCP
# ================================
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    print(f"Connesso al WiFi_Terminal ({HOST})")
except Exception as e:
    print(f"Errore di connessione a {HOST}:{PORT}")
    print(e)
    input("Premi INVIO per uscire...")
    exit()

# ================================
#  FUNZIONI START/STOP
# ================================
def send_start():
    try:
        s.sendall(b"VL53_START\n")
        print(">> START inviato")
    except:
        print("Errore invio START")

def send_stop():
    try:
        s.sendall(b"VL53_STOP\n")
        print(">> STOP inviato")
    except:
        print("Errore invio STOP")

# ================================
#  SETUP GRAFICO
# ================================
fig, ax = plt.subplots()
heatmap = ax.imshow(np.zeros((8,8)), cmap='jet', vmin=0, vmax=3000)
plt.colorbar(heatmap)

# ================================
#  AGGIORNAMENTO HEATMAP
# ================================
def update(frame):
    try:
        data = s.recv(4096).decode(errors="ignore").strip()
    except:
        return [heatmap]

    for packet in data.split("\n"):
        if packet.startswith("VL53|"):
            try:
                values = list(map(int, packet[5:].split(",")))
                if len(values) == 64:
                    matrix = np.array(values).reshape((8,8))
                    heatmap.set_data(matrix)
            except:
                pass

    return [heatmap]

ani = animation.FuncAnimation(fig, update, interval=10, blit=False)

# Avvio streaming
send_start()

plt.show()

# Stop streaming quando si chiude la finestra
send_stop()
s.close()

