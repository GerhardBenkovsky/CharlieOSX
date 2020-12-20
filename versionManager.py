import time, _thread, os
import urequests

class VersionManagment:
    '''
    
    '''
    def __init__ (self, settings, brick, config, logger):
        logger.info(self, 'Initialisating VersionManagment')
        self.__settings = settings
        self.__brick = brick
        self.__config = config
        self.logger = logger
        self.newAvai = False # As a fallback
        try:
            f = open("VERSION", "r")
            lns = f.readlines()
            f.close()
            ln = lns[0]
            ln = ln.replace("\n", "").replace("\r", "").replace(" ", "")
            self.version = VersionObject()
            self.version.parseFromString(ln)
            self.logger.info(self, 'Using version ' + str(self.version))
        except:
            self.logger.warn(self, "Error reading version!")
        
        ## Check if there is a new version
        self.checkForUpdates()
        
        

    def checkForUpdates(self, force=False):
        if(self.__config["checkForUpdates"] or force):
            repoPath = "http://raw.githubusercontent.com/TheGreyDiamond/CharlieOSX/versioningNew/VERSION" ### !!!!! CHANGE IN MERGE TO MAIN REPO !!!!!
            try:
                self.logger.info(self, 'Checking if a new version is avaiable')
                response = urequests.get(repoPath)
                remoteVersion = response.text
                remoteVersion = remoteVersion.replace("\n", "").replace("\r", "").replace(" ", "")
                remoteVersionObj = VersionObject()
                remoteVersionObj.parseFromString(remoteVersion)
                newAvai = not(self.version.isNewer(remoteVersionObj))
                self.newAvai = newAvai
                if(newAvai):
                    self.logger.info("A new version if ready to be downloaded, current version: " + str(self.version) + " remote version: " + str(remoteVersionObj))
            except:
                self.logger.warn(self, "Unable to check for updates")
        else:
            self.logger.info(self, 'Skipping update check')
        return self.newAvai
    
    def getUpdateStatus(self):
        ''' 
        Returns True if there is a newer version ready
        '''
        return self.newAvai
    
    def __repr__(self):
        return 'TODO'

    def __str__(self):
        return 'VersionManager'

class VersionObject():
    def __init__(self, major=0, minor=0, fix=0):
        self.major = major
        self.minor = minor
        self.fix = fix
    
    def __str__(self):
        return(self.major + "." + self.minor + "." + self.fix)
    
    def parseFromString(self, string):
        parts = string.split(".")
        try:
            self.major = int(parts[0])
            self.minor = int(parts[1])
            self.fix = int(parts[2])
        except ValueError:
            return(False)
        else:
            return(True)

    
    def getMajor(self):
        return(self.major)

    def getMinor(self):
        return(self.minor)

    def getFix(self):
        return(self.fix)

    def isNewer(self, remoteVersion):
        '''
        Returns True if the the local version is newer then `remoteVersion`
        '''
        isNewerB = False
        # Starting with Major
        if(self.major >= remoteVersion.getMajor()):
            isNewerB = True
        
        # Then Minor
        if(self.minor >= remoteVersion.getMinor()):
            isNewerB = True
        
        if(self.fix >= remoteVersion.getFix()):
            isNewerB = True
        
        return(isNewerB)