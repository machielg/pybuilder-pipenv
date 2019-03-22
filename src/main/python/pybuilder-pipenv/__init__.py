import json
import os

from pybuilder.core import Project, Logger, init


@init
def pipenv_deps(project: Project, logger: Logger):
    logger.debug("Initializing pybuilder-pipenv")
    assert len(project.dependencies) == 0, logger.error("Existing dependencies exist while using pybuilder-pipenv")
    lock_file = project.expand_path("Pipfile.lock")
    logger.debug("Found Pipfile.lock at {}".format(lock_file))
    assert os.path.isfile(lock_file), "Pipfile.lock not found, did you run pipenv lock?"
    with open(lock_file) as json_file:
        locks = json.load(json_file)
        assert locks['_meta']['pipfile-spec'] == 6, "pybuilder-pipenv is only tested with pipfile-spec v6"
        defaults = locks['default']
        for package, info in defaults.items():
            project.depends_on(package, info['version'])
