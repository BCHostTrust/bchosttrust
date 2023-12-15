import struct
import typing


class BCHTEntry:
    """A BCHT Entry to be embedded into a BCHTBlock.

    Attributes
    ----------
    domain_name : str
        The domain name in string. Must not exceed 4294967295 charactors.
        Non-ASCII domain names are accepted, but they must be encoded 
        using IDNA encoding.
    attitude : int
        The attitude of the entry. Must be in the range of 0 to 255.
        See bchosttrust.attitudes for more details.
    MAX_DOMAIN_LENGTH : int
        Maximum length accepted in the domain_name field.
        This is the largest number a unsigned 32-bit number can handle.
    MAX_ATTITUDE : inr
        Maximum value of the attitude field.
        This is the largest number a unsigned 8-bit number can handle.

    Raises
    ------
    ValueError
        If any of the values are invalid.
    """

    MAX_DOMAIN_LENGTH = 4294967295  # Length within unsigned integer 32 bit
    MAX_ATTITUDE = 255  # unsigned integer 8 bit

    def __init__(self, domain_name: str, attitude: int):
        if not 0 <= attitude <= self.MAX_ATTITUDE:
            raise ValueError("Attitude must be within the range of 0 to 255.")
        try:
            domain_name_bytes = domain_name.encode("ascii")
        except UnicodeEncodeError as e:
            raise ValueError(
                "Domain name must only contain ASCII charactor. If non-ASCII charactors exists, escape them with IDNA encoding first.")
        if len(domain_name_bytes) > self.MAX_DOMAIN_LENGTH:
            raise ValueError(
                "Length of domain name must not exceed 4294967295.")

        self.attitude = attitude
        self.domain_name = domain_name

    def __repr__(self) -> str:
        return "BCHTEntry(domain_name={}, attitude={})".format(self.domain_name, self.attitude)

    def __eq__(self, b: typing.Self) -> bool:
        if type(self) != type(b):
            return False
        return self.attitude == b.attitude and self.domain_name == b.domain_name

    @classmethod
    def from_raw(cls, raw_bytes: bytes) -> typing.Self:
        """Generate a BCHT Entry object from its bytes form.

        Parameters
        ----------
        raw_bytes : bytes
            The BCHT Entry in bytes

        Returns
        -------
        BCHTEntry
            The BCHT Entry in Python object

        Raises
        ------
        ValueError
            If the length of the BCHT Entry is invalid
        """

        raw_bytes_len = len(raw_bytes)
        if raw_bytes_len < 5:
            raise ValueError("Length of BCHT Entry must be at least 5 bytes.")

        attitude = raw_bytes[0]
        domain_name_len = int.from_bytes(raw_bytes[1:5])

        if (5 + domain_name_len) != raw_bytes_len:
            raise ValueError(
                "Length of BCHT Entry does not match the one in its header")
        domain_name_bytes = raw_bytes[5:(5 + domain_name_len)]
        domain_name = domain_name_bytes.decode("ascii")

        return cls(domain_name, attitude)

    def raw(self) -> bytes:
        """Return the BCHT Entry in its bytes form.

        Returns
        -------
        bytes
            The BCHT Entry in bytes.
        """

        attitude_bytes = struct.pack("B", self.attitude)  # unsigned char
        domain_name_bytes = self.domain_name.encode("ascii")
        domain_name_len = len(domain_name_bytes)
        domain_name_len_bytes = struct.pack(
            ">L", domain_name_len)  # unsigned long

        return attitude_bytes + domain_name_len_bytes + domain_name_bytes


class BCHTBlock:
    ...
