from typing import Optional

from TieredSpell import TieredSpell


class Spell:
    """
    Represents a spell containing a group of tiered variants.

    Attributes:
        display_name (str | None): The resolved display name of the spell.
        school (str): The magic school the spell belongs to. Must be one of the valid schools.
        tiered_spell_group (int): The group index this spell belongs to. Must be non-negative.
        name_locale_code (str | None): The locale code for the spell's display name.
        tiered_spells (list[TieredSpell]): The list of tiered spell variants associated with this spell.

    Note:
        A class-level counter tracks the total number of instances created. Use get_count() to retrieve it.
    """

    # Tracks the total number of Spell instances created.
    _count_: int = 0

    # Valid school names accepted by the school property setter.
    VALID_SCHOOLS: list[str] = [
        'Fire', 'Ice', 'Storm', 'Myth', 'Life', 'Death', 'Balance',
        'Sun', 'Moon', 'Star', 'Shadow',
    ]


    def __init__(self, school: str, tiered_spell_group: int, name_locale_code: str) -> None:
        """
        Initialize a Spell instance.

        Args:
            school (str): The magic school the spell belongs to. Must be one of the valid schools.
            tiered_spell_group (int): The group index this spell belongs to. Must be non-negative.
            name_locale_code (str): The locale code for the spell's display name.
        """

        self.display_name: Optional[str] = None

        self.school = school
        self.tiered_spell_group = tiered_spell_group
        self.name_locale_code: str = name_locale_code

        self.tiered_spells: list[TieredSpell] = []

        Spell._count_ += 1


    @property
    def school(self) -> str:
        """
        Get the spell school.

        Returns:
            str: The school of the spell.
        """

        return self._school

    @school.setter
    def school(self, value: str) -> None:
        """
        Set the spell school.

        Args:
            value (str): The school of the spell. Must be one of the valid schools.

        Raises:
            ValueError: If value is not a recognised school.
        """

        if value not in self.VALID_SCHOOLS:
            raise ValueError(f'School must be a valid school, got {value}.')

        self._school: str = value


    @property
    def tiered_spell_group(self) -> int:
        """
        Get the tiered spell group index.

        Returns:
            int: The group index this spell belongs to.
        """

        return self._tiered_spell_group

    @tiered_spell_group.setter
    def tiered_spell_group(self, value: int) -> None:
        """
        Set the tiered spell group index.

        Args:
            value (int): The group index this spell belongs to. Must be non-negative.

        Raises:
            ValueError: If value is a negative integer.
        """

        if value < 0:
            raise ValueError(f'TieredSpellGroup must be a non-negative integer, got {value}.')

        self._tiered_spell_group: int = value


    @classmethod
    def get_count(cls) -> int:
        """
        Get the total number of Spell instances created.

        Returns:
            int: The total instance count.
        """

        return cls._count_


    def add_tiered_spell(self, tiered_spell: TieredSpell) -> None:
        """
        Add a tiered spell variant to this spell.

        Args:
            tiered_spell (TieredSpell): The tiered spell instance to append.
        """

        self.tiered_spells.append(tiered_spell)
