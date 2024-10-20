# ******************************************************************************
#
# IdentifyPlus
# ---------------------------------------------------------
# Extended identify tool. Supports displaying and modifying photos
#
# Copyright (C) 2012-2014 NextGIS (info@nextgis.org)
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
# ******************************************************************************

import json
import xml.etree.ElementTree as ET

import requests
from qgis.PyQt.QtCore import QByteArray
from qgis.PyQt.QtGui import QPixmap


def gdallocationinfoXMLOutputProcessing(outputXMLString):
    """
    return: [ErrCode, Data]
    """
    rootNode = None

    try:
        rootNode = ET.fromstring(outputXMLString)
    except ET.ParseError as err:
        return [1, "Input data error: " + str(err.msg)]

    alert_node = rootNode.find("Alert")
    if alert_node is not None:
        return [2, alert_node.text]

    location_info_node = rootNode.find("BandReport").find("LocationInfo")
    if location_info_node is None:
        return [3, "Not found LocationInfo tag"]

    try:
        jsonLocationInfo = json.JSONDecoder().decode(
            location_info_node.text.encode("utf-8")
        )

        if "error" in jsonLocationInfo:
            err_msg = (
                "Error code: "
                + str(jsonLocationInfo["error"]["code"])
                + " message: \n"
                + jsonLocationInfo["error"]["message"]
            )
            return [4, err_msg]
        else:
            results = []
            for r in jsonLocationInfo["results"]:
                attrs = r["attributes"]
                attrs.update({"layerId": str(r["layerId"])})
                attrs.update({"layerName": r["layerName"]})

                results.append(attrs)

            return [None, results]
    except ValueError:
        pass

    try:
        data = location_info_node.text.encode("utf-8")
        xmlLocationInfo = ET.fromstring(data)

        features = []
        for child in xmlLocationInfo:
            attrs = {}
            for k in list(child.attrib.keys()):
                attrs.update({k: child.attrib[k]})

            features.append(attrs)

        return [None, features]
    except ValueError:
        pass
    except ET.ParseError:
        pass

    return [10, "Cann't parse input data"]


def getImageByURL(url, proxy):
    response = requests.get(url, proxies=proxy)

    img = QPixmap()
    img.loadFromData(QByteArray(response.content))

    return img
