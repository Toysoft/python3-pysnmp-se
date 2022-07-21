"""Command Generator Application (GETNEXT)"""
from pysnmp.mapping.udp.role import Manager
from pysnmp.proto.api import alpha

# Protocol version to use
ver = alpha.protoVersions[alpha.protoVersionId1]

# SNMP table header
headVars = [ ver.ObjectName('1.3.6') ]

# Create request & response message objects
req = ver.Message(); rsp = ver.Message()
req.apiAlphaSetCommunity('public')

# Create PDU, load var-binds, attach PDU to SNMP message
req.apiAlphaSetPdu(ver.GetNextRequestPdu())
apply(req.apiAlphaGetPdu().apiAlphaSetVarBindList,
      map(lambda x, ver=ver: (x.get(), ver.Null()), headVars))

def cbFun(wholeMsg, transportAddr, (req, rsp, headVars)):
    rsp.berDecode(wholeMsg)
    if req.apiAlphaMatch(rsp):
        # Check for SNMP errors reported
        errorStatus = rsp.apiAlphaGetPdu().apiAlphaGetErrorStatus()
        if errorStatus and errorStatus != 2:
            raise errorStatus
       
        # Build SNMP table from response
        tableIndices = apply(req.apiAlphaGetPdu().apiAlphaGetTableIndices,
                             [rsp.apiAlphaGetPdu()] + headVars)

        # Report SNMP table
        varBindList = rsp.apiAlphaGetPdu().apiAlphaGetVarBindList()
        for rowIndices in tableIndices:
            for cellIdx in filter(lambda x: x!=-1, rowIndices):
                print transportAddr, varBindList[cellIdx].apiAlphaGetOidVal()

        # Remove completed SNMP table columns
        map(lambda idx, headVars=headVars: headVars.__delitem__(idx), \
            filter(lambda x: x==-1, tableIndices[-1]))
        if len(headVars) == 0: raise "EOM"

        # Generate request for next row
        lastRow = map(lambda cellIdx, varBindList=varBindList: \
                      varBindList[cellIdx].apiAlphaGetOidVal(), \
                      filter(lambda x: x!=-1, tableIndices[-1]))
        apply(req.apiAlphaGetPdu().apiAlphaSetVarBindList, \
              map(lambda (x, y): (x.get(), None), lastRow))
        
        req.apiAlphaGetPdu().apiAlphaGetRequestId().inc(1)
        return 1

tspDsp = Manager()
try:
    while 1:
        tspDsp.sendAndReceive(req.berEncode(), ('localhost', 1161), \
                              (cbFun, (req, rsp, headVars)))
except "EOM":
    pass
