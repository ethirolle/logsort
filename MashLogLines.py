## specify the input file here:
infile='C:/Users/ethirolle/PycharmProjects/logsort/001.log'


## create regex to find log linss that start with datetimestamp
import re
## pattern finds date-time stamp at start of line, like
## 2017-11-08 20:38:38
pattern = re.compile("^(\d){4}-(\d){2}-(\d){2} (\d){2}:(\d){2}:(\d){2}")

## open input & output files
fin=open(infile,'r')
fout=open(infile+'mash.txt','w')

## Read the first two lines
line1 = fin.readline()
line2 = fin.readline()

## loop through entire file
while line2:
    ## if next line starts with a datetimestamp, just write current line as-is
    if pattern.match(line2):
        fout.write(line1)
        print line1
        line1=line2
    ## but if next line does NOT start with a datetimestamp, combine next line with the current line
        ## when joining lines, use hopefully-unique separator '||>>||',
        ## so we can find-and-replace this back to newlines later
    else:
        line1 = line1.rstrip('\n') + '||>>||' + line2

    line2 = fin.readline()

## write out the last line
fout.write(line1)
print line1

## close up the files
fin.close()
fout.close()