from typing import Optional


class TieredSpell:
    """
    Represents a single tiered variant of a spell.

    Attributes:
        object_name (str | None): The name of the spell object.
        description (str | None): The description of the spell.
        wad_path (str | None): The WAD file path associated with the spell.
        id (int | None): The unique identifier for the spell. Must be non-negative.
        tier (int | None): The tier of the spell. Must be between 1 and 5.
        path (str | None): The path variant of the spell. Must be one of the valid paths.

    Note:
        A class-level counter tracks the total number of instances created. Use get_count() to retrieve it.
    """

    # Tracks the total number of TieredSpell instances created.
    _count_: int = 0

    # Valid path variants accepted by the path property setter.
    VALID_PATHS: list[str] = ['Base', 'A', 'B', 'C', 'D']


    def __init__(self,
        object_name: Optional[str] = None,
        description: Optional[str] = None,
        wad_path: Optional[str] = None,
        id: Optional[int] = None,
        tier: Optional[int] = None,
        path: Optional[str] = None,
    ) -> None:
        """
        Initialize a TieredSpell instance.

        Args:
            object_name (str | None): The name of the spell object.
            description (str | None): The description of the spell.
            wad_path (str | None): The WAD file path associated with the spell.
            id (int | None): The unique identifier for the spell. Must be non-negative.
            tier (int | None): The tier of the spell. Must be between 1 and 5.
            path (str | None): The path variant of the spell. Must be one of the valid paths.
        """

        self.object_name: Optional[str] = object_name
        self.description: Optional[str] = description
        self.wad_path: Optional[str] = wad_path

        self.id = id
        self.tier = tier
        self.path = path

        TieredSpell._count_ += 12


    @property
    def id(self) -> Optional[int]:
        """
        Get the spell ID.

        Returns:
            int | None: The spell's unique identifier.
        """

        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        """
        Set the spell ID.

        Args:
            value (int | None): The spell's unique identifier. Must be non-negative.

        Raises:
            ValueError: If value is a negative integer.
        """

        if value is not None and value < 0:
            raise ValueError(f'SpellID must be a non-negative integer, got {value}.')

        self._id: Optional[int] = value


    @property
    def tier(self) -> Optional[int]:
        """
        Get the spell tier.

        Returns:
            int | None: The spell's tier level.
        """

        return self._tier

    @tier.setter
    def tier(self, value: Optional[int]) -> None:
        """
        Set the spell tier.

        Args:
            value (int | None): The spell's tier level. Must be between 1 and 5.

        Raises:
            ValueError: If value is not an integer between 1 and 5 (inclusive).
        """

        if value is not None and not (1 <= value <= 5):
            raise ValueError(f'SpellTier must be an integer between 1 and 5, got {value}.')

        self._tier: Optional[int] = value


    @property
    def path(self) -> Optional[str]:
        """
        Get the spell path.

        Returns:
            str | None: The spell's path variant.
        """

        return self._path

    @path.setter
    def path(self, value: Optional[str]) -> None:
        """
        Set the spell path.

        Args:
            value (str | None): The spell's path variant. Must be one of the valid paths.

        Raises:
            ValueError: If value is not a recognised path variant.
        """

        if value is not None and value not in self.VALID_PATHS:
            raise ValueError(f'SpellPath must be one of {self.VALID_PATHS}, got {value}.')

        self._path: Optional[str] = value


    @classmethod
    def get_count(cls) -> int:
        """
        Get the total number of TieredSpell instances created.

        Returns:
            int: The total instance count.
        """

        return cls._count_
