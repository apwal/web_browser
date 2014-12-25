#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os

# CW import
from cubicweb.entities import AnyEntity


class EntityCWUpload(AnyEntity):
    """ Define the 'CWUpload' entity associated functions.
    """
    __regid__ = "CWUpload"

    def dc_title(self):
        """ Method the defined the upload file entity title.
        """
        return u"{0} <{1}>".format(self.title, self.form_name)

    def icon_url(self):
        """ Method to get an icon for this entity.
        """
        print self.related_processing[0].status
        if self.related_processing[0].status == "error":
            return self._cw.data_url(os.path.join("icons", "error.ico"))
        elif self.related_processing[0].status == "success":
            return self._cw.data_url(os.path.join("icons", "success.ico"))
        elif self.related_processing[0].status == "running":
            return self._cw.data_url(os.path.join("icons", "running.ico"))     
        else:
            return self._cw.data_url(os.path.join("icons", "scheduled.ico"))

