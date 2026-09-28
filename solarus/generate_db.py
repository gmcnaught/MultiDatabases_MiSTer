#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github"))

from db_helpers import (  # noqa: E402
    ArchiveMember,
    SelectiveArchive,
    build_multi_selective_archive_database,
    generation_timestamp,
    generator_parser,
    github_latest_release,
    http_get_bytes,
    matching_release_asset,
    read_archive_members,
    release_asset_url,
    write_bundle,
)


FOLDER = "solarus"
UPSTREAM = "gmcnaught/solarus-mister"
ARCHIVE_ID = "release"
ASSET_PATTERN = re.compile(r"solarus-mister-(v\d+\.\d+\.\d+)\.zip", re.IGNORECASE)
CORE_PATTERN = re.compile(r"_Other/Solarus_\d{8}\.rbf")
MODULE_PATTERN = re.compile(r"games/Solarus/platform/mem_wc/mem_wc-[^/]+\.ko")
INSTALL_ROOTS = ("Scripts/", "_Other/", "docs/Solarus/", "games/Solarus/")
# Release provenance for the ZIP itself, so it is dropped instead of landing on
# the SD card root.
IGNORED = ("BUILD-INFO.txt",)
# Upstream v1.3.1 launches through the shared mister-hybrid platform instead of
# the v1.2 auto-launch daemon: MiSTer.ini [Solarus] main= points at
# games/Solarus/platform/MiSTer_hybrid, which starts games/Solarus/launch.sh from
# the hybrid.d/ registry entry next to it. Scripts/Solarus.sh turns that main=
# line on and removes the old daemon. (v1.3.0 shipped the hook under linux/, a
# root folder the Downloader refuses for this database, so it was never
# published here.)
REQUIRED = (
    "Scripts/Solarus.sh",
    "games/Solarus/launch.sh",
    "games/Solarus/libs/libsolarus.so.1",
    "games/Solarus/platform/MiSTer_hybrid",
    "games/Solarus/platform/hybrid.d/Solarus.conf",
    "games/Solarus/platform/launch_lib.sh",
    "games/Solarus/solarus-run",
)


def selected_files(
    members: Sequence[ArchiveMember],
) -> tuple[tuple[str, ArchiveMember], ...]:
    """Validate the release layout and install every file it publishes."""
    installable = [member for member in members if member.path not in IGNORED]
    unexpected = sorted(
        member.path
        for member in installable
        if not member.path.startswith(INSTALL_ROOTS)
    )
    if unexpected:
        raise RuntimeError(
            "Solarus MiSTer ZIP installs outside its MiSTer folders: "
            + ", ".join(unexpected)
        )

    cores = sorted(
        member.path for member in installable if CORE_PATTERN.fullmatch(member.path)
    )
    if len(cores) != 1:
        raise RuntimeError(
            "Solarus MiSTer ZIP must ship exactly one "
            "_Other/Solarus_YYYYMMDD.rbf core, found: "
            + (", ".join(cores) or "none")
        )

    missing = sorted(set(REQUIRED).difference(member.path for member in installable))
    if missing:
        raise RuntimeError(
            "Solarus MiSTer ZIP is missing required files: " + ", ".join(missing)
        )

    return tuple(
        (member.path, member)
        for member in sorted(installable, key=lambda member: member.path)
    )


def main() -> int:
    args = generator_parser(
        FOLDER, "Generate the Solarus MiSTer database"
    ).parse_args()
    release = github_latest_release(UPSTREAM)
    asset = matching_release_asset(release, ASSET_PATTERN)
    archive_url = release_asset_url(asset)
    archive_data = http_get_bytes(archive_url)
    members = read_archive_members(archive_data)

    version = ASSET_PATTERN.fullmatch(str(asset["name"])).group(1)
    selected = selected_files(members)
    database = build_multi_selective_archive_database(
        folder=FOLDER,
        repository=args.repository,
        timestamp=generation_timestamp(args.timestamp),
        archives=(
            SelectiveArchive(
                archive_id=ARCHIVE_ID,
                url=archive_url,
                data=archive_data,
                selected_files=selected,
                description=f"Installing Solarus MiSTer {version}",
                # An already-loaded kernel module stays resident after its file
                # changes, so a matching module update takes effect on reboot.
                reboot_paths=tuple(
                    path for path, _ in selected if MODULE_PATTERN.fullmatch(path)
                ),
            ),
        ),
        filter_terms=(FOLDER, "other"),
        tag_aliases=((FOLDER, "solarus-mister"),),
    )
    write_bundle(database, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
