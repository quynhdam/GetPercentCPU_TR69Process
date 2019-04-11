#$language = "python"
#$interface = "1.0"


import os
import subprocess
import datetime
LOG_DIRECTORY = os.path.join(
	os.path.expanduser('~'), 'SecureCRT')

LOG_FILE_TEMPLATE = os.path.join(
	LOG_DIRECTORY, "Command_Results.txt")
LOG = os.path.join(
	LOG_DIRECTORY, "Results.txt")

SCRIPT_TAB = crt.GetScriptTab()

COMMANDS = [	
	"top",
	]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():

	if not os.path.exists(LOG_DIRECTORY):
		os.mkdir(LOG_DIRECTORY)

	if not os.path.isdir(LOG_DIRECTORY):
		crt.Dialog.MessageBox(
			"Log output directory %r is not a directory" % LOG_DIRECTORY)
		return

	if not SCRIPT_TAB.Session.Connected:
		crt.Dialog.MessageBox(
			"Not Connected.  Please connect before running this script.")
		return

	SCRIPT_TAB.Screen.IgnoreEscape = True
	
	while True:
		if not SCRIPT_TAB.Screen.WaitForCursor(1):
			break
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1

	prompt = SCRIPT_TAB.Screen.Get(rowIndex, 0, rowIndex, colIndex)
	prompt = prompt.strip()

	for (index, command) in enumerate(COMMANDS):
		command = command.strip()

		# Set up the log file for this specific command
		logFileName = LOG_FILE_TEMPLATE % {"NUM" : NN(index + 1, 2)}
		
		# Send the command text to the remote
		SCRIPT_TAB.Screen.Send(command + '\r')

		# Wait for the command to be echo'd back to us.
		SCRIPT_TAB.Screen.WaitForString('\r', 1)
		SCRIPT_TAB.Screen.WaitForString('\n', 1)
		SCRIPT_TAB.Screen.Send("q" + chr(13))
		# Use the ReadString() method to get the text displayed while
		# the command was runnning.  Note also that the ReadString()
		# method captures escape sequences sent from the remote machine
		# as well as displayed text.  As mentioned earlier in comments
		# above, if you want to suppress escape sequences from being
		# captured, set the Screen.IgnoreEscape property = True.
		result = SCRIPT_TAB.Screen.ReadString(prompt)
	
		result = result.strip()
		
		filep = open(logFileName, 'a')

		# If you don't want the command logged along with the results, comment
		# out the very next line
		filep.write("<<<=========================================================================================>>>"+ os.linesep)
		filep.write("Results of command: " + command + " at " +datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + os.linesep)

		# Write out the results of the command to our log file
		filep.write(result + os.linesep)
		
		# Close the log file
		filep.close()
		GetCPU()
		

	# Once we're complete, let's bring up the directory containing the
	# log files.
	LaunchViewer(LOG_DIRECTORY)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def LaunchViewer(filename):
	try:
		os.startfile(filename)
	except AttributeError:
		subprocess.call(['open', filename])


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def NN(number, digitCount):
	# Normalizes a single digit number to have digitCount 0s in front of it
	format = "%0" + str(digitCount) + "d"
	return format % number 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def GetCPU():
	
	logResult=LOG
	logFileName = LOG_FILE_TEMPLATE

	f = open(logFileName, 'r')
	for line in f:
		if "tr69" in line:
			string = line
			#crt.Dialog.MessageBox(string)
			arr=string.split()
			for n in arr:
				#crt.Dialog.MessageBox(arr[5])
				#if arr[5] > 0.5 :
					#crt.Dialog.MessageBox("CPU of TR69 process over 50%")
				fResult=open(logResult,'a')
				now = datetime.datetime.now()
				date_time = now.strftime("%m/%d/%Y, %H:%M:%S ===> ")
				fResult.write(date_time + arr[5] + os.linesep)
				fResult.close()
				break	
			break
	crt.Screen.Send("echo 'Done'" +chr(13))
main()

