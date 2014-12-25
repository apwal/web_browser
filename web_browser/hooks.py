#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import datetime
import subprocess

# CW import
from cubicweb import Binary, ValidationError
from cubicweb.server import hook
from cubicweb.predicates import is_instance


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
            with repo.internal_session() as cnx:

                # Get the number of tasks running and kill zombies after updating
                # the corresponding CWProcessing entity
                nb_of_running_tasks = 0
                if "web_browser_running_tasks" in globals():
                    for entity, process in globals()["web_browser_running_tasks"]:
                        if process.poll() is not None:

                            # Update the task status
                            processing = entity.related_processing[0]
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
                        cmd = ["sleep", "1"]
                        process = subprocess.Popen(cmd)

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
