#    PyDAI - Python Data Acquisition and Instrumentation
#
#    Copyright (C) 2012 Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
from glob import glob

setup(name='PyDAI',
      version='0.1',
      description='Python Data Acquisition and Instrumentation',
      author='Jeffrey M Brown, Greg A Cohoon, Kyle T Taylor',
      url='https://github.com/brownjm/PyDAI',
      license='GPL',
      packages=['src', 'test'],
      package_dir={'pydai':''},
      package_data={'':['devices']}
      )
