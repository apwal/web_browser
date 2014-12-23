#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cgi import parse_qs
from cubicweb.view import View


###############################################################################
# Web Service Views
###############################################################################

class CWRegisterTaskView(View):
    """ Custom view to fill and commit a new task.
    """
    __regid__ = "web-service-task"


    def call(self, **kwargs):
        """ Create the task registration view.
        """
        # Get some parameters
        path = self._cw.relative_path()
        if "?" in path:
            path, param = path.split("?", 1)
            kwargs.update(parse_qs(param))
        method_name = kwargs["method"][0]
        module_name = kwargs["module"][0]

        # Page title
        self.w(u'<h3 class="panel-title">New task ("{0}": {1})</h3>'.format(
            module_name, method_name))


