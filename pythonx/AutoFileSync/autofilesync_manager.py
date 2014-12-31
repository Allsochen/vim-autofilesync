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
import threading
import traceback

mutex = threading.Lock()

def mkdirs(dirs, times=5):
    for i in range(times):
        try:
            if not os.path.exists(dirs):
               os.makedirs(dirs)
               break
        except:
            time.sleep(1)

def rmtree(dirs, times=5):
    for i in range(times):
        try:
            if os.path.exists(dirs):
                #os.removedirs(dirs)
                shutil.rmtree(dirs)
                break
        except:
            time.slee(1)

def showMsg(msg):
    """Silent to display a message.
    """
    #vim.command("echo ''")
    #vim.command("set nomore noshowmode")
    vim.command("echomsg \"%s\"" % msg)
    vim.command("silent! redraw")

class Configuration(object):
    def __init__(self):
        self.dest = None
        self.excludesSuffix = [".svn"]
        self.excludesPaths = [".autofilesync"]
        self.patterns = []

    def _setExcludesPaths(self, excludesPaths):
        self.excludesPaths = excludesPaths
        for excursion in excludesPaths:
            self.patterns.append(re.compile(excursion))

    def isExceptPath(self, path):
        # Attemps to match full string.
        for excludepath in self.excludesPaths:
            #print ("%s ==> %s" % (excludepath, path))
            if path.find(excludepath) >= 0:
                return True
        # Attemps to match pattern.
        for pattern in self.patterns:
            if pattern.match(path) != None:
                return True
        return False

class AutoFileSyncManager(object):

    def __init__(self, options):
        self.options = options

    def isEnable(self):
        if vim.eval('g:autofilesync_enable') == "true":
            return True
        return False

    def syncFile(self):
        """Use thread to avoid the editor can't work.
        """
        if self.isEnable():
            AutoFileSyncSingleFileThread(self.options).start()

    def syncUpdateFiles(self):
        """Use thread to avoid the editor can't work.
        """
        if self.isEnable():
            AutoFileSyncUpdateFileThread(self.options).start()

    def syncAllFiles(self):
        """Use thread to avoid the editor can't work.
        """
        if self.isEnable():
            AutoFileSyncFilesThread(self.options).start()

class AutoFileSyncSingleFileThread(threading.Thread):

    def __init__(self, options):
        threading.Thread.__init__(self)
        self.afs = AutoFileSync(options)

    def run(self):
        try:
            mutex.acquire()
            self.afs.syncFile()
        except Exception as e:
            print (traceback.format_exc())
        finally:
            mutex.release()

class AutoFileSyncUpdateFileThread(threading.Thread):

    def __init__(self, options):
        threading.Thread.__init__(self)
        self.afs = AutoFileSync(options)

    def run(self):
        try:
            mutex.acquire()
            self.afs.syncUpdateFiles()
        except Exception as e:
            print (traceback.format_exc())
        finally:
            mutex.release()

class AutoFileSyncFilesThread(threading.Thread):

    def __init__(self, options):
        threading.Thread.__init__(self)
        self.afs = AutoFileSync(options)

    def run(self):
        try:
            mutex.acquire()
            self.afs.syncAllFiles()
        except Exception as e:
            print (traceback.format_exc())
        finally:
            mutex.release()

class AutoFileSync:

    def __init__(self, options):
        self.configFileName = options.get("configFileName", "autofilesync.json")
        self.findConfigFileDepth = int(options.get("findConfigFileDepth", "5"))
        self.projectSearchPaths = options.get("projectSearchPaths", [])

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
                mkdirs(configuration.dest)
                #print ("source: %s, configPath: %s, dest: %s" % (source, configPath, configuration.dest))
                #${PROJECT_ROOT}/aaa/bbb/a.txt
                destFilePath = source.replace(configPath, configuration.dest).replace("\\\\", "\\")
                (fpath, fname) = os.path.split(destFilePath)
                #print ("path: %s, name: %s" % (fpath, fname))
                #print ("copy file path: %s" % destFilePath)
                mkdirs(fpath)
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
                try:
                    mkdirs(dest)
                    showMsg("sync update start: %s" % dest.replace("\\", "/"))
                    # Recursively copy an entire directory.
                    for root, subdirs, files in os.walk(configPath):  
                        target = root.replace(configPath, dest)
                        for filepath in files:
                            (base, extension) = os.path.splitext(source)
                            if extension in configuration.excludesSuffix:
                                continue
                            if configuration.isExceptPath(root):
                                continue
                            srcFile = os.path.join(root, filepath)
                            destFile = srcFile.replace(configPath, dest)
                            if os.path.exists(destFile):
                                if os.path.getmtime(srcFile) <= os.path.getmtime(destFile):
                                    continue
                            #print ("sync: %s" % destFile)
                            shutil.copy(srcFile, target)
                        for subdir in subdirs:
                            targetSubdir = os.path.join(target, subdir)
                            if configuration.isExceptPath(targetSubdir):
                                continue
                            mkdirs(targetSubdir)
                    showMsg("sync update succ: %s" % dest.replace("\\", "/"))
                except Exception as e:
                    print (traceback.format_exc())

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
                try:
                    rmtree(dest)
                    mkdirs(dest)
                    showMsg("sync all start: %s" % dest.replace("\\", "/"))
                    # Recursively copy an entire directory.
                    i = 1
                    for root, subdirs, files in os.walk(configPath):  
                        target = root.replace(configPath, dest)
                        for filepath in files:
                            (base, extension) = os.path.splitext(source)
                            if extension in configuration.excludesSuffix:
                                continue
                            if configuration.isExceptPath(root):
                                continue
                            srcFile = os.path.join(root, filepath)
                            destFile = srcFile.replace(configPath, dest)
                            #if os.path.getmtime(srcFile) <= os.path.getmtime(destFile):
                            #    continue
                            #print ("sync: %s" % destFile)
                            shutil.copy(os.path.join(root, filepath), target)
                        for subdir in subdirs:
                            targetSubdir = os.path.join(target, subdir)
                            if configuration.isExceptPath(targetSubdir):
                                continue
                            #print ("mkdir: %s" % targetSubdir)
                            mkdirs(targetSubdir)
                    showMsg("sync all succ: %s" % dest.replace("\\", "/"))
                except Exception as e:
                    #showMsg("sync all fail: %s" % dest.replace("\\", "/"))
                    #print ("sync all fail.%s" % e.msg)
                    print (traceback.format_exc())

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
        config = open(self.getFullConfig(configPath), newline='', encoding='utf-8').read()
        #print ("content: %s" % config)
        data = json.loads(config)
        configuration = Configuration()
        configuration.dest = self.getJson(data, "dest", "")
        configuration.excludesSuffix = self.getJson(data, "excludesSuffix", [".svn"])
        configuration._setExcludesPaths(self.getJson(data, "excludesPaths", []))
        return configuration

    def getJson(self, json, key, dft):
        try:
            return json[key]
        except:
            return dft



