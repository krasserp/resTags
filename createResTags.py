#!/usr/bin/python2.7
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import sys
from sys import argv
import os


class MyHTMLParser(HTMLParser):
    
    #current path
    currentPath = os.getcwd()

    #file to manipulate
    originFileName = ''
    #currentFile name without the extension
    currentFileName = ''

    #resource Prefixer the same as the file name
    resPreFix = currentFileName
    allDataToReplace = {}
    counter = 0
    attr = None

    def setTheNames(self,string):
        self.originFileName = string
        self.currentFileName = self.originFileName.split('.')[0]
        self.resPreFix = self.currentFileName

    # write to the destination files
    def saveToFiles(self,resTag,appendHTMLTag):
        currentFileName = self.currentFileName
        #create append to the resTags file for the parsed html file
        # only if there is something to write
        if resTag != False:
            f = open(self.currentPath+'/AllResTags.xml','a') #currentFileName+'.xml','a')
            f.write(resTag+'\n')
            f.close()

        # create append to the destination html file including the res tags
        f = open(self.currentPath+'/'+currentFileName+'_resed.html','a')
        f.write(appendHTMLTag+'\n')
        f.close()


    def handle_starttag(self, tag, attrs):
        allAttr = ''
        for attr in attrs:
            allAttr +=' '+attr[0]+'="'+attr[1]+'" '
            #print "     attr:", attr
        #print allAttr
        self.saveToFiles(False,'<'+tag+' '+allAttr+'>')


    def handle_endtag(self, tag):
        self.saveToFiles(False,'</'+tag+'>')



    def handle_data(self, data):
        #print "Data     :", data
        checkKey = data.strip()
        keyExists = self.allDataToReplace.get(checkKey)
        #only if there is something
        if checkKey != '':
            # if we have the string alrady 
            if keyExists != None:
                
                # print 'found key' , keyExists, ' at position ', self.counter
                # key exists so we can use it no need for a new res tag 
                # setting the string to append ot the new html file
                appendHTMLTag = '${res.'+keyExists+'}'
                # call the save to function to append to the files
                self.saveToFiles(False,appendHTMLTag)
    
            ## if the string has not been found so far
            if keyExists == None:
                self.counter +=1
                # if the key does not exist add it to the dictionary 
                self.allDataToReplace[checkKey] = self.resPreFix+'_'+str(self.counter)
                #create the res tag to add to the res tag file
                resTag = '<res label="%s">%s</res>'% (self.resPreFix+'_'+str(self.counter), checkKey)
                # setting the string to append ot the new html file
                appendHTMLTag = '${res.'+self.resPreFix+'_'+str(self.counter)+'}'
                # call the save to function to append to the files
                self.saveToFiles(resTag,appendHTMLTag)
            #print self.allDataToReplace
    
    def returnAllText(self):
        return self.allDataToReplace



def parseAndAppend(fileName):
    # working dir
    currentPath = os.getcwd()

    pathAndFileName = currentPath + '/' + fileName

    parser = MyHTMLParser()
    #set the names
    parser.setTheNames(fileName)
    # get the actual html of the file
    contents = open(pathAndFileName).read()
    #feed the parser
    parser.feed(contents)


def printHelp():
    print """This script will convert all text within html tags (within an htm(l) file) to resTags. 
Pass in your html filenames as arguments ie. htmlToRes filename1.html filename2.html etc... 
For each file passed as an argument a new version containing the resTags will be created. 
The new file names are the orignal filename +_resed.html. 
All resTags are saved in a new file named AllResTags.xml. 
Then the resTags can be added to your survey.xml.
Your refrenced html files in the html tags in the survey.xml can be replaced by the newly created yourfileName_resed.html"""
    sys.exit()



#pseudo help,...
if len(argv) > 1:
    if argv[1] == '-h':
        printHelp()


##which files to convert? already run exit

fileList = []
# Fetch the arguments and make sure they are all either html or html
for x, i in enumerate(argv):
    if x > 0 :
        fileNameExtension = argv[x].split('.')
        # simple check if the file was already converted to a res?
        if os.path.exists(fileNameExtension[0]+'_resed.html'):
            print ('This file has already been converted to use res tags please check your survey folder for ', fileNameExtension[0]+'_resed.html' )
            sys.exit()

        if 'htm' in fileNameExtension[len(fileNameExtension)-1].lower():
            fileList.append(argv[x])
        else:
            print('Only html files are allowed! You passed this file', argv[x])    
            sys.exit() 

##SAVES IN APPEND MODE SO ONLY RUN ONCE!!!!!!!!!
#creates and saves all res tags to this file AllResTags.xml    
for item in fileList:
    parseAndAppend(item)

if len(fileList) > 0 :
    print 'Finished running the restag creation.  Find your resTags in this file: AllResTags.xml.  Add the resTags to your survey.xml and change all your html file references to the newly created yourFileName_resed.html file name'
else:
    printHelp()   
