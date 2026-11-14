# onedrive-photo-namer

Renames photos and videos from a camera-upload folder to the Dropbox Camera Uploads naming convention
(`YYYY-MM-DD HH.MM.SS.ext`) and moves them to a destination folder, logging every rename to a spreadsheet. Works on
png, jpg, jpeg and mp4 files; the date comes from the file's metadata or its name.

## Run it

`uv sync`, then `uv run --frozen main.py` (proof mode: shows what it would do, changes nothing) or
`uv run --frozen main.py final` (makes the changes). Tested on Windows only.

## Configuration

`.pref\config.json`:

| Key | What it is | Example |
|---|---|---|
| `source` | Folder to rename from | `C:\path\Camera Uploads Raw\` |
| `dest` | Where renamed files go | `C:\path\Camera Uploads\` |
| `second-copy` | Optional folder for a second copy | `C:\path\Renamed Temp\` |
| `sourcetest`, `desttest` | Folders used in proof mode | |
| `log` | Spreadsheet the renames are logged to | `log.xlsx` |
| `timezone` | Time zone for dates ([list](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)) | `America/Chicago` |

## Schedule

On the author's PC: Task Till Dawn, every 30 minutes, via `.cmd\final-mode.cmd` (final mode, through a shared job
runner that writes a JSON log).

## Output

Renamed files in `dest`, and one row per rename in the `log` spreadsheet. Files whose date can't be read are left
where they are.
