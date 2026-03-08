# Tiered-Spells

Tiered Spell Extraction for Wizard101.

Parses Wizard101 game data files to extract and organize tiered spell information, mapping spells to their tiers, paths, and IDs.

## Requirements

- Python 3.10+
- Wizard101 game data extracted to a `Root/` directory

## Project Structure

```
Root/
├── TemplateManifest.de.xml     # Spell ID manifest
├── TieredSpells.de.xml         # Tiered spell group list
├── Spells/
│   └── Tiered Spells/          # Individual tiered spell data files
└── Locale/
    └── en-US/
        ├── Spell.lang          # Spell display name localization
        └── Spells.lang         # Spells localization
```

```
Main.py         # Entry point and data extraction pipeline
Spell.py        # Spell class representing a spell with tiered variants
TieredSpell.py  # TieredSpell class representing a single tiered variant
```

## Classes

### `Spell`
Represents a spell containing a group of tiered variants.

| Attribute | Type | Description |
|---|---|---|
| `display_name` | `str \| None` | Display name of the spell |
| `spell_code` | `str \| None` | Internal code identifier |
| `tiered_spell_group` | `int \| None` | Group index (non-negative) |
| `tiered_spells` | `list[TieredSpell]` | List of tiered variants |

### `TieredSpell`
Represents a single tiered variant of a spell.

| Attribute | Type | Description |
|---|---|---|
| `object_name` | `str \| None` | Spell object name |
| `wad_path` | `str \| None` | WAD file path |
| `spell_id` | `int \| None` | Unique spell ID (non-negative) |
| `spell_tier` | `int \| None` | Tier level (1–5) |
| `spell_path` | `str \| None` | Path variant (`Base`, `A`, `B`, `C`, or `D`) |

## Output

Results are exported to a JSON file. Each entry represents a spell with its tiered variant IDs keyed by tier and path (e.g. `1`, `2A`, `3B`).

## Usage

```
python Main.py
```
