#! /usr/bin/env python
# Python program to demonstrate
# main() function
import sys, os
import fileinput
import subprocess

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
    #exit(1)
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
