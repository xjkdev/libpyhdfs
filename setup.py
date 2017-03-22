import os
import sys

from distutils.core import setup, Extension

if 'JAVA_HOME' not in os.environ:
    raise ValueError('JAVA_HOME not defined in environment')


java_home = os.environ['JAVA_HOME']


def find_directory_containing(search_paths, filename):
    for path in search_paths:
        for root, dirs, files in os.walk(path, followlinks=True):
            if filename in files:
                return os.path.realpath(os.path.join(path, root))


def java_directory_containing(filename):
    directory = find_directory_containing((java_home,), filename)
    if directory is not None:
        return directory

    print('Unable to find {}'.format(filename))
    sys.exit(1)

libjvm = 'libjvm.so'
libhdfs = 'libhdfs.so'
if sys.platform == 'darwin':
    libjvm = 'libjvm.dylib'
    libhdfs = 'libhdfs.dylib'

pyhdfs = Extension('pyhdfs',
        sources=['src/pyhdfs.c'],
        include_dirs=[
            'src',
            java_directory_containing('jni.h'),
            java_directory_containing('jni_md.h'),
            ],
        libraries=['hdfs'],
        library_dirs=['lib'],
        runtime_library_dirs=[
            java_directory_containing(libjvm),
            find_directory_containing((
                '/usr/lib',
                '/usr/lib64',
                '/etc',
                'lib'
                ),
                libhdfs),
            ],
        )

setup(name='python-hdfs',
        version='0.4.1',
        author='Jake Xie, Deng Zhiping, Joshua Downer',
        author_email='xjk2008@gmail.com',
        description="Python wrapper for libhdfs",
        long_description=(open('README').read()),
        url="https://github.com/xjkdev/pyhdfs",
        license="Apache License 2.0",
        platforms=["GNU/Linux"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: System :: Filesystems',
            'Topic :: Utilities',
            ],
        ext_modules=[pyhdfs],
        )
