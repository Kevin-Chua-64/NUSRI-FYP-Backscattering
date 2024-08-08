import tkinter as tk
import socket
import threading

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('BackCom GUI')
        self.geometry('500x300')
        self.setup()

    def setup(self):
        # Create canvas
        canvas = tk.Frame(self, height=300, width=400)
        canvas.pack(side=tk.TOP)
        title = tk.Label(canvas, text='Temperature Monitoring System', font=("Arial", 14, "bold"))
        title.place(x=50, y=15, width=300, height=40)
        index = tk.Label(canvas, text='Address            Temparature (\u2103)', font=("Arial", 12, "bold"), relief='ridge')
        index.place(x=50, y=60, width=300, height=40)
        addr = tk.Label(canvas, text='0x0000\n\n0x0001\n\n0x0010\n\n0x0011', font=("Arial", 12), relief='ridge')
        addr.place(x=50, y=90, width=120, height=160)

        # Set string variable
        self.info = tk.StringVar()
        self.info.set('...\n\n...\n\n...\n\n...')
        infoLabel = tk.Label(canvas, textvariable=self.info, font=("Arial", 12), relief='ridge')
        infoLabel.place(x=160, y=90, width=190, height=160)

    def updateInfo(self, info: str):
        # Current data
        temp = self.info.get()
        temp = temp.split('\n\n')
        # Received data
        info = info.split(' ')
        addr = int(info[0])
        # Update
        temp[addr] = info[1]
        self.info.set('\n\n'.join([temp[0], temp[1], temp[2], temp[3]]))


def udpUpdate(gui):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', 12000))
    print('The server is ready to receive:')
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        gui.updateInfo(message.decode())


def main():
    gui = Gui()

    t1 = threading.Thread(target=udpUpdate, args=(gui,))
    t1.start()

    gui.mainloop()


if __name__ == '__main__':
    main()
    