from pybuilder.core import Dependency, Project

from pipenv_pybuilder_support import PipenvPybuilderTests


class TestUsePipenvSources(PipenvPybuilderTests):

    # @unittest.skip
    def test_index_in_dependency(self):
        print(self.tmp_directory)
        lock = self.two_deps_and_one_dev
        lock['_meta']['sources'].append({
            "name": "my-pi",
            "url": "https://my-pi/simple",
            "verify_ssl": True
        })
        lock['default']['humanize']['index'] = 'my-pi'

        p = self._build(lock).project  # type: Project
        deps = [Dependency("humanize", "==0.5.1", None),
                Dependency("tomlkit", "==0.5.2", None)]
        self.assertEqual("https://my-pi/simple", p.get_property("install_dependencies_extra_index_url"))
        self.assertListEqual(deps, p.dependencies)
