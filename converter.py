import glob
from os import path
import os
import shutil

source_path = '../../data/recogtrend_test/results/*'
images_folder = '../../data/my-drive/Database_FoodTrend_Data/**/*.jpg'

files = glob.glob(source_path)

images_listed = {path.basename(f)[:-4]: [] for f in glob.glob(images_folder)}
for f in glob.glob(images_folder):
	images_listed[path.basename(f)[:-4]] += [path.basename(path.dirname(f))]
for f in files:
	print(path.basename(f))
for f in files:
	if path.basename(f).isnumeric():
		continue
	print(path.basename(f))
	if path.basename(f)[:-4] in images_listed:
		for folder in images_listed[path.basename(f)[:-4]]:
			target_path = path.join(path.dirname(f), folder, path.basename(f))
			print('We moved', f, target_path)

			if not os.path.exists(os.path.dirname(target_path)):
				os.mkdir(os.path.dirname(target_path))
			shutil.copy(f, target_path)


# print('images_listed', images_listed)