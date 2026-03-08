from typing import Optional


class TieredSpell:
    """
    Represents a tiered spell with an optional ID, tier, and path.

    Attributes:
        object_name (str | None): The name of the spell object.
        wad_path (str | None): The WAD file path associated with the spell.
        spell_id (int | None): The unique identifier for the spell. Must be non-negative.
        spell_tier (int | None): The tier of the spell. Must be between 1 and 5.
        spell_path (str | None): The path variant of the spell. Must be 'Base', 'A', 'B', 'C', or 'D'.

    Note:
        A class-level counter tracks the total number of instances created. Use get_count() to retrieve it.
    """

    _count: int = 0

    def __init__(self,
        object_name: Optional[str] = None,
        wad_path: Optional[str] = None,
        spell_id: Optional[int] = None,
        spell_tier: Optional[int] = None,
        spell_path: Optional[str] = None,
        ) -> None:
        """
        Initialize a TieredSpell instance.

        Args:
            object_name (str | None): The name of the spell object.
            wad_path (str | None): The WAD file path associated with the spell.
            spell_id (int | None): The unique identifier for the spell. Must be non-negative.
            spell_tier (int | None): The tier of the spell. Must be between 1 and 5.
            spell_path (str | None): The path variant of the spell. Must be 'Base', 'A', 'B', 'C', or 'D'.
        """

        self.object_name: Optional[str] = object_name
        self.wad_path: Optional[str] = wad_path

        self.spell_id = spell_id
        self.spell_tier = spell_tier
        self.spell_path = spell_path

        TieredSpell._count += 1


    @property
    def spell_id(self) -> Optional[int]:
        """
        Get the spell ID.

        Returns:
            int | None: The spell's unique identifier.
        """

        return self._spell_id

    @spell_id.setter
    def spell_id(self, value: Optional[int]) -> None:
        """
        Set the spell ID.

        Args:
            value (int | None): The spell's unique identifier. Must be non-negative.

        Raises:
            ValueError: If value is a negative integer.
        """

        if value is not None and value < 0:
            raise ValueError(f"SpellID must be a non-negative integer, got {value}.")

        self._spell_id: Optional[int] = value


    @property
    def spell_tier(self) -> Optional[int]:
        """
        Get the spell tier.

        Returns:
            int | None: The spell's tier level.
        """

        return self._spell_tier

    @spell_tier.setter
    def spell_tier(self, value: Optional[int]) -> None:
        """
        Set the spell tier.

        Args:
            value (int | None): The spell's tier level. Must be between 1 and 5.

        Raises:
            ValueError: If value is not an integer between 1 and 5 (inclusive).
        """

        if value is not None and not (1 <= value <= 5):
            raise ValueError(f"SpellTier must be an integer between 1 and 5, got {value}.")

        self._spell_tier: Optional[int] = value


    @property
    def spell_path(self) -> Optional[str]:
        """
        Get the spell path.

        Returns:
            str | None: The spell's path variant.
        """

        return self._spell_path

    @spell_path.setter
    def spell_path(self, value: Optional[str]) -> None:
        """
        Set the spell path.

        Args:
            value (str | None): The spell's path variant. Must be 'Base', 'A', 'B', 'C', or 'D'.

        Raises:
            ValueError: If value is not one of 'Base', 'A', 'B', 'C', or 'D'.
        """

        if value is not None and value not in ('Base', 'A', 'B', 'C', 'D'):
            raise ValueError(f"SpellPath must be one of 'Base', 'A', 'B', 'C', or 'D', got '{value}'.")

        self._spell_path: Optional[str] = value


    @classmethod
    def get_count(cls) -> int:
        """
        Get the total number of TieredSpell instances created.

        Returns:
            int: The total instance count.
        """

        return cls._count
