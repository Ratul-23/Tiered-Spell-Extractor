# Tiered-Spells

Tiered Spell Extraction for Wizard101.

Parses Wizard101 game files directly from the WAD archive to extract and organize tiered spell information, mapping spells to their tiers, paths, IDs, schools, and descriptions.

## Requirements

- Python 3.10+
- Wizard101 installed
- [wiztype](https://github.com/wizspoil/wiztype) JSON type dump placed as `types.json` in the project root

### Python Dependencies

```
pip install katsuba
```

## Project Structure

```
Main.py           # Entry point and pipeline
Spell.py          # Spell class
TieredSpell.py    # TieredSpell class
SpellData.py      # SpellData dataclass
Deserializer.py   # WAD archive deserializer (singleton)
types.json        # wiztype type dump (not included)
```

## Classes

### `Spell`
Represents a spell containing a group of tiered variants.

| Attribute | Type | Description |
|---|---|---|
| `display_name` | `str \| None` | Resolved display name of the spell |
| `school` | `str` | Magic school (`Fire`, `Ice`, `Storm`, etc.) |
| `tiered_spell_group` | `int` | Group index (non-negative) |
| `name_locale_code` | `str` | Locale code for the display name |
| `tiered_spells` | `list[TieredSpell]` | List of tiered variants |

### `TieredSpell`
Represents a single tiered variant of a spell.

| Attribute | Type | Description |
|---|---|---|
| `object_name` | `str` | Internal object name |
| `wad_path` | `str` | WAD file path |
| `desc` | `str \| None` | Resolved description |
| `desc_locale_code` | `str` | Locale code for the description |
| `id` | `int \| None` | Unique spell ID (non-negative) |
| `tier` | `int \| None` | Tier level (1–5) |
| `path` | `str \| None` | Path variant (`Base`, `A`, `B`, `C`, or `D`) |

### `SpellData`
Dataclass holding raw data extracted from a tiered spell file.

| Attribute | Type | Description |
|---|---|---|
| `object_name` | `str` | Internal object name |
| `name_locale_code` | `str` | Locale code for the display name |
| `desc_locale_code` | `str` | Locale code for the description |
| `school` | `str` | Magic school |

## Output

Results are exported to `Tiered-Spells.json`. Each entry represents a spell with its display name, school, group index, locale code, and a list of tiered variants with their IDs, tiers, paths, and descriptions.

## Usage

```
python Main.py
```
