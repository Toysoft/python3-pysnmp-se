"""Command Generator Application (GET)"""
from pysnmp.mapping.udp.role import Manager
from pysnmp.proto.api import alpha

# Protocol version to use
ver = alpha.protoVersions[alpha.protoVersionId1]

# Build message
req = ver.Message()
req.apiAlphaSetCommunity('public')

# Build PDU
req.apiAlphaSetPdu(ver.GetRequestPdu())
req.apiAlphaGetPdu().apiAlphaSetVarBindList(('1.3.6.1.2.1.1.1.0', ver.Null()),
                                            ('1.3.6.1.2.1.1.2.0', ver.Null()))

def cbFun(wholeMsg, transportAddr, req):
    rsp = ver.Message()
    rsp.berDecode(wholeMsg)

    # Make sure this is a response to this request
    if req.apiAlphaMatch(rsp):
        errorStatus = rsp.apiAlphaGetPdu().apiAlphaGetErrorStatus()
        if errorStatus:
            print 'Error: ', errorStatus
        else:
            for varBind in rsp.apiAlphaGetPdu().apiAlphaGetVarBindList():
                print varBind.apiAlphaGetOidVal()
        return 1

tsp = Manager()
tsp.sendAndReceive(req.berEncode(), ('localhost', 1161), (cbFun, req))
