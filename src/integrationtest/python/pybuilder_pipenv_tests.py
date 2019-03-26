import os
import unittest

import re
from pybuilder.core import Project, Dependency

from pipenv_pybuilder_support import PipenvPybuilderTests


class SetupPyOutputTest(PipenvPybuilderTests):

    def test_conversion_to_setup_py(self):
        p = self._build(self.two_deps_and_one_dev).project  # type: Project

        deps = [
            Dependency('humanize', '==0.5.1'),
            Dependency('tomlkit', '==0.5.2')]
        self.assertListEqual(deps, p.dependencies)
        setup_py = "target/dist/sample-1.0.dev0/setup.py"

        self.assert_file_exists(setup_py)
        with open(self.full_path(setup_py)) as f:
            content = f.read()
            assert "tailer" not in content  # no develop dependencies

            setup_file = re.sub(' +', ' ', content.replace(os.linesep, ""))
            assert "install_requires = [ 'humanize==0.5.1', 'tomlkit==0.5.2' ]" in setup_file


if __name__ == "__main__":
    unittest.main()
