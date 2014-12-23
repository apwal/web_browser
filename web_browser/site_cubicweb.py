#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

options = (
    (
        "menu_json",
        {
            "type": "string",
            "default": "",
            "help": "json file describing all the processings that will "
                    "appear in the web browser.",
            "group": "web_browser", "level": 0,
        }
    ),
)
