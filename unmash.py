## specify the input (mashed) file here
infile='C:/Users/ethirolle/PycharmProjects/logsort/001.logmash.sort'

## import library needed for string replace operation
import string

## open input & output files
fin=open(infile,'r')
fout=open(infile+'-unmash.txt','w')

line=fin.readline()

## loop through whole file, replacing the mash separator with newlines
while line:
    splitline=string.replace(line, '||>>||', '\n')
    print splitline
    fout.write(splitline)
    line = fin.readline()

## close up files
fin.close()
fout.close()