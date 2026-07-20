# Builtin Imports
from pathlib import Path
import re
import shutil

# Pip Imports
from jinja2 import Template, Environment, FileSystemLoader

# Local Imports
from project.format import *
from project.cmake import CMake
from project.language import Language

class Project(object):
    ROOT: Final[Path] = Path(__file__).resolve().parents[4]

    def __init__(self,
                 project_name: str,
                 project_language: Language,
                 project_type: str,
                 project_author: str,
                 project_namespace: str = "",
                 project_version: str = "0.1.0",
                 project_description: str = "") -> None: # raises ValueError
        self.name: str = project_name
        self.package_name: str = to_pascal_case(project_name)
        self.language: Language = project_language
        self.type: str = project_type
        self.author: str = project_author
        self.namespace: str = project_namespace
        self.version: str = project_version
        self.description: str = project_description
        self.env: Environment = Environment(
            loader=FileSystemLoader(Project.ROOT),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    @property
    def env(self) -> Environment: return self._env

    @env.setter
    def env(self, value: Environment) -> None:
        self._env = value
        self._env.filters["to_screaming_case"] = to_screaming_case
        self._env.filters["to_pascal_case"] = to_pascal_case

    def render(self, cmake_version: str) -> None:

        return

    def render_old(self, cmake: CMake) -> None:  # raises ValueError, jinja2.TemplateNotFound
        # Remove irrelevant directories based on the project type
        if self.type == "Executable":
            shutil.rmtree(Project.ROOT/"include")
            shutil.rmtree(Project.ROOT/"test_package")
        elif self.type == "Interface Library":
            shutil.rmtree(Project.ROOT/"src")

        entries: list[Path] = sorted(Project.ROOT.rglob("*"), key=lambda p: len(p.parts), reverse=True)

        for path in entries:
            if path.is_file() and path.suffix == ".j2":
                template: Template = self._env.get_template(path.relative_to(Project.ROOT).as_posix())
                path.write_text(template.render(project=self, cmake=cmake), encoding="utf-8")

        for path in entries:
            name: str = path.name.removesuffix(".j2")
            if "{{" in name:
                name = self._env.from_string(name).render(project=self, cmake=cmake)
            if name != path.name:
                path.rename(path.with_name(name))
