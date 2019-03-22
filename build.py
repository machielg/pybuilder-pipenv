from pybuilder.core import use_plugin, init, Project, Author

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.distutils")
use_plugin('python.integrationtest')
use_plugin("copy_resources")

name = "pybuilder-pipenv"
default_task = ["clean", "analyze", "publish"]
summary = "PyBuilder plugin using pipenv for dependency specification"
authors = [Author("Machiel Keizer-Groeneveld", "machielg@gmail.com")]

version = "1.0.0.dev"

license = 'Apache'
url = 'https://github.com/ImmobilienScout24/pybuilder_aws_plugin'


@init
def set_properties(project: Project):
    project.depends_on("pybuilder")

    project.set_property('flake8_break_build', True)
    project.set_property('flake8_include_test_sources', True)
    project.set_property('flake8_include_scripts', True)
    project.set_property('flake8_max_line_length', 130)

    project.set_property("copy_resources_target", "$dir_dist/pybuilder-pipenv")
    project.get_property("copy_resources_glob").append("LICENSE*")
    project.include_file("pybuilder-pipenv", "LICENSE.txt")

    project.set_property("distutils_classifiers", [
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing'])
