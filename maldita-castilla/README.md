# Maldita Castilla MiSTer database

- Database ID:
  [`MultiDatabases/maldita-castilla`](https://theypsilon.github.io/DB-Inspector_MiSTer/?database-url=https%3A%2F%2Fraw.githubusercontent.com%2Ftheypsilon%2FMultiDatabases_MiSTer%2Fdb%2Fmaldita-castilla%2Fdb.json)
- Upstream:
  [`gmcnaught/maldita.castilla-mister`](https://github.com/gmcnaught/maldita.castilla-mister)
- Database URL:
  `https://raw.githubusercontent.com/theypsilon/MultiDatabases_MiSTer/db/maldita-castilla/db.json`

Maldita Castilla MiSTer is a hybrid FPGA/ARM port of Locomalito's GameMaker
game. The ARM-side `gmloader` engine runs the original game while a custom FPGA
core accelerates rasterisation. The database follows the latest stable,
versioned upstream release and installs its dated core and Cores-menu MGL, the
ARM engine and its launcher, the mister-hybrid `main=` hook with this core's
registry entry, runtime libraries, the optional write-combining kernel module,
and the included game. Everything lands under `_Other/` and `games/gmloader/`.

The original `game.droid` data is byte-identical to Locomalito's original
`data.win`. Locomalito publishes the original game—not the commercial EX
edition—under
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.en).
That permits noncommercial sharing of unmodified material with attribution.
See the [official game page](https://locomalito.com/games/maldita-castilla) and
the [license terms](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.en).

## Installation

Download
[`downloader_MultiDatabases_maldita-castilla.zip`](https://raw.githubusercontent.com/theypsilon/MultiDatabases_MiSTer/db/maldita-castilla/downloader_MultiDatabases_maldita-castilla.zip),
extract it to `/media/fat` on the MiSTer SD card, and run the MiSTer updaters.

Add this required section to `/media/fat/MiSTer.ini`:

```ini
[Maldita Castilla]
main=/media/fat/games/gmloader/platform/MiSTer_hybrid
```

The RBF launch entry point is installed as
`/media/fat/_Other/MalditaCastilla_YYYYMMDD.rbf`, with
`/media/fat/_Other/Maldita Castilla.mgl` pointing at it. Select either from
MiSTer's **_Other** menu. The core loads, and the `main=` hook starts the ARM
engine through `games/gmloader/launch.sh`, which its entry in
`games/gmloader/platform/hybrid.d/` names. Do not point `main=` at
`launch.sh` or another shell script. Creating an empty
`/media/fat/games/gmloader/NOENGINE` file stops the hook from starting the
engine without editing `MiSTer.ini`.

**Upgrading from the v0.3.x database:** replace the old
`main=games/gmloader/MiSTer_Maldita` line with the one above. The update removes
`games/gmloader/MiSTer_Maldita` and the `games/Maldita Castilla/` launcher and
module files. Until you change the line, loading the core only loads the core.

If the Downloader requests a reboot after installing or updating the `mem_wc`
kernel module, reboot before the next launch so an already-loaded copy cannot
remain resident. No BIOS file or separately supplied game file is required.

No daemon is required. When upgrading an older manual installation, delete a
leftover `/media/fat/games/Maldita Castilla/_handler.sh` before launching: the
Master_Daemon treats that filename as a hook and can otherwise start a second
engine. If multiple dated `_Other/MalditaCastilla_*.rbf` files remain after an
update, remove the older copies so the Cores menu cannot launch a stale core.
