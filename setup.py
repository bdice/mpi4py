#! /usr/bin/env python
# Author:  Lisandro Dalcin
# Contact: dalcinl@gmail.com
# Id:      $Id$

"""
MPI for Python
==============

This package provides MPI support for Python scripting in parallel
environments. It is constructed on top of the MPI-1/MPI-2
specification, but provides an object oriented interface which closely
follows the MPI-2 C++ bindings.

This module supports point-to-point (send, receive) and collective
(broadcast, scatter, gather, reduction) communications of any
*picklable* Python object.

For objects exporting single-segment buffer interface (strings, NumPy
arrays, etc.), blocking/nonbloking/persistent point-to-point,
collective and one-sided (put, get, accumulate) communications are
fully supported, as well as parallel I/O (blocking and nonbloking,
collective and noncollective read and write operations using explicit
file offsets, individual file pointers and shared file
pointers).

There is also full support for group and communicator (inter, intra,
Cartesian and graph topologies) creation and management, as well as
creating user-defined datatypes. Additionally, there is almost
complete support for dynamic process creation and management (spawn,
name publishing).
"""

# --------------------------------------------------------------------
# Metadata
# --------------------------------------------------------------------

name     = 'mpi4py'
version  = open('VERSION.txt').read().strip()
descr    = __doc__.split('\n')[1:-1]; del descr[1:3]
devstat  = ['Development Status :: 5 - Production/Stable']
download = 'http://pypi.python.org/packages/source/%s/%s/%s-%s.tar.gz'

classifiers = """
License :: Public Domain
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
Operating System :: Microsoft :: Windows
Intended Audience :: Developers
Intended Audience :: Science/Research
Programming Language :: C
Programming Language :: Python
Programming Language :: Cython
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries :: Python Modules
"""

keywords = """
scientific computing
parallel computing
message passing
MPI
"""

platforms = """
Linux
Unix
Mac OS X
Windows
"""

metadata = {
    'name'             : name,
    'version'          : version,
    'description'      : descr.pop(0),
    'long_description' : '\n'.join(descr),
    'url'              : 'http://mpi4py.googlecode.com/',
    'download_url'     : download % (name[0], name, name, version),
    'classifiers'      : [c for c in classifiers.split('\n') if c],
    'keywords'         : [k for k in keywords.split('\n')    if k],
    'platforms'        : [p for p in platforms.split('\n')   if p],
    'provides'         : ['mpi4py', 'mpi4py.MPI',],
    'requires'         : ['pickle'],
    'license'          : 'Public Domain',
    'author'           : 'Lisandro Dalcin',
    'author_email'     : 'dalcinl@gmail.com',
    'maintainer'       : 'Lisandro Dalcin',
    'maintainer_email' : 'dalcinl@gmail.com',
    }
metadata['classifiers'] += devstat

del name, version, descr, devstat, download

# --------------------------------------------------------------------
# Extension modules
# --------------------------------------------------------------------

def ext_modules():
    import sys
    # MPI extension module
    MPI = dict(name='mpi4py.MPI',
               sources=['src/MPI.c'],
               depends=[],
               define_macros=[('MPICH_SKIP_MPICXX', '1'),
                              ('OMPI_SKIP_MPICXX',  '1'),],
               )
    return [MPI]

def headers():
    return []

def executables():
    import sys, os
    from distutils import sysconfig
    libraries = []
    library_dirs = []
    comp_args = []
    link_args = []
    if not sys.platform.startswith('win'):
        py_version = sysconfig.get_python_version()
        cfgDict = sysconfig.get_config_vars()
        if '-pthread' in cfgDict.get('CC', ''):
            comp_args.append('-pthread')
        libraries = ['python' + py_version]
        for var in ('LIBDIR', 'LIBPL'):
            library_dirs += cfgDict.get(var, '').split()
        for var in ('LIBS', 'MODLIBS', 'SYSLIBS', 'LDLAST',):
            link_args += cfgDict.get(var, '').split()
    pyexe = dict(name='mpi4py',
                 sources=['src/python.c'],
                 libraries=libraries,
                 library_dirs=library_dirs,
                 extra_compile_args=comp_args,
                 extra_link_args=link_args)
    return [pyexe]


# --------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------

from distutils.core import setup
from conf.mpidistutils import Distribution, Extension, Executable
from conf.mpidistutils import config, build, build_ext
from conf.mpidistutils import build_exe, install_exe, clean_exe
LibHeader = lambda header: str(header)
ExtModule = lambda extension: Extension(**extension)
ExeBinary = lambda executable: Executable(**executable)

def main():
    """
    call distutils.setup(*targs, **kwargs)
    """
    setup(packages    = ['mpi4py'],
          package_dir = {'mpi4py' : 'src/mpi4py'},
          headers     = [LibHeader(hdr) for hdr in headers()],
          ext_modules = [ExtModule(ext) for ext in ext_modules()],
          executables = [ExeBinary(exe) for exe in executables()],
          distclass = Distribution,
          cmdclass = {'config'      : config,
                      'build'       : build,
                      'build_ext'   : build_ext,
                      'build_exe'   : build_exe,
                      'clean_exe'   : clean_exe,
                      'install_exe' : install_exe,
                      },
          **metadata)

if __name__ == '__main__':
    # hack distutils.sysconfig to eliminate debug flags
    from distutils import sysconfig
    cvars = sysconfig.get_config_vars()
    cflags = cvars.get('OPT')
    if cflags:
        cflags = cflags.split()
        for flag in ('-g', '-g3'):
            if flag in cflags:
                cflags.remove(flag)
        cvars['OPT'] = str.join(' ', cflags)
    # and now call main
    main()
# --------------------------------------------------------------------
