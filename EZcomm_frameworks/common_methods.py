from sys import stdout
from traceback import print_exc

"""
its framework for both server and client 
it contains methods like 
'unpack_data' and 
'pack_data'

"""


def unpack_data(packed_message: bytes):
    """
        :param packed_message: the data to be unpacked

        :return False on failure;;
        :return tuple (type_of_data: str, fd_address_email: dict {"fd":fd1,"addr":("host1",port1), "email":"email1"}, data: bytes) on success
    """

    type_of_data: str = str(packed_message[0:4], "utf-8")  # as length of the strings 'text' and 'file' are 4

    temp_fd_address_email = packed_message[packed_message.index(b"{"):packed_message.index(b"}") + 1]

    fd_address_email: dict = None
    try:
        fd_address_email = eval(temp_fd_address_email)
    except NameError:
        print_exc(file=stdout)
    except SyntaxError:
        print_exc(file=stdout)
    except TypeError:
        print_exc(file=stdout)
    if not fd_address_email:
        print("couldn't pack as fd_address_email part of value of param 'packed_message' is wrong.")
        return False

    data: bytes = packed_message[packed_message.index(b"}") + 1:]
    return type_of_data, fd_address_email, data


def pack_data(type_of_data: str, fd_address_email: dict, data: bytes):
    """
        :param type_of_data: type of data to be packed(appended at begining); values are 'text' and 'file' and 'serv' (these 3 only)
        :param fd_address_email: dict {"fd":fd1,"addr":("host1",port1), "email":"email1"}, combination of file descriptor(fd) and address to be packed(appended at middle)
        :param data: main data to be packed(appended at end)

        :return bytes on success;;
        :return False on failue
    """

    if type(type_of_data) != str:
        print("couldn't pack as TYPE of param 'type_of_data' is wrong.\nneeds => 'str'")
        return False
    if type_of_data != "text" and type_of_data != "file" and type_of_data != "serv":
        print("couldn't pack as VALUE of param 'type_of_data' is wrong.")
        print("needs type_of_data: values are 'text' and 'file' and 'serv' (these 3 only)")
        return False

    if type(fd_address_email) != dict:
        print("couldn't pack as TYPE of param 'fd_address_email' is wrong.\nneeds => 3-dict where 'fd' and 'addr' and 'email' are the keys")
        return False
    if len(fd_address_email) != 3:
        print("couldn't pack as LENGTH of param 'fd_address_email' is wrong.\nneeds => 3-dict where 'fd' and 'addr' and 'email' are the keys")
        return False
    elif type(fd_address_email["fd"]) != int:
        print("couldn't pack as TYPE of param 'fd_address_email[\"fd\"]' is wrong.\nneeds to be 'int'")
        return False
    elif type(fd_address_email["addr"]) != tuple:
        print("couldn't pack as TYPE of param 'fd_address_email[\"addr\"]' is wrong.\nneeds to be 'tupple'")
        return False
    elif type(fd_address_email["email"]) != str:
        print("couldn't pack as TYPE of param 'fd_address_email[\"email\"]' is wrong.\nneeds to be 'str'")
        return False
    if len(fd_address_email["addr"]) != 2:
        print("couldn't pack as LENGTH of param 'fd_address_email[\"addr\"]' is wrong.\nneeds => 2-tuple (host: str, port: int)")
        return False
    elif type(fd_address_email["addr"][0]) != str:
        print("couldn't pack as TYPE of param 'fd_address_email[\"addr\"][0]' is wrong.\nneeds first value of 2-tuple => host: 'str'")
        return False
    elif type(fd_address_email["addr"][1]) != int:
        print("couldn't pack as TYPE of param 'fd_address_email[\"addr\"][1]' is wrong.\nneeds second value of 2-tuple => port: 'int'")
        return False

    return bytes(type_of_data, "utf-8") + bytes(str(fd_address_email), "utf-8") + data
