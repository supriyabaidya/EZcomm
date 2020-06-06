from socket import socket
from struct import pack, unpack, calcsize, error
from sys import stdout
from traceback import print_exc

from EZcomm_frameworks.common_methods import unpack_data

"""
its framework for client only 
it contains methods like 
'socket_data_send' and 
'socket_data_receive'

"""


def socket_data_send(soc: socket, data: bytes):
    try:
        # data_to_be_send = json.dumps(data)
        # print("data_to_be_send")
        # print(data_to_be_send)
        temp_data = pack("!I", len(data)) + data
        # print("temp_data")
        # print(temp_data)
        if soc.sendall(temp_data):  # sendall returns None on success
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


def socket_data_receive(soc: socket):
    try:
        temp_buffer_size = calcsize("!I")
        temp_length = soc.recv(temp_buffer_size)
        length = unpack("!I", temp_length)[0]
        data_received = bytes()
        while len(data_received) < length:
            temp_data = soc.recv(length - len(data_received))
            if not temp_data:
                return None
            data_received += temp_data

        # print("data_received")
        # print(data_received)
        return data_received
    except OSError as err:
        print("OSError in socket_data_receive(): " + str(err.args))
        print_exc(file=stdout)
        return False
    except error as err:
        print("struct.error in socket_data_receive(): " + str(err.args))
        print_exc(file=stdout)
        return False


def handle_responses_from_server(response: bytes):
    unpacked_response = unpack_data(response)
    if unpacked_response:
        type_of_response: str = unpacked_response[0]
        if type_of_response == "text":
            handled_value = text_handler(response)
            if handled_value:
                return "text", handled_value  # handled_value is tuple contains sender, message
            else:
                return False
        elif type_of_response == "serv":
            handled_value = server_data_handler(response)
            if handled_value:
                return "serv", handled_value  # handled_value is dict whose key are each clients email and values are dict contains fd and addr
            else:
                return False
        elif type_of_response == "file":
            file_handler(response)
    else:
        print("Couldn't unpack the response in handle_responses_from_server().")
        return False


def text_handler(response: bytes):
    unpacked_response = unpack_data(response)
    if unpacked_response:
        sender: str = str(unpacked_response[1]["email"])
        message: str = str(unpacked_response[2], "utf-8")
        return sender, message
    else:
        print("Couldn't unpack the response in text_handler().")
        return False


def server_data_handler(response: bytes):
    unpacked_response = unpack_data(response)
    if unpacked_response:
        main_data: bytes = unpacked_response[2]
        str_main_data = str(main_data, "utf-8")

        # 1. if 'clients_lists' is received from server inside of main_data
        if str_main_data.__contains__("clients_lists"):
            # temp_clients_lists = str_main_data[str_main_data.index("{"):str_main_data.rindex("}") + 1]
            temp_clients_lists = str_main_data.replace("clients_lists", "")
            socket_clients_list: dict = None
            try:
                socket_clients_list = eval(temp_clients_lists)
            except NameError:
                print_exc(file=stdout)
            except SyntaxError:
                print_exc(file=stdout)
            except TypeError:
                print_exc(file=stdout)
            if not socket_clients_list:
                print("couldn't get socket_clients_list as VALUE of param 'response' is wrong.")
                return False

            return socket_clients_list

    else:
        print("Couldn't unpack the response in server_data_handler().")
        return False


def file_handler(response: bytes):
    unpacked_response = unpack_data(response)
    if unpacked_response:
        pass
    else:
        print("Couldn't unpack the response in file_handler().")
        return False
