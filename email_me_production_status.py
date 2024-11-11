#! /usr/bin/env python
# Python program to demonstrate
# main() function
import sys, os
import fileinput
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import subprocess 
from xml.dom.minidom import parse

#print("Hello")

# def sendemail()
# project has difference 2/1000, please go to poms to stop submission
# definition has 100 total files and 1 in merging.

def email_me_production_status(email, text, html, project):

    msg=MIMEMultipart('alternative')
    
    msg['Subject'] = "Status of production campaign: " + project
    msg['From'] = "noreply-uboonepro"
    msg['To'] = email
    msg['Cc'] = "liang.neu.liu@gmail.com"
    rcpt=["liang.neu.liu@gmail.com"] + [email]
    
    
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    msg.attach(part1) # text must be the first one
    msg.attach(part2) # html must be the last one
    
    
    # Send the mail
    
    me="uboonepro"
    #you="liang.neu.liu@gmail.com"
    server = smtplib.SMTP('localhost')
    server.sendmail(me, rcpt, msg.as_string())
    server.quit()

def write_the_message(manager, xml, stage, defs, inputdef):
#    inputdef=get_input_def_from_xml(xml, stage)
    input_total, input_merging = check_input_defs(inputdef)
    output_total, output_merging = check_output_defs(defs)
    difference, check_input_results = check_input_difference(xml, stage)
    completeness = int(100*(float(input_total) - float(difference))/float(input_total))
    
    sum_output_merging = 0
    for imerging in output_merging:
	sum_output_merging+=int(imerging)


    if int(difference) != 0 :
        text=""
        html="<html><head></head><body>"
        # Running status
    
        text+="Hi " + manager + "\n"
        text+="Campaign Running! \n"
        text+="Your job is " + str(completeness) + "% complete!  \n"
        text+="Total input files      : " + str(input_total) + " in input definition " + inputdef + "\n"
        text+="Submited files         : " + str(int(input_total) - int(difference)) + "\n"
        text+="Files in waiting pool  : " + str(difference) + "\n"
        text+="Files in output definition : " + "\n"
        for i in range(len(output_total)):
            text+="    " + str(output_total[i]) + " files in " + defs.split(",")[i] + "\n"
            text+="    " + str(output_merging[i]) + " files in merging pool." + "\n"
        text+=check_input_results
        #print(text)
        
     
        html+="""<p style="color: black;">Hi """ + manager + """ </p>"""
        html+="""<h2 style="color: green;">Campaign Running! </h2>"""
        html+="""<p style="color: black;">Your job is """ + str(completeness) + """% complete! </p>"""
        html+="""<p style="color: black;">Total input files      : """ + str(input_total) + """ in input definitio """ + inputdef + """</p>"""
        html+="""<p style="color: black;">Submited files         : """ + str(int(input_total) - int(difference)) + """</p>"""
        html+="""<p style="color: black;">Files in waiting pool  : """ + str(difference) + """</p>"""
        html+="""<p style="color: black;">Files in output definition : """ + """</p>"""
        for i in range(len(output_total)):
            html+="""<p style="color: black;">    """ + str(output_total[i]) + """ files in """ + defs.split(",")[i] + """</p>"""
            html+="""<p style="color: limegreen;">    """ + str(output_merging[i]) + """ files in merging pool.""" + """</p>"""
	for line in check_input_results.split("\n"):
            html+="""<p style="color: black;">""" + line + """"</p>"""
        html+="""</body></html>"""
        #print(html)
	return text, html, 2
    

    # submission is complete, merging 

    if int(difference) == 0 and sum_output_merging != 0:
        text=""
        html="<html><head></head><body>"
        # Running status
    
        text+="Hi " + manager + "\n"
        text+="Campaign Merging! \n"
        text+="Your job is " + str(completeness) + "% complete!  \n"
        text+="Please go to the page of your campaign to stop the submission. (Please ignore if you have stopped the submission)\n"
        text+="Files in output definition : " + "\n"
        for i in range(len(output_total)):
            text+="    " + str(output_total[i]) + " files in " + defs.split(",")[i] + "\n"
            text+="    " + str(output_merging[i]) + " files in merging pool." + "\n"
        text+="Total input files      : " + str(input_total) + " in input definition " + inputdef + "\n"
        text+="Submited files         : " + str(int(input_total) - int(difference)) + "\n"
        text+="Files in waiting pool  : " + str(difference) + "\n"
        text+=check_input_results
        #print(text)
        
     
        html+="""<p style="color: black;">Hi """ + manager + """ </p>"""
        html+="""<h2 style="color: limegreen;">Campaign Merging! </h2>"""
        html+="""<p style="color: black;">Your job is """ + str(completeness) + """% complete! </p>"""
        html+="""<p style="color: red;">Please go to the page of your campaign to stop the submission. (Please ignore if you have stopped the submission)</p>"""
        html+="""<p style="color: black;">Files in output definition : """ + """</p>"""
        for i in range(len(output_total)):
            html+="""<p style="color: black;">    """ + str(output_total[i]) + """ files in """ + defs.split(",")[i] + """</p>"""
            html+="""<p style="color: limegreen;">    """ + str(output_merging[i]) + """ files in merging pool.""" + """</p>"""
        html+="""<p style="color: black;">Total input files      : """ + str(input_total) + """ in input definition """ + inputdef + """</p>"""
        html+="""<p style="color: black;">Submited files         : """ + str(int(input_total) - int(difference)) + """</p>"""
        html+="""<p style="color: black;">Files in waiting pool  : """ + str(difference) + """</p>"""
	for line in check_input_results.split("\n"):
            html+="""<p style="color: black;">""" + line + """"</p>"""
        html+="""</body></html>"""
        #print(html)
	return text, html, 1
    
 
    # merging is complete, run check_def.sh and exit
    if int(difference) == 0 and sum_output_merging == 0:
        print('/exp/uboone/app/users/uboonepro/check_defs_script/check_defs.sh -i ' + inputdef + ' -o ' + defs)
	check_defs_output = subprocess.check_output('/exp/uboone/app/users/uboonepro/check_defs_script/check_defs.sh -i ' + inputdef + ' -o ' + defs, shell=True)
        #print(check_defs_output)
        text=""
        html="<html><head></head><body>"
        # Running status
    
        text+="Hi " + manager + "\n"
        text+="Campaign Complete! \n"
        text+="Your job is " + str(completeness) + "% complete!  \n"
        text+="Please post output definition to the spreadsheet! \n"
        text+="Files in output definition : " + "\n"
        for i in range(len(output_total)):
            text+="    " + str(output_total[i]) + " files in " + defs.split(",")[i] + "\n"
            text+="    " + str(output_merging[i]) + " files in merging pool." + "\n"
        text+="Total input files      : " + str(input_total) + " in input definition " + inputdef + "\n"
        text+="Submited files         : " + str(int(input_total) - int(difference)) + "\n"
        text+="Files in waiting pool  : " + str(difference) + "\n"
        text+="check_def.sh output\n"
	for line in check_defs_output.split("\n"):
	    text+=line + "\n"
        #print(text)
        
     
        html+="""<p style="color: black;">Hi """ + manager + """ </p>"""
        html+="""<h2 style="color: red;">Complete! </h2>"""
        html+="""<p style="color: black;">Your job is """ + str(completeness) + """% complete! </p>"""
        html+="""<p style="color: red;">Please post output definition to the spreadsheet! </p>"""
        html+="""<p style="color: black;">Files in output definition : """ + """</p>"""
        for i in range(len(output_total)):
            html+="""<p style="color: black;">    """ + str(output_total[i]) + """ files in """ + defs.split(",")[i] + """</p>"""
            html+="""<p style="color: limegreen;">    """ + str(output_merging[i]) + """ files in merging pool.""" + """</p>"""
        html+="""<p style="color: black;">Total input files      : """ + str(input_total) + """ in input definition """ + inputdef + """</p>"""
        html+="""<p style="color: black;">Submited files         : """ + str(int(input_total) - int(difference)) + """</p>"""
        html+="""<p style="color: black;">Files in waiting pool  : """ + str(difference) + """</p>"""
        html+="""<h2 style="color: blue;">check_def.sh output! </h2>"""
	for line in check_defs_output.split("\n"):
	    if line[4:7] == '32m':
		html+="""<p style="color: green;">""" + line[7:-4] + """</p>"""
	    elif line[4:7] == '34m':
		html+="""<p style="color: dodgerblue;">""" + line[7:-4] + """</p>"""
	    elif line[4:7] == '31m':
		html+="""<p style="color: red;">""" + line[7:-4] + """</p>"""
 	    else:
		html+="""<p style="color: black;">""" + line + """</p>"""

        html+="""</body></html>"""
        #print(html)
	return text, html, 0

def get_input_def_from_xml(xml, stage):
    docs = parse(xml) 
    inputdef=''
    for xmlprojoect in docs.getElementsByTagName('project'):
        for xmlstage in xmlprojoect.getElementsByTagName('stage'):
	    if xmlstage.getAttribute("name") != stage:
		continue
            for xmlinputdef in xmlstage.getElementsByTagName("inputdef"):
		inputdef=xmlinputdef.firstChild.data
    return inputdef

def check_input_difference(xml, stage):
    print(xml)
    #print(xml_results)
    xml_results=subprocess.check_output('project.py --xml ' + xml + ' --stage ' + stage + ' --check_input', shell=True)
    difference=''
    for line in xml_results.split('\n'):
	if 'Final' in line:
            difference=line.split(' ')[2]
    return difference, xml_results
	
	
def check_input_defs(idef):
    return check_defs(idef)

def check_defs(idef):
    print(idef)
    try:
        samdef_snapshot_id=subprocess.check_output('samweb take-snapshot ' + idef, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
        exit(1)
    idef_snapshot=idef+'_check_status_production_info_email_snapshot'
    print('samweb create-definition ' + idef_snapshot + '  "snapshot_id ' + samdef_snapshot_id.split("\n")[0] +'" > /dev/null')
    os.system('samweb create-definition ' + idef_snapshot + '  "snapshot_id ' + samdef_snapshot_id.split("\n")[0] +'" > /dev/null')
    nfiles_input=subprocess.check_output('samweb count-files defname:' + idef_snapshot, shell=True)
    nfiles_input=int(nfiles_input.split("\n")[0])
    if nfiles_input == 0:
        print("0 files in " + idef)
 #       exit(1)
    nfiles_output_merging=subprocess.check_output('samweb count-files "defname:' + idef_snapshot + ' and merge.merge 1 and merge.merged 0"', shell=True).split("\n")[0]
    os.system('samweb delete-definition ' + idef_snapshot)
    return nfiles_input, nfiles_output_merging


def check_output_defs(defs):
    definitions=defs.split(',')
    nfiles_total = [ ]
    nfiles_merging = [ ]
    for idef in definitions:
	total, merging = check_defs(idef)
	nfiles_total.append(total)
	nfiles_merging.append(merging)
    return nfiles_total, nfiles_merging


def find_string_in_files(file_path, search_string):
    #print(file_path) 
    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                if search_string in line:
                    print("Found in {} on line {}: {}".format(file_path, line_number, line.strip()))
    		    return 0
    except (IOError, UnicodeDecodeError):
        # Skip files that cannot be opened or decoded
	exit(-1)




def find_string_in_path(path, search_string):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path[-3:] == 'xml' and '2024' in file_path :
	        #print(file_path) 
                try:
                    with open(file_path, 'r') as f:
                        for line_number, line in enumerate(f, start=1):
                            if search_string in line:
                                print("Found in {} on line {}: {}".format(file_path, line_number, line.strip()))
				return file_path
                except (IOError, UnicodeDecodeError):
                    # Skip files that cannot be opened or decoded
                    continue
    return ""

def setup_project(project, stage):
    print(project)
    is_project_in_email_pool = find_string_in_files("/exp/uboone/app/home/uboonepro/liangliu/email/email.sh", project)
    file_path = find_string_in_path("/exp/uboone/app/home/uboonepro/xml/", project)
    if len(file_path) == 0:
	print("Cannot find project : \033[0;31m" + project +"\033[0m")
	exit(1)
    print("Checking xml files: \033[0;32m" + file_path + "\033[0m passed")
    inputdef = get_input_def_from_xml(file_path, stage)
    if len(inputdef) == 0: 
	print("Cannot find stage : \033[0;31m" + stage +"\033[0m")
	exit(2)
    if 'makeup' in inputdef or 'Makeup' in inputdef:
	print("This is a makeups, will not be put into email pool")
	if is_project_in_email_pool == 0:
            print(project + " exsit in email pool!")
	    exit(3)
        else:
            print(project + " is not in email pool!")
	    exit(3)
    print("Checking stage : \033[0;32m" + stage + "\033[0m passed") 
    print("Checking input def :  \033[0;32m" + inputdef + "\033[0m passed") 
    command=" --xml " + file_path + " --project " + project + " --stage " + stage + " --inputdef " + inputdef 
    print(command)
    if is_project_in_email_pool == 0:
	print(project + " exsit in email pool!")
	exit(3)
    else:
	print("Put " + project + " into email pool!")
    return command

def find_and_replace_or_add_line(path, search_string, new_line):
    file_path = path
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Search for the string and track if it was found
        found = False
        with open(file_path, 'w') as f:
            for line in lines:
                if search_string in line:
                    f.write(new_line + '\n')
                    found = True
                else:
                    f.write(line)
            
            # If the string was not found, add the new line
            if not found:
                f.write(new_line + '\n')

    except (IOError, UnicodeDecodeError):
        # Skip files that cannot be opened or decodeda
	print("failed to email")
	exit(3)
        #continue

def removal_from_email_pool(project):
    file_path = "/exp/uboone/app/home/uboonepro/liangliu/email/email.sh"
    try:
	with open(file_path, 'r') as f:
	    lines = f.readlines()
	for line in lines:
	    if project in line:
	        find_and_replace_or_add_line(file_path, project, "#"+line)
    except (IOError, UnicodeDecodeError):
	exit(3)


def help():
    print("help")

# Defining main function
def main(argv):
    manager=''
    email=''
    defs=''
    xml=''
    stage=''
    project=''
    setup=0
    
    args = argv[1:]
    while len(args) > 0:
	if args[0] == '-h' or args[0] == '--help' :
	    help()
	    return 0
	elif args[0] == '--setup':
	    setup=1
	    del args[0]
	elif args[0] == '--manager':
	    manager=args[1]
 	    del args[0:2]
	elif args[0] == '--email':
	    email=args[1]
 	    del args[0:2]
	elif args[0] == '--defs':
	    defs=args[1]
 	    del args[0:2]
	elif args[0] == '--project':
	    project=args[1]
 	    del args[0:2]
	elif args[0] == '--xml':
	    xml=args[1]
 	    del args[0:2]
	elif args[0] == '--inputdef':
	    inputdef=args[1]
 	    del args[0:2]
	elif args[0] == '--stage':
	    stage=args[1]
 	    del args[0:2]
	else:
	    print('Unknown option %s' % args[0])
	    return 1

    if setup == 1:
	cmd=setup_project(project, stage)
        command='/exp/uboone/app/home/uboonepro/liangliu/email/email_me_production_status.py --manager "' + manager + '" --email ' + email + ' --defs ' + defs + cmd
	print(command) 
	find_and_replace_or_add_line("/exp/uboone/app/home/uboonepro/liangliu/email/email.sh", project, command)
	os.system(command + " > /dev/null")
	exit(0)

    text, html, status = write_the_message(manager, xml, stage, defs, inputdef)
    email_me_production_status(email, text, html, project)
    if status != 0:
	print(argv)
    elif status == 0:
	removal_from_email_pool(project)
    exit(0)

    #if int(input_merging) != 0:
    #	print(inputdef + str(input_merging))
    #else:
    #	print("success")


# Using the special variable 
# __name__
if __name__=="__main__":
    sys.exit(main(sys.argv))


