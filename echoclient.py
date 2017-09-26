import socket
import os
import pygubu
import tkinter

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


class MyApplication(pygubu.TkApplication):
    def _create_ui(self):
        self.builder = builder = pygubu.Builder()

        builder.add_from_file(os.path.join(CURRENT_DIR, '445_a1.ui'))

        self.mainwindow = builder.get_object('mainwindow')
        self.request = builder.get_object('req_entry')
        self.host = builder.get_object('host_entry')
        self.port = builder.get_object('port_entry')
        self.response = builder.get_object('resp_text')
        self.popular = builder.get_object("pop_text")
        self.message = builder.get_object('msg_entry')
        self.message.configure(foreground="gray")

        builder.connect_callbacks(self)

    def quit(self):
        self.mainwindow.quit()

    def clear(self):
        self.response.delete("1.0", tkinter.END)
        self.message.configure(text="Enter a request, host, and port. Send the request to receive a reponse",
                               foreground="gray")

    def run(self):
        self.mainwindow.mainloop()

    def help_request(self, contents):
        response = ""

        print(len(contents))

        if len(contents) == 2:
            response = "httpc help\n\nhttpc is a curl-like application but supports HTTP protocol only.\n"\
                    + "Usage: \n\thttpc command [arguments]\n"\
                    + "The commands are:\n"\
                    + "\tget\texecutes a HTTP GET request and prints the response.\n"\
                    + "\tpost\texecutes a HTTP POST request and prints the response.\n"\
                    + "\thelp\tprints this screen.\n\n"\
                    + "Use 'httpc help [command]' for more information about a command.\n\n"
        elif contents[2].lower() == "get":
            response = "Usage: httpc get [-v] [-h key:value] URL\r\n\r\n"\
                        + "Get executes a HTTP GET request for a given URL.\r\n\r\n"\
                        + "\t-v\tprints the detail of the response such as protocol, status, and headers.\n\r\n\r"\
                        + "\t-h key:value\tassociates headers to HTTP request with the format 'key:value'.\n\n"

        response += "--------------------------------------------------------------------------\n\n"

        self.response.insert(tkinter.END, response)

    def get_request(self, contents):
        request = ""

        contents[1] = "GET"

        for content in contents:
            request += str(content) + " "

        return request

    def post_request(self, contents):
        request = ""

        return request

    def send_request(self):
        goodrequest = nothelp = True
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            line = self.request.get().rstrip("\r\n")
            contents = line.split(" ")

            print(contents[1])

            if contents[0].lower() == "httpc":
                if contents[1].lower() == "help":
                    self.help_request(contents)
                    nothelp = False
                elif contents[1].lower() == "get":
                    request = self.get_request(contents)
                elif contents[1].lower() == "post":
                    request = self.post_request(contents)
                else:
                    print("2")
                    goodrequest = False
            else:
                goodrequest = False
                print("1")

            if goodrequest and nothelp:
                request += "HTTP/1.0\r\nHost: " + str(self.host.get()) + "\r\n\r\n"
                self.message.configure(text="Request accepted", foreground="green")
                # line = self.request.get().rstrip("\r\n") + "HTTP/1.0\r\nHost: " + self.host.get() + "\r\n\r\n"
                #        # + "\r\n" + "Content-Type: application/json\r\n"\
                #        # + "Content-Length: 17\r\n\r\n{'Assignment': 1}"
                conn.connect((self.host.get(), int(self.port.get())))
                print(request)
                request = request.encode("utf-8")
                conn.send(request)
                # MSG_WAITALL waits for full request or error
                message = conn.recv(4096)
                response = message.decode("utf-8")
                response += "\n\n--------------------------------------------------------------------------\n\n"
                self.response.insert(tkinter.END, str() + "\r\n")
            else:
                self.message.configure(text="Request not accepted", foreground="red")
        finally:
            conn.close()


if __name__ == '__main__':
    root = tkinter.Tk()
    root.resizable(width=False, height=False)
    root.title("Jacques' Request System")
    app = MyApplication(root)
    app.run()
