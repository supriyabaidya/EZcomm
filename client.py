import socket
import sys
import threading
import traceback

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from client2_designer import Ui_Client

from EZcomm_frameworks.common_methods import pack_data
from EZcomm_frameworks.client_methods import socket_data_receive, socket_data_send, handle_responses_from_server


#
# def data_receive(client_socket: socket.socket, buffer):
#     print("\ndata_receive is started : ")
#     while True:
#         try:
#             """receive start"""
#             length = client_socket.recv(4)  # 4=(max len) of words/chars ,i.e, up to 9999 chars are supported
#             if not length:
#                 return
#             loop_count = ceil(int(length) / int(buffer))
#             data = bytes("", "utf-8")
#             for i in range(loop_count):
#                 temp_data = client_socket.recv(buffer)
#                 data = data + temp_data
#             print(ctime(time()), " : ", str(data, "utf-8"))
#             """receive end"""
#         except ValueError:
#             traceback.print_exception(*(sys.exc_info()))
#         except EOFError:
#             traceback.print_exception(*(sys.exc_info()))
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt in client: ")
#         except ConnectionError:
#             traceback.print_exception(*(sys.exc_info()))
#
#
# def data_send(client_socket: socket.socket, buffer):
#     print("\ndata_send is started : " + buffer)
#     while True:
#         try:
#             """send start"""
#             data = bytes(input(">"), "utf-8")
#             if not data:
#                 return
#             client_socket.sendall(bytes(str(len(str(data, "utf-8"))), "utf-8"))  # sending length
#             client_socket.sendall(data)  # sending data
#             """send end"""
#         except ValueError:
#             traceback.print_exception(*(sys.exc_info()))
#         except EOFError:
#             traceback.print_exception(*(sys.exc_info()))
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt in client: ")
#         except ConnectionError:
#             traceback.print_exception(*(sys.exc_info()))
#
#
#
# class GuiClientEx(QtWidgets.QWidget, client_designer.Ui_Client):
#     def __init__(self):
#         super(GuiClientEx, self).__init__(flags=Qt.MSWindowsFixedSizeDialogHint)
#
#         self.setupUi(self)
#
#         self.setWindowIcon(QtGui.QIcon("client3.png"))
#         self.le_server_host.setText("127.0.0.1")
#         self.pb_connect.clicked.connect(pb_connect_callback)
#         self.pb_send.clicked.connect(pb_send_callback)
#         self.le_recepient_addr.setText("(\"127.0.0.1\",52892)")
#

class GuiClient2Ex(QtWidgets.QMainWindow, Ui_Client):
    def __init__(self):
        super(GuiClient2Ex, self).__init__(flags=Qt.MSWindowsFixedSizeDialogHint)

        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("client3.png"))
        self.le_host.setText("127.0.0.1")
        self.le_email.setText("@sb.com")
        self.pb_connect.clicked.connect(pb_connect_callback)
        self.pb_send.clicked.connect(pb_send_callback)
        # self.le_recepient_addr.setText("(\"127.0.0.1\",52892)")
        self.lv_clients.setModel(clients_list_model)


mainwindow_client: GuiClient2Ex = None
clients_list_model = QtGui.QStandardItemModel()
clients_list = dict()
email: str = ""

host = "127.0.0.1"
port = 8080
buffer_size = 512
server_address = (host, port)
socket_client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_connected = False


#
# def get_all_clients():
#     print("\nget_all_clients is started : ")
#     while True:
#         try:
#             if not socket_data_send(socket_client, "clients_lists"):
#                 break
#             """receive start"""
#             data_received = socket_data_receive(socket_client)
#             if data_received is None:  # no data is received
#                 sleep(20)
#                 continue
#             elif not data_received:  # Erro ocurred while socket_data_receive is called
#                 break
#             # print(ctime(time()), " : ", data_received)
#             """receive end"""
#
#             global clients_list
#             try:
#                 clients_list = eval(data_received)
#             except NameError:
#                 traceback.print_exc(file=sys.stdout)
#             except SyntaxError:
#                 traceback.print_exc(file=sys.stdout)
#             except TypeError:
#                 traceback.print_exc(file=sys.stdout)
#             except ValueError:
#                 traceback.print_exc(file=sys.stdout)
#             print("own: " + str(socket_client.getsockname()))
#             print(clients_list)
#             sleep(20)
#         except ValueError as err:
#             print("ValueError in get_all_clients(): " + str(err.args))
#             traceback.print_exc(file=sys.stdout)
#             return
#         except OSError as err:
#             print("OSError in get_all_clients(): " + str(err.args))
#             traceback.print_exc(file=sys.stdout)
#             sleep(5)
#             return
#


def get_all_responses_from_server():
    print("\nget_all_responses_from_server is started : ")
    while True:
        try:
            """receive start"""
            data_received = socket_data_receive(socket_client)
            if data_received is None:  # no data is received from socket_data_receive()
                continue
            elif not data_received:  # Error ocurred from socket_data_receive()
                break
            # print(ctime(time()), " : ", str(data_received),"utf-8")
            """receive end"""

            handled_value = handle_responses_from_server(data_received)
            if handled_value:
                # 1. 'text' handled result
                if handled_value[0] == "text":
                    try:
                        msg: str = "\nfrom '" + handled_value[1][0] + " : " + handled_value[1][1]
                        print(msg)
                        # mainwindow_client.te_output.setText(msg)
                    except BaseException:
                        traceback.print_exc(file=sys.stdout)
                    # print("from '" + handled_value[1][0], end="' : ")
                    # print(handled_value[1][1])

                # 2. 'serv' handled result
                if handled_value[0] == "serv":
                    global clients_list
                    clients_list = handled_value[1]
                    clients_list_model.clear()
                    for eachemail in iter(clients_list):
                        item = QtGui.QStandardItem(eachemail)
                        clients_list_model.appendRow(item)

        except ValueError as err:
            print("ValueError in get_all_clients(): " + str(err.args))
            traceback.print_exc(file=sys.stdout)
            return
        except OSError as err:
            print("OSError in get_all_clients(): " + str(err.args))
            traceback.print_exc(file=sys.stdout)
            return


def signin_request():
    try:
        signin_request_data = pack_data("text", {"fd": 0, "addr": socket_client.getsockname(), "email": email}, bytes("signin_request", "utf-8"))
        if not socket_data_send(socket_client, signin_request_data):
            return False
        return True
    except OSError as err:
        print("OSError in signin(): " + str(err.args))
        traceback.print_exc(file=sys.stdout)
        return False


def pb_connect_callback():
    try:
        global server_address
        global host
        host = mainwindow_client.le_host.text()
        server_address = (host, port)
        global email
        email = mainwindow_client.le_email.text()
        if email[0] == "@":
            print("please insert email")
            return
        print("Connecting to server : ", server_address)
        socket_client.connect(server_address)
        print("Connected to server : ", socket_client.getsockname())

        if not signin_request():
            print("couldn't sign in using the email: " + email)
            return

        global is_connected
        is_connected = True

        # widget.le_recepient_addr.setText(str(socket_client.getsockname()))
        thread_refresh_clients_list = threading.Thread(target=get_all_responses_from_server, daemon=True)
        # make the thread daemonic, to force stop running get_all_responses_from_server on exit
        thread_refresh_clients_list.start()
        """disable pb_connect"""
        mainwindow_client.pb_connect.setEnabled(False)
        mainwindow_client.le_host.setEnabled(False)
        mainwindow_client.le_email.setEnabled(False)
        """gui enable/visible"""
        """gui enable/visible end"""
    except OSError as err:
        print("OSError in pb_connect_callback(): " + str(err.args))
        traceback.print_exc(file=sys.stdout)
    finally:
        print("\npb_connect_callback is done.")


def pb_send_callback():
    try:
        selected_index = mainwindow_client.lv_clients.currentIndex()
        # print("selected_index")
        # print(selected_index)
        selected_item: QtGui.QStandardItem = clients_list_model.itemFromIndex(selected_index)
        if selected_item:
            selected_value = selected_item.text().strip()
            if selected_value == email:
                print("You DICKHEAD, select any client/recepient other than yourself")
            else:
                mainwindow_client.lbl_selected_client.setText(selected_value)
                test_addr: dict = clients_list[selected_value]
                temp_test_data = bytes(mainwindow_client.te_input.toPlainText(), "utf-8")

                test_data = pack_data("text", test_addr, temp_test_data)
                if socket_data_send(socket_client, test_data):
                    mainwindow_client.te_output.setText(mainwindow_client.te_output.toPlainText() + "\nfrom 'ME' : " + mainwindow_client.te_input.toPlainText())
                    mainwindow_client.te_input.clear()
                    print("successfully sent")
                else:
                    print("not sent")
        else:
            print("please select any client/recepient")

    except OSError as err:
        print("OSError in pb_send_callback(): " + str(err.args))
        traceback.print_exc(file=sys.stdout)
    except BaseException as err:
        print("OSError in pb_send_callback(): " + str(err.args))
        traceback.print_exc(file=sys.stdout)
    finally:
        print("\npb_send_callback is done.")


def main():
    """main entry point"""
    """gui"""
    app = QtWidgets.QApplication(sys.argv)
    global mainwindow_client
    mainwindow_client = GuiClient2Ex()
    """gui end"""
    """logic"""
    pb_connect_callback()
    """logic end"""
    mainwindow_client.show()
    a = app.exec_()
    # global ui_closed
    # ui_closed = True
    # print("Quiting...")
    # global get_all_clients_interval
    # sleep(get_all_clients_interval + 5)
    # print("server is shutting down or disconnected you...")
    if is_connected:
        print("disconnecting...")
        socket_client.shutdown(socket.SHUT_RDWR)
        socket_client.close()
        print("disconnected.")
        # input("Hit Enter to quit.\n")
    sys.exit(a)


if __name__ == '__main__':
    main()
