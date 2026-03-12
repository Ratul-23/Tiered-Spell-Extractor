import os
import re
import json

from typing import Optional

from Deserializer import Deserializer
from SpellData import SpellData

from Spell import Spell
from TieredSpell import TieredSpell


INSTALL_PATH: str = 'C:/ProgramData/KingsIsle Entertainment/Wizard101/'
TYPE_DUMP_PATH: str = 'types.json'

LOCALE_CODE_EXCEPTIONS: dict[str, str] = {
    'Colossal_00000003': 'Nightbringer',
    'Colossal_00000004': 'Daybreaker',
}

TIER_PATH_PATTERN: re.Pattern = re.compile(r'-\s*T(\d+)(?:\s*-\s*(\w+))?')

SKIP_PATHS: set[str] = {'TEMP', 'AB', 'BA'}


def build_spells(object_name_by_group: dict[int, str], spell_data_by_path: dict[str, SpellData]) -> list[Spell]:
    """
    Build a list of Spell instances from the tiered spell group mapping.

    Args:
        object_name_by_group (dict[int, str]): A mapping of group index to tier-one spell object name.
        spell_data_by_path (dict[str, SpellData]): A mapping of file path to SpellData instance.

    Returns:
        list[Spell]: A list of Spell instances populated with school, group index, and locale code.
    """

    spells: list[Spell] = []

    for tiered_group, object_name in object_name_by_group.items():
        path: str = os.path.join('Spells/Tiered Spells/', object_name + '.xml')

        spell_data: Optional[SpellData] = spell_data_by_path.get(path)
        if spell_data is None:
            continue

        spells.append( Spell(spell_data.school, tiered_group, spell_data.name_locale_code) )

    return spells


def resolve_display_name(
    spells: list[Spell],
    string_by_locale_code: dict[str, str],
    exceptions: dict[str, str],
    ) -> list[Spell]:
    """
    Resolve and assign a display name to each spell using its locale code.

    Args:
        spells (list[Spell]): The list of spells to resolve.
        string_by_locale_code (dict[str, str]): A mapping of locale code to string value.
        exceptions (dict[str, str]): Manual overrides for unrecognised locale codes.

    Returns:
        list[Spell]: The same list of spells with display names populated.
    """

    for spell in spells:
        locale_code: str = spell.name_locale_code

        if locale_code in exceptions:
            spell.display_name = exceptions[locale_code]

        else:
            spell.display_name = string_by_locale_code.get(locale_code, '')

    return spells


def build_tiered_spells(
    spells: list[Spell],
    spell_data_by_path: dict[str, SpellData],
    spell_id_by_path: dict[str, int],
    ) -> list[Spell]:
    """
    Build TieredSpell instances from spell data and attach them to their parent Spell.

    Args:
        spells (list[Spell]): The list of spells to attach tiered variants to.
        spell_data_by_path (dict[str, SpellData]): A mapping of file path to SpellData instance.
        spell_id_by_path (dict[str, int]): A mapping of file path to spell ID.

    Returns:
        list[Spell]: The same list of spells with tiered variants populated.
    """

    spell_by_key: dict[tuple[str, str], Spell] = {
        (spell.name_locale_code, spell.school): spell
        for spell in spells
    }

    for path, spell_data in spell_data_by_path.items():
        spell: Optional[Spell] = spell_by_key.get((spell_data.name_locale_code, spell_data.school))
        if spell is None:
            continue

        spell_id: int = spell_id_by_path.get(path, -1)
        tiered_spell: TieredSpell = TieredSpell(spell_data.object_name, path, spell_data.desc_locale_code, spell_id)

        spell.add_tiered_spell(tiered_spell)

    return spells


def resolve_tiered_spells(spells: list[Spell], string_by_locale_code: dict[str, str]) -> list[Spell]:
    """
    Resolve the description, tier, and path for each tiered spell.

    Skips tiered spells whose path is in SKIP_PATHS.

    Args:
        spells (list[Spell]): The list of spells to resolve.
        string_by_locale_code (dict[str, str]): A mapping of locale code to string value.

    Returns:
        list[Spell]: The same list of spells with tiered spell data populated.
    """

    for spell in spells:
        for tiered_spell in spell.tiered_spells:
            tiered_spell.desc = string_by_locale_code.get(tiered_spell.desc_locale_code, '')

            match = TIER_PATH_PATTERN.search(tiered_spell.object_name)

            if match:
                tiered_spell.tier = int(match.group(1))
                path: str = match.group(2) or 'A'
            else:
                tiered_spell.tier = 1
                path = 'Base'

            if path in SKIP_PATHS:
                continue

            tiered_spell.path = path

    return spells


def spell_to_dict(spell: Spell) -> dict:
    """
    Serialize a Spell instance to a dictionary for JSON export.

    Args:
        spell (Spell): The spell instance to serialize.

    Returns:
        dict: A dictionary containing the spell's data and its tiered variants.
    """

    return {
        'display_name': spell.display_name,
        'school': spell.school,
        'tiered_spell_group': spell.tiered_spell_group,
        'name_locale_code': spell.name_locale_code,
        'tiered_spells': [
            {
                'object_name': tiered_spell.object_name,
                'wad_path': tiered_spell.wad_path,
                'description': tiered_spell.desc,
                'description_locale_code': tiered_spell.desc_locale_code,
                'id': tiered_spell.id,
                'tier': tiered_spell.tier,
                'path': tiered_spell.path,
            }
            for tiered_spell in spell.tiered_spells
        ],
    }


def export_spells(spells: list[Spell], output_path: str) -> None:
    """
    Export a list of spells to a JSON file.

    Args:
        spells (list[Spell]): The list of spells to export.
        output_path (str): The file path to write the JSON output to.
    """

    data: list[dict] = [spell_to_dict(spell) for spell in spells]

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main() -> None:
    """
    Entry point for the Tiered Spells processing pipeline.
    """

    deserializer: Deserializer = Deserializer(INSTALL_PATH, TYPE_DUMP_PATH)

    # {TieredSpellGroup: ObjectName}
    object_name_by_group: dict[int, str] = deserializer.get_object_name_by_group()

    # {Path: SpellData}
    spell_data_by_path: dict[str, SpellData] = deserializer.get_spell_data_by_path()

    # {Path: SpellID}
    spell_id_by_path: dict[str, int] = deserializer.get_spell_id_by_path()

    # {LocaleCode, String}
    string_by_locale_code: dict[str, str] = deserializer.get_string_by_locale_code()

    spells: list[Spell] = build_spells(object_name_by_group, spell_data_by_path)

    spells = resolve_display_name(spells, string_by_locale_code, LOCALE_CODE_EXCEPTIONS)
    spells = build_tiered_spells(spells, spell_data_by_path, spell_id_by_path)

    spells = resolve_tiered_spells(spells, string_by_locale_code)

    export_spells(spells, 'Tiered-Spells.json')


if __name__ == '__main__':
    main()
