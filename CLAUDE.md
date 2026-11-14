# onedrive-photo-namer: notes for Claude

Renames camera uploads to `YYYY-MM-DD HH.MM.SS.ext` and moves them to the destination folder (`main.py final`).
Running it and config keys: `README.md`. **This repo is public** (`themarkwilliams/onedrive`): nothing private or
secret goes in it, notes included.

## How it runs

- Task Till Dawn on xps, "OneDrive Photo Namer", every 30 minutes, via `.cmd\final-mode.cmd` under mark-modules' job
  runner (25 min timeout, homelab#254). Log: `C:\Code\.logs\onedrive-photo-namer.rename.log`; Grafana's `xps-jobs`
  alerts cover it.
- Logs through `mark_log` since 2026-11-13: each rename at INFO, "Filename already used" at WARNING (#2).
- Ask Mark before adding or changing a schedule.

## Config and secrets

`.pref\config.json` is tracked (public): folders, the log spreadsheet and time zone only, never secrets.
`.pref\config-u.json` (an alternate config) is gitignored.

## Gotchas and decisions

- The folder is `onedrive-photo-namer`, the repo `onedrive` (homelab#28).
- `desktop.ini` is skipped; a file whose date can't be read (e.g. `IMG_20260906_130656.jpg`) stays in the source
  folder.
- `.gitignore` ignored itself until 2026-11-13, and the README was tracked as `readme.md`; both fixed then.

## Issues

To-dos, bugs and deferred work are GitHub issues in `themarkwilliams/onedrive` (rules: `C:\OneDrive\Code\issues.md`),
never TODO files or notes. Area labels: `rename` (dates, names and moves, `main.py`), `scheduling` (the Task Till
Dawn job and launcher), `logging` (the job log and levels).
