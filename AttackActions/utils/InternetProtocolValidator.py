import ipaddress
import validators


class InternetProtocolValidator:
    @staticmethod
    def is_valid_ip(ip_string: str) -> bool:
        """
        Validates if the provided string is a valid IP address (IPv4 or IPv6).

        Args:
            ip_string (str): The IP address string to validate.

        Returns:
            bool: True if valid IP address, False otherwise.
        """
        try:
            ipaddress.ip_address(ip_string)  # This will raise an exception if invalid
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_port(port: str) -> bool:
        try:
            int(port)
            # https://www.cloudflare.com/learning/network-layer/what-is-a-computer-port/
            if 0 < int(port) < 65535:
                return True
            return False
        except ValueError:
            return False

    @staticmethod
    def is_valid_url(url: str) -> bool:
        if validators.url(url) is True:
            return True
        return False

