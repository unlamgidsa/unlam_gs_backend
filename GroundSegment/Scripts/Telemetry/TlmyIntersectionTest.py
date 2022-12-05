import cProfile
import json
import os

def fromTxtToDict(tlmyVars):
    return json.loads(tlmyVars)


def intersectionBetweenSets615(tlmys, exTlmysSet, exTlmys):
    for i in range(615):
        res = intersectionBetweenSet(tlmys, exTlmysSet, exTlmys)
    
    return res

def regularIntersections615(tlmys, exTlmys):
    pktlist = [] #list of dictionaries
    for i in range(615):
        for tlm in tlmys:
            res = list(filter(lambda x:x["fullName"] == tlm, exTlmys))
    return res

    

    return pktlist

def intersectionBetweenSet(tlmys, exTlmysSet, exTlmys):
    #tlmys es un set
    intersection_ids = tlmys & exTlmysSet
    #Todo muy lindo pero ahora hay que juntar las variables por clave

    return [x for x in exTlmys if x["fullName"] in intersection_ids]

def regularIntersection(tlmys, exTlmys):
    pktlist = [] #list of dictionaries
    for tlm in tlmys:
        res = list(filter(lambda x:x["fullName"] == tlm, exTlmys))
        if(len(res)>0):
            pktlist.append(res[0])

    return pktlist

def main():
    tlmys = ['RTEmuSat.SinValue1631', 'RTEmuSat.SinValue4111', 'RTEmuSat.SinValue7375', 'RTEmuSat.SinValue7434', 
    'RTEmuSat.SinValue214', 'RTEmuSat.SinValue7120', 'RTEmuSat.SinValue3152', 'RTEmuSat.SinValue5377', 
    'RTEmuSat.SinValue1233', 'RTEmuSat.SinValue4021', 'RTEmuSat.SinValue6675', 'RTEmuSat.SinValue6204', 
    'RTEmuSat.SinValue3230', 'RTEmuSat.SinValue5235', 'RTEmuSat.SinValue4814', 'RTEmuSat.SinValue5661', 
    'RTEmuSat.SinValue5834', 'RTEmuSat.SinValue4047', 'RTEmuSat.SinValue3940', 'RTEmuSat.SinValue4169', 
    'RTEmuSat.SinValue2237', 'RTEmuSat.SinValue3153', 'RTEmuSat.SinValue5984', 'RTEmuSat.SinValue6496', 
    'RTEmuSat.SinValue1461', 'RTEmuSat.SinValue7477', 'RTEmuSat.SinValue632', 'RTEmuSat.SinValue7452', 
    'RTEmuSat.SinValue1996', 'RTEmuSat.SinValue708']


    mfile = os.path.join(os.path.dirname(__file__), 'SerializedTelemetry.txt')
    f = open(mfile,'rt')
    tlmyVars = f.read()
    f.close()
    exTlmys =fromTxtToDict(tlmyVars)
    pktlist = regularIntersections615(tlmys, exTlmys)


    tlmys = set(tlmys)
    exTlmysSet = set(x["fullName"] for x in exTlmys)
    pktlist = intersectionBetweenSets615(tlmys, exTlmysSet, exTlmys)
    print(pktlist)




if __name__ == "__main__":
    cProfile.run('main()')
    #main()

"""
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.003    0.003    0.698    0.698 <string>:1(<module>)
        1    0.002    0.002    0.002    0.002 TlmyIntersectionTest.py:13(<listcomp>)
        1    0.426    0.426    0.585    0.585 TlmyIntersectionTest.py:15(regularIntersection)
   225000    0.159    0.000    0.159    0.000 TlmyIntersectionTest.py:18(<lambda>)
        1    0.048    0.048    0.695    0.695 TlmyIntersectionTest.py:24(main)
     7501    0.027    0.000    0.027    0.000 TlmyIntersectionTest.py:43(<genexpr>)
        1    0.000    0.000    0.029    0.029 TlmyIntersectionTest.py:5(fromTxtToDict)
        1    0.000    0.000    0.002    0.002 TlmyIntersectionTest.py:8(intersectionBetweenSet)
"""
    

