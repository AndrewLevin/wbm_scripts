#this will make a json for all of the lumis where prescale set 1 was used
#it should be run with python2.7 (at least it does not work with python2.6)
#based on /afs/cern.ch/user/d/dsperka/public/forGeorgia/compareWBMTriggerRates.py

import json
import sys
import os
import argparse

from cernSSOWebParser import parseURLTables

parser = argparse.ArgumentParser(description='compare hlt reports')

args = parser.parse_args()

f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt")

good_run_lumis=json.loads(f_json.read())

output_json = {}

for run in good_run_lumis:

    #if run != "258211":
    #    continue

    print run

    url="https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/PrescaleChanges?RUN="+str(run)

    tables=parseURLTables(url)

    assert(len(tables) == 1)

    prescale_indices = []

    for i in range(0,len(tables[0])):
    
        table = tables[0][i]

        if i == 0:
            table=tables[0][i][6:len(table)-1]

        prescale_index = int (table[2])

        lumisection = int(table[1])

        prescale_indices.append([prescale_index,lumisection])

    for j in range(0,len(prescale_indices)):
        #for prescale_index in prescale_indices:

        if prescale_indices[j][0] == 1:

            if run not in output_json:
                output_json[str(run)] = []

            if j == len(prescale_indices) - 1:
                url="https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/LumiSections?RUN="+str(run)
                tableslumi=parseURLTables(url)
                output_json[str(run)].append([prescale_indices[j][1],int(tableslumi[1][len(tableslumi[1]) - 1][0])])

            else:
                output_json[str(run)].append([prescale_indices[j][1],prescale_indices[j+1][1]-1])

output_json_dump=json.dumps(output_json)

print output_json_dump
