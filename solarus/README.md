# Solarus MiSTer database

- Database ID:
  [`MultiDatabases/solarus`](https://theypsilon.github.io/DB-Inspector_MiSTer/?database-url=https%3A%2F%2Fraw.githubusercontent.com%2Ftheypsilon%2FMultiDatabases_MiSTer%2Fdb%2Fsolarus%2Fdb.json)
- Upstream:
  [`gmcnaught/solarus-mister`](https://github.com/gmcnaught/solarus-mister)
- Database URL:
  `https://raw.githubusercontent.com/theypsilon/MultiDatabases_MiSTer/db/solarus/db.json`

Solarus MiSTer is a hybrid FPGA/ARM port of the [Solarus](https://www.solarus-games.org)
2D action-RPG engine rather than a standalone FPGA core: the engine runs as ARM
software while a custom FPGA core composites the frame and drives video, audio,
and input. The generator follows the latest GitHub release ZIP named
`solarus-mister-vX.Y.Z.zip` and installs every MiSTer file it publishes — the
`_Other/Solarus_YYYYMMDD.rbf` core and its MGL, the `games/Solarus` engine,
launcher and libraries, the mister-hybrid `main=` hook with this core's registry
entry in `games/Solarus/platform/`, the `Scripts/Solarus.sh` and
`Scripts/Solarus_CoresMenu.sh` entries, and the on-card `docs/Solarus` README.
Only the ZIP's own `BUILD-INFO.txt` release provenance is left out, since it is
not a MiSTer file. Updates to the write-combining kernel module are marked as
requiring a reboot, because an already-loaded copy stays resident.

## Installation

Download
[`downloader_MultiDatabases_solarus.zip`](https://raw.githubusercontent.com/theypsilon/MultiDatabases_MiSTer/db/solarus/downloader_MultiDatabases_solarus.zip),
extract it to `/media/fat` on the MiSTer SD card, and run the MiSTer updaters.

No manual `MiSTer.ini` edit and no BIOS files are required. A **128 MB SDRAM
expansion board** is required, because a quest's graphics are staged into SDRAM
at load time.

Copy at least one quest (a `<name>.sol` file) into
`/media/fat/games/Solarus/quests/`, then run **Solarus** from the MiSTer
**Scripts** menu once. That first run adds
`main=/media/fat/games/Solarus/platform/MiSTer_hybrid` to the `[Solarus]`
section of `MiSTer.ini` (backing the file up first) and loads the core. After
that, loading the core from the menu is enough; pick a quest from the OSD with
**Load Quest**. **Scripts → Solarus_CoresMenu** turns that `main=` line off
and on again.

**Upgrading from the v1.2.x database:** run **Solarus** from the Scripts menu
once after the update. It removes the old auto-launch daemon, its
`user-startup.sh` line and `_handler.sh`, and turns on the `main=` line above.
Until then, loading the core does not start a quest.

Quests are separate downloads with their own licenses — see the upstream
[Getting quests](https://github.com/gmcnaught/solarus-mister#getting-quests)
section. The database supplies only the core, the engine, and the launchers; it
does not include quest data.
