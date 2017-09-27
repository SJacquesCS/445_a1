import socket
import os
import pygubu
import tkinter
import sys

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
            response = "httpc is a curl-like application but supports HTTP protocol only.\n\n" \
                       + "Usage: httpc command [arguments]\n\n" \
                       + "The commands are:\n" \
                       + "\tget\texecutes a HTTP GET request and prints the response.\n" \
                       + "\tpost\texecutes a HTTP POST request and prints the response.\n" \
                       + "\thelp\tprints this screen.\n\n" \
                       + "Use 'httpc help [command]' for more information about a command.\n\n"
        elif contents[2].lower() == "get":
            response = "Usage: httpc get [-v] [-h key:value] URL\n\n" \
                       + "Get executes a HTTP GET request for a given URL.\n\n" \
                       + "\t-v\tPrints the detail of the response such as protocol, status, and headers.\n" \
                       + "\t-h key:value\t\tAssociates headers to HTTP request with the format 'key:value'.\n"
        elif contents[2].lower() == "post":
            response = "Usage: httpc  httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n\n" \
                       + "Post executes a HTTP POST request for a given URL with inline data or from file.\n\n" \
                       + "\t-v\tPrints the detail of the response such as protocol, status, and headers.\n" \
                       + "\t-h key:value\t\tAssociates headers to HTTP request with the format 'key:value'.\n" \
                       + "\t-d string\t\tAssociates an inline data to the body HTTP POST request.\n" \
                       + "\t-f file\t\tAssociates the content of a file to the body HTTP POST request.\n\n" \
                       + "Either [-d] or [-f] can be used but not both.\n\n"

        response += "--------------------------------------------------------------------------\n\n"

        self.response.insert(tkinter.END, response)

    def get_request(self, contents, conn):
        request = ""
        verbose = False
        headers = False
        print('in get')

        contents[1] = "GET"

        # CHECK HERE FOR BUGS AND SHIT

        # if len(contents) > 2 and contents[2] == "-v":
        #     verbose = True
        #
        # if contents[2] == "-h" or contents[3] == "-h":
        #     headers = True

        contents.pop(0)

        for content in contents:
            request += str(content) + " "

        request += "HTTP/1.0\r\nHost: " + str(self.host.get()) + "\r\n\r\n"
        conn.connect((self.host.get(), int(self.port.get())))
        request = request.encode("utf-8")
        conn.send(request)
        message = conn.recv(4096)
        response = message.decode("utf-8")
        response += "\n\n--------------------------------------------------------------------------\n\n"
        self.response.insert(tkinter.END, str(response)) n

    def post_request(self, contents, conn):
        request = ""

        return request

    def send_request(self):
        goodrequest = nothelp = True
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            contents = self.request.get().rstrip("\r\n").split(" ")

            print(contents[1])

            if contents[0].lower() == "httpc":
                if contents[1].lower() == "help":
                    self.help_request(contents)
                    nothelp = False
                elif contents[1].lower() == "get":
                    self.get_request(contents, conn)
                elif contents[1].lower() == "post":
                    self.post_request(contents, conn)
                else:
                    goodrequest = False
            else:
                goodrequest = False

            if goodrequest:
                # line = self.request.get().rstrip("\r\n") + "HTTP/1.0\r\nHost: " + self.host.get() + "\r\n\r\n"
                #        # + "\r\n" + "Content-Type: application/json\r\n"\
                #        # + "Content-Length: 17\r\n\r\n{'Assignment': 1}"
                self.message.configure(text="Request accepted", foreground="green")
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
