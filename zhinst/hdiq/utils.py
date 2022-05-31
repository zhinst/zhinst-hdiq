import errno
import ifaddr
import socket


def discover_devices(timeout: int = 5) -> list:
    """
    Search for all available devices on all networks of this computer

    Args:
        timeout (int, optional): Timeout(s). Defaults to `5`

    Returns:
        list: List of available devices. [(device_name: str, ip: str)]
    """
    devices = []
    ip_networks = _get_ip_list()

    for ip in ip_networks:
        with socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        ) as sock:
            sock.settimeout(timeout)
            sent, port = _discovery_multicast(ip, sock)
            if sent:
                devices = _receive_devices(port, sock, devices)
    return devices


def _get_ip_list() -> list:
    """
    Return a list of all ips of this computer

    Returns:
        list: A list containing all the ips of this computer
    """
    adapters = ifaddr.get_adapters()
    ip_list = []
    for adapter in adapters:
        for ip in adapter.ips:
            if isinstance(ip.ip, str):
                ip_list.append(ip.ip)
    assert len(ip_list) > 0
    return ip_list


def _get_local_ip(ip: str, port: int = 80) -> str:
    """
    For a given IP, return the local IP that can access it

    Args:
        ip (str): Remote IP
        port (int, optional): Remote port. Defaults to `80`

    Returns:
        str: The local IP that can access the given remote IP
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((ip, port))
        local_ip = s.getsockname()[0]
    return local_ip


def _receive_devices(port: int, sock: socket.socket, devices: list) -> list:
    """
    After sending the device discovery request, collect all available
        devices

    Args:
        port (int): Local port
        sock (socket.socket): Socket object
        devices (list): List of available devices.
            [(device_name: str, ip: str)]

    Returns:
        list: Updated list of available devices.
            [(device_name: str, ip: str)]
    """
    try:
        while True:
            data, _ = sock.recvfrom(port)
            split_data = data.decode("utf-8").split(":")
            if len(split_data) == 3:
                devices.append((split_data[0].strip(), split_data[2].strip()))
            else:
                raise ValueError(data)
    except (socket.timeout, OSError):
        pass
    return devices


def _discovery_multicast(ip: str, sock: socket.socket, attempts: int = 5):
    """
    Send a multicast command on the given network to discover available
        devices.
    If port is in use, try the next port up to <attempts> times

    Args:
        ip (str): Local IP
        sock (socket.socket): Socket object
        attempts (int, optional): Number of times trying different ports
            if port is in use. Defaults to `5`.

    Returns:
        tuple: (sent: bool, port: int) ``sent`` is `True` after sending the
            command. ``port`` is the one used for the connection
    """
    multicast_ip = "239.253.1.1"
    port = 50000
    sent = False
    for i in range(attempts):
        try:
            port += i
            sock.bind((ip, port))
            sock.sendto(b"hdiq-discovery-request-py", (multicast_ip, port))
            sent = True
        except OSError as e:
            if e.errno == errno.EADDRINUSE and i < attempts:
                print(f"Socket Error {errno.EADDRINUSE}: socket in use")
                continue
            break
        else:
            break
    return sent, port
