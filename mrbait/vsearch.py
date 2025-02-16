#!/usr/bin/python
import subprocess
from subprocess import Popen, PIPE, CalledProcessError
import os
import re
from mrbait import seq_graph as sg

"""Includes utilities for calling VSEARCH and parsing output of pairwise alignments"""

def allpairsGlobal(binary, threads, seqpath, qid, qcov, pw, minlen, qmask):
	vsearch = [binary,
			"--allpairs_global", seqpath,
			"--threads", str(threads),
			"--id", str(qid),
			"--minseqlength", str(minlen),
			"--blast6out", pw,
			"--rowlen", "0", "--self",
			"--target_cov", str(qcov),
			"--qmask", str(qmask),
			"--quiet"]
	command = " ".join(vsearch)

	#Vsearch subprocess
	proc = Popen(vsearch, stdout=PIPE, stdin=PIPE, env={'PATH': os.getenv('PATH')})

	#WRap to enable keyboard interrupe
	try:
		t = proc.communicate()[0]
	except KeyboardInterrupt:
		proc.kill()
		raise KeyboardInterrupt

	#Get return code from process
	if proc.returncode:
		raise CalledProcessError ("VSEARCH exited with non-zero status")

def usearchGlobal(binary, threads, seqpath, qpath, qid, qcov, pw, minlen, qmask):
	vsearch = [binary,
			"--usearch_global", seqpath,
			"--db", qpath,
			"--minseqlength", str(minlen),
			"--threads", str(threads),
			"--id", str(qid),
			"--blast6out", pw,
			"--rowlen", "0", "--self",
			"--target_cov", str(qcov),
			"--qmask", str(qmask),
			"--quiet"]
	command = " ".join(vsearch)

	#Vsearch subprocess
	proc = Popen(vsearch, stdout=PIPE, stdin=PIPE, env={'PATH': os.getenv('PATH')})

	#WRap to enable keyboard interrupe
	try:
		t = proc.communicate()[0]
	except KeyboardInterrupt:
		proc.kill()
		raise KeyboardInterrupt

	#Get return code from process
	if proc.returncode:
		raise CalledProcessError ("VSEARCH exited with non-zero status")

#Function to sort FASTA by length, needed before allpairsGlobal call
def sortByLength(binary, seqpath, outpath, minlen):
	vsearch = [binary,
			"--sortbylength", seqpath,
			"--minseqlength", str(minlen),
			"--output", outpath,
			"--quiet"]
	command = " ".join(vsearch)
	#print(command)
	#Vsearch subprocess
	proc = Popen(vsearch, stdout=PIPE, stdin=PIPE, env={'PATH': os.getenv('PATH')})

	#WRap to enable keyboard interrupe
	try:
		t = proc.communicate()[0]
	except KeyboardInterrupt:
		proc.kill()
		raise KeyboardInterrupt

	#Get return code from process
	if proc.returncode:
		raise CalledProcessError ("VSEARCH exited with non-zero status")

#function to mask a given FASTA file and return outputs 
def fastxMask(binary, seqpath, outpath):
	vsearch = [binary,
			"--fastx_mask", seqpath,
			"--min_unmasked_pct", str(0.0),
			"--fastaout", outpath,
			"--qmask", "dust",
			"--quiet"]
	command = " ".join(vsearch)
	#print(command)
	#Vsearch subprocess
	proc = Popen(vsearch, stdout=PIPE, stdin=PIPE, env={'PATH': os.getenv('PATH')})

	#WRap to enable keyboard interrupe
	try:
		t = proc.communicate()[0]
	except KeyboardInterrupt:
		proc.kill()
		raise KeyboardInterrupt

	#Get return code from process
	if proc.returncode:
		raise CalledProcessError ("VSEARCH exited with non-zero status")
		
#Function to sort FASTA by length, needed before allpairsGlobal call
def fastxRevcomp(binary, seqpath, outpath, minlen):
	vsearch = [binary,
			"--fastx_revcomp", seqpath,
			"--fastaout", outpath,
			"--quiet"]
	command = " ".join(vsearch)
	#print(command)
	#Vsearch subprocess
	proc = Popen(vsearch, stdout=PIPE, stdin=PIPE, env={'PATH': os.getenv('PATH')})

	#WRap to enable keyboard interrupe
	try:
		t = proc.communicate()[0]
	except KeyboardInterrupt:
		proc.kill()
		raise KeyboardInterrupt

	#Get return code from process
	if proc.returncode:
		raise CalledProcessError ("VSEARCH exited with non-zero status")


#Function to parse output of allpairsGlobal
def parsePairwiseAlign(filename):
	#Function assumes id's are the first 2 positions, and prepended with "id_"
	#Also assumes file is tab delimited
	#print("parsing pw file")
	bad_ids = []
	filehandle = open(filename, "r")
	for line in filehandle:
		array = re.split(r'\t+', line)
		bad1 = re.sub('id_', '', array[0])
		bad2 = re.sub('id_', '', array[1])
		bad_ids.append([bad1, bad2])
	return(bad_ids)
