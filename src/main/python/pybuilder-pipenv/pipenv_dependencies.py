import json
import os

from pybuilder.core import Project, Logger


class PipenvDependencies:

    def __init__(self, project: Project, logger: Logger):
        self.log = logger
        self.project = project

    def populate_project(self):
        self.log.debug("Initializing pybuilder-pipenv")
        self._check_existing_dependencies()
        lock_file = self._get_lock_file()
        self.lockfile_to_project(lock_file)

    def lockfile_to_project(self, lock_file):
        with open(lock_file) as json_file:
            locks = json.load(json_file)
            assert locks['_meta']['pipfile-spec'] == 6, "pybuilder-pipenv is only tested with pipfile-spec v6"
            self._source_to_index_url(locks['_meta']['sources'])
            defaults = locks['default']
            for package, info in defaults.items():
                self._package_to_dependency(info, package)

    def _package_to_dependency(self, info: dict, package: str):
        self.project.depends_on(package, info['version'])

    def _source_to_index_url(self, sources: list):
        non_standard_urls = list(
            (source['url'] for source in sources if 'https://pypi.org/simple' not in source['url'].strip()))
        if len(non_standard_urls) >= 1:
            self.project.set_property("install_dependencies_extra_index_url", non_standard_urls[0])
        elif len(non_standard_urls) == 2:
            self.project.set_property("install_dependencies_index_url", non_standard_urls[1])
        elif len(non_standard_urls) > 2:
            self.log.warn("Found more than 2 extra sources in Pipfile.lock, which is not supported in pybuilder")

    def _get_lock_file(self):
        lock_file = self.project.expand_path("Pipfile.lock")
        assert os.path.isfile(lock_file), "Pipfile.lock not found at {}, did you run pipenv lock?".format(lock_file)
        self.log.debug("Found Pipfile.lock at {}".format(lock_file))
        return lock_file

    def _check_existing_dependencies(self):
        assert len(self.project.dependencies) == 0, self.log.error(
            "Existing dependencies exist while using pybuilder-pipenv")
