# -*- coding: UTF-8 -*-

import os
import shutil

from fabric.api import local, lcd

from .base import BuilderBase
from .binarybuilders import PyInstallerBuilderLinux

from buildtools.defines import LINUX_BUILD_DIR


class BuilderLinuxBinary(BuilderBase):
    """
    Base class for all Linux binary builders.
    """
    def __init__(self, create_archive=True, is_stable=False):
        super(BuilderLinuxBinary, self).__init__(LINUX_BUILD_DIR, is_stable)

        self._archiveFullName = os.path.join(self.build_dir,
                                             'outwiker_linux_unstable_x64.7z')

        self._create_archive = create_archive
        self._exe_path = os.path.join(self.build_dir, u'outwiker_exe')

    def _build_binary(self):
        """
        Build with cx_Freeze
        """
        src_dir = self.temp_sources_dir
        dest_dir = self._exe_path
        temp_dir = self.facts.temp_dir

        builder = PyInstallerBuilderLinux(src_dir, dest_dir, temp_dir)
        builder.build()

    def _create_plugins_dir(self):
        """
        Create empty 'plugins' dir if it not exists
        """
        pluginsdir = os.path.join(self.temp_sources_dir, u"plugins")

        # Create the plugins folder(it is not appened to the git repository)
        if not os.path.exists(pluginsdir):
            os.mkdir(pluginsdir)

    def _build(self):
        self._copy_necessary_files()
        self._create_plugins_dir()
        self._build_binary()

        if self._create_archive:
            self._build_archive()

    def clear(self):
        super(BuilderLinuxBinary, self).clear()
        self._remove(self._archiveFullName)

    def _build_archive(self):
        # Create archive without plugins
        with lcd(self._exe_path):
            local("7z a ../outwiker_linux_unstable_x64.7z ./* ./plugins -r -aoa")

    def _copy_necessary_files(self):
        shutil.copy(u'copyright.txt', self.facts.temp_dir)
        shutil.copy(u'LICENSE.txt', self.facts.temp_dir)