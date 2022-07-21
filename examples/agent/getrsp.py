"""Command Responder Application (GET PDU)"""
from pysnmp.mapping.udp.role import Agent
from pysnmp.proto.api import alpha

def cbFun(tsp, metaReq, (octetStream, srcAddr)):
    metaReq.decode(octetStream)
    req = metaReq.apiAlphaGetCurrentValue()

    # Build response from request object
    rsp = req.apiAlphaReply()

    reportStr = '%s (version ID %s) from %s: ' % \
                (req.apiAlphaGetPdu().apiAlphaGetPduType(), \
                 req.apiAlphaGetProtoVersionId(), srcAddr)
    
    # Support only a single PDU type (but any proto version)
    if req.apiAlphaGetPdu().apiAlphaGetPduType() == alpha.getRequestPduType:
        # Produce response var-binds
        varBinds = []
        for oid, val in req.apiAlphaGetPdu().apiAlphaGetVarBinds():
            version = val.apiAlphaGetProtoVersionId()
            val = alpha.vers[version].OctetString('%s %s = %s' % \
                                                  (reportStr, oid, val))
            varBinds.append((oid, val))
        apply(rsp.apiAlphaGetPdu().apiAlphaSetVarBinds, varBinds)
    else:
        # Report unsupported request type
        rsp.apiAlphaGetPdu().apiAlphaSetErrorStatus(5)
        print reportStr + 'unsupported request type'
    
    # Return response object & manager's address
    return (rsp.berEncode(), srcAddr)

metaReq = alpha.MetaMessage()

tsp = Agent((cbFun, metaReq), [('localhost', 1161)])
tsp.receiveAndSend()
