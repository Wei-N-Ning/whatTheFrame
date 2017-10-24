
import os
import sys
import zipimport

imp = zipimport.zipimporter(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build', 'wtf.pz')))
assert imp.find_module('whatTheFrame')
whatTheFrame = imp.load_module('whatTheFrame')
assert whatTheFrame.VarDeepInspect

sys.stdout.write('packageTests: DONE\n')
