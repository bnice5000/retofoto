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

import argparse
from cmath import log
import datetime
import ipaddress
import logging
from multiprocessing import Pool
import socket
import sys

from icmplib import ping
import netifaces
import sqlalchemy as db
import sqlalchemy_utils
import yaspin

logging.root.handlers = []
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    level=logging.DEBUG,
    filename="retofoto.log",
)

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.ERROR)

# set a format which is simpler for console use
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


class FileTools:
    """Class that works with the database."""

    file_name = "retofoto"
    programmer_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def write_database(self, active_hosts):
        """method that writes to the database

        Args:
            active_hosts (List[str]): A list of the ip addresses from hosts.
        """
        # Set database file name
        database_file = f"sqlite:///{self.file_name}.sqlite"

        # Check to see if database exists if it does not create it.
        if not sqlalchemy_utils.database_exists(database_file):
            logging.debug("Database %s exists", database_file)
            sqlalchemy_utils.create_database(database_file)

        engine = db.create_engine(database_file)
        connection = engine.connect()
        metadata = db.MetaData()

        # create a table based on date time
        todays_host_table = db.Table(
            self.programmer_date,
            metadata,
            db.Column("id", db.Integer, primary_key=True),
            db.Column("host", sqlalchemy_utils.IPAddressType),
            db.Column("ports", sqlalchemy_utils.ScalarListType()),
        )
        metadata.create_all(engine)
        query = db.insert(todays_host_table)
        results = connection.execute(query, active_hosts)
        results.close()
        connection.close()
        engine.dispose()

    # end FileTools
class HelperNetwork:
    """Class that handles interaction with the network"""

    def __init__(self, ip_range=None, port_list=None, pool_size=50, socket_timeout=3):
        """The init class. Called with initializing the class

        Args:
            ip_range (str, optional): IP Base and CIDR. If no value is added defaults to system ip and subnet mask Defaults to None.
            port_list (List, optional): The list of ports to scan. If no ports are added defaults to the entire range. Defaults to None.
            pool_size (int, optional): The size of the multiprocessor pool. Defaults to 50.
            socket_timeout (int, optional): the timeout length for sockets. Defaults to 3.
        """

        # If property ip_range is none, get default interfaces gateway and subnet mask.
        if ip_range is None:

            gateways = netifaces.gateways()
            default_interface = gateways["default"][netifaces.AF_INET]
            default_net_info = netifaces.ifaddresses(default_interface[1])[
                netifaces.AF_INET
            ][0]
            self.ip_range = ipaddress.IPv4Network(
                (default_net_info["broadcast"], default_net_info["netmask"]),
                strict=False,
            )
        else:
            self.ip_range = ip_range

        # If port_lost is none, use all ports
        if port_list is None:
            self.port_list = range(1, 65536)
        else:
            self.port_list = port_list

        self.pool_size = pool_size
        self.socket_timeout = socket_timeout
        self.active_hosts = []


    def scan_network(self):
        """Scans the network based on the ip addresses in ipaddress in ip_range"""

        ips = [str(ip) for ip in ipaddress.ip_network(self.ip_range)]

        # Enable multiprocessing to speed up the run
        with Pool(self.pool_size) as pool:
            hosts = pool.map(self._ping_sweep, ips)

        # clean all the Nones out of active_hosts.
        self.active_hosts = [host for host in hosts if host is not None]
        logging.debug(self.active_hosts)

    def _ping_sweep(self, ip_addr):
        """Checks to see if the IP Address is host is alive

        Args:
            ip_addr (str): IP address

        Returns:
            Dict: A dictionary containing the ipaddress and the ports that were scanned.
        """
        host = ping(ip_addr, count=1, privileged=False)
        if host.is_alive:
            logging.debug("ip_addr %s is active", ip_addr)
            return {"host": ip_addr, "ports": self._scan_ports(ip_addr)}

    def _scan_ports(self, host):
        """Using Sockets, scans the ports to see if they are open

        Args:
            host (str): The ip address of the host

        Returns:
            List: A list of the ports that are active.
        """

        active_ports = []

        for port in self.port_list:
            logging.debug("Checking host %s and port %s", host, port)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.socket_timeout)
                result = sock.connect_ex((host, port))
                if result == 0:
                    logging.debug("Port %s is alive", port)
                    active_ports.append(port)

        return active_ports

    # end HelperNetwork


def main():
    """The main corpus of the program. Initializes the parser, checks its values.
    Kicks off the scanning. Saves the results to a database. Initializes spinner to entertain."""

    parser = argparse.ArgumentParser(
        description="Scan the network for active hosts and open ports"
    )
    parser.add_argument(
        "-r", "--range", type=str, help="The CIDR representation of the range to scan"
    )
    parser.add_argument(
        "-p",
        "--ports",
        action="append",
        nargs="+",
        type=int,
        help="the list of ports to scan",
    )
    args, leftovers = parser.parse_known_args()

    scan = HelperNetwork()
    if args.range is not None:
        try:
            scan.ip_range = ipaddress.ip_network(args.range)
        except ValueError:
            logging.exception("Must be a valid IP")

    if args.ports is not None:
        scan.port_list = args.ports[0]

    # This created and interactive command prompt while you wait.
    # Progress bar was not as useful due to the indeterminate nature of pooling.
    text = "Scanning Network"
    with yaspin.yaspin().bold.bouncingBall as sp:
        sp.text = text
        scan.scan_network()

    output = FileTools()
    output.write_database(scan.active_hosts)
    print("Network scan complete and information saved to the database.")


# end main


if __name__ == "__main__":

    main()
