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
from cubicweb.web.views.basecomponents import HeaderComponent, ApplLogo
from cubicweb.web.views.boxes import SearchBox
from logilab.common.registry import yes


##############################################################################
# Modify the html template
##############################################################################

class WebBrowserLogo(HeaderComponent):
    """ Build the instance logo, usually displayed in the header. """
    __regid__ = "logo"
    __select__ = yes()
    order = -1
    context = _("header-left",)

    def render(self, w):
        w(u"<a href='{0}'><img id='logo' src='{1}' alt='logo'/></a>".format(
            self._cw.base_url(),
            self._cw.data_url(os.path.join("icons", "web_browser.ico"))))


##############################################################################
# Update the registery
##############################################################################

def registration_callback(vreg):
    """ Register the tuned components.
    """
    vreg.register_and_replace(WebBrowserLogo, ApplLogo)
    vreg.unregister(SearchBox)


