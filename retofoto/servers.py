class Server:

    server_type = None

    def __init__(self, ip_address=None, mac_address=None, open_ports=None):
        self.ip_address = ip_address
        self.mac_address = mac_address

        if open_ports is None:
            open_ports = []
        else:
            self.open_ports = open_ports


class WebServer(Server):

    server_type = "web"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class SSHServer(Server):

    server_type = "ssh"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class TelnetServer(Server):

    server_type = "telnet"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class FTPServer(Server):

    server_type = "ftp"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class SMTPServer(Server):

    server_type = "smtp"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class POP3Server(Server):

    server_type = "pop3"
    # There will be more class specific properties here

    def __init__(self):
        super().__init__()


class IMAPServer(Server):

    server_type = "imap"
    # There will be more class specific properties here

    def __init_subclass__(cls) -> None:
        return super().__init__()
