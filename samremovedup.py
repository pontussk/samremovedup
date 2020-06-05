#!/usr/bin/env python
#pontus.skoglund@gmail.com

"""
Uses the first read among any set of reads with identical start position and fragment length. Keeps track of all fragment lengths for each start position to account for BAM files not sorting on fragment length or end position.
"""

import sys

lastRead = None
lastlengths=[]
for line in sys.stdin:
	if line[0] == '@':
		print line,
		continue
		
	fields = line.split()
	flag = int(fields[1])
	if flag & 0x4: #unmapped read
		continue
    
	chrname = fields[2]
	pos = int(fields[3])
	seq = fields[9]
	length=len(seq)
	
	if lastRead == (chrname, pos) and length in lastlengths:  #True if read is a duplicate
		continue
		
	elif lastRead == (chrname, pos) and length not in lastlengths:  #True if read has same start position but different end (length) as previous reads at same start, use this read
		lastlengths.append(length)
		print line,

	else: #new start position, use this read
		lastRead = (chrname, pos)
		lastlengths=[]
		lastlengths.append(length)
		print line,