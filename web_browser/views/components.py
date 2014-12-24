#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import json

# CW import
from cubicweb.predicates import nonempty_rset, anonymous_user
from cubicweb.web import component

# WEB BROWSER import
from utils import load_forms

# RQL UPLOAD import
from cubes.rql_upload.views.components import CWUploadBox


###############################################################################
# Navigation Box 
###############################################################################

class WebBrowserBox(component.CtxComponent):
    """ Display a box containing navigation shortcuts.
    """
    __regid__ = "ctx-web-browser"
    __select__ = (component.CtxComponent.__select__ & ~anonymous_user())
    context = "left"
    title = _("Web Browser")
    order = 0

    def render_body(self, w):
        """ Create the different item of the navigation box
        """
        # Get the tree menu from the configuration file
        tree_menu = load_forms(self._cw.vreg.config)

        # Build redirection url
        url = self._cw.build_url("view", vid="upload-view",
                                 title=self._cw._("Register new task"))

        # Code to initialize the tree when the document is loaded
        tree_script = u"""
            <script type="text/javascript">
            $(function(){{
                $("#tree").dynatree({{
                    onActivate: function(node) {{
                        document.location.href = 
                            "{0}&method=" + node.data.title +
                            "&module=" + node.data.module +
                            "&form_name=" + node.data.module + "." + node.data.title;
                    }},
                    title: "Web Browser",
                    clickFolderMode: 2,
                    persist: true,
                    checkbox: false,
                    selectMode: 1,
                    children: {1}
                }});
            }});
            </script>
        """.format(url, tree_menu)
        w(tree_script)

        # Add a <div> element where the tree should appear
        w(u"<div id='tree'> </div>")


class TaskManagerBox(component.CtxComponent):
    """ Display a box containing task shortcuts.
    """
    __regid__ = "ctx-task-manager"
    __select__ = (component.CtxComponent.__select__ & ~anonymous_user())
    context = "left"
    title = _("Task manager")
    order = 1

    def render_body(self, w):
        """ Create a navigation box to keep trace of each tasks.
        """
        href = self._cw.build_url(
            "view", vid="task-manager", title=self._cw._("Task manager"))
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'{0}</a>'.format(self._cw._("Task manager")))
        w(u'</div></div><br/>')


def registration_callback(vreg):
    """ Register the tuned components.
    """
    vreg.register(WebBrowserBox)
    vreg.register(TaskManagerBox)
    vreg.unregister(CWUploadBox)
