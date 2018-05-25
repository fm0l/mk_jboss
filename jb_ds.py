#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Name: jb_ds.py
## Version: 0.1
## Author:  Federico Mollura

### Script For Check_MK JBoss/Wildfly DataSource Monitoring

### Imports

import os
import json
import sys
import re

### Please configure here the Datasources you need to Monitor

datasources = ["ExampleDS", "MySQL"]

### JBoss CLI Connection

connectCLI = '/opt/wf01/wildfly/bin/jboss-cli.sh --connect --controller=192.168.x.x:xyz'

## Check if kubectl is working after setting the environment
checkCLI = connectCLI + ' -c version &>/dev/null; if [ $? -eq 0 ]; then echo "0"; else echo "1"; fi'
checkConn = int(os.popen(checkCLI).read())

### Main

results = {}
lenghtDs = len(datasources)

if checkConn != 0:
	for i in range(0,lenghtDs):
		dsValue = datasources[i]
		print str('3'), str("JBoss_DataSource_") + str(dsValue), str("-"), str('CANT CONNECT TO JBOSS CLI!')
	sys.exit(1)
	
### Now i ask JBoss CLI about DS Connection

for i in range(0,lenghtDs):
	dsValue = datasources[i]
	toValue = '/subsystem=datasources/data-source=' + dsValue + ':test-connection-in-pool'	
	connectToValue = connectCLI + ' ' + '-c' ' ' + toValue 
	outPut = os.popen(connectToValue).read()
	if re.findall('success', outPut):
		results[dsValue] = 'True'
	else:
		results[dsValue] = 'False'

### Read Values and format output

for i in range(0,lenghtDs):
	dsValue = datasources[i]
	boolOut = results.get(dsValue)
	if boolOut == 'True':
		print str('0'), str("JBoss_DataSource_") + str(dsValue), str("-"), str('DS is OK!')
	elif boolOut == 'False':
		print str('2'), str("JBoss_DataSource_") + str(dsValue), str("-"), str('DS is not OK!')
	else:
		print str('3'), str("JBoss_DataSource_") + str(dsValue), str("-"), str('DS is not OK!')

