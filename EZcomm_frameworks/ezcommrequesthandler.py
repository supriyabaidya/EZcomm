from socket import socket, fromfd, AF_INET, SOCK_STREAM
from socketserver import BaseRequestHandler
from struct import pack, unpack, calcsize, error
from sys import stdout
from threading import Thread
from traceback import print_exc

from time import sleep

from EZcomm_frameworks.common_methods import pack_data, unpack_data

"""
its framework for server only 
it contains class like 
'EzCommRequestHandler'
and method like 'socket_data_send_to'

"""


def socket_data_send_to(soc: socket, data: bytes):
    try:
        temp_data = pack("!I", len(data)) + data
        if soc.sendall(temp_data):  # sendall returns None on success
            print("Failed to transfer all data")
            return False

        return True  # returns True on success
    except OSError as err:
        print("OSError in socket_data_send_to(): " + str(err.args))
        print_exc(file=stdout)
        return False
    except error as err:
        print("struct.error in socket_data_send_to(): " + str(err.args))
        print_exc(file=stdout)
        return False


class EzCommRequestHandler(BaseRequestHandler):
    # clients_list = []
    socket_clients_list = []
    socket_clients_dict = dict()
    """ format of the dictionar 'socket_clients_dict'
        {
            "email1": {"fd":fd1,"addr":("host1",port1)},
            "email2": {"fd":fd2,"addr":("host2",port2)}
        }
    """

    def setup(self):
        self.socket_client: socket = self.request
        # self.clients_list.append(self.client_address)
        self.client_email: str = ""
        self.socket_clients_list.append(self.socket_client)
        print("\nsetup is called.\nConnected to client : ", self.client_address)  # self.client_address is the raddar i.e, self.request.getpeername()
        # print(self.clients_list)
        print(self.socket_clients_list)

    def socket_data_send(self, data: bytes):
        try:
            temp_data = pack("!I", len(data)) + data
            if self.socket_client.sendall(temp_data):  # sendall returns None on success
                print("Failed to transfer all data")
                return False

            return True  # returns True on success
        except OSError as err:
            print("OSError in socket_data_send(): " + str(err.args))
            print_exc(file=stdout)
            return False
        except error as err:
            print("struct.error in socket_data_send(): " + str(err.args))
            print_exc(file=stdout)
            return False

    def socket_data_receive(self):
        try:
            temp_buffer_size = calcsize("!I")
            temp_length = self.socket_client.recv(temp_buffer_size)
            length = unpack("!I", temp_length)[0]
            data_received = bytes()
            while len(data_received) < length:
                temp_data = self.socket_client.recv(length - len(data_received))
                if not temp_data:
                    return None
                data_received += temp_data

            return data_received
        except OSError as err:
            print("OSError in socket_data_receive(): " + str(err.args))
            print_exc(file=stdout)
            return False
        except error as err:
            print("struct.error in socket_data_receive(): " + str(err.args))
            print_exc(file=stdout)
            return False

    def data_passing(self):
        """
        taking data from one client and send it to another client

        :return: None
        """
        print("\ndata_passing is started : ")
        while True:
            try:
                data_received = self.socket_data_receive()
                if data_received is None:  # no data is received
                    continue
                elif not data_received:  # Ending data_serve forcebly (Error ocurred from socket_data_receive())
                    print("error while fetching data in data_passing() from: " + str(self.client_address))
                    break

                unpacked_data_received = unpack_data(data_received)
                if unpacked_data_received:
                    type_of_data: str = unpacked_data_received[0]
                    main_data: bytes = unpacked_data_received[2]
                    data_to_be_send = pack_data(type_of_data, {"fd": self.socket_client.fileno(), "addr": self.client_address, "email": self.client_email},
                                                main_data)  # packed_data with sender's fd_address_email info
                    recepient_fd: int = unpacked_data_received[1]["fd"]
                    try:
                        recepient_socket: socket = fromfd(recepient_fd, AF_INET, SOCK_STREAM)
                        socket_data_send_to(recepient_socket, data_to_be_send)
                    except OSError as err:
                        print("OSError for socket_data_send_to in data_passing(): " + str(err.args))
                        print("recepient_fd does not exit as recepient_socket is closed")
                else:
                    print("Couldn't unpack the data_received in data_passing().")

            except ValueError as err:
                print("ValueError in data_passing(): " + str(err.args))
                print_exc(file=stdout)
                print("\ndata_passing() is done for: " + str(self.client_address))
                return
            except OSError as err:
                print("OSError in data_passing(): " + str(err.args))
                print_exc(file=stdout)
                print("\ndata_passing() is done for: " + str(self.client_address))
                return
        print("\ndata_passing() is done for: " + str(self.client_address))

    def send_all_clients_list(self):
        print("\nsend_all_clients_list is started : ")
        while True:
            try:
                packed_clients_lists = pack_data("serv", {"fd": 0, "addr": self.client_address, "email": ""}, bytes("clients_lists" + str(self.socket_clients_dict), "utf-8"))
                if packed_clients_lists:
                    if not self.socket_data_send(packed_clients_lists):
                        print("error while sending 'socket_clients_list' to: " + str(self.client_address))
                        break
                    # else:
                    #     print(self.socket_clients_list)
                    # break  # remove it
                else:
                    print("Couldn't pack the 'clients_lists' in send_all_clients_list().")
                sleep(10)

            except ValueError as err:
                print("ValueError in send_all_clients_list(): " + str(err.args))
                print_exc(file=stdout)
                print("\nsend_all_clients_list() is done for: " + str(self.client_address))
                return
            except OSError as err:
                print("OSError in send_all_clients_list(): " + str(err.args))
                print_exc(file=stdout)
                print("\nsend_all_clients_list() is done for: " + str(self.client_address))
                return
        print("\nsend_all_clients_list() is done for: " + str(self.client_address))

    def signin_response(self):
        try:
            signin_response_received = self.socket_data_receive()
            if signin_response_received is None:  # no data is received
                return False
            elif not signin_response_received:  # Ending signin_response forcebly (Error ocurred from socket_data_receive())
                return False

            unpacked_signin_response_received = unpack_data(signin_response_received)
            if unpacked_signin_response_received:
                msgbody: str = str(unpacked_signin_response_received[2], "utf-8")
                if msgbody.__contains__("signin_request"):
                    fd_addr_email: dict = unpacked_signin_response_received[1]
                    email: str = fd_addr_email["email"]
                    fd_addr_email["fd"] = self.socket_client.fileno()  # assigning fd of eachclient[serverside]
                    self.socket_clients_dict[email] = fd_addr_email
                    self.client_email = email
            else:
                return False
            return True
        except OSError as err:
            print("OSError in signin_response(): " + str(err.args))
            print_exc(file=stdout)
            return False

    def handle(self):
        try:
            print("\nrequest handle is started")
            if not self.signin_response():
                print("couldn't sign in the user: " + self.client_address)
                return
            thread_send_all_clients_list = Thread(target=self.send_all_clients_list, daemon=True)
            # make all threads(all send_all_clients_list thread) daemonic, to force stop all running data_serve
            thread_send_all_clients_list.start()

            thread_data_passing = Thread(target=self.data_passing, daemon=True)
            # make all threads(all data_passing thread) daemonic, to force stop all running data_serve
            thread_data_passing.start()

            # on clients quit data_passing completed first(as it calls self.socket_data_receive() on first line for wait to recv) then send_all_clients_list,
            # that why join on send_all_clients_list is called before data_passing to wait for both of them to complete
            thread_send_all_clients_list.join()  # to wait in handle until execution of send_all_clients_list() is compeleted
            thread_data_passing.join()  # to wait in handle until execution of data_passing() is compeleted
            print("\nrequest handle is done")
        except OSError as err:
            print("OSError in handle(): " + str(err.args))
            print_exc(file=stdout)
            return

    def finish(self):
        # self.clients_list.remove(self.client_address)
        self.socket_clients_list.remove(self.socket_client)
        del self.socket_clients_dict[self.client_email]
        self.socket_client.close()
        print("\nfinish is called.\nDisconnected the client.\n")
