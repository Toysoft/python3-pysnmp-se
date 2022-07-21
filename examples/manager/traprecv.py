"""Notification Receiver Application (TRAP PDU)"""
from pysnmp.mapping.udp.role import Agent
from pysnmp.proto.api import alpha

def cbFun(tsp, metaReq, (wholeMsg, transportAddr)):
    metaReq.decode(wholeMsg)
    req = metaReq.apiAlphaGetCurrentComponent()

    reportStr = '%s (version ID %s) from %s:\n' % \
                (req.apiAlphaGetPdu().apiAlphaGetPduType(), \
                 req.apiAlphaGetProtoVersionId(), transportAddr)
    
    if req.apiAlphaGetPdu().apiAlphaGetPduType() == alpha.trapPduType:
        pdu = req.apiAlphaGetPdu()
        if req.apiAlphaGetProtoVersionId() == alpha.protoVersionId1:
            print reportStr + \
                  'Enterprise: %s\n' % pdu.apiAlphaGetEnterprise() + \
                  'Agent Address: %s\n' % pdu.apiAlphaGetAgentAddr() + \
                  'Generic Trap: %s\n' % pdu.apiAlphaGetGenericTrap() + \
                  'Specific Trap: %s\n' % pdu.apiAlphaGetSpecificTrap() + \
                  'Uptime: %s\n' % pdu.apiAlphaGetTimeStamp() + \
                  'Var-binds:'
        for varBind in pdu.apiAlphaGetVarBindList():
            print varBind.apiAlphaGetOidVal()
    else:
        print reportStr + 'unsupported request type'

    return ('', transportAddr)

metaReq = alpha.MetaMessage()

tsp = Agent((cbFun, metaReq), [('localhost', 1162)])
tsp.receiveAndSend()
