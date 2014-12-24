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

    def has_been_processed(self):
        """ Tell us if the registered task has been processed by the server.
        """
        if len(self.is_processed) > 0:
            return True
        else:
            return False

    def dc_title(self):
        """ Method the defined the upload file entity title.
        """
        return u"{0} <{1}>".format(self.title, self.form_name)

    def icon_url(self):
        """ Method to get an icon for this entity.
        """
        #return self._cw.data_url(os.path.join("icons", "error.ico"))
        #return self._cw.data_url(os.path.join("icons", "success.ico"))
        return self._cw.data_url(os.path.join("icons", "scheduled.ico"))

