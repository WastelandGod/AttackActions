import ipaddress


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


