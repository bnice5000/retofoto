class Helper:

    ip_range = None
    port_list = None

    # this might be better as a singleton. I will have to have a think on it.

    def scan_network(self, ip_range):
        pass

    def scan_server_ports(self, port_list=None):

        if port_list is None:
            self.port_list = []
        else:
            self.port_list = port_list

    def read_database(self):
        pass

    def write_database(self):
        pass

    def ip_longitudinal_compare(self):
        pass

    def detect_port_server_type(self):
        pass
