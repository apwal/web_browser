#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cubicweb.view import View


###############################################################################
# CWSearch Widgets
###############################################################################

class CWUploadView(View):
    """ Monitor each submitted tasks.
    """
    __regid__ = "task-manager"

    def call(self, **kwargs):
        """ Create a view to monitor each submitted tasks.
        """
        # Get all uploaded tasks
        rql = u"Any X Where X is CWUpload"
        rset = self._cw.execute(rql)
        self.wview("list", rset=rset)

