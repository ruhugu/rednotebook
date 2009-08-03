# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Copyright (c) 2009  Jendrik Seipp
# 
# RedNotebook is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# RedNotebook is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with RedNotebook; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------

from __future__ import with_statement, division

import sys
import signal
import random
import operator
import os
from urllib2 import urlopen, URLError
import webbrowser
import unicode
import logging

import filesystem


def getHtmlDocFromWordCountDict(wordCountDict, type, ignore_list):
	sortedDict = sorted(wordCountDict.items(), key=lambda (word, freq): freq)
	
	if type == 'word':
		# filter short words
		sortedDict = filter(lambda (word, freq): len(word) > 4, sortedDict)
		
	# filter words in ignore_list
	sortedDict = filter(lambda (word, freq): word.lower() not in ignore_list, sortedDict)
	
	oftenUsedWords = []
	numberOfWords = 42
	
	'''
	only take the longest words. If there are less words than n, 
	len(longWords) words are returned
	'''
	tagCloudWords = sortedDict[-numberOfWords:]
	if len(tagCloudWords) < 1:
		return [], ''
	
	minCount = tagCloudWords[0][1]
	maxCount = tagCloudWords[-1][1]
	
	deltaCount = maxCount - minCount
	if deltaCount == 0:
		deltaCount = 1
	
	minFontSize = 10
	maxFontSize = 50
	
	fontDelta = maxFontSize - minFontSize
	
	'delete count information from word list'
	tagCloudWords = map(lambda (word, count): word, tagCloudWords)
	
	'search words with unicode sort function'
	tagCloudWords.sort(key=unicode.coll)
	
	htmlElements = []
	
	htmlHead = 	'<body><div style="text-align:center; font-family: sans-serif">'
	htmlTail = '</div></body>'
	
	for wordIndex in range(len(tagCloudWords)):
		count = wordCountDict.get(tagCloudWords[wordIndex])
		fontFactor = (count - minCount) / deltaCount
		fontSize = int(minFontSize + fontFactor * fontDelta)
		
		htmlElements.append('<a href="search/' + str(wordIndex) + '">' + \
								'<span style="font-size:' + str(int(fontSize)) + 'px">' + \
									tagCloudWords[wordIndex] + \
								'</span>' + \
							'</a>' + \
							#Add some whitespace &#xA0;
							#'<span style="font-size:5px; color:white"> _ </span>' + \
							'<span> </span>' + \
							'\n')
		
	#random.shuffle(htmlElements)	
	
	htmlDoc = htmlHead
	htmlDoc += reduce(operator.add, htmlElements, '')
	htmlDoc += htmlTail
	
	return (tagCloudWords, htmlDoc)


def set_environment_variables(config):
	variables = {}
	
	for variable, value in variables.iteritems():
		if not os.environ.has_key(variable): #and config.has_key(variable):
			# Only add environment variable if it does not exist yet
			os.environ[variable] = config.read(variable, default=value)
			logging.info('%s set to %s' % (variable, value))
			
	for variable in variables.keys():
		if os.environ.has_key(variable):
			logging.info('The environment variable %s has value %s' % (variable, os.environ.get(variable)))
		else:
			logging.info('There is no environment variable called %s' % variable)
	
			
def redirect_output_to_file():
	'''
	Changes stdout and stderr to a file or None if the file could not be opened.
	
	This is necessary to suppress the error messages on Windows when closing 
	the application.
	'''
	try:
		assert sys.platform == 'win32'
	except AssertionError:
		return
	
	#logfile_path = os.path.join(filesystem.appDir, 'rednotebook.log')
	logfile_path = filesystem.logFile
	
	try:
		logfile = open(logfile_path, 'w')
	except IOError:
		logging.info('logfile could not be found, disabling logging')
		logfile = None
	
	sys.stdout = logfile
	sys.stderr = logfile


def setup_signal_handlers(redNotebook):
	'''
	Catch abnormal exits of the program and save content to disk
	Look in signal man page for signal names
	
	SIGKILL cannot be caught
	SIGINT is caught again by KeyboardInterrupt
	'''
	
	signals = []
	
	try:
		signals.append(signal.SIGHUP)  #Terminal closed, Parent process dead
	except AttributeError: 
		pass
	try:
		signals.append(signal.SIGINT)  #Interrupt from keyboard (CTRL-C)
	except AttributeError: 
		pass
	try:
		signals.append(signal.SIGQUIT) #Quit from keyboard
	except AttributeError: 
		pass
	try:
		signals.append(signal.SIGABRT) #Abort signal from abort(3)
	except AttributeError: 
		pass
	try:
		signals.append(signal.SIGTERM) #Termination signal
	except AttributeError: 
		pass
	try:
		signals.append(signal.SIGTSTP) #Stop typed at tty
	except AttributeError: 
		pass
	
	
	def signal_handler(signum, frame):
		logging.info('Program was abnormally aborted with signal %s' % signum)
		redNotebook.saveToDisk()
		sys.exit()

	
	msg = 'Connected Signals: '
	
	for signalNumber in signals:
		try:
			msg += str(signalNumber) + ' '
			signal.signal(signalNumber, signal_handler)
		except RuntimeError:
			msg += '\nFalse Signal Number: ' + signalNumber
	
	logging.info(msg)
				

def get_new_version_number(currentVersion):
	newVersion = None
	
	try:
		projectXML = urlopen('http://www.gnomefiles.org/app.php/RedNotebook').read()
		tag = 'version '
		position = projectXML.upper().find(tag.upper())
		newVersion = projectXML[position + len(tag):position + len(tag) + 5]
		logging.info('%s is newest version. You have version %s' % (newVersion, currentVersion))
	except URLError:
		logging.error('New version info could not be read')
	
	if newVersion:
		if newVersion > currentVersion:
			return newVersion
	
	return None


def check_new_version(mainFrame, currentVersion, startup=False):
	if get_new_version_number(currentVersion):
		mainFrame.show_new_version_dialog()
	elif not startup:
		mainFrame.show_no_new_version_dialog()
		
		
def write_file(content, filename):
	filename = os.path.join(filesystem.tempDir, filename)
	with open(filename, 'w') as file:
		file.write(content)
		

def show_html_in_browser(html, filename='tmp.html'):
	write_file(html, filename)
	filename = os.path.join(filesystem.tempDir, filename)
	
	html_file = os.path.abspath(filename)
	html_file = 'file://' + html_file
	webbrowser.open(html_file)
	
class StreamDuplicator(object):
	def __init__(self, default, duplicates):
		if not type(duplicates) == list:
			duplicates = [duplicates]
		self.duplicates = duplicates
		self.default = default
		
	@property
	def streams(self):
		return [self.default] + self.duplicates
	
	def write(self, str):
		#print 'write', self.default, self.duplicates, self.streams
		for stream in self.streams:
			#print stream
			stream.write(str)
		
	def flush(self):
		for stream in self.streams:
			stream.flush()
			
	#def close(self):
	#	for stream in self.streams():
	#		self.stream.close()
	
	
