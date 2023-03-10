import socket
import time

from zhinst.hdiq import utils


class Hdiq:
    """
    High-level driver for the Zurich Instruments HDIQ

    Attributes:
        ip (str): IP of the HDIQ device
        port (int, optional): Port used for the HDIQ connection.
            Defaults to `4242`
        timeout (int, optional): Timeout(s). Defaults to `60`

    """

    _TTL = 60

    def __init__(self, ip: str, port: int = 4242, timeout: int = 60):
        self.port = port
        self.ip_with_port = (ip, port)
        self.local_ip = utils._get_local_ip(ip, port)
        self.local_ip_with_port = (self.local_ip, self.port)
        self.timeout = timeout

    def set_lo_to_exp(self, channel: int) -> bool:
        """
        Route the LO signal to the Exp output

        Args:
            channel (int): Channel number `1-8` supported

        Returns:
            bool: True if `ACK` is received
        """
        command = f"setLOtoExp{channel}"
        return bool(self._send_command_loop(command))

    def set_rf_to_exp(self, channel: int) -> bool:
        """
        Route the upconverted RF signal to the Exp port

        Args:
            channel (int): Channel number `1-8` supported

        Returns:
            bool: True if `ACK` is received
        """
        command = f"setRFtoExp{channel}"
        return bool(self._send_command_loop(command))

    def set_rf_to_calib(self, channel: int) -> bool:
        """
        Route the upconverted RF signal to the Calib port

        Args:
            channel (int): Channel number `1-8` supported

        Returns:
            bool: True if `ACK` is received
        """
        command = f"setRFtoCalib{channel}"
        return bool(self._send_command_loop(command))

    def get_channel_status(self, channel: int) -> str:
        """
        Returns the channel status `1-3`
        1: RF output to Exp port
        2: RF output to Calib port
        3: LO input to Exp port
        Default is `1`

        Args:
            channel (int): Channel number `1-8` supported

        Returns:
            str: Channel status `1-3`
        """
        request = f"getChannelStatus{channel}"
        return self._send_request(request)

    def _send_command_loop(self, command: str, is_request: bool = False):
        """
        Try to send the command until success or timeout

        Args:
            command (str): Corresponding command
            is_request (bool, optional): Defaults to False

        Returns:
            str: Returns the result of _send_command()
        """
        start_time = end_time = time.time()
        sent = False
        while not sent and end_time - start_time < self.timeout:
            sent = self._send_command(command, is_request)
            end_time = time.time()
        return sent

    def _send_request(self, request: str) -> str:
        """
        Requests a message other than `ACK` from the HDIQ.

        Args:
            request (str): The request command

        Returns:
            str: Returns the corresponsing status
        """
        reply = self._send_command_loop(request, is_request=True)
        if reply is None:
            return ""
        return str(reply)

    def _send_command(self, command: str, is_request: bool = False):
        """
        Send the command to HDIQ at port `4242`.
        Parse response from HDIQ.

        Args:
            command (str):
            is_request (bool, optional): Defaults to False

        Returns:
            (str, bool): Returns str if there was a request,
                otherwise bool
        """
        with socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        ) as sock:
            sock.bind(self.local_ip_with_port)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, self._TTL)
            sock.sendto(str.encode(command), self.ip_with_port)
            ack = False
            result = None
            sock.settimeout(self.timeout)
            try:
                data, _ = sock.recvfrom(self.port)
                if "ack" in data.decode("utf-8").lower():
                    ack = True
                    if is_request:
                        data, _ = sock.recvfrom(self.port)
                        result = data.decode("utf-8")
            except socket.timeout:
                pass
        return result if is_request else ack
