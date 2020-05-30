
import os
import shutil
from pathlib import Path
from distutils.core import setup
from Cython.Build import cythonize

cwd = Path.cwd()
#print('cwd: {}'.format(cwd))
root_dir = cwd.parent
#print('root_dir: {}'.format(root_dir))

_source_list = ['calc_lib.pyx']
source_tmp_dir = 'src_tmp'
root_source_list = [str(root_dir.joinpath(path)) for path in _source_list]
source_list = [os.path.join(source_tmp_dir, path) for path in _source_list]
#print(root_source_list)
#print(source_list)

for (source, root_source) in zip(source_list, root_source_list):
	src_dir, src_name = os.path.split(source)
	os.makedirs(src_dir, exist_ok=True)
	shutil.copy2(root_source, source)
	
setup(
	name = 'Calc Lib',
	ext_modules = cythonize(source_list),
)

