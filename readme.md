# OneDrive Scripts
A collection of scripts to improve OneDrive. 

## rename-camera-roll.py
This script will rename files in your OneDrive Camera Roll folder using the Dropbox Camera Uploads Naming Convention (YYYY-MM-DD HH.MM.SS.ext) on all png, jpg, jpeg and mp4 files in the folder specified.

### Configuration
In the config.json file, specify: 
- The path of your OneDrive Camera Roll folder.
- The path where you'd like to store your renamed files.
- Your [timezone](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)

### Usage
The script has two modes: proof and final. 

Proof: See what the output of the script will be before making any changes. This is the default.

Final: Make the changes.

For the script to do anything, run it in final mode by adding the word 'final' as a parameter when calling the script.

	e.g. rename-camera-roll.py final

### Notes
- This script hasn't been run/tested on anything besides Windows.
- There may only ever be one script in this expansive 'collection'