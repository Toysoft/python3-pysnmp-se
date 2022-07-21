#!/usr/bin/env python
from distutils.core import setup

if __name__ == "__main__":
	from sys import hexversion
	if hexversion >= 0x2030000:
		# work around distutils complaints under Python 2.2.x
		extraArguments = {
			'classifiers': [
				"""License :: OSI Approved :: BSD License""",
				"""Programming Language :: Python""",
				"""Topic :: Software Development :: Libraries :: Python Modules""",
				"""Intended Audience :: Developers""",
			],
			'download_url': "https://sourceforge.net/project/showfiles.php?group_id=102250",
			'keywords': 'snmp,pysnmp,speed,twistedsnmp',
			'long_description' : """Patched PySNMP 3.4.x with speed enhancements

This is the PySNMP 3.4.x branch of code with various speed 
enhancements, the most important being the replacement of 
string-based OIDs with tuple-based OIDs.  This makes PySNMP-SE
slightly incompatible with PySNMP, hence the 3.5.x numbering
scheme.
""",
			'platforms': ['Any'],
		}
	else:
		extraArguments = {
		}

	setup(
		name="pysnmp-se",
		version="3.5.2",
		description="Python SNMP Toolkit (Speed Enhanced)",
		maintainer="Mike Fletcher",
		author_email="mcfletch@vextech.ca",
		url="http://twistedsnmp.sourceforge.net/",
		packages = [
			'pysnmp',
			'pysnmp.asn1',
			'pysnmp.asn1.encoding',
			'pysnmp.asn1.encoding.ber',
			'pysnmp.proto',
			'pysnmp.proto.api',
			'pysnmp.proto.api.alpha',
			'pysnmp.proto.api.generic',
			'pysnmp.test',
			'pysnmp.mapping',
			'pysnmp.mapping.udp',
			'pysnmp.compat',
			'pysnmp.compat.pysnmp1x',
			'pysnmp.compat.pysnmp2x',
			'pysnmp.compat.snmpy',
		],
		license="BSD",
		options = {
			'sdist':{'force_manifest':1,'formats':['gztar','zip'],},
		},
		**extraArguments
	)
