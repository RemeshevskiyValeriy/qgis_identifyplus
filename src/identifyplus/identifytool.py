# -*- coding: utf-8 -*-

#******************************************************************************
#
# IdentifyPlus
# ---------------------------------------------------------
# Extended identify tool. Supports displaying and modifying photos.
#
# Copyright (C) 2012-2016 NextGIS (info@nextgis.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

import abc


class IdentifyTool:
    def __init__(self, name, desc):
        self._name = name
        self._desc = desc

    @abc.abstractmethod
    def identify(self, identifyResult):
        return

    @staticmethod
    @abc.abstractmethod
    def isAvailable(target):
        return