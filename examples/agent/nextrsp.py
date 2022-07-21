"""Command Responder Application (GETNEXT PDU)"""
from pysnmp.mapping.udp.role import Agent
from pysnmp.proto.api import alpha

mibInstVer = alpha.protoVersions[alpha.protoVersionId1]
mibInstr = [ (mibInstVer.ObjectName('1.3.6.1'), 'Integer', 26011971),
             (mibInstVer.ObjectName('1.3.6.2'), 'OctetString', __doc__) ]

def cbFun(tsp, metaReq, (wholeMsg, transportAddr)):
    metaReq.berDecode(wholeMsg)
    req = metaReq.apiAlphaGetCurrentComponent()

    # Build response from request object
    rsp = req.apiAlphaReply()

    # Support only a single PDU type (but any proto version)
    if req.apiAlphaGetPdu().apiAlphaGetPduType() == \
           alpha.getNextRequestPduType:
        # Produce response var-binds
        varBinds = []; errorIndex = -1
        for oid, val in map(lambda x: x.apiAlphaGetOidVal(),
                            req.apiAlphaGetPdu().apiAlphaGetVarBindList()):
            mibIdx = -1; errorIndex = errorIndex + 1
            # Search next OID to report
            for idx in range(len(mibInstr)):
                if idx == 0:
                    if oid < mibInstr[idx][0]:
                        mibIdx = idx
                        break
                else:
                    if oid >= mibInstr[idx-1][0] and oid < mibInstr[idx][0]:
                        mibIdx = idx
                        break
            else:
                # Out of MIB
                rsp.apiAlphaGetPdu().apiAlphaSetEndOfMibIndices(errorIndex)

            # Report value if OID is found
            if mibIdx != -1:
                mibOid, mibVar, mibVal = mibInstr[mibIdx]                
                ver = alpha.protoVersions[rsp.apiAlphaGetProtoVersionId()]
                if hasattr(ver, mibVar):
                    varBinds.append((ver.ObjectName(mibOid), \
                                     getattr(ver, mibVar)(mibVal)))
                    continue
                else:
                    # Variable not available over this proto version
                    rsp.apiAlphaGetPdu().apiAlphaSetErrorIndex(errorIndex)
                    rsp.apiAlphaGetPdu().apiAlphaSetErrorStatus(5)

            varBinds.append((oid, val))

        apply(rsp.apiAlphaGetPdu().apiAlphaSetVarBindList, varBinds)
    else:
        # Report unsupported request type
        rsp.apiAlphaGetPdu().apiAlphaSetErrorStatus(5)
        print '%s (version ID %s) from %s: unsupported request type' % \
              (req.apiAlphaGetPdu().apiAlphaGetPduType(), \
               req.apiAlphaGetProtoVersionId(), transportAddr)
    
    # Return response object & manager's address
    return (rsp.berEncode(), transportAddr)

metaReq = alpha.MetaMessage()

tsp = Agent((cbFun, metaReq), [('localhost', 1161)])
tsp.receiveAndSend()
