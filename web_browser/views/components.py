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
from cubicweb.web.views.boxes import EditBox
from cubicweb.selectors import is_instance, one_line_rset

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
        tree_menu = load_forms(self._cw.vreg.config, "menu_json")

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
        w(u"<div class='btn-toolbar'>")
        w(u"<div class='btn-group-vertical btn-block'>")
        href = self._cw.build_url(
            rql="Any X ORDERBY D DESC Where X is CWUpload, X creation_date D")
        w(u"<a class='btn btn-primary' href='{0}'>".format(href))
        w(u"{0}</a>".format(self.title))
        w(u"</div></div><br/>")


class SaveTaskResultBox(component.CtxComponent):
    """ Display a box containing a download shortcut.
    """
    __regid__ = "ctx-save-task-result"
    __select__ = (component.CtxComponent.__select__ & is_instance("CWUpload") &
                  one_line_rset())
    context = "left"
    title = _("Download result")
    order = 2

    def render_body(self, w):
        """ Create a navigation box to dowload the results.
        """
        w(u"<div class='btn-toolbar'>")
        w(u"<div class='btn-group-vertical btn-block'>")
        href = self._cw.build_url(
            "add/CWSearch", path=self.cw_rset.printable_rql())
        w(u"<a class='btn btn-primary' href='{0}'>".format(href))
        w(u"{0}</a>".format(self.title))
        w(u"</div></div><br/>")


def registration_callback(vreg):
    """ Register the tuned components.
    """
    vreg.register(SaveTaskResultBox)
    vreg.register(WebBrowserBox)
    vreg.register(TaskManagerBox)
    vreg.unregister(CWUploadBox)
    vreg.unregister(EditBox)
