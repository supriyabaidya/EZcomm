from socket import gethostname
from socketserver import ThreadingTCPServer
from sys import stdout
from traceback import print_exc

from EZcomm_frameworks.ezcommrequesthandler import EzCommRequestHandler

host = ""
port = 8080
server_address = (host, port)
socket_server: ThreadingTCPServer = None


# noinspection PyUnboundLocalVariable
def start_server():
    try:
        global socket_server
        with ThreadingTCPServer(server_address, EzCommRequestHandler) as socket_server:
            socket_server.daemon_threads = True  # make all threads(all ThreadingTCPServer thread for each client request) daemonic, to force stop all running client request(EzCommRequestHandler) handler on exit
            # socket_server = socketserver.TCPServer(server_address, EzCommRequestHandler)
            print("Server is started at host:", gethostname())
            print("Server is started at address:", server_address)
            # socket_server.allow_reuse_address = True  # not working CHECK?
            print("Waiting for client")
            socket_server.serve_forever()
    except OSError as err:
        print("OSError in start_server(): " + str(err.args))
        print_exc(file=stdout)
        # traceback.print_exception(*(sys.exc_info()))
    except KeyboardInterrupt:
        print("KeyboardInterrupt in start_server()")
    finally:
        print("\nstart_server is done.")


#
# class GuiServer(QtWidgets.QWidget):
#     def __init__(self):
#         super(GuiServer, self).__init__(flags=Qt.MSWindowsFixedSizeDialogHint)
#
#         self.ui = server_designer.Ui_Server()
#         self.ui.setupUi(self)
# class GuiServer2Ex(QtWidgets.QMainWindow, server2_designer.Ui_Server):
#     def __init__(self):
#         super(GuiServer2Ex, self).__init__(flags=Qt.MSWindowsFixedSizeDialogHint)
#
#         self.setupUi(self)
#         self.setWindowIcon(QtGui.QIcon("server3.png"))


def main():
    start_server()
    # thread_start_server = threading.Thread(target=start_server, daemon=True)
    # thread_start_server.start()
    # thread_start_server.join()

    if socket_server is not None:
        print("server is shutting down...")
        socket_server.shutdown()
        socket_server.server_close()
        print("server is shut down.")
        input("Hit Enter to quit.\n")


if __name__ == "__main__":
    main()
