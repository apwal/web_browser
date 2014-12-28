#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" Exemple:
> python task_launcher.py -i test -m numpy -f exp -a [0.] -k {} -o "[('res', False)]" -e 995 -u 6
"""

# System import
import os
import sys
import json
import pwd
import logging
from optparse import OptionParser

# Define the logger
logger = logging.getLogger(__file__)

# CW import
from cubicweb.cwconfig import CubicWebConfiguration as cwcfg

# RQL DOWNLAOD import
from cubes.rql_download.fuse.fuse_mount import get_cw_connection, get_cw_option


def load_function(module_name, function_name):
    """ Load a function defined in a specific module.

    Parameters
    ----------
    module_name: str
        the name of the module (python format).
    function_name: str
        the name of the function to load.

    Returns
    -------
    func: @func
        the callable function (None if no function can be loaded).
    """
    # First import the module
    try :
        __import__(module_name)
    except ImportError, e :
        logging.error("Could not import {0}: {1}".format(module_name, e))
        raise Exception("Could not import {0}: {1}".format(module_name, e))
    module = sys.modules[module_name]

    # Get the function
    return getattr(module, function_name, None)


def build_expression(module_name, function_name, args, kwargs, outputs):
    """ Build the expression to evaluate in the proper namespace.

    Parameters
    ----------
    module_name: str
        the name of the module (python format).
    function_name: str
        the name of the function to load.
    args: list
        the ordered function arguments.
    kwargs: dict
        the function arguments.
    outputs: dict
        the ordered name of the outputs.

    Returns
    -------
    namesapce: dict
        the namespace where the function expresion has to be executed.
    expression: str
        the function expression.
    """
    # Get the callable function
    function = load_function(module_name, function_name)

    # Get output parameter names$
    output_names = [item[0] for item in outputs]

    # Build the expression namespace
    namespace = {"function" : function}
    for parameter_name in output_names:
        namespace[parameter_name] = None
    for parameter_name, parameter_value in kwargs.iteritems():
        namespace[parameter_name] = parameter_value
    logger.debug("Namespace = {0}".format(namespace))
   
    # Build the expression
    fargs = [repr(x) for x in args]
    for parameter_name, parameter_value in kwargs.iteritems():
        fargs.append("{0} = {0}".format(parameter_name))
    expression = "function({0})".format(", ".join(fargs))
    if output_names: 
        output_expression = ", ".join(output_names)
        expression = "{0} = {1}".format(output_expression, expression)
    logger.debug("Expression = {0}".format(expression))

    return namespace, expression


def set_outputs_in_db(namespace, outputs, instance_name, eid, uid):
    """ Save the outputs in a cw database.

    Parameters
    ----------
    namesapce: dict
        the namespace where the function expresion has to be executed.
    outputs: list
        the ordered name of the outputs.
    instance_name: str
        the name of the cubicweb instance.
    eid: int
        the entity eid.
    eid: int
        the user uid.
    """
    # Get a Cubicweb in memory connection
    cw_connection = get_cw_connection(instance_name)

    # Get the cw session to execute rql requests
    cw_session = cw_connection.session

    # Store the results in the db
    for parameter_name, is_file in outputs:

        # Get the parameter value
        print parameter_name, is_file
        parameter_value = namespace[parameter_name]
        logger.debug("Output: {0} = {1} ({2})".format(
            parameter_name, parameter_value, is_file))

        # Insert in db
        if is_file:
            rql = ("INSERT ExternalResource X: X name '{0}', X filepath '{1}', "
                   "X uploaded_by U, Y results  X WHERE U eid '{2}', Y eid "
                   "'{3}'".format(parameter_name, parameter_value, uid, eid))
        else:
            rql = ("INSERT ScoreValue X: X name '{0}', X value '{1}', "
                   "X uploaded_by U, Y results  X WHERE U eid '{2}', Y eid "
                   "'{3}'".format(parameter_name, parameter_value, uid, eid))
        print rql
        logger.debug("RQL: {0}".format(rql))
        cw_session.execute(rql)

    # Shut down the cw connection
    cw_session.commit()
    cw_connection.shutdown()


if __name__ == "__main__":

    # Define script options
    parser = OptionParser()
    parser.add_option("-i", "--instance", dest="instance_name",
                      help="the instance name.")
    parser.add_option("-m", "--module", dest="module_name",
                      help="the module name.")
    parser.add_option("-f", "--function", dest="function_name",
                      help="the function name.")
    parser.add_option("-a", "--args", dest="args",
                      help="the ordered function arguments: 'value1,...'")
    parser.add_option("-k", "--kwargs", dest="kwargs",
                      help="the function arguments: 'name1=value1,...'")
    parser.add_option("-o", "--outputs", dest="outputs",
                      help="the function outputs. 'name1,...'")
    parser.add_option("-e", "--eid", dest="eid",
                      help="the entity eid.'")
    parser.add_option("-u", "--uid", dest="uid",
                      help="the user uid.'")
    (options, args) = parser.parse_args()

    # Setup the logger: cubicweb change the logging config and thus
    # we setup en axtra stream handler
    logger.setLevel(logging.DEBUG)

    # Command line parameters
    logger.debug(
        "Command line parameters: instance name = {0}, module name = "
        "{1}, function name = {2}, args = {3}, kwargs = {4}, "
        "outputs = {5}".format(
            options.instance_name, options.module_name, options.function_name,
            options.args, options.kwargs, options.outputs))

    # Build expression and namespace
    namespace, expression = build_expression(
        options.module_name, options.function_name, eval(options.args),
        eval(options.kwargs), eval(options.outputs))

    # Execute it
    def f():
        exec expression in namespace  
    f()

    # Save the outputs in a cw entity
    set_outputs_in_db(
        namespace, eval(options.outputs), options.instance_name,
        int(options.eid), int(options.uid))


