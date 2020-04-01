import fileinput
import sys
from os import path as pa

patterns = [
	('		<amount>28w0</amount>', '		<amount>280</amount>')
]


def replaceAll(file):
	for line in fileinput.input(file, inplace=1):
		for (searchExp, replaceExp) in patterns:
			if searchExp in line:
				line = line.replace(searchExp, replaceExp)
		sys.stdout.write(line)

import glob

source_path = '../../data/annotation/results/**/*.xml'
for path in glob.glob(source_path):
	print(pa.abspath(path))
	replaceAll(pa.abspath(path))

