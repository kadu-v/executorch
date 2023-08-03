# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import shutil

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install


def custom_command():
    src_dst_list = [
        ("schema/scalar_type.fbs", "exir/serialize/scalar_type.fbs"),
        ("schema/program.fbs", "exir/serialize/program.fbs"),
    ]
    for src, dst in src_dst_list:
        print(f"copying from {src} to {dst}")
        shutil.copyfile(src, dst)

    for _, dst in src_dst_list:
        if not os.path.isfile(dst):
            raise FileNotFoundError(
                f"Could not find {dst}, copying file from {src} fails."
            )


class CustomInstallCommand(install):
    def run(self):
        custom_command()
        install.run(self)


class CustomDevelopCommand(develop):
    def run(self):
        custom_command()
        develop.run(self)


class CustomEggInfoCommand(egg_info):
    def run(self):
        custom_command()
        egg_info.run(self)


setup(
    package_dir={
        "executorch/backends": "backends",
        "executorch/exir": "exir",
        "executorch/schema": "schema",
        "executorch/extension": "extension",
    },
    cmdclass={
        "install": CustomInstallCommand,
        "develop": CustomDevelopCommand,
        "egg_info": CustomEggInfoCommand,
    },
)
