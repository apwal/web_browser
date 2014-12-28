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
from cubicweb.predicates import is_instance
from cubicweb.view import EntityView


###############################################################################
# CWUpload 
###############################################################################

class CWUploadOutOfContextView(EntityView):
    """ This view enables us to reflect the task status.
    """
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("CWUpload")

    def cell_call(self, row, col):
        """ Create the CWUploadOutOfContextView outofcontext view.
        """
        # Get the scan entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the scan image url
        status_image = u"<img alt='' src='{0}'>".format(entity.icon_url())

        # Create the div that will contain the list item
        self.w(u"<div class='ooview'><div class='well'>")

        # Create a bootstrap row item
        self.w(u"<div class='row'>")
        # > first element: the image
        self.w(u"<div class='col-md-2'><p class='text-center'>{0}</p>"
                "</div>".format(status_image))
        # > second element: the uploeded task description + link
        self.w(u"<div class='col-md-4'><h4>{0}</h4>".format(
            entity.view("incontext")))
        self.w(u"Submission date <em>{0}</em> - Submitted by <em>{1}</em>"
                "</div>".format(entity.creation_date.date(),
                                entity.uploaded_by[0].view("incontext")))
        # > third element: the see more button
        self.w(u"<div class='col-md-3'>")
        self.w(u"<button class='btn btn-danger' type='button' "
                "style='margin-top:8px' data-toggle='collapse' "
                "data-target='#info-{0}'>".format(row))
        self.w(u"See more")
        self.w(u"</button></div>")
        # Close row item
        self.w(u"</div>")

        # Create a div that will be shown or hide when the see more button is
        # clicked
        self.w(u"<div id='info-{0}' class='collapse'>".format(row))
        self.w(u"<dl class='dl-horizontal'>")
        # > add the submitted form values
        task_parameters = json.load(entity.result_form[0].data)
        for key, value in task_parameters.iteritems():
            if key != "upload_title":
                self.w(u"<dt>{0}</dt><dd>{1}</dd>".format(key, value))
        self.w(u"</div>")

        # Close list item
        self.w(u"</div></div>")


###############################################################################
# CWProcessing 
###############################################################################

class CWProcessingOfContextView(EntityView):
    """ This view enables us to reflect the task results.
    """
    __regid__ = "outofcontext"
    __select__ = EntityView.__select__ & is_instance("CWProcessing")

    def cell_call(self, row, col):
        """ Create the CWProcessingOfContextView outofcontext view.
        """
        # Get the scan entity
        entity = self.cw_rset.get_entity(row, col)

        # Get the scan image url
        status_image = u"<img alt='' src='{0}'>".format("") #entity.icon_url())

        # Create the div that will contain the list item
        self.w(u"<div class='ooview'><div class='well'>")

        # Create a bootstrap row item
        self.w(u"<div class='row'>")
        # > first element: the image
        self.w(u"<div class='col-md-2'><p class='text-center'>{0}</p>"
                "</div>".format(status_image))
        # > second element: the uploeded task description + link
        self.w(u"<div class='col-md-4'><h4>{0}</h4>".format(
            entity.view("incontext")))
        self.w(u"Submission date <em>{0}</em> - Submitted by <em>{1}</em>"
                "</div>".format(entity.creation_date.date(),
                                entity.uploaded_by[0].view("incontext")))
        # > third element: the see more button
        self.w(u"<div class='col-md-3'>")
        self.w(u"<button class='btn btn-danger' type='button' "
                "style='margin-top:8px' data-toggle='collapse' "
                "data-target='#info-{0}'>".format(row))
        self.w(u"See more")
        self.w(u"</button></div>")
        # Close row item
        self.w(u"</div>")

        # Create a div that will be shown or hide when the see more button is
        # clicked
        self.w(u"<div id='info-{0}' class='collapse'>".format(row))
        self.w(u"<dl class='dl-horizontal'>")
        # > add the submitted form values
        for rentity in entity.results:
            if hasattr(rentity, "filepath"):
                self.w(u"<dt>{0}</dt><dd>{1}</dd>".format(
                    rentity.name, rentity.filepath))
            else:
                self.w(u"<dt>{0}</dt><dd>{1}</dd>".format(
                    rentity.name, rentity.value))
        self.w(u"</div>")

        # Close list item
        self.w(u"</div></div>")

