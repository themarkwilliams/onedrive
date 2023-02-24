import os
import json
import ffmpeg
from datetime import datetime
import dateutil
import dateutil.parser
import pytz  # for time zones
from PIL import Image
from PIL.ExifTags import TAGS

timezone = pytz.timezone("America/Chicago")
#from pathlib import Path

def get_date_filmed(path):
	# uses ffprobe command to extract all possible metadata from the media file
	# Other data is returned with this, I'm interested in ['tags']['creation_time']
	metadata = ffmpeg.probe(path)["streams"][1]
	#this gets the time of the metadata and when the image/video was captured
	ct = metadata['tags']['creation_time']
	create_time = dateutil.parser.isoparse(ct)
	# Documentation on astimezone - https://pypi.org/project/pytz/
	create_time_local = create_time.astimezone(timezone)
	return (create_time_local)

def get_date_taken(path):
	#EXIF Reference https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html
	try:
		create_time = Image.open(path)._getexif()[36867]
	except:
		try:
			create_time = Image.open(path)._getexif()[36868]
		except:
			create_time = "No Value"

	dt = datetime.strptime(create_time, "%Y:%m:%d %H:%M:%S")
	return dt

#Get Script Parameters
scriptpath = os.path.dirname(__file__) + "\\"
print(scriptpath)

# Get config
config = scriptpath + 'config.json'
with open(config) as f:
	config = json.load(f)
	f.close()

sourcepath = config["source"]

for root, dirs, files in os.walk(sourcepath):
	for f in files:
		fdate = None
		p = os.path.join(root, f)
		#print(p,type(p))
		#print(get_date_taken(p))
		#For Extensions: .jpg, .png, 
		if f.endswith(".png"):
			ext = ".png"
			fdate = get_date_taken(p)
		if f.endswith(".jpg"):
			ext = ".jpg"
			fdate = get_date_taken(p)
		if (f.endswith(".mp4")):
			ext = ".mp4"
			fdate = get_date_filmed(p)
		print (fdate, type(fdate))
		
		if fdate:
			print("old filename: ", f)
			#YYYY-MM-DD HH.MM.SS
			newname = fdate.strftime("%Y-%m-%d %H.%M.%S") + ext
			print("new filename: ", newname)

			if not(f == newname):
				print("rename this")
				continue