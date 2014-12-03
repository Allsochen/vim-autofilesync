#!/usr/bin/env python
# encoding: utf-8

# author: erxiao.chen.gd@gmail.com
# date 2014-11-25 15:31:25
# version: 1.0

"""Contains the AutoFileSyncManager facade used by all Vim Functions.
"""
import os
import re
import string
import os.path
import sys
import vim
import time
import json
import shutil

def showMsg(msg):
    """Silent to display a message.
    """
    vim.command("echo ''")
    vim.command("set nomore noshowmode")
    vim.command("silent! redraw")
    vim.command("echomsg \"%s\"" % msg)

class Configuration(object):
    def __init__(self):
        self.dest = None
        self.excludesSuffix = [".svn"]
        self.excludesPaths = [".autofilesync"]
        self.patterns = []
        for excursion in self.excludesPaths:
            self.patterns.append(re.compile(excursion))

    def isExceptPath(self, path):
        # Attemps to match full string.
        for excursion in self.excludesPaths:
            if path.find(excursion) >= 0:
                return True
        # Attemps to match pattern.
        for pattern in self.patterns:
            if pattern.match(path) != None:
                return True
        return False

class AutoFileSyncManager:

    def __init__(self, options):
        self.configFileName = options.get("configFileName", "autofilesync.json")
        self.findConfigFileDepth = int(options.get("findConfigFileDepth", "5"))
        self.projectSearchPaths = options.get("projectSearchPaths", [])
        self.syncCacheDir = options.get("syncCacheDir", ".autofilesync")

    def getFullConfig(self, configPath):
        """Returns a full path of the configuration which contains the file name.
        """
        return os.path.join(configPath, self.configFileName)

    def isProjectSearchPath(self, source):
        # No confige the project search home paths yet.
        if len(self.projectSearchPaths) == 0:
            return True
        for path in self.projectSearchPaths:
            if source.find(path) >= 0:
                return True
        return False

    def isNeedToSync(self, configPath, suffixFilePath, source):
        cachePath = os.path.join(configPath, self.syncCacheDir)
        if not os.path.exists(cachePath):
            os.makedirs(cachePath)
        # build the cache path: ${PROJECT_ROOT}/${syncCacheDir}/path/.sync.filename
        cacheSrcFile = cachePath + suffixFilePath
        (fpath, fname) = os.path.split(cacheSrcFile)
        cacheFile = os.path.join(fpath, ".%s.sync" % fname)
        if not os.path.exists(cacheFile):
            cacheDirname = os.path.dirname(cacheFile)
            if not os.path.exists(cacheDirname):
                os.makedirs(cacheDirname)
            open(cacheFile, 'a').close()
            os.utime(cacheFile, None)
            return True
        if os.path.getmtime(cacheFile) <= os.path.getatime(source):
            os.utime(cacheFile, None)
            return True
        else:
            return False


    def syncFile(self):
        # Gain the current open file.
        source = vim.eval("expand(\"%:p\")")
        if not self.isProjectSearchPath(source):
            return
        configPath = self.findConfigPath(source)
        if configPath == None:
            #print ("No autofilesync.json configuration for project.")
            return
        else:
            configuration = self.parseConfig(configPath)
            if configuration and configuration.dest != None:
                # Create the target path.
                if not os.path.exists(configuration.dest):
                   os.makedirs(configuration.dest)
                #print ("source: %s, configPath: %s, dest: %s" % (source, configPath, configuration.dest))
                #${PROJECT_ROOT}/aaa/bbb/a.txt
                destFilePath = source.replace(configPath, configuration.dest).replace("\\\\", "\\")
                (fpath, fname) = os.path.split(destFilePath)
                #print ("path: %s, name: %s" % (fpath, fname))
                #print ("copy file path: %s" % destFilePath)
                if not os.path.exists(fpath):
                    os.makedirs(fpath)
                # is need to copy
                # modify time
                shutil.copy(source, destFilePath)
                showMsg("sync succ: %s" % destFilePath.replace("\\", "/"))

    def syncUpdateFiles(self):
        # Gain the open file.
        source = vim.eval("expand(\"%:p\")")
        if not self.isProjectSearchPath(source):
            return
        configPath = self.findConfigPath(source)
        if configPath == None:
            #print ("No autofilesync.json configuration for project.")
            return
        else:
            configuration = self.parseConfig(configPath)
            dest = configuration.dest

            if dest != None:
                # Create the target path.
                if not os.path.exists(dest):
                   os.makedirs(dest)
                # Recursively copy an entire directory.
                for root, subdirs, files in os.walk(configPath):  
                    target = root.replace(configPath, dest)
                    for filepath in files:
                        (base, extension) = os.path.splitext(source)
                        if extension in configuration.excludesSuffix:
                            continue
                        if configuration.isExceptPath(base):
                            continue
                        shutil.copy(os.path.join(root, filepath), target)
                    for subdir in subdirs:
                        targetSubdir = os.path.join(target, subdir)
                        if not os.path.exists(targetSubdir):
                            os.makedirs(targetSubdir)
                showMsg("sync all succ: %s" % dest.replace("\\", "/"))

    def syncAllFiles(self):
        # Gain the open file.
        source = vim.eval("expand(\"%:p\")")
        if not self.isProjectSearchPath(source):
            return
        configPath = self.findConfigPath(source)
        if configPath == None:
            #print ("No autofilesync.json configuration for project.")
            return
        else:
            configuration = self.parseConfig(configPath)
            dest = configuration.dest

            if dest != None:
                # Try three times.
                try:
                    # Remove all files and create the target path later.
                    if os.path.exists(dest):
                        shutil.rmtree(dest)
                    os.makedirs(dest)
                except:
                    # execute again.
                    # Remove all files and create the target path later.
                    try:
                        if os.path.exists(dest):
                            shutil.rmtree(dest)
                        os.makedirs(dest)
                    except:
                        if os.path.exists(dest):
                            shutil.rmtree(dest)
                        os.makedirs(dest)

                # Recursively copy an entire directory.
                for root, subdirs, files in os.walk(configPath):  
                    target = root.replace(configPath, dest)
                    for filepath in files:
                        (base, extension) = os.path.splitext(source)
                        if extension in configuration.excludesSuffix:
                            continue
                        if configuration.isExceptPath(base):
                            continue
                        shutil.copy(os.path.join(root, filepath), target)
                    for subdir in subdirs:
                        targetSubdir = os.path.join(target, subdir)
                        if not os.path.exists(targetSubdir):
                            os.makedirs(targetSubdir)
                showMsg("sync all succ: %s" % dest.replace("\\", "/"))

    def findConfigPath(self, source):
        """Returns the project configuration file like `/data/home/allsochen/projects/autofilesync.json` if exists.
        """
        (fpath, fname) = os.path.split(source)
        #print ("fpath: %s, fname: %s" % (fpath, fname))
        path = None
        for i in range(self.findConfigFileDepth):
            configFile = os.path.join(fpath, self.configFileName)
            if os.path.exists(configFile):
                path = fpath
                break
            fpath = os.path.abspath(os.path.join(os.path.dirname(fpath),"."))
        #print ("config file path: %s" % path)
        return path

    """Parse the project configuration file.
    The 
    {
        "target": "Y:\\home\\allsochen\\projects\\MTT\\TestServer",
        "excludesSuffix": [".svn"]
        "excludesPaths": [".svn"]
    }
    """
    def parseConfig(self, configPath):
        try:
            config = open(self.getFullConfig(configPath), newline='', encoding='utf-8').read()
            #print ("content: %s" % config)
            data = json.loads(config)
            configuration = Configuration()
            configuration.dest = self.getJson(data, "dest", "")
            configuration.excludesSuffix = self.getJson(data, "excludesSuffix", [".svn"])
            configuration.excludesPaths = self.getJson(data, "excludesPaths", [])
            return configuration
        except:
            showMsg("load autofilesync configuration error.")
            return Configuration()

    def getJson(self, json, key, dft):
        try:
            return json[key]
        except:
            return dft



