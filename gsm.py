import sys
from os import path
from subprocess import call
import json
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
        self.message(value="git submodule manager %s" % self.version)

    " Run. "
    def run(self):
        # parse args
        if self.parseArgs() == True:
            # install
            if self.cmd == 'install':
                if self.readJson() == True:
                    self.addSubmodules()
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
        if len(sys.argv) != 2:
            self.message(code='ERR', value="invalid command, try -h for help")
            return False
        # if command argument
        cmd = sys.argv[1]
        if cmd:
            if cmd == '-h':
                self.message(value="- install git submodules:")
                self.message(value="  python gsm.py install")
                return False
            elif cmd == 'install':
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
            self.message(code='OK', value="%s" % self.json_file)
            return True
        else:
            self.message(code='ERR', value="could not find `%s`" % self.json_file)
            return False

    " Add Git Submodules. "
    def addSubmodules(self):
        for dst, src in self.dependencies:
            self.message(value="- Installing %s" % (dst))
            self.message(value="  Source: %s" % (src))
            call(["git", "submodule", "add", "-f", src, dst])
        # check if all submodules installed
        # self.message(code='OK', value='add git submodules')

" Main "
def main():
    gsm = GSM()
    gsm.run()
    sys.exit()

" Enter Main "
if __name__ == '__main__':
    main()