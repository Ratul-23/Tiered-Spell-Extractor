from typing import Optional

from TieredSpell import TieredSpell


class Spell:
    """
    Represents a spell containing a group of tiered variants.

    Attributes:
        display_name (str | None): The display name of the spell.
        school (str | None): The school of the spell.
        tiered_spell_group (int | None): The group index this spell belongs to. Must be non-negative.
        lang_code (str | None): The internal code identifier for the spell.
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


    def __init__(self,
        display_name: Optional[str] = None,
        school: Optional[str] = None,
        tiered_spell_group: Optional[int] = None,
        lang_code: Optional[str] = None,
    ) -> None:
        """
        Initialize a Spell instance.

        Args:
            display_name (str | None): The display name of the spell.
            school (str | None): The school of the spell.
            tiered_spell_group (int | None): The group index this spell belongs to. Must be non-negative.
            lang_code (str | None): The internal code identifier for the spell.
        """

        self.display_name: Optional[str] = display_name
        self.school = school
        self.tiered_spell_group = tiered_spell_group
        self.lang_code: Optional[str] = lang_code

        self.tiered_spells: list[TieredSpell] = []

        Spell._count_ += 1


    @property
    def tiered_spell_group(self) -> Optional[int]:
        """
        Get the tiered spell group index.

        Returns:
            int | None: The group index this spell belongs to.
        """

        return self._tiered_spell_group

    @tiered_spell_group.setter
    def tiered_spell_group(self, value: Optional[int]) -> None:
        """
        Set the tiered spell group index.

        Args:
            value (int | None): The group index this spell belongs to. Must be non-negative.

        Raises:
            ValueError: If value is a negative integer.
        """

        if value is not None and value < 0:
            raise ValueError(f'TieredSpellGroup must be a non-negative integer, got {value}.')

        self._tiered_spell_group: Optional[int] = value


    @property
    def school(self) -> Optional[str]:
        """
        Get the spell school.

        Returns:
            str | None: The school of the spell.
        """

        return self._school

    @school.setter
    def school(self, value: Optional[str]) -> None:
        """
        Set the spell school.

        Args:
            value (str | None): The school of the spell. Must be one of the valid schools.

        Raises:
            ValueError: If value is not a recognised school.
        """

        if value is not None and value not in self.VALID_SCHOOLS:
            raise ValueError(f'School must be a valid school, got {value}.')

        self._school: Optional[str] = value


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
