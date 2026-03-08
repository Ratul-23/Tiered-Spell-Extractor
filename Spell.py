from typing import Optional

from TieredSpell import TieredSpell


class Spell:
    """
    Represents a spell containing a group of tiered variants.

    Attributes:
        display_name (str | None): The display name of the spell.
        spell_code (str | None): The internal code identifier for the spell.
        tiered_spell_group (int | None): The group index this spell belongs to. Must be non-negative.
        tiered_spells (list[TieredSpell]): The list of tiered spell variants associated with this spell.

    Note:
        A class-level counter tracks the total number of instances created. Use get_count() to retrieve it.
    """

    _count: int = 0

    def __init__(self,
        display_name: Optional[str] = None,
        spell_code: Optional[str] = None,
        tiered_spell_group: Optional[int] = None,
    ) -> None:
        """
        Initialize a Spell instance.

        Args:
            display_name (str | None): The display name of the spell.
            spell_code (str | None): The internal code identifier for the spell.
            tiered_spell_group (int | None): The group index this spell belongs to. Must be non-negative.
        """

        self.display_name: Optional[str] = display_name
        self.spell_code: Optional[str] = spell_code
        self.tiered_spell_group = tiered_spell_group

        self.tiered_spells: list[TieredSpell] = []

        Spell._count += 1


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
            raise ValueError(f"TieredSpellGroup must be a non-negative integer, got {value}.")

        self._tiered_spell_group: Optional[int] = value


    @classmethod
    def get_count(cls) -> int:
        """
        Get the total number of Spell instances created.

        Returns:
            int: The total instance count.
        """

        return cls._count


    def add_tiered_spell(self, tiered_spell: TieredSpell) -> None:
        """
        Add a tiered spell variant to this spell.

        Args:
            tiered_spell (TieredSpell): The tiered spell instance to append.
        """

        self.tiered_spells.append(tiered_spell)
