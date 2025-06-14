import sys
import os
import shutil
import json
import ffmpeg
from datetime import datetime
import dateutil
import dateutil.parser
import pytz  # for time zones
from PIL import Image
from PIL.ExifTags import TAGS
from colorama import init
from colorama import Fore, Back, Style
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
init()

# X	Add argment check for final
# X	Add Colors
# X	Better format screen output
# X	Actually Rename file
# X	Move to dest directory
# X	Log Results to Excel
# X Add error handling to jpeg ext
# X	Handle duplicate second pictures
# TODO	Possibly rename the project

# Get Script Parameters
scriptpath = os.path.dirname(__file__) + "\\"
print(scriptpath)

# Get config
# scriptpath + 'config.json'
config = os.path.join(scriptpath, '.pref', 'config.json')

with open(config) as f:
    config = json.load(f)
    f.close()

sourcepath = config["source"]
destpath = config["dest"]
destsecondpath = config["second-copy"]
logpath = scriptpath + config["log"]

print("Source: ", sourcepath)
print("Dest: ", destpath)

timezone = pytz.timezone(config["timezone"])

def get_date_filmed(path):
	# uses ffprobe command to extract all possible metadata from the media file
	# Other data is returned with this, I'm interested in ['tags']['creation_time']
	metadata = ffmpeg.probe(path)["streams"][1]
	# this gets the time of the metadata and when the image/video was captured
	ct = metadata['tags']['creation_time']
	create_time = dateutil.parser.isoparse(ct)
	# Documentation on astimezone - https://pypi.org/project/pytz/
	create_time_local = create_time.astimezone(timezone)
	return (create_time_local)


def get_screenshot_date(file_path):
	# https://x.com/i/grok?conversation=1920649389707542832
    """
    Extract date and time from a screenshot filename and return a datetime object.

    Args:
        file_path (str): Path to the screenshot file (e.g., 'Screenshot_20250108-143022.png')

    Returns:
        datetime: Datetime object representing the date and time in the filename

    Raises:
        ValueError: If the filename format is invalid
    """
    try:
        # Extract filename from path
        filename = os.path.basename(file_path)

        # Remove 'Screenshot_' prefix and '.png' suffix
        date_str = filename.replace('Screenshot_', '').replace('.png', '')

        # Parse the date string (YYYYMMDD-HHMMSS) into a datetime object
        return datetime.strptime(date_str, '%Y%m%d-%H%M%S')
    except ValueError:
        raise ValueError(
            "Invalid filename format. Expected 'Screenshot_YYYYMMDD-HHMMSS.png'")


def get_date_taken(path, filename, ext):
	# EXIF Reference https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
	try:
		create_time = Image.open(path)._getexif()[36867]
	except:
		try:
			create_time = Image.open(path)._getexif()[36868]
		except:
			# This is for jpegs created by the Plant Checking App
			# Metadata isn't complete, but the filename is right so use that.
			if ext == ".jpeg":
				rawfile = os.path.splitext(filename)[0]
				rawfile = rawfile[0:len(rawfile)-6]
				# print(rawfile)
				datetry = datetime.strptime(rawfile, "%Y-%m-%dT%H_%M_%S")
				# print(datetry,type(datetry))
				create_time = datetry
			else:
				create_time = "No Value"

	if type(create_time) is datetime:
		dt = create_time
	else:
		try:
			dt = datetime.strptime(create_time, "%Y:%m:%d %H:%M:%S")
		except:
			dt = None
	return dt


def main():
    df = pd.DataFrame(columns=['Date', 'Sequence', 'Source', 'Old', 'Dest', 'New'])

    # Run in Proof mode unless "final" is provided as an argument
    args = sys.argv[1:]
    # print("Arg Length: ", len(args))

    if ("FINAL" in (x.upper() for x in args) and len(args) >= 1):
        runmode = "final"
    else:
        runmode = "proof"

    # For Testing
    # runmode = "final"

    for root, dirs, files in os.walk(sourcepath):
        if (runmode == "final"):
            print(Fore.WHITE + Back.MAGENTA +
                "***************** FINAL MODE *****************" + Back.BLACK + Fore.WHITE)
        else:
            print(Fore.BLUE + "***************** PROOF MODE *****************" +
                Back.BLACK + Fore.WHITE)

        i = 0
        for f in files:
            i = i+1
            fdate = None
            p = os.path.join(root, f)
            ext = os.path.splitext(p)[1].lower()
            # print(p,type(p))
            # print(get_date_taken(p))
            # print(ext,type(ext))

            piclist = ['.png', '.jpg', '.jpeg']
            movlist = ['.mp4']

            if ext in piclist:
                fdate = get_date_taken(p, f, ext)
            if ext in movlist:
                ext = ".mp4"

                fdate = get_date_filmed(p)
            if fdate == None and f.find("Screenshot") >= 0:
                fdate = get_screenshot_date(p)

            # print(fdate, type(fdate))

            if fdate:
                # Rename the file
                # YYYY-MM-DD HH.MM.SS
                newname = fdate.strftime("%Y-%m-%d %H.%M.%S") + ext

                # Check if the new filename has already been used
                count = 1
                while (newname in set(df['New'])):
                    newname = fdate.strftime("%Y-%m-%d %H.%M.%S") + "-" + str(count) + ext
                    count = count + 1

                if not (f == newname):
                    if (runmode == "final"):
                        if os.path.exists(sourcepath+f):
                            if not os.path.exists(destpath):
                                print("\tDestination path doesn't exist.")
                                os.mkdir(destpath)
                                print("\tPath created: ", destpath)

                    if count > 1:
                        print("\t" + Fore.RED + Back.YELLOW +
                            "Filename already used." + Fore.WHITE + Back.BLACK)

                    print(str(i) + "\t" + Fore.RED + f + Fore.YELLOW + "  ->  " +
                                        Fore.GREEN + newname + Back.BLACK + Fore.WHITE)

                    if (runmode == "final"):
                        try:
                                # Move the file
                                # This puts a second copy for full preservation
                                shutil.copy(sourcepath+f, destsecondpath+newname)
                                results = shutil.move(sourcepath+f, destpath+newname)
                                new_row = {'Date': datetime.now(),
                                                                'Sequence': i,
                                                                'Source': sourcepath,
                                                                'Old': f,
                                                                'Dest': destpath,
                                                                'New': newname}
                                df.loc[len(df)] = new_row
                        except:
                            print("\tFile can't be renamed and moved:", f)
                # print("\tSource + F:", sourcepath+f)
                # print("\tDest + newname: ", destpath+newname)
                            continue
                else:
                    print(str(i) + "\t" + Back.BLUE + Fore.WHITE + f + \
                        " correctly named." + Back.BLACK + Fore.WHITE)
                    if (runmode == "final"):
                        try:
                            # Move the file
                            results = shutil.move(sourcepath+f, destpath+newname)
                            new_row = {'Date': datetime.now(),
                                        'Sequence': i,
                    'Source' : sourcepath,
                    'Old': f,
                    'Dest': destpath,
                    'New': newname}
                            df.loc[len(df)] = new_row
                            # print("\ttrying to move the correctly named file")
                        except:
                            print("\tFile can't be renamed and moved:", f)
            else:
                print(str(i) + "\t" + Back.RED + "Date not determinable: ",
                    f, Fore.WHITE + Back.BLACK)

    # Save the results to Excel if final mode
    # https://stackoverflow.com/questions/69289569/append-data-to-the-last-row-of-the-excel-sheet-using-pandas
    if (runmode == "final"):
        wb = load_workbook(filename=logpath)
        ws = wb["Pictures"]
        for r in dataframe_to_rows(df, index=False,header=False):
            ws.append(r)
        wb.save(logpath)

    # input("Press ENTER to continue")

if __name__ == "__main__":
    main()