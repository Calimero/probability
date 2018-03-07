# Copyright 2018 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Install tensorflow_probability."""
import datetime
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install as InstallCommandBase
from setuptools.dist import Distribution

__version__ = '0.0.1'

REQUIRED_PACKAGES = [
    'six >= 1.10.0',
    'numpy >= 1.11.1',
]
REQUIRED_TENSORFLOW_VERSION = '1.5.0'

if '--gpu' in sys.argv:
  use_gpu = True
  sys.argv.remove('--gpu')
else:
  use_gpu = False

if '--release' in sys.argv:
  release = True
  sys.argv.remove('--release')
else:
  # Build a nightly package by default.
  release = False

gpu_suffix = '-gpu' if use_gpu else ''

if release:
  project_name = 'tensorflow-probability{}'.format(gpu_suffix)
  tensorflow_package_name = 'tensorflow{}>={}'.format(
      gpu_suffix, REQUIRED_TENSORFLOW_VERSION)
else:
  # Nightly releases use date-based versioning of the form
  # '0.1.dev20180305', and depend on nightly TensorFlow.
  project_name = 'tfp-nightly{}'.format(gpu_suffix)
  datestring = datetime.datetime.now().strftime('%Y%m%d')
  __version__ = '{}.dev{}'.format(__version__, datestring)
  tensorflow_package_name = 'tf-nightly{}'.format(gpu_suffix)

REQUIRED_PACKAGES.append(tensorflow_package_name)


class BinaryDistribution(Distribution):
  """This class is needed in order to create OS specific wheels."""

  def has_ext_modules(self):
    return False

setup(
    name=project_name,
    version=__version__,
    description='Probabilistic modeling and statistical '
                'inference in TensorFlow',
    author='Google Inc.',
    author_email='no-reply@google.com',
    url='http://github.com/tensorflow/probability',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    # Add in any packaged data.
    include_package_data=True,
    package_data={'': ['*.so']},
    exclude_package_data={'': ['BUILD', '*.h', '*.cc']},
    zip_safe=False,
    distclass=BinaryDistribution,
    cmdclass={
        'pip_pkg': InstallCommandBase,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='tensorflow probability bayesian machine learning',
)
