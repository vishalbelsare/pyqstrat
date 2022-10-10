import setuptools
from distutils.core import setup, Extension
import numpy as np
import pybind11
import glob
import os
import sys


if __name__ == '__main__':
    _conda_prefix = os.getenv('CONDA_PREFIX')
    _conda_prefix_1 = os.getenv('CONDA_PREFIX_1')
    if _conda_prefix is None and _conda_prefix_1 is None:
        raise RuntimeError("CONDA_PREFIX and CONDA_PREFIX_1 not found in env variables")

    conda_prefix = _conda_prefix if _conda_prefix else _conda_prefix_1
    pybind_11_include = [pybind11.get_include()]
    np_include = [np.get_include()]

    if sys.platform in ["win32", "cygwin"]:
        include_dirs = [f'{conda_prefix}/include',
                        f'{conda_prefix}/Library/include']
        
        library_dirs = [f'{conda_prefix}/lib',
                        f'{conda_prefix}/Library/lib',
                        f'{conda_prefix}/bin',
                        f'{conda_prefix}/Library/bin']
    else:
        include_dirs = [f'{conda_prefix}/lib']       
        library_dirs = [f'{conda_prefix}/lib']

    cpp_dir = 'pyqstrat/cpp'

    io_module = Extension('pyqstrat.pyqstrat_io',
                          sources = [f'{cpp_dir}/io/{file}' for file in ['read_file.cpp', 'csv_reader.cpp']],
                          include_dirs=include_dirs + np_include,
                          library_dirs=library_dirs,
                          libraries=['zip'],
                          extra_compile_args=['-std=c++11', '-Ofast'])

    opt_cpp_files = glob.glob(f'{cpp_dir}/options/*.cpp') + glob.glob(f'{cpp_dir}/lets_be_rational/*.cpp')
    options_module = Extension('pyqstrat.pyqstrat_cpp',
                               sources=opt_cpp_files,
                               include_dirs=include_dirs + pybind_11_include,
                               library_dirs=library_dirs,
                               libraries=['zip', 'hdf5_cpp', 'hdf5', 'boost_iostreams'],
                               extra_compile_args=['-std=c++11', '-Ofast'])

    with open('version.txt', 'r') as f:
        version = f.read().strip()

    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()

    with open('README.rst', 'r') as f:
        long_description=f.read()
        
    setup(name='pyqstrat',
          version=version,
          ext_modules = [io_module, options_module],
          author_email='abbasi.sal@gmail.com',
          url='http://github.com/abbass2/pyqstrat/',
          license='BSD',
          python_requires='>=3.7',
          install_requires=requirements,
          description='fast / extensible library for backtesting quantitative strategies',
          long_description=long_description,
          packages=['pyqstrat'],
          include_package_data=True,
          platforms='any',
          classifiers = [
              'Development Status :: 4 - Beta',
              'Natural Language :: English',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: BSD License',
              'Operating System :: OS Independent',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Software Development :: Libraries :: Application Frameworks',
              'Topic :: Office/Business :: Financial :: Investment',
              'Programming Language :: Python :: 3.7',
              'Programming Language :: Python :: 3 :: Only',
          ],
          zip_safe = False)
