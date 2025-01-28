#! /usr/bin/env python
# Python program to demonstrate
# main() function
import sys, os
import fileinput
import subprocess
import ROOT

import samweb_cli
samweb = None           # Initialized SAMWebClient object

import project_utilities

def import_samweb():

    # Get intialized samweb, if not already done.

    global samweb
    global extractor_dict
    global expMetaData


    if samweb == None:
        samweb = project_utilities.samweb()
        from extractor_dict import expMetaData




def check_input_difference(xml, stage):
    print(xml)
    #print(xml_results)
    xml_results=subprocess.check_output('project.py --xml ' + xml + ' --stage ' + stage + ' --check_input', shell=True).decode("utf-8")
    print(xml_results.split("\n"))
    difference=""
    for line in xml_results.split("\n"):
        if "Final" in line:
            difference=line.split(" ")[2]
    print(difference)
    print(xml_results)
    return difference, xml_results


def check_input_defs(idef):
    return check_defs(idef)

def check_defs(idef):
    import_samweb()
    try:
        samdef_snapshot_id=samweb.takeSnapshot(defname=idef)
    except subprocess.CalledProcessError as e:
        print(e)
        exit(1)
    idef_snapshot=idef+'_check_status_production_info_email_snapshot'
    dims_snapshot="snapshot_id {}".format(samdef_snapshot_id)
    samweb.createDefinition(defname=idef_snapshot, dims=dims_snapshot)
    nfiles_input=samweb.countFiles(defname=idef_snapshot)
    print("{} files in {}".format(nfiles_input, idef_snapshot))
    nfiles_output_merging=samweb.countFiles(dimensions="defname: {} and merge.merge 1 and merge.merged 0".format(idef_snapshot))
    samweb.deleteDefinition(defname=idef_snapshot)
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
