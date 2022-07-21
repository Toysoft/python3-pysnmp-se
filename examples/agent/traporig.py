"""Notification Originator Application"""
from pysnmp.mapping.udp.role import Manager
from pysnmp.proto.api import alpha

# Protocol version to use
ver = alpha.protoVersions[alpha.protoVersionId1]

req = ver.Message()
req.apiAlphaSetCommunity('public')
req.apiAlphaSetPdu(ver.TrapPdu())

# Traps have quite different semantics among proto versions
if req.apiAlphaGetProtoVersionId() == alpha.protoVersionId1:
    req.apiAlphaGetPdu().apiAlphaSetEnterprise('1.3.6.1.1.2.3.4.1')
    req.apiAlphaGetPdu().apiAlphaSetSpecificTrap(1)

tsp = Manager()
tsp.send(req.berEncode(), ('localhost', 1162))
