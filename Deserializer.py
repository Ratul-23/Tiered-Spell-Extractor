import os
from typing import Optional, Self

from katsuba import KatsubaError
from katsuba.op import TypeList, SerializerOptions, Serializer, LazyList, LazyObject, STATEFUL_FLAGS # type: ignore
from katsuba.wad import Archive # type: ignore

from SpellData import SpellData


class Deserializer:
    """
    Singleton deserializer for KingsIsle WAD archive data.

    Handles deserialization of ObjectProperty binary files and lang files
    from the game's Root.wad archive.

    Note:
        Only one instance is created. Subsequent instantiations return the same object.
    """

    _instance: Optional[Self] = None


    def __new__(cls, *args, **kwargs) -> Self:
        """
        Return the existing instance or create a new one.

        Returns:
            Self: The singleton Deserializer instance.
        """

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(self, install_path: str, type_list_path: str) -> None:
        """
        Initialize the Deserializer instance.

        No-ops if the instance has already been initialized.

        Args:
            install_path (str): Path to the Wizard101 installation directory.
            type_list_path (str): Path to the wiztype JSON type list file.
        """

        if hasattr(self, '_archive'):
            return

        game_data_path: str = os.path.join(install_path, 'Data', 'GameData')
        type_list: TypeList = TypeList.open(type_list_path)

        serializer_opts : SerializerOptions = SerializerOptions()
        serializer_opts.flags |= STATEFUL_FLAGS
        serializer_opts.shallow = False
        serializer_opts.skip_unknown_types = True

        self._serializer: Serializer = Serializer(serializer_opts, type_list)
        self._archive: Archive = Archive.mmap(os.path.join(game_data_path, 'Root.wad'))


    def get_object_name_by_group(self) -> dict[int, str]:
        """
        Deserialize TieredSpells.xml and map each group index to its tier-one spell object name.

        Returns:
            dict[int, str]: A mapping of group index to tier-one spell object name, or an empty dict on failure.
        """

        try:
            data: LazyObject = self._archive.deserialize('TieredSpells.xml', self._serializer)

        except (KatsubaError, OSError) as exception:
            print(f'Warning: Failed to deserialize TieredSpells.xml: {exception}')
            return {}

        spell_groups: Optional[LazyList] = data.get('m_tieredSpellGroupList')
        if spell_groups is None:
            return {}

        return {
            index:
            entry.get('m_tierOneSpell').decode('utf-8').strip()
            for index, entry in enumerate(spell_groups)
        }


    def get_spell_id_by_path(self) -> dict[str, int]:
        """
        Deserialize TemplateManifest.xml and map each tiered spell file path to its spell ID.

        Returns:
            dict[str, int]: A mapping of file path to spell ID for entries under 'Spells/Tiered Spells/', or an empty dict on failure.
        """

        try:
            data: LazyObject = self._archive.deserialize('TemplateManifest.xml', self._serializer)

        except (KatsubaError, OSError) as exception:
            print(f'Warning: Failed to deserialize TemplateManifest.xml: {exception}')
            return {}

        serialized_templates: Optional[LazyList] = data.get('m_serializedTemplates')
        if serialized_templates is None:
            return {}

        spell_id_by_path: dict[str, int] = {}

        for template in serialized_templates:
            file_name: str = template.get('m_filename').decode('utf-8').strip()

            if file_name.startswith('Spells/Tiered Spells/'):
                spell_id_by_path[file_name] = int(template.get('m_id'))

        return spell_id_by_path


    def get_string_by_locale_code(self) -> dict[str, str]:
        """
        Parse both Spell.lang and Spells.lang and merge them into a single mapping.

        Returns:
            dict[str, str]: A combined mapping of locale code to string value.
        """

        name_by_spell_code: dict[str, str] = self._parse_lang_files('Locale/en-US/Spell.lang')
        name_by_spells_code: dict[str, str] = self._parse_lang_files('Locale/en-US/Spells.lang')

        return name_by_spell_code | name_by_spells_code


    def _parse_lang_files(self, lang_file_path: str) -> dict[str, str]:
        """
        Parse a UTF-16 lang file from the archive and map each locale code to its string value.

        Args:
            lang_file_path (str): The path to the lang file within the archive.

        Returns:
            dict[str, str]: A mapping of locale code to string value, or an empty dict if the file is not found.
        """

        try:
            data: bytes = self._archive[lang_file_path]

        except KeyError:
            print(f'Warning: {lang_file_path} not found in archive.')
            return {}

        content: str = data.decode('utf-16')
        lines: list[str] = [line.strip() for line in content.splitlines()]
        file_name: str = os.path.basename(lang_file_path).removesuffix('.lang').strip()
        name_by_code: dict[str, str] = {}

        i: int = 1 # Skip the header line (e.g. '1:Spell')

        while i < len(lines) - 2:
            if not lines[i] or not lines[i + 2]:
                i += 1
                continue

            code: str = file_name + '_' + lines[i]
            name: str = lines[i + 2]

            name_by_code[code] = name

            i += 3

        return name_by_code


    def get_spell_data_by_path(self) -> dict[str, SpellData]:
        """
        Deserialize all tiered spell files and map each file path to its spell data.

        Returns:
            dict[str, SpellData]: A mapping of file path to a SpellData instance, or an empty dict on failure.
        """

        spell_data_by_path: dict[str, SpellData] = {}

        for file in self._archive.iter_glob('Spells/Tiered Spells/*.xml'):
            try:
                data: LazyObject = self._archive.deserialize(file, self._serializer)

            except (KatsubaError, OSError) as exception:
                print(f'Warning: Failed to deserialize {file}: {exception}')
                continue

            try:
                object_name: str = data['m_name'].decode('utf-8').strip()
                name_locale_code: str = data['m_displayName'].decode('utf-8').strip()
                desc_locale_code: str = data['m_description'].decode('utf-8').strip()
                school: str = data['m_sMagicSchoolName'].decode('utf-8').strip()

            except KeyError as exception:
                print(f'Warning: Missing property {exception} in {file}')
                continue

            spell_data_by_path[file] = SpellData(object_name, name_locale_code, desc_locale_code, school)

        return spell_data_by_path
