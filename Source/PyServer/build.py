# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import argparse,sys,os
parser = argparse.ArgumentParser()
parser.add_argument("--ue4path", help="path to unreal engine base directory")
args = parser.parse_args()
ue4path=args.ue4path
if ue4path is None:
    ue4path=os.environ.get('UE4PATH',None)

if ue4path is None:
    print('Error no unreal engine path defined use env. variable UE4PATH or --ue4path',file=sys.stderr)
    sys.exit(-1)

import sysconfig,os
libdir=sysconfig.get_config_var('LIBPL')
libfile=sysconfig.get_config_var('LDLIBRARY')
include_path=sysconfig.get_path('include')
file_dir=os.path.abspath(os.path.dirname(__file__))


fd=open('Private/PyConfig.h','w')
print('//this is autogenerated file by build.py Dont Edit!!!',file=fd)
print('#pragma once',file=fd)
#print('#include "PyServerPrivatePCH.h"',file=fd)
#print('extern "C" {',file=fd)
assert(os.path.isfile(libdir+'/'+libfile))
print('#define PYTHON_LIB "'+libdir+'/'+libfile+'"',file=fd)
print('#define SYSPATH "'+file_dir+'/Private"',file=fd)
assert(os.path.isfile(include_path+'/Python.h'))
print('#include "'+include_path+'/Python.h"',file=fd)
fd.close()
#print('}',file=fd)
assert(os.system("python3 -m compileall .")==0) #saves time incase of syntax errors in python files

#trying to guess project name and project file
project_dir=os.path.abspath(file_dir+'/../../../../')
import glob
ret=glob.glob(project_dir+'/*.uproject')
if len(ret)==0:
    print("Error: canot find project file in ",project_dir,file=sys.stderr)
    sys.exit(-1)
project_file=ret[0]
project_name=os.path.splitext(os.path.basename(project_file))[0]
print('found project file',project_file)

os.system("mono "+ue4path+'/Engine/Binaries/DotNET/UnrealBuildTool.exe '+project_name+' Development Linux -project="'+project_file+\
    '" -editorrecompile -progress -noubtmakefiles -NoHotReloadFromIDE')

fd=open('run.sh','w')
print('#!/bin/bash',file=fd)
print('#Tish is auto generated script Don\'t Edit!!!',file=fd)
print('cd '+ue4path,file=fd)
print('Engine/Binaries/Linux/UE4Editor "'+project_file+'" -nocore -project='+project_file,file=fd)
fd.close()
assert(os.system("chmod +x ./run.sh")==0)

#	mono /local/ori/GameEngines/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool.exe testplugin Development Linux -project="/local/learn/ur4/testplugin/testplugin.uproject" -editorrecompile -progress -noubtmakefiles -NoHotReloadFromIDE
