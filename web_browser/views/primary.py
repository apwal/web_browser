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
from cubicweb.web.views.primary import PrimaryView
from cubicweb.selectors import is_instance
from logilab.mtconverter import xml_escape

# RQL UPLOAD import
from cubes.rql_upload.views.primary import UploadFormPrimaryView
from cubes.rql_upload.schema import CWUpload


class ResultFormPrimaryView(PrimaryView):
    """ Class that define how to display an UploadForm entity.

    The table display may be tuned by specifing the 'upload-table' class in
    a css.
    """
    __select__ = PrimaryView.__select__ & is_instance("UploadForm")

    def display_form(self, entity):
        """ Generate the html code.
        """
        # Get the source entity
        src_entity = entity.reverse_result_form[0]

        # Switch base on the source entity
        if isinstance(src_entity, CWUpload):
            # Get the json form
            json_data = json.load(entity.data)
        else:
            # Get the data from the description field
            json_data = {}
            for splitter in ["returncode: ", "stdout: ", "stderr: "]:
                json_data[splitter[:-2]] = entity.description[1: -1].split(
                    splitter)[1]
            for key, value in json_data.iteritems():
                for splitter in ["returncode: ", "stdout: ", "stderr: "]:
                    value = value.split(splitter)[0]
                json_data[key] = value

        # Display a title
        self.w(u'<div class="page-header">')
        self.w(u'<h2>{0}</h2>'.format(xml_escape(entity.dc_title())))
        self.w(u'</div><hr>')

        self.w(u'<table class="upload-table">')

        # Display the form
        for label, attribute in json_data.iteritems():
            self.w(u'<tr><td><b>{0}</b></td><td>{1}</td></tr>'.format(
                   self._cw._(label), attribute))

        # Link to the upload entity
        self.w(u'<tr><td><b>{0}</b></td><td>{1}</td></tr>'.format(
               self._cw._("Related upload"), src_entity.view("outofcontext")))

        self.w(u'</table>')

    def call(self, rset=None):
        """ Create the form primary view.
        """
        # Get the entity that contains the form
        entity = self.cw_rset.get_entity(0,0)

        # Display the form
        self.display_form(entity)
        

def registration_callback(vreg):
    """ Register the tuned primary views.
    """
    vreg.register_and_replace(ResultFormPrimaryView, UploadFormPrimaryView)

