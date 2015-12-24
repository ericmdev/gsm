#!/usr/local/bin/python
# coding: utf-8

import sys
from os import path
from subprocess import call
from shutil import rmtree
import json
from re import sub
from pprint import pprint

" Terminal Colors "
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

" GSM "
class GSM(object):

    version = str('1.0.0')
    json_file = str('gitsubmodule.json')
    gitmodules_file = str('.gitmodules')
    gitconfig_file = path.join('.git', 'config')
    dependencies = dict()
    devDependencies = dict()
    cmd = str('install');
    _jsonExists = bool(False)

    " Property. "
    @property
    def jsonExists(self):
        if path.isfile(self.json_file):
            exists = True
        else:
            exists = False
        self._jsonExists = exists
        return self._jsonExists

    " Initialise. "
    def __init__(self):
        # self.message(value="git submodule manager %s" % self.version)
        pass

    " Run. "
    def run(self):
        # parse args
        if self.parseArgs() == True:
            # install
            if self.cmd == 'install':
                if self.readJson() == True:
                    self.install()
            # update
            elif self.cmd == 'update':
                self.update()
            # remove
            elif self.cmd == 'remove':
                # e.g: test/gsm_test
                plugin_path = sys.argv[2]
                self.remove(plugin_path)
        else:
            pass

    " Message "
    def message(self, value, code=None): 
        if code:
            if code == 'OK':
                color = bcolors.OKGREEN
            elif code == 'ERR':
                color = bcolors.FAIL
            print("gsm %s%s!%s %s" % (color, code, bcolors.ENDC, value))
        else:
            print(value)

    " Parse Arguments. "
    def parseArgs(self):
        # check argv length
        if len(sys.argv) < 2:
            self.message(code='ERR', value="invalid command, try -h for help")
            return False
        # if command argument
        cmd = sys.argv[1]
        if cmd:
            if cmd == '-h':
                self.message(value="- install git submodules:")
                self.message(value="  python gsm.py install")
                return False
            elif cmd in ['install', 'update', 'remove']:
                self.cmd = cmd
                return True
            else:
                self.message(code='ERR', value="unknown command `%s`" % cmd)
                return False
        else:
            self.message(code='ERR', value="no command given")
            return False

    " Read JSON. "
    def readJson(self):
        if self.jsonExists == True:
            with open(self.json_file) as data_file: 
                try:   
                    data = json.load(data_file)
                except ValueError as e:
                    self.message(code='ERR', value="no JSON object could be decoded, please check `%s`" % self.json_file)
                    return False
            self.dependencies = data["dependencies"].items()
            self.devDependencies = data["devDependencies"].items()
            # self.message(code='OK', value="%s" % self.json_file)
            return True
        else:
            self.message(code='ERR', value="could not find `%s`" % self.json_file)
            return False

    " Install (Add) Git Submodules. "
    def install(self):
        for dst, src in self.dependencies:
            self.message(value="- Installing %s" % (dst))
            self.message(value="  Source: %s" % (src))
            call(["git", "submodule", "add", "-f", src, dst])
        # check if all submodules installed
        self.message(code='OK', value='install')

    " Update Git Submodules. "
    def update(self):
        self.message(value="- Updating")
        call(["git", "submodule", "update", "--init", "--recursive"])
        self.message(code='OK', value='update')

    " Remove Git Submodule. "
    def remove(self, plugin_path):
        self.message(value="- Removing %s%s%s" % (bcolors.BOLD, plugin_path, bcolors.ENDC))
        if self.removeModuleEntry(plugin_path) == True:
            pass
        if self.removeModuleConfig(plugin_path) == True:
            pass
        if self.removeModuleCached(plugin_path) == True:
            pass
        if self.removeModuleDirectory(plugin_path) == True:
            pass

    # Remove Module Entry
    def removeModuleEntry(self, plugin_path):
        # remove the module's entry in the .gitmodules file
        data = ''
        skip = 0
        with open (self.gitmodules_file, "r") as gitmodules_file:
            for line in gitmodules_file:
                if skip == 0:
                    if line.rstrip() == "[submodule \"%s\"]" % plugin_path:
                        # skip next 2 lines (path, url)
                        skip = 2
                    else:
                        data += "".join(line)
                else:
                    skip = skip -1
        # update file
        try:
            f = open(self.gitmodules_file, "w")
            f.write(data)
            f.close()
            self.message(code='OK', value='removed from %s' % (self.gitmodules_file))
            return True
        except IOError as e:
            self.message(code='ERR', value="I/O error: %s" % e)
            return False

    # Remove Module Config
    def removeModuleConfig(self, plugin_path):
        # remove the module's entry in the .git/config file
        data = ''
        skip = 0
        with open (self.gitconfig_file, "r") as gitconfig_file:
            for line in gitconfig_file:
                if skip == 0:
                    if line.rstrip() == "[submodule \"%s\"]" % plugin_path:
                        # skip next line (url)
                        skip = 1
                    else:
                        data += "".join(line)
                else:
                    skip = skip -1
        # update file
        try:
            f = open(self.gitconfig_file, "w")
            f.write(data)
            f.close()
            self.message(code='OK', value='removed from %s' % (self.gitconfig_file))
            return True
        except IOError as e:
            self.message(code='ERR', value="I/O error: %s" % e)
            return False

    # Remove Module Cached
    def removeModuleCached(self, plugin_path):
        call(["git", "rm", "--cached", plugin_path])
        self.message(code='OK', value='removed from cached')
        return True

    # Remove Module Directory
    def removeModuleDirectory(self, plugin_path):
        if path.exists(plugin_path):
            rmtree(plugin_path)
            self.message(code='OK', value='removed directory %s' % plugin_path)
            return True
        else:
            return False

" Main "
def main():
    gsm = GSM()
    gsm.run()
    sys.exit()

" Enter Main "
if __name__ == '__main__':
    main()