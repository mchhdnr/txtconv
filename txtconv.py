import sys
import os.path

def get_input(msg):
	sys.stdout.write(msg)
	sys.stdout.flush()
	return sys.stdin.readline().replace("\n","")

def parse_range(str):
	if len(str)==0:
		return -1,1
	if str[0].isdigit():
		num = int(str[0])-1
		if len(str)>2 and str[1]=="from" and str[2].isdigit():
			num2 = int(str[2])-1
			return num2,(num2+num)
		else:
			return 0,num
	elif str[0]=="first":
		if len(str)>1 and str[1].isdigit():
			num = int(str[1])-1
			return 0,num
	elif str[0]=="last":
		if len(str)>1 and str[1].isdigit():
			num = int(str[1])-1
			return num,-1
	elif str[0]=="from":
		if len(str)>1 and str[1].isdigit():
			num = int(str[1])-1
			if len(str)>3 and str[2]=="to" and str[3].isdigit():
				num2 = int(str[3])-1
				return num,num2
			return num,-1
	print("unrecognized range: %s" % " ".join(str))
	return -1,-1


argv = sys.argv
argc = len(argv)

print("\033[1;4mTEXT FILE CONVERTER\033[0m")

if argc < 2:
	print("usage: txtconv.py [files]")
	quit()

for fname in argv[1:]:
	try:
		fp = open(fname)
	except IOError:
		print("failed to open ",fname)
		continue
	ext = os.path.splitext(fname)[1]
	data = fp.read()
	newext = ".dat"
	wfname = fname.replace(ext,newext)
	newfname = fname.replace(ext,"")

	sys.stdout.write("\033[38;5;202m")
	if "\r\n" in data:
		#CRLF
		print(" [CRLF] ",end="")
		lines = data.split("\r\n")
	elif "\r" in data:
		#CR
		print(" [CR] ",end="")
		lines = data.split("\r")
	else:
		#assume LF
		print(" [LF] ",end="")
		lines = data.split("\n")
	ln = len(lines)
	print(fname,"(",ln,") -> ",wfname)
	
	start = 0
	end = ln-1
	
	writeflag=False
	delflag=False
	while True:
		cmd = get_input("\033[38;5;202m >\033[38;5;214m>\033[38;5;226m> \033[0m")
		word = cmd.split(" ")
		if word[0]=="quit" or word[0]=="q":
			#q
			fp.close()
			quit()
		elif word[0]=="continue":
			#skip this
			break
		elif word[0]=="skip" or word[0]=="delete" or word[0]=="del":
			#del **
			if len(word) == 1:
				print("usage: [skip/delete/del] [lines to skip]\n")
				continue
			if word[0]=="skip" and len(word) == 3:
				if word[1]=="this" and word[2]=="file":
					break
			start,end=parse_range(word[1:])	
			if start!=-1:
				if end!=-1:
					print("skip: %d ~ %d" % (start+1,end+1))
				else:
					print("skip: %d ~ end" % (start+1))
					end=ln-1
				delflag=True
			else:
				delflag=False
				start=0
				end=ln-1

			continue
		elif word[0]=="print" or word[0]=="write":
			#print **d
			if len(word) == 1:
				print("usage: [print/write] [lines to write]\n")
				continue
			start,end=parse_range(word[1:])
			if start!=-1:
				if end!=-1:
					print("print: %d ~ %d" % (start+1,end+1))
				else:
					print("print: %d ~ end" % (start+1))
					end=ln-1
				delflag=False
			else:
				delflag=False
				start=0
				end=ln-1
			continue
		elif word[0]=="run" or word[0]=="r":
			#run
			writeflag=True
			break
		elif word[0]=="new":
			if len(word) < 3:
				print("usage: new [extension/filename] [string]")
				continue
			if word[1]=="ext" or word[1]=="extension":
				newext = "."+word[2]
				print("new extension set to %s" % newext)
				wfname = newfname+newext
			elif word[1]=="filename":
				wfname = word[2]+newext
				newfname = word[2]
			print("new output file name ",wfname)
		elif word[0]=="show":
			print("extension\t%s" % newext)
			if delflag:
				print("range\t\tskip ", end="")
			else:
				print("range\t\tprint ", end="")
			print("from %d to %d" % (start+1,end+1))
		else:
			print("invalid command ",word[0])
	if writeflag:
		sys.stdout.write("writing...")
		sys.stdout.flush()
		try:
			fw = open(fname.replace(ext,newext),"w")
		except IOError:
			sys.stdout.write("\nfailed to open the output file\n")
		else:
			i=0
			while i<ln:
				if (delflag and ( i<start or end<i ) ) or (not(delflag) and start<=i and i<=end ):
					if i!=ln-1:
						fw.write(lines[i]+"\n")
					else:
						fw.write(lines[i])
				i+=1
			fw.close()
			sys.stdout.write("done\n")
			sys.stdout.flush()
