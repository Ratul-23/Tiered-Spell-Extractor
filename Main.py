import time

from Deserializer import Deserializer
from SpellData import SpellData

from Spell import Spell
from TieredSpell import TieredSpell


INSTALL_PATH: str = 'C:/ProgramData/KingsIsle Entertainment/Wizard101/'
TYPE_DUMP_PATH: str = ''


def main() -> None:
    deserializer: Deserializer = Deserializer(INSTALL_PATH, TYPE_DUMP_PATH)

    # {TieredSpellGroup: ObjectName}
    object_name_by_group: dict[int, str] = deserializer.get_object_name_by_group()

    # {Path: SpellID}
    spell_id_by_path: dict[str, int] = deserializer.get_spell_id_by_path()

    # {LocaleCode, String}
    name_by_spell_code: dict[str, str] = deserializer.get_string_by_locale_code()

    # {Path: SpellData}
    spell_data_by_path: dict[str, SpellData] = deserializer.get_spell_data_by_path()


if __name__ == '__main__':
    main()
