
from pathlib import Path
from distutils.core import setup
from Cython.Build import cythonize

cwd = Path.cwd()
print(cwd)
root_dir = cwd.parent
print(root_dir)

_source_list = ["calc_lib.pyx"]
source_list = [str(root_dir.joinpath(path)) for path in _source_list]
print(source_list)

setup(
	name = 'Calc Lib',
	ext_modules = cythonize(source_list),
)

