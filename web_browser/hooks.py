#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import sys
import datetime
import subprocess
import json
from operator import itemgetter

# CW import
from cubicweb import Binary, ValidationError
from cubicweb.server import hook
from cubicweb.predicates import is_instance

# WEB BROWSER import
from cubes.web_browser.views.utils import load_forms
from cubes.web_browser.views.formfields import CONVERSION_TYPES

# RQL DOWNLOAD import
from cubes.rql_download.fuse.fuse_mount import get_cw_option


###############################################################################
# Web Browser insert
###############################################################################

class CWAddTask(hook.Hook):
    """ CubicWeb hook that is called before adding the new task.
    """
    __regid__ = "webbrowser.task_add_hook"
    __select__ = hook.Hook.__select__ & is_instance("CWUpload")
    events = ("before_add_entity",)

    def __call__(self):
        """ Before adding the CWUpload entity, create a CWProcessing entity.
        """
        # Here we want to execute rql request with user permissions: user who
        # is creating this entity
        with self._cw.security_enabled(read=True, write=True):

            # Create the associated processing task
            processing_eid = self._cw.create_entity(
                "CWProcessing", status=u"scheduled",
                uploaded_by=self._cw.user.eid).eid

            # Link the processing with the submitted task
            self._cw.add_relation(
                self.entity.eid, "related_processing", processing_eid)

            # Create an entity to store the task result
            result_eid = self._cw.create_entity(
                "UploadForm", data=Binary(json.dumps({})),
                data_format=u"text/json", data_name=u"result.json",
                uploaded_by=self._cw.user.eid).eid

            # Link the processing with the final results
            self._cw.add_relation(processing_eid, "result_form", result_eid)


###############################################################################
# Task Manager Startup
###############################################################################

class ServerStartupHook(hook.Hook):
    """ On startup, register a task to process the submitted taks.
    """
    __regid__ = "webborwser.process_hook"
    events = ("server_startup",)
    max_nb_of_tasks = 1

    def __call__(self):
        """ Method to execute the 'ServerStartupHook' hook.
        """
        def process_tasks(repo):
            """ Delete all CWSearch entities that have expired.
            """
            # Local import
            import json
            import subprocess

            # Get the internal session
            with repo.internal_session() as cnx:

                # Get the number of tasks running and kill zombies after updating
                # the corresponding CWProcessing entity
                nb_of_running_tasks = 0
                _globals = globals()
                if _globals is not None and "web_browser_running_tasks" in _globals:
                    for entity, process in _globals["web_browser_running_tasks"]:
                        if process.poll() is not None:

                            # Store the process result
                            stdout, stderr = process.communicate()
                            result_struct = {
                                "returncode": process.returncode,
                                "stderr": stderr or "None",
                                "stdout": stdout or "None"
                            }

                            # Get the task related processing and result
                            processing = entity.related_processing[0]
                            result_eid = cnx.execute(
                                "Any X Where X is UploadForm, Y result_form X, "
                                "Y eid '{0}'".format(processing.eid))[0][0]

                            # Update the result entity
                            cnx.execute(
                                "SET X description '{0}' WHERE X eid '{1}'".format(
                                    repr(result_struct).replace("'",""), result_eid))

                            # Update the task status
                            if process.poll() == 0:
                                cnx.execute(
                                    "SET X status 'success' WHERE X eid '{0}'".format(
                                        processing.eid))
                            else:
                                cnx.execute(
                                    "SET X status 'error' WHERE X eid '{0}'".format(
                                        processing.eid))

                            # Kill the zombie
                            process.wait()
                            globals()["web_browser_running_tasks"].remove(
                                (entity, process))
                        
                        else:
                            nb_of_running_tasks += 1

                # Run the submitted tasks
                rset = cnx.execute(
                    "Any X ORDERBY D Where X is CWUpload, X creation_date D, "
                    "X related_processing Y, Y status 'scheduled'")

                for entity in rset.entities():
                    if nb_of_running_tasks < self.max_nb_of_tasks:

                        # Create the command associated to the submitted task
                        task_parameters = json.load(entity.result_form[0].data)
                        cmd = self.get_commandline(task_parameters)
                        process = subprocess.Popen(
                            cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

                        # Update the task status
                        processing = entity.related_processing[0]
                        cnx.execute(
                            "SET X status 'running' WHERE X eid '{0}'".format(
                                processing.eid))

                        # Create zombie process, keep trace in memory to deal with
                        # them later.
                        if "web_browser_running_tasks" not in globals():
                            globals()["web_browser_running_tasks"] = [
                                (entity, process)]
                        else:
                            globals()["web_browser_running_tasks"].append(
                                (entity, process))

                        # Increment the number of running tasks counter
                        nb_of_running_tasks += 1
                    else:
                        break

                # Commit changes
                cnx.commit()

        # Set the process event loop every minute
        dt = datetime.timedelta(1. / (1440. * 10.))
        self.repo.looping_task(
            dt.total_seconds(), process_tasks, self.repo)

        # Call the clean function manually on the startup
        process_tasks(self.repo)

    def get_commandline(self, parameters):
        """ Method to generate a comandline representation of the task.
        """
        # Get command line arguments
        parameters.pop("upload_title")
        module_name = parameters.pop("module")
        function_name = parameters.pop("method")

        # Split args and kwargs
        config = {"upload_structure_json": get_cw_option(
            self.repo.schema.name, "upload_structure_json")}
        form = load_forms(config, "upload_structure_json")

        # Get the form parameters
        parameters_description = form["{0}.{1}".format(module_name, function_name)]
        type_parameters = dict((item["name"], item["type"])
                               for item in parameters_description)

        # Get the args parameters from the form
        args_parameters = dict((item["name"], item["order"])
                               for item in parameters_description
                               if "order" in item)
        args_parameters = sorted(args_parameters.items(), key=itemgetter(1))
        args_parameters = [item[0] for item in args_parameters]

        # Get the args and kwargs values
        kwargs = {}
        for name, value in parameters.iteritems():
            converter = CONVERSION_TYPES[type_parameters[name]]
            if name in args_parameters:
                args_parameters[args_parameters.index(name)] = converter(value)
            else:
                kwargs[name] = converter(value)

        # Get the outputs
        # ToDo: dynamic from task form
        outputs = ["res"]         

        # Construct the command line
        commandline = [sys.executable, "-m", "cubes.web_browser.task_luncher",
                "-i", self.repo.schema.name, "-m", module_name, "-f", function_name,
               "-a", repr(args_parameters), "-k", repr(kwargs), "-o",
               repr(outputs)]

        return commandline
