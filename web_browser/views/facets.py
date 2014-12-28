#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cubicweb.web import facet
from cubicweb.selectors import is_instance


############################################################################
# FACETS 
############################################################################

class TimepointFacet(facet.RQLPathFacet):
    __regid__ = "timepoint-facet"
    __select__ = is_instance("CWUpload")
    path = ["X related_processing P", "P status S"]
    order = 1
    filter_variable = "S"
    title = _("Status")


