import os
import re
import json
import time

from typing import Any, Optional

from Spell import Spell
from TieredSpell import TieredSpell


MANIFEST_PATH: str = 'Root/TemplateManifest.de.xml'
SPELL_GROUP_PATH: str = 'Root/TieredSpells.de.xml'

SPELL_LANG_PATH: str = 'Root/Locale/en-US/Spell.lang'
SPELLS_LANG_PATH: str = 'Root/Locale/en-US/Spells.lang'

TIERED_SPELL_PATH: str = 'Root/Spells/Tiered Spells'

JSON_EXPORT_PATH: str = 'Tiered-Spells-for-Syrup.json'


SPELL_GROUP_EXCEPTIONS: dict[str, str] = {
    'Catalan': 'Catalan the Lightning Lizard',
    'Savage Paw': 'Jaguar Shaman',
    'Winter Moon': 'MoonSkull Priestess',
    'Lord of Night': 'ThunderHorn Mummy',
    'Skeletal Dragon': 'Bone Dragon',
    'Woolly Mammoth': 'Wooly Mammoth',
    'Gnomes': 'Gnomes!',
}

SPELL_CODE_EXCEPTIONS: dict[str, str] = {
    'Colossal_00000003': 'Nightbringer',
    'Colossal_00000004': 'Daybreaker',
}


TIER_PATH_PATTERN: re.Pattern = re.compile(r'-\s*T(\d+)(?:\s*-\s*(\w+))?')

SKIP_PATHS: set[str] = {'TEMP', 'AB', 'BA'}

PATH_ORDER: dict[str, int] = {'Base': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4}


def get_object_name_by_group(spell_group_path: str = SPELL_GROUP_PATH) -> dict[int, str]:
    """
    Load the tiered spell group list and map each group index to its tier-one spell object name.

    Args:
        spell_group_path (str): Path to the tiered spell group JSON file. Defaults to SPELL_GROUP_PATH.

    Returns:
        dict[int, str]: A mapping of group index to tier-one spell object name.
    """

    with open(spell_group_path, 'r', encoding='utf-8') as spell_group_file:
        data: dict[str, Any] = json.load(spell_group_file)

    object_name_by_group: dict[int, str] = {
        index: str(entry['m_tierOneSpell']).strip()
        for index, entry in enumerate(data['m_tieredSpellGroupList'])
    }

    return object_name_by_group


def get_spell_id_by_object_name(manifest_path: str = MANIFEST_PATH) -> dict[str, int]:
    """
    Load the template manifest and map each tiered spell object name to its spell ID.

    Args:
        manifest_path (str): Path to the template manifest JSON file. Defaults to MANIFEST_PATH.

    Returns:
        dict[str, int]: A mapping of tiered spell object name to spell ID.
    """

    with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
        data: dict[str, Any] = json.load(manifest_file)

    spell_id_by_object_name: dict[str, int] = {
        (
            str(obj['m_filename'])
            .replace('Spells/Tiered Spells/', '')
            .replace('.xml', '')
            .strip()
        ): int(obj['m_id'])

        for obj in data['m_serializedTemplates']
        if 'Spells/Tiered Spells/' in obj.get('m_filename', '')
    }

    return spell_id_by_object_name


def load_lang_file(lang_path: str) -> dict[str, str]:
    """
    Load a UTF-16 lang file and map each spell code to its display name.

    The file format is irregular — entries are not guaranteed to appear at
    fixed intervals, so each line is scanned sequentially. A valid entry
    consists of a spell code at line i and a display name at line i + 2.

    Args:
        lang_path (str): Path to the UTF-16 encoded lang file.

    Returns:
        dict[str, str]: A mapping of spell code to display name.
    """

    with open(lang_path, 'r', encoding='utf-16') as lang_file:
        lines: list[str] = [line.strip() for line in lang_file]

    name_by_code: dict[str, str] = {}

    i: int = 1
    while i < len(lines) - 2:
        code, name = lines[i], lines[i + 2]

        if code and name:
            name_by_code[code] = name
            i += 3

        else:
            i += 1

    return name_by_code


def build_spells(
    object_name_by_group: dict[int, str],
    tiered_spell_path: str = TIERED_SPELL_PATH,
    spell_group_exceptions: dict[str, str] = SPELL_GROUP_EXCEPTIONS,
    ) -> list[Spell]:
    """
    Build a list of Spell instances from the tiered spell group mapping.

    Args:
        object_name_by_group (dict[int, str]): A mapping of group index to tier-one spell object name.
        tiered_spell_path (str): Path to the tiered spell data directory. Defaults to TIERED_SPELL_PATH.
        spell_group_exceptions (dict[str, str]): Object name overrides for mismatched file names. Defaults to SPELL_GROUP_EXCEPTIONS.

    Returns:
        list[Spell]: A list of Spell instances populated with spell code and group index.
    """

    spells: list[Spell] = []

    for group, object_name in object_name_by_group.items():
        file_name: str = spell_group_exceptions.get(object_name, object_name)
        tiered_spell_file_path: str = os.path.join(tiered_spell_path, file_name + '.de.xml')

        try:
            with open(tiered_spell_file_path, 'r', encoding='utf-8') as tiered_spell_file:
                data: dict[str, Any] = json.load(tiered_spell_file)

        except FileNotFoundError:
            print(f'Warning: {file_name} not found at {tiered_spell_path}.')
            continue

        spells.append(
            Spell(
                spell_code = data['m_displayName'].strip(),
                tiered_spell_group = group
            )
        )

    return spells


def resolve_display_names(
    spells: list[Spell],
    name_by_spell_code: dict[str, str],
    name_by_spells_code: dict[str, str],
    spell_code_exceptions: dict[str, str] = SPELL_CODE_EXCEPTIONS,
    ) -> list[Spell]:

    """
    Resolve and assign a display name to each spell using its spell code.

    Args:
        spells (list[Spell]): The list of spells to resolve.
        name_by_spell_code (dict[str, str]): A mapping of Spell_ codes to display names.
        name_by_spells_code (dict[str, str]): A mapping of Spells_ codes to display names.
        spell_code_exceptions (dict[str, str]): Manual overrides for unrecognised spell codes. Defaults to SPELL_CODE_EXCEPTIONS.

    Returns:
        list[Spell]: The same list of spells with display names populated.
    """

    for spell in spells:
        if spell.spell_code is None:
            continue

        spell.display_name = resolve_spell_code(
            spell.spell_code,
            name_by_spell_code,
            name_by_spells_code,
            spell_code_exceptions,
        )

    return spells


def resolve_spell_code(
    spell_code: str,
    name_by_spell_code: dict[str, str],
    name_by_spells_code: dict[str, str],
    spell_code_exceptions: dict[str, str] = SPELL_CODE_EXCEPTIONS,
    ) -> str:

    """
    Resolve a single spell code to its display name.

    Checks for a 'Spells_' prefix, a 'Spell_' prefix, or a manual exception
    entry. Prints a warning and returns an empty string if no match is found.

    Args:
        spell_code (str): The raw spell code from the game data.
        name_by_spell_code (dict[str, str]): A mapping of Spell_ codes to display names.
        name_by_spells_code (dict[str, str]): A mapping of Spells_ codes to display names.
        spell_code_exceptions (dict[str, str]): Manual overrides for unrecognised spell codes. Defaults to SPELL_CODE_EXCEPTIONS.

    Returns:
        str: The resolved display name, or an empty string if not found.
    """

    if spell_code.startswith('Spells_'):
        return name_by_spells_code.get(spell_code.removeprefix('Spells_'), '')

    elif spell_code.startswith('Spell_'):
        return name_by_spell_code.get(spell_code.removeprefix('Spell_'), '')

    elif spell_code in spell_code_exceptions:
        return spell_code_exceptions[spell_code]

    else:
        print(f'{spell_code} not found in Lang files')
        return ''


def index_spells_by_display_name(spells: list[Spell]) -> dict[str, Spell]:
    """
    Index a list of spells by their display name, excluding spells with no display name.

    Args:
        spells (list[Spell]): The list of spells to index.

    Returns:
        dict[str, Spell]: A mapping of display name to Spell instance.
    """

    return {
        spell.display_name: spell
        for spell in spells
        if spell.display_name
    }


def build_tiered_spells(
    spell_by_display_name: dict[str, Spell],
    spell_id_by_object_name: dict[str, int],
    name_by_spell_code: dict[str, str],
    name_by_spells_code: dict[str, str],
    spell_code_exceptions: dict[str, str] = SPELL_CODE_EXCEPTIONS,
    tiered_spell_path: str = TIERED_SPELL_PATH,
    ) -> list[Spell]:

    """
    Scan the tiered spell directory, parse each file, and attach TieredSpell
    instances to their parent Spell.

    Skips files with invalid extensions, unparseable tier/path patterns,
    unresolvable display names, or malformed JSON.

    Args:
        spell_by_display_name (dict[str, Spell]): A mapping of display name to Spell instance.
        spell_id_by_object_name (dict[str, int]): A mapping of object name to spell ID.
        name_by_spell_code (dict[str, str]): A mapping of Spell_ codes to display names.
        name_by_spells_code (dict[str, str]): A mapping of Spells_ codes to display names.
        spell_code_exceptions (dict[str, str]): Manual overrides for unrecognised spell codes. Defaults to SPELL_CODE_EXCEPTIONS.
        tiered_spell_path (str): Path to the tiered spell data directory. Defaults to TIERED_SPELL_PATH.

    Returns:
        list[Spell]: The list of spells with their tiered variants populated.
    """

    for file in os.scandir(tiered_spell_path):
        if not file.is_file() or not file.name.endswith('.de.xml'):
            continue

        file_name: str = file.name.removesuffix('.de.xml').strip()

        result = parse_tier_and_path(file_name)
        if result is None:
            continue

        spell_tier, spell_path = result

        try:
            with open(file.path, 'r', encoding='utf-8') as tiered_spell_file:
                data: dict[str, Any] = json.load(tiered_spell_file)

        except json.JSONDecodeError:
            print(f'Warning: {file_name} could not be parsed.')
            continue

        spell_code: str = data['m_displayName'].strip()
        display_name: str = resolve_spell_code(
            spell_code,
            name_by_spell_code,
            name_by_spells_code,
            spell_code_exceptions,
        )

        spell: Optional[Spell] = spell_by_display_name.get(display_name)
        if spell is None:
            continue

        object_name: str = data['m_name']
        wad_path: str = os.path.join(tiered_spell_path, file_name + '.xml')
        spell_id: int = spell_id_by_object_name.get(object_name, 0)
        tiered_spell: TieredSpell = TieredSpell(
            object_name,
            wad_path,
            spell_id,
            spell_tier,
            spell_path,
        )

        spell.add_tiered_spell(tiered_spell)

    return list(spell_by_display_name.values())


def parse_tier_and_path(file_name: str) -> Optional[ tuple[int, str] ]:
    """
    Parse a tiered spell file stem to extract the tier level and path variant.

    If no tier pattern is found, defaults to tier 1 and path 'Base'.
    If the path is in SKIP_PATHS, returns None to signal the file should be skipped.

    Args:
        file_name (str): The file stem (filename without the '.de.xml' suffix).

    Returns:
        tuple[int, str] | None: A (tier, path) tuple, or None if the file should be skipped.
    """

    match = TIER_PATH_PATTERN.search(file_name)

    if match:
        spell_tier: int = int(match.group(1))
        spell_path: str = match.group(2) or 'A'
    else:
        spell_tier = 1
        spell_path = 'Base'

    if spell_path in SKIP_PATHS:
        return None

    return spell_tier, spell_path


def tiered_spell_sort_key(tiered_spell: TieredSpell) -> tuple[int, int]:
    """
    Return a sort key for a TieredSpell based on tier then path order.

    Args:
        tiered_spell (TieredSpell): The tiered spell instance to generate a key for.

    Returns:
        tuple[int, int]: A (tier, path_order) tuple used for sorting.
    """

    tier: int = tiered_spell.spell_tier or 0
    path: int = PATH_ORDER.get(tiered_spell.spell_path or '', 99)

    return tier, path


def spell_to_dict(spell: Spell) -> dict:
    """
    Serialize a Spell instance to a dictionary for JSON export.

    The tier/path combination is used as the key for each TieredSpell entry.
    Tier 1 Base is represented as '1', all others as the tier number followed
    by the path letter (e.g. '2A', '3B').

    Args:
        spell (Spell): The spell instance to serialize.

    Returns:
        dict: A dictionary containing the spell's display name, group index, and tiered spell IDs.
    """

    result: dict = {
        'display_name': spell.display_name,
        'tiered_spell_group': str(spell.tiered_spell_group),
    }

    for tiered_spell in sorted(spell.tiered_spells, key=tiered_spell_sort_key):
        key: str = str(tiered_spell.spell_tier)

        if tiered_spell.spell_path and tiered_spell.spell_path != 'Base':
            key += tiered_spell.spell_path

        result[key] = str(tiered_spell.spell_id)

    return result


def export_spells(spells: list[Spell], output_path: str) -> None:
    """
    Export a list of spells to a JSON file.

    Args:
        spells (list[Spell]): The list of spells to export.
        output_path (str): The file path to write the JSON output to.
    """

    data = [spell_to_dict(spell) for spell in spells]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main() -> None:
    """
    Entry point for the Tiered Spells processing pipeline.
    """

    start: float = time.perf_counter()

    # {TieredSpellGroup: ObjectName}
    object_name_by_group: dict[int, str] = get_object_name_by_group(SPELL_GROUP_PATH)

    # {ObjectName: SpellID}
    spell_id_by_object_name: dict[str, int] = get_spell_id_by_object_name(MANIFEST_PATH)

    # {SpellCode: DisplayName}
    name_by_spell_code: dict[str, str] = load_lang_file(SPELL_LANG_PATH)
    name_by_spells_code: dict[str, str] = load_lang_file(SPELLS_LANG_PATH)

    spells: list[Spell] = build_spells(object_name_by_group, TIERED_SPELL_PATH, SPELL_GROUP_EXCEPTIONS)
    spells = resolve_display_names(spells, name_by_spell_code, name_by_spells_code, SPELL_CODE_EXCEPTIONS)

    # {DisplayName: Spell}
    spell_by_display_name: dict[str, Spell] = index_spells_by_display_name(spells)

    spells = build_tiered_spells(
        spell_by_display_name,
        spell_id_by_object_name,
        name_by_spell_code,
        name_by_spells_code,
        SPELL_CODE_EXCEPTIONS,
    )

    # for spell in spells:
    #     print(
    #         f'DisplayName: {spell.display_name}\n'
    #         f'SpellCode: {spell.spell_code}\n'
    #         f'TieredSpellGroup: {spell.tiered_spell_group}\n'
    #     )

    #     for tiered_spell in spell.tiered_spells:
    #         print(
    #             f'ObjectName: {tiered_spell.object_name}\n'
    #             f'WadPath: {tiered_spell.wad_path}\n'
    #             f'SpellID: {tiered_spell.spell_id}\n'
    #             f'SpellTier: {tiered_spell.spell_tier}\n'
    #             f'SpellPath: {tiered_spell.spell_path}\n'
    #         )

    export_spells(spells, JSON_EXPORT_PATH)

    elapsed: float = time.perf_counter() - start
    print(f'Completed in {elapsed:.2f}s')


if __name__ == '__main__':
    main()
