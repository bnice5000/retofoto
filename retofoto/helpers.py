#!/usr/bin/env python

"""retrofoto helper for OPSC-540 final project.

These are the helper classes to work with networking and data storage.

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

import sqlalchemy


class Helper:
    """These are the helper classes.

    The helper classes do things like scan the network and write to the database.
    """

    ip_range = None
    port_list = None

    # this might be better as a singleton. I will have to have a think on it.

    def scan_network(self, ip_range):
        """Scans the network looking for live hosts.

        Args:
            ip_range (str): takes a string that is an ip range to scan.

        Returns:
            list[str]: A list of ip address of active hosts.
        """
        pass

    def scan_server_ports(self, server_ip, port_list=None):
        """Scan a server ip looking for active ports.

        Args:
            server_ip (str): the server ip to be scanned.
            port_list (list[str], optional): A list of ports to scan. Defaults to None.
        """

        if port_list is None:
            self.port_list = []
        else:
            self.port_list = port_list

    def initialize_database(self, fine_name=None):
        """Initializes the database

        Args:
            fine_name (str, optional): The file name of the database to initialize. Defaults to None.
        """
        db = sqlalchemy.create_engine("sqlite:///retofoto.db")

    def read_database(self):
        """The implementation to read the database"""
        pass

    def write_database(self):
        """The implementation to write to the database"""
        pass

    def ip_longitudinal_compare(self):
        """The longitudinal comparison of the database information to the current state of the network."""
        pass

    def detect_port_server_type(self):
        """Makes a guess as to the server port type. Also, asserts confidence interval in its guess."""
        pass
