"""
   Invoke base API methods, catch possible exceptions and translate them
   into legacy PySNMP 1.x counterparts.

   Copyright 1999-2002 by Ilya Etingof <ilya@glas.net>. See LICENSE for
   details.
"""
import pysnmp.proto.error, pysnmp.asn1.error, pysnmp.asn1.encoding.ber.error
from pysnmp.compat.pysnmp1x import error

class Base:
    """Base compatibility class
    """
    def _wrapper(self, fun, *args):
        """Call passed function and translate possible exceptions
        """
        try:
            return apply(fun, args)

        # Catch transport exceptions

        except pysnmp.mapping.udp.error.BadArgumentError as why:
            raise error.BadArgument(why)

        except pysnmp.mapping.udp.error.NoResponseErroras as why:
            raise error.NoResponse(why)

        except pysnmp.mapping.udp.error.NetworkErroras as why:
            raise error.TransportError(why)
        
        # Catch protocol package exceptions

        except pysnmp.proto.error.BadArgumentError as  why:
            raise error.BadArgument(why)
        
        except pysnmp.proto.error.ProtoError as why:
            raise error.SNMPEngineError(why)        

        # Catch ber package exceptions
        
        except pysnmp.asn1.encoding.ber.error.BadArgumentError as why:
            raise error.BEREngineError(why)

        except pysnmp.asn1.encoding.ber.error.TypeMismatchError as why:
            raise error.UnknownTag(why)

        except pysnmp.asn1.encoding.ber.error.OverFlowError as why:
            raise error.OverFlow(why)

        except pysnmp.asn1.encoding.ber.error.UnderRunError as why:
            raise error.BadEncoding(why)

        except pysnmp.asn1.encoding.ber.error.BadEncodingError as why:
            raise error.BadEncoding(why)

        except pysnmp.asn1.encoding.ber.error.BerEncodingError as why:
            raise error.BEREngineError(why)

        # Catch asn1 package exceptions
        
        except pysnmp.asn1.error.BadArgumentError as why:
            raise error.BadArgument(why)

        except pysnmp.asn1.error.ValueConstraintError as why:
            raise error.TypeMismatch(why)

        except pysnmp.asn1.error.Asn1Error as why:
            raise error.PySNMPError(why)
