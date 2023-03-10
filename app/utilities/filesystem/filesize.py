from app.utilities.strings import NeStrings


class FileSize:
    def __init__(self):
        pass

    @staticmethod
    def __traditional_system():
        traditional = [
            (1024 ** 5, 'P'),
            (1024 ** 4, 'T'),
            (1024 ** 3, 'G'),
            (1024 ** 2, 'M'),
            (1024 ** 1, 'K'),
            (1024 ** 0, 'B'),
        ]
        return traditional

    @staticmethod
    def __alternative_system():
        alternative = [
            (1024 ** 5, ' PB'),
            (1024 ** 4, ' TB'),
            (1024 ** 3, ' GB'),
            (1024 ** 2, ' MB'),
            (1024 ** 1, ' KB'),
            (1024 ** 0, (' byte', ' bytes')),
        ]
        return alternative

    @staticmethod
    def __verbose_system():
        verbose = [
            (1024 ** 5, (' petabyte', ' petabytes')),
            (1024 ** 4, (' terabyte', ' terabytes')),
            (1024 ** 3, (' gigabyte', ' gigabytes')),
            (1024 ** 2, (' megabyte', ' megabytes')),
            (1024 ** 1, (' kilobyte', ' kilobytes')),
            (1024 ** 0, (' byte', ' bytes')),
        ]
        return verbose

    @staticmethod
    def __iec_system():
        iec = [
            (1024 ** 5, 'Pi'),
            (1024 ** 4, 'Ti'),
            (1024 ** 3, 'Gi'),
            (1024 ** 2, 'Mi'),
            (1024 ** 1, 'Ki'),
            (1024 ** 0, ''),
        ]
        return iec

    @staticmethod
    def __si_system():
        si = [
            (1000 ** 5, 'P'),
            (1000 ** 4, 'T'),
            (1000 ** 3, 'G'),
            (1000 ** 2, 'M'),
            (1000 ** 1, 'K'),
            (1000 ** 0, 'B'),
        ]
        return si

    @staticmethod
    def file_size_readable(bytes, system=None):
        """Human-readable file size.

        Using the traditional system, where a factor of 1024 is used::

        >>> size(10)
        '10B'
        >>> size(100)
        '100B'
        >>> size(1000)
        '1000B'
        >>> size(2000)
        '1K'
        >>> size(10000)
        '9K'
        >>> size(20000)
        '19K'
        >>> size(100000)
        '97K'
        >>> size(200000)
        '195K'
        >>> size(1000000)
        '976K'
        >>> size(2000000)
        '1M'

        Using the SI system, with a factor 1000::

        >>> size(10, system=si)
        '10B'
        >>> size(100, system=si)
        '100B'
        >>> size(1000, system=si)
        '1K'
        >>> size(2000, system=si)
        '2K'
        >>> size(10000, system=si)
        '10K'
        >>> size(20000, system=si)
        '20K'
        >>> size(100000, system=si)
        '100K'
        >>> size(200000, system=si)
        '200K'
        >>> size(1000000, system=si)
        '1M'
        >>> size(2000000, system=si)
        '2M'

        """
        system = NeStrings.defaultIfEmpty(system, "alternative").lower()
        if system not in ["si", "iec", "verbose", "alternative", "traditional"]:
            system = "alternative"
        if system == "alternative":
            sys_prof = FileSize.__si_system()
        if system == "iec":
            sys_prof = FileSize.__iec_system()
        if system == "verbose":
            sys_prof = FileSize.__verbose_system()
        if system == "alternative":
            sys_prof = FileSize.__alternative_system()
        if system == "traditional":
            sys_prof = FileSize.__traditional_system()

        for factor, suffix in sys_prof:
            if bytes >= factor:
                break
        amount = int(bytes / factor)
        if isinstance(suffix, tuple):
            singular, multiple = suffix
            if amount == 1:
                suffix = singular
            else:
                suffix = multiple
        return str(amount) + suffix
