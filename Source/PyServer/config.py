# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import argparse,sys,os
parser = argparse.ArgumentParser()
parser.add_argument("--entry_point", help="sets the module where main_loop function exists")
args = parser.parse_args()

file_str="""#Autogenerated file (by config.py) dont edit!
import track_test
main_module=track_test
main_loop=track_test.main_loop
kill=track_test.kill
def reload():
  import imp
  imp.reload(track_test)
  if hasattr(track_test,'reload'):
    track_test.reload()
  print('entrypoint reloaded')
"""

if args.entry_point is not None:
    fd=open("Private/entry_point.py","w")
    fd.write(file_str.replace('track_test',args.entry_point))
    fd.close()

