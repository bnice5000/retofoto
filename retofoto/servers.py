#!/usr/bin/env python

"""retrofoto servers for OPSC-540 final project.

These are the server classes to work with server specific configurations.

__author__ = "Brian Levin"
__copyright__ = "Copyright 2022, Brian Levin"
__credits__ = ["Brian Levin", "Todd Strunce"]
__license__ = "AGPL"
__version__ = "0.0.1"
__maintainer__ = "Brian Levin"
__email__ = "brian.levin@mymail.champlain.edu"
__status__ = "Assignment"
__note__ = "This is experimental and could use error handling. Use at your own peril!"
"""


class Server:
    """The server base class. This is the generic class from which all other server classes inherit.

    These classes are used to construct other classes. The classes are then used to write the information to the database.
    This class will also be used if there is an open port but no specific guess as to its server type.
    """

    server_type = None

    def __init__(self, ip_address=None, mac_address=None, open_ports=None):
        """The initializer of the server base class

        Args:
            ip_address (str, optional): the IP address of the server. Defaults to None.
            mac_address (str, optional): the mac address of the server. Defaults to None.
            open_ports (list[str], optional): the open ports on the server. Defaults to None.
        """
        self.ip_address = ip_address
        self.mac_address = mac_address

        if open_ports is None:
            open_ports = []
        else:
            self.open_ports = open_ports


class WebServer(Server):
    """A web server

    If the server is determined to be a web server this class will contain the properties and methods to handle a scrap of the landing page.
    It will also look for additional information that tends to exist on web servers such as the server type (apache, nginx, iis) and any potentially related database connections.

    Args:
        Server (obj): The parent server class
    """

    server_type = "web"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class SSHServer(Server):
    """An SSH server

    Args:
        Server (obj): The parent server class

        If the server is determined to be an SSH server this class will contain the properties and methods to handle interacting with the server.
        It will also look to see if a login prompt is offered and probe it for standard misconfigurations.
    """

    server_type = "ssh"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class TelnetServer(Server):
    """A telnet server

    Args:
        Server (obj): the parent server class

        If the server is determined to be a telnet server this class will contain the properties and methods to handle interacting with the server.
        It will also look to see if a login prompt is offered and probe it for standard misconfigurations.

    """

    server_type = "telnet"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class FTPServer(Server):
    """An FTP server

    Args:
        Server (obj): the parent server class

        If the server is determined to be an FTP server this class will contain the properties and methods to handle interacting with the server.
        It will also look to see if a login prompt is offered and probe it for standard misconfigurations.

    """

    server_type = "ftp"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class SMTPServer(Server):
    """An SMTP server

    Args:
        Server (obj): the parent server class

        If the server is determined to be an SMTP server this class will contain the properties and methods to handle interacting with the server.
        It will also look to see if a login prompt is offered and probe it for standard misconfigurations.

    """

    server_type = "smtp"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class POP3Server(Server):
    """A POP server

    Args:
        Server (obj): the parent server class

        If the server is determined to be a POP3 server this class will contain the properties and methods to handle interacting with the server.
        It will also look to see if a login prompt is offered and probe it for standard misconfigurations.

    """

    server_type = "pop3"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class IMAPServer(Server):
    """An IMAP server

    Args:
        Server (obj): the parent server class

        If the server is determined to be an IMAP server this class will contain the properties and methods to handle interacting with the server.
        It will also look to see if a login prompt is offered and probe it for standard misconfigurations.

    """

    server_type = "imap"
    # There will be more class specific properties here

    def __init_subclass__(cls) -> None:
        return super().__init__()
