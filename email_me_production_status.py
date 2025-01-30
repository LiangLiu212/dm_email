#! /usr/bin/env python
# Python program to demonstrate
# main() function
import sys, os
sys.path.append("/exp/uboone/app/home/uboonepro/liangliu/email")
import fileinput
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import subprocess 
from xml.dom.minidom import parse
from dm_email_utils import check_definition
from dm_email_utils import check_xml


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



def write_message_running(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging):
    text=""
    html="""<html><head></head><body>"""
    # Running status

    text+="Hi " + manager + "\n"
    text+="Campaign Running! \n"
    text+="Your job is " + str(completeness) + "% complete!  \n"
    text+="Total input files      : " + str(input_total) + " in input definition " + inputdef + "\n"
    text+="Submited files         : " + str(int(input_total) - int(difference)) + "\n"
    text+="Files in waiting pool  : " + str(difference) + "\n"

    # make a table to summary 
    text+="Output definition " + "\n"
    text+="files in definition " + "\n"
    text+="files in merging pool " + "\n"
    
    for i in range(len(output_total)):
        text+=defs.split(",")[i] + "\n"
        text+=str(output_total[i]) + "\n"
        text+=str(output_merging[i]) + "\n"

    text+="Files in output definition : " + "\n"
    for i in range(len(output_total)):
        text+="    " + str(output_total[i]) + " files in " + defs.split(",")[i] + "\n"
        text+="    " + str(output_merging[i]) + " files in merging pool." + "\n"
    text+=check_input_results
    #print(text)
    
    html+="""<p style="color: black;">Hi """ + manager + """ </p>"""
    html+="""<h2 style="color: green;">Campaign Running! </h2>"""
    html+="""<p style="color: black;">Your job is """ + str(completeness) + """% complete! </p>"""

    html+="""<table><tr><th>Input definition</th><td>""" +inputdef+ """</td></tr>"""
    html+="""<tr><th>Files in definition</th><td>""" +str(int(input_total))+ """</td></tr>"""
    html+="""<tr><th>Submitted files</th><td>""" + str(int(input_total) - int(difference)) +"""</td></tr>"""
    html+="""<tr><th>Waiting files</th><td>""" + str(difference) +"""</td></tr></table>"""
    html+="""<table><thead><tr><th>Output definition</th><th>Files in definition</th><th>Files in merging pool</th></thead><tbody>"""
    for i in range(len(output_total)):
        html+="""<tr>"""
        html+="""<td>"""+defs.split(",")[i]+"""</td>"""
        html+="""<td>"""+str(output_total[i])+"""</td>"""
        html+="""<td>"""+str(output_merging[i])+"""</td>"""
        html+="""</tr>"""
    html+="""</tbody></table>"""

    html+="""<p><a href="https://docs.google.com/spreadsheets/d/12Kd2GsfRDqKliq6KT2xAyzqiYpNyYWqpV3gih4Ee01s/edit?gid=972888436#gid=972888436">DM Campaign Spreadsheet</a></p>"""
    html+="""<p><a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a></p>"""

    html+="""<p style="color: black;">Files in output definition : """ + """</p>"""
    for i in range(len(output_total)):
        html+="""<p style="color: black;">    """ + str(output_total[i]) + """ files in """ + defs.split(",")[i] + """</p>"""
        html+="""<p style="color: limegreen;">    """ + str(output_merging[i]) + """ files in merging pool.""" + """</p>"""
    for line in check_input_results.split("\n"):
        html+="""<p style="color: black;">""" + line + """"</p>"""
    html+="""</body></html>"""
    #print(html)
    return text, html, 2


def write_message_merging(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging):
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
    html+="""<p style="color: red;">Please go to the page of your campaign in <a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a> to stop the submission. (Please ignore if you have stopped the submission)</p>"""


    html+="""<table><tr><th>Input definition</th><td>""" +inputdef+ """</td></tr>"""
    html+="""<tr><th>Files in definition</th><td>""" +str(int(input_total))+ """</td></tr>"""
    html+="""<tr><th>Submitted files</th><td>""" + str(int(input_total) - int(difference)) +"""</td></tr>"""
    html+="""<tr><th>Waiting files</th><td>""" + str(difference) +"""</td></tr></table>"""
    html+="""<table><thead><tr><th>Output definition</th><th>Files in definition</th><th>Files in merging pool</th></thead><tbody>"""
    for i in range(len(output_total)):
        html+="""<tr>"""
        html+="""<td>"""+defs.split(",")[i]+"""</td>"""
        html+="""<td>"""+str(output_total[i])+"""</td>"""
        html+="""<td>"""+str(output_merging[i])+"""</td>"""
        html+="""</tr>"""
    html+="""</tbody></table>"""
    html+="""<p><a href="https://docs.google.com/spreadsheets/d/12Kd2GsfRDqKliq6KT2xAyzqiYpNyYWqpV3gih4Ee01s/edit?gid=972888436#gid=972888436">DM Campaign Spreadsheet</a></p>"""
    html+="""<p><a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a></p>"""



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
    

def write_message_complete(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging):
    try:
        check_defs_output = subprocess.check_output('/exp/uboone/app/users/uboonepro/check_defs_script/check_defs.sh -i ' + inputdef + ' -o ' + defs, shell=True)
    except subprocess.CalledProcessError as e:
        exit(1)
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

    output_files = []
    output_events = []
    parents_files = []
    parents_events = []
    for line in check_defs_output.split("\n"):
        if 'Input:' in line:
            input_files = line.split()[1]
            input_events = line.split()[2]
        elif 'Output:' in line:
            output_files.append(line.split()[1])
            output_events.append(line.split()[2])
        elif 'Parents:' in line:
            parents_files.append(line.split()[1])
            parents_events.append(line.split()[2])

    html+="""<p style="color: black;">Hi """ + manager + """ </p>"""
    html+="""<h2 style="color: red;">Complete! </h2>"""
    html+="""<p style="color: black;">Your job is """ + str(completeness) + """% complete! </p>"""
    html+="""<p style="color: red;">Please post output definition to the <a href="https://docs.google.com/spreadsheets/d/12Kd2GsfRDqKliq6KT2xAyzqiYpNyYWqpV3gih4Ee01s/edit?gid=972888436#gid=972888436">DM Campaign Spreadsheet</a>!</p>"""

    html+="""<table><tr><th>Input definition</th><td>""" +inputdef+ """</td></tr>"""
    html+="""<tr><th>Files in definition</th><td>""" +str(int(input_total))+ """</td></tr>"""
    html+="""<tr><th>Events in definition</th><td>""" + str(input_events) +"""</td></tr></table>"""
    html+="""<tr><th>Submitted files</th><td>""" + str(int(input_total) - int(difference)) +"""</td></tr>"""
    html+="""<table><thead><tr><th>Output definition</th><th>Output files</th><th>Output events</th></thead><tbody>"""
    for i in range(len(output_total)):
        html+="""<tr>"""
        html+="""<td>"""+defs.split(",")[i]+"""</td>"""
        html+="""<td>"""+str(output_files[i])+"""</td>"""
        html+="""<td>"""+str(output_events[i])+"""</td>"""
        html+="""</tr>"""
    html+="""</tbody></table>"""

    html+="""<p><a href="https://docs.google.com/spreadsheets/d/12Kd2GsfRDqKliq6KT2xAyzqiYpNyYWqpV3gih4Ee01s/edit?gid=972888436#gid=972888436">DM Campaign Spreadsheet</a></p>"""
    html+="""<p><a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a></p>"""


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



def write_message_makeups(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging):
    text=""
    html="<html><head></head><body>"
    # Running status

    text+="Hi " + manager + "\n"
    text+="Campaign Makeups Running! \n"
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
    html+="""<h2 style="color: mediumpurple;">Campaign Makeups Running! </h2>"""
    html+="""<p style="color: black;">Your job is """ + str(completeness) + """% complete! </p>"""
    html+="""<p style="color: red;">Please go to the page of your campaign in <a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a> to stop the submission. (Please ignore if you have stopped the submission)</p>"""

    html+="""<table><tr><th>Input definition</th><td>""" +inputdef+ """</td></tr>"""
    html+="""<tr><th>Files in definition</th><td>""" +str(int(input_total))+ """</td></tr>"""
    html+="""<tr><th>Submitted files</th><td>""" + str(int(input_total) - int(difference)) +"""</td></tr>"""
    html+="""<tr><th>Waiting files</th><td>""" + str(difference) +"""</td></tr></table>"""
    html+="""<table><thead><tr><th>Output definition</th><th>Files in definition</th><th>Files in merging pool</th></thead><tbody>"""
    for i in range(len(output_total)):
        html+="""<tr>"""
        html+="""<td>"""+defs.split(",")[i]+"""</td>"""
        html+="""<td>"""+str(output_total[i])+"""</td>"""
        html+="""<td>"""+str(output_merging[i])+"""</td>"""
        html+="""</tr>"""
    html+="""</tbody></table>"""
    html+="""<p><a href="https://docs.google.com/spreadsheets/d/12Kd2GsfRDqKliq6KT2xAyzqiYpNyYWqpV3gih4Ee01s/edit?gid=972888436#gid=972888436">DM Campaign Spreadsheet</a></p>"""
    html+="""<p><a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a></p>"""


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
    


def write_message_makeups_reminder(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging):
    text=""
    html="<html><head></head><body>"
    # Running status

    text+="Hi " + manager + "\n"
    text+="Campaign Makeups Needed! \n"
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
    html+="""<h2 style="color: mediumvioletred;">Campaign Makeups Needed! </h2>"""
    html+="""<p style="color: black;">Your job is """ + str(completeness) + """% complete! </p>"""
    html+="""<p style="color: red;">Please go to the page of your campaign in <a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a> to stop the submission. (Please ignore if you have stopped the submission)</p>"""

    html+="""<table><tr><th>Input definition</th><td>""" +inputdef+ """</td></tr>"""
    html+="""<tr><th>Files in definition</th><td>""" +str(int(input_total))+ """</td></tr>"""
    html+="""<tr><th>Submitted files</th><td>""" + str(int(input_total) - int(difference)) +"""</td></tr>"""
    html+="""<tr><th>Waiting files</th><td>""" + str(difference) +"""</td></tr></table>"""
    html+="""<table><thead><tr><th>Output definition</th><th>Files in definition</th><th>Files in merging pool</th></thead><tbody>"""
    for i in range(len(output_total)):
        html+="""<tr>"""
        html+="""<td>"""+defs.split(",")[i]+"""</td>"""
        html+="""<td>"""+str(output_total[i])+"""</td>"""
        html+="""<td>"""+str(output_merging[i])+"""</td>"""
        html+="""</tr>"""
    html+="""</tbody></table>"""
    html+="""<p><a href="https://docs.google.com/spreadsheets/d/12Kd2GsfRDqKliq6KT2xAyzqiYpNyYWqpV3gih4Ee01s/edit?gid=972888436#gid=972888436">DM Campaign Spreadsheet</a></p>"""
    html+="""<p><a href="https://pomsgpvm02.fnal.gov/poms/index/uboone/production">POMS</a></p>"""

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
    



def write_the_message(manager, xml, project, stage, defs, inputdef, campaign_status):
#    inputdef=get_input_def_from_xml(xml, stage)
    input_total, input_merging = check_definition.check_input_defs(inputdef)
    output_total, output_merging = check_definition.check_output_defs(defs)
    difference, check_input_results = check_definition.check_input_difference(xml, stage)
    completeness = int(100*(float(input_total) - float(difference))/float(input_total))

    sum_output_merging = 0
    for imerging in output_merging:
        sum_output_merging+=int(imerging)


    if campaign_status == 'running':   # compaign is running; the difference is not 0. set it to merging stage once the difference is 0
        if int(difference) != 0 :
            text, html, message_code=write_message_running(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging)
            return text, html, message_code
        else:
            change_campaign_status(project, stage, campaign_status, "merging")
            exit(0)

    elif campaign_status == 'merging':
        print("merging")
        if sum_output_merging != 0:
            text, html, message_code=write_message_merging(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging)
            return text, html, message_code
        else:
            print('/exp/uboone/app/users/uboonepro/check_defs_script/check_defs.sh -i ' + inputdef + ' -o ' + defs)
            try:
                check_defs_output = subprocess.check_output('/exp/uboone/app/users/uboonepro/check_defs_script/check_defs.sh -i ' + inputdef + ' -o ' + defs, shell=True)
            except subprocess.CalledProcessError as e:
                exit(1)
            output_files = []
            output_events = []
            parents_files = []
            parents_events = []
            for line in check_defs_output.split("\n"):
                if 'Input:' in line:
                    input_files = line.split()[1]
                    input_events = line.split()[2]
                    print(input_files)
                    print(input_events)
                elif 'Output:' in line:
                    output_files.append(line.split()[1])
                    output_events.append(line.split()[2])
                    print(output_files)
                    print(output_events)
                elif 'Parents:' in line:
                    parents_files.append(line.split()[1])
                    parents_events.append(line.split()[2])
                    print(parents_files)
                    print(parents_events)
            
            campaign_complete = False
            for i in range(len(output_files)):
                if float(output_files[i])/float(input_files) > 0.945 or float(output_events[i])/float(input_events) > 0.945:
                    campaign_complete = True
                
            if campaign_complete:
                change_campaign_status(project, stage, campaign_status, "complete")
                exit(0)
            else:
                change_campaign_status(project, stage, campaign_status, "makeups") # info manager to submit makeups; makeups need to adjust the resource of computing
                exit(0)


    elif campaign_status == 'makeups':
        # check the input defs, to reminder the manager to start the makeups
        # if the manager start the makeups, then, check the merging pool
        print("merging")
        makeup_inputdef = check_xml.get_input_def_from_xml(xml, stage)
        if makeup_inputdef == inputdef:
            text, html, message_code=write_message_makeups_reminder(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging)
            return text, html, message_code
        else:
            if sum_output_merging != 0:
                text, html, message_code=write_message_makeups(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging)
                return text, html, message_code
            else:
                print('/exp/uboone/app/users/uboonepro/check_defs_script/check_defs.sh -i ' + inputdef + ' -o ' + defs)
                try:
                    check_defs_output = subprocess.check_output('/exp/uboone/app/users/uboonepro/check_defs_script/check_defs.sh -i ' + inputdef + ' -o ' + defs, shell=True)
                except subprocess.CalledProcessError as e:
                    exit(1)
                output_files = []
                output_events = []
                parents_files = []
                parents_events = []
                for line in check_defs_output.split("\n"):
                    if 'Input:' in line:
                        input_files = line.split()[1]
                        input_events = line.split()[2]
                    elif 'Output:' in line:
                        output_files.append(line.split()[1])
                        output_events.append(line.split()[2])
                    elif 'Parents:' in line:
                        parents_files.append(line.split()[1])
                        parents_events.append(line.split()[2])
                print(input_files)
                print(input_events)
                print(output_files)
                print(output_events)
                print(parents_files)
                print(parents_events)

                campaign_complete = False
                for i in range(len(output_files)):
                    if float(output_files[i])/float(input_files) > 0.945 or float(output_events[i])/float(input_events) > 0.945:
                        campaign_complete = True
    
                if campaign_complete:
                    change_campaign_status(project, stage, campaign_status, "complete")
                    exit(0)
                else:
                    #change_campaign_status(project, campaign_status, "makeups") # info manager to submit makeups; makeups need to adjust the resource of computing   
                    text, html, message_code=write_message_makeups_reminder(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging)
                    return text, html, message_code

    elif campaign_status == 'complete':
        text, html, message_code=write_message_complete(manager, defs, inputdef, input_total, input_merging, output_total, output_merging, difference, check_input_results, completeness, sum_output_merging)
        return text, html, message_code


def setup_project(project, stage):
    print(project)
    is_project_in_email_pool = check_xml.find_string_in_files("/exp/uboone/app/home/uboonepro/liangliu/email/email.sh", project, stage)
    file_path = check_xml.find_string_in_path("/exp/uboone/app/home/uboonepro/xml/", project)
    if len(file_path) == 0:
        print("Cannot find project : \033[0;31m" + project +"\033[0m")
        exit(1)
    print("Checking xml files: \033[0;32m" + file_path + "\033[0m passed")
    inputdef = check_xml.get_input_def_from_xml(file_path, stage)
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
    command=" --xml " + file_path + " --project " + project + " --stage " + stage + " --inputdef " + inputdef + " --status running"
    print(command)
    if is_project_in_email_pool == 0:
        print(project + " exsit in email pool!")
        exit(3)
    else:
        print("Put " + project + " into email pool!")
    return command


def removal_from_email_pool(project, stage):
    file_path = "/exp/uboone/app/home/uboonepro/liangliu/email/email.sh"
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if project in line and stage in line:
                check_xml.find_and_replace_or_add_line(file_path, project, stage, "#"+line)
    except (IOError, UnicodeDecodeError):
        exit(3)


def change_campaign_status(project, stage, old_status, new_status):
    file_path = "/exp/uboone/app/home/uboonepro/liangliu/email/email.sh"
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if project in line and stage in line:
                new_cmd = line.replace(old_status, new_status)
                check_xml.find_and_replace_or_add_line(file_path, project, stage, new_cmd)
                os.system(new_cmd + "> /dev/null")
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
    campaign_status=''
    
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
        elif args[0] == '--status':
            campaign_status=args[1]
            del args[0:2]
        else:
            print('Unknown option %s' % args[0])
            return 1

    if setup == 1:
        cmd=setup_project(project, stage)
        command='/exp/uboone/app/home/uboonepro/liangliu/email/email_me_production_status.py --manager "' + manager + '" --email ' + email + ' --defs ' + defs + cmd
        print(command) 
        check_xml.find_and_replace_or_add_line("/exp/uboone/app/home/uboonepro/liangliu/email/email.sh", project, stage, command)
        os.system(command + " > /dev/null")
        exit(0)

    text, html, status = write_the_message(manager, xml, project, stage, defs, inputdef, campaign_status)
    email_me_production_status(email, text, html, project)
    if status != 0:
        print(argv)
    elif status == 0:
        removal_from_email_pool(project, stage)
    exit(0)


# Using the special variable 
# __name__
if __name__=="__main__":
    sys.exit(main(sys.argv))


