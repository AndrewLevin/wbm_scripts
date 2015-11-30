#checks if a level 1 trigger is prescaled, except when the prescale index is 1
#should be run with python2.7, at least it doesn't work with python2.6
#this is based on /afs/cern.ch/user/d/dsperka/public/forGeorgia/compareWBMTriggerRates.py

import json
import sys
import os
import argparse

from cernSSOWebParser import parseURLTables

parser = argparse.ArgumentParser(description='compare hlt reports')

args = parser.parse_args()

f_json=open("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt")

good_run_lumis=json.loads(f_json.read())

for run in good_run_lumis:

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

    url="https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/RunSummary?RUN=%s&DB=default" % (run)

    tables=parseURLTables(url)
    l1_hlt_mode=tables[1][1][3]

    url="https://cmswbm.web.cern.ch/cmswbm/cmsdb/servlet/TriggerMode?KEY=%s" % (l1_hlt_mode)
    tables=parseURLTables(url)

    for i in range(0,len(tables[3])):

        if 'L1_SingleEG30' not in tables[3][i]:
            continue

        for j in range(0,len(prescale_indices)):
        #for prescale_index in prescale_indices:

            if prescale_indices[j][0] == 1:
                continue

            assert(int(tables[3][i][2:len(tables[3][i])-1][prescale_indices[j][0]]) == 1)
