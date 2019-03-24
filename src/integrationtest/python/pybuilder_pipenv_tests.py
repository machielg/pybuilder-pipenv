import os
import re
import unittest

from integrationtest_support import IntegrationTestSupport

LOCK_FILE = """
{
    "_meta": {
        "hash": {
            "sha256": "dcfe3cf0f6a7e748cbc1ba39e6b5aba8d1d464a18624cdab7b8f637949d4e75e"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.6"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            },
            {
                "name": "local",
                "url": "http://local.pypi/simple",
                "verify_ssl": true
            }            
        ]
    },
    "default": {
        "humanize": {
            "hashes": [
                "sha256:a43f57115831ac7c70de098e6ac46ac13be00d69abbf60bdcac251344785bb19"
            ],
            "index": "pypi",
            "version": "==0.5.1"
        },
        "tomlkit": {
            "hashes": [
                "sha256:d6506342615d051bc961f70bfcfa3d29b6616cc08a3ddfd4bc24196f16fd4ec2",
                "sha256:f077456d35303e7908cc233b340f71e0bec96f63429997f38ca9272b7d64029e"
            ],
            "index": "pypi",
            "version": "==0.5.2"
        }
    },
    "develop": {
        "tailer": {
            "hashes": [
                "sha256:78d60f23a1b8a2d32f400b3c8c06b01142ac7841b75d8a1efcb33515877ba531"
            ],
            "version": "==0.4.1"
        }
    }
}"""

PYB_BUILD_FILE = """
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")
use_plugin("pypi:pybuilder-pipenv")
name = "sample"

default_task = 'prepare'
"""


class PybuilderPipenvTest(IntegrationTestSupport):

    def test_conversion_to_setup_py(self):
        self.write_build_file(PYB_BUILD_FILE)
        self.create_directory("src/main/python/")
        self.write_file("Pipfile.lock", LOCK_FILE)
        reactor = self.prepare_reactor()
        reactor.build('publish')

        setup_py = "target/dist/sample-1.0.dev0/setup.py"
        self.assert_file_exists(setup_py)
        with open(self.full_path(setup_py)) as f:
            content = f.read()
            assert "tailer" not in content  # no develop dependencies

            setup_file = re.sub(' +', ' ', content.replace(os.linesep, ""))
            assert "install_requires = [ 'humanize==0.5.1', 'tomlkit==0.5.2' ]" in setup_file


if __name__ == "__main__":
    unittest.main()
