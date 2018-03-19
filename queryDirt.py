#!/usr/bin/python

import requests as rq
import json
import sys

################################################################################
################################################################################
def meanVal(list):
    count = 0
    _sum = 0
    for i in list:
        count += 1
        _sum  += i[1]

    return _sum/count

def printingfunction(sndmean, sltmean, clymean, other, dominanttex):
    print '\t ***********************************'
    print '\t PARTICLE-SIZE DISTRIBUTION: '
    print '\t \t SAND PERCENTAGE: ', sndmean
    print '\t \t SILT PERCENTAGE: ', sltmean
    print '\t \t CLAY PERCENTAGE: ', clymean
    print '\t \t OTHER PERCENTAGE: ', other
    print '\n'

    print '\t DOMINANT SOIL TEXTURES: '
    for element in dominanttex:
        if element[1] > 0:
            print '\t \t', element[0], '|', element[1]


#################################################################################
#################################################################################
payload = {'lat' : str(sys.argv[1]), 'lon' : str(sys.argv[2])}

r = rq.get('http://rest.soilgrids.org/query', params = payload)

data = r.json()
datastring = json.dumps(data, indent=4, sort_keys=True)

parsed = json.loads(datastring)

sndlst = sorted(parsed["properties"]["SNDPPT"]["M"].iteritems())
sltlst = sorted(parsed["properties"]["SLTPPT"]["M"].iteritems())
clylst = sorted(parsed["properties"]["CLYPPT"]["M"].iteritems())

sndmean = meanVal(sndlst)
sltmean = meanVal(sltlst)
clymean = meanVal(clylst)
other   = 100 - (sndmean + sltmean + clymean)

soiltextures = parsed["properties"]["TAXNWRB"].iteritems()
dominanttex = reversed(sorted(soiltextures, key=lambda soil: soil[1]))

printingfunction(sndmean, sltmean, clymean, other, dominanttex)
