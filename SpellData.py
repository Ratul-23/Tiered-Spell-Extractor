from dataclasses import dataclass


@dataclass
class SpellData:
    """
    Represents the raw data extracted from a tiered spell file.

    Attributes:
        object_name (str): The internal object name of the spell.
        name_locale_code (str): The locale code for the spell's display name.
        desc_locale_code (str): The locale code for the spell's description.
        school (str): The magic school the spell belongs to.
    """

    object_name: str
    name_locale_code: str
    desc_locale_code: str
    school: str
