from pybuilder.core import Project, Logger, init

from .pipenv_dependencies import PipenvDependencies


@init
def pipenv_deps(project: Project, logger: Logger):
    PipenvDependencies(project, logger).populate_project()
