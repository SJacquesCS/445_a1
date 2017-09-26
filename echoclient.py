import socket
import sys
import argparse
import tkinter


def send_request(host, port, request, responsefield):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        line = request.rstrip("\r\n") + " HTTP/1.0\r\n" \
        + "Host: " + host + "\r\n" \
        + "Content-Type: application/json\r\n" \
        + "Content-Length: 17\r\n\r\n{'Assignment': 1}"
        conn.connect((host, int(port)))
        print("connected")
        print(line)
        newrequest = line.encode("utf-8")
        conn.send(newrequest)
        # MSG_WAITALL waits for full request or error
        message = conn.recv(4096)
        # responsefield.configure(text=str(message.decode("utf-8")))
        sys.stdout.write("Replied: " + message.decode("utf-8"))
    finally:
        conn.close()


window = tkinter.Tk()
window.title("Jacques' Requests")
window.resizable(width=False, height=False)

tkinter.Frame(height=5, relief=tkinter.SUNKEN).grid(row=0)
tkinter.Frame(width=5, relief=tkinter.SUNKEN).grid(column=0)

cmdlabel = tkinter.Label(window, text="Request: ").grid(row=1, column=1, sticky="W")
request = tkinter.Entry(window, width=100)
request.grid(row=1, column=2, columnspan=2, sticky="W")

tkinter.Frame(height=5, relief=tkinter.SUNKEN).grid(row=2)

hostlabel = tkinter.Label(window, text="Host: ").grid(row=3, column=1, sticky="W")
host = tkinter.Entry(window, width=20)
host.grid(row=3, column=2, sticky="W")

tkinter.Frame(height=5, relief=tkinter.SUNKEN).grid(row=4)

portlabel = tkinter.Label(window, text="Port: ").grid(row=5, column=1, sticky="W")
port = tkinter.Entry(window, width=10)
port.grid(row=5, column=2, sticky="W")

tkinter.Frame(height=5, relief=tkinter.SUNKEN).grid(row=8)

responselabel = tkinter.Label(window, text="Response: ").grid(row=9, column=1, sticky="W")
response = tkinter.Text(window, width=75, height=20)
response.grid(row=9, column=2, columnspan=2, sticky="W")

tkinter.Frame(height=5, relief=tkinter.SUNKEN).grid(row=6)

sendbutton = tkinter.Button(window, text="Send Request",
                            width=20, command=lambda: send_request(
                                            host.get(),
                                            port.get(),
                                            request.get(),
                                            response))
sendbutton.grid(row=7, column=2)

clearbutton = tkinter.Button(window, text="Clear All", width=20)
clearbutton.grid(row=7, column=3)

tkinter.Frame(height=5, relief=tkinter.SUNKEN).grid(row=10)
tkinter.Frame(width=5, relief=tkinter.SUNKEN).grid(column=4)

window.mainloop()
