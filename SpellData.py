from dataclasses import dataclass


@dataclass
class SpellData:
    """
    Represents the raw data extracted from a tiered spell file.

    Attributes:
        object_name (str): The internal object name of the spell.
        description (str): The description code of the spell.
        spell_code (str): The display name code of the spell.
        school (str): The magic school the spell belongs to.
    """

    object_name: str
    description: str
    spell_code: str
    school: str
