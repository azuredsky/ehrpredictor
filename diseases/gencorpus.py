import os
from os.path import isfile

# The script will generate the full-corpus txt used to make the indexes.

output = open("diseases-full-corpus.txt", "w")

dirs = [f for f in os.listdir(".") if not isfile(f)]
for d in dirs:
    files = os.listdir(d)
    for f in files:
        output.write("{0} {0}/{1}\n".format(d, f))