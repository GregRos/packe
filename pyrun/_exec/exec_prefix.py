import os
from pathlib import Path
from shutil import which
from subprocess import STDOUT, Popen
from typing import Protocol

from termcolor import colored
from pyrun._root import package_root


class ExecInfo(Protocol):
    path: Path
    cwd: Path


class PrefixExecFailed(Exception, ExecInfo):
    path: Path
    cwd: Path

    def __init__(self, path: Path, cwd: Path):
        rel_path = path.relative_to(cwd)
        super().__init__(f"Failed to execute {rel_path} in {cwd}")
        self.cwd = cwd
        self.path = path


class PrefixExecutor:
    def __init__(self, path: Path, cwd: Path, prefix: str, prolog: Path | None = None):
        self.path = path
        self.prefix = prefix
        self.cwd = cwd
        self.prolog = prolog

    def exec(self):
        exec_dir = package_root / "bash-exec"
        exec_target = str(exec_dir / "exec.bash")
        bash_path = which("bash")
        if not bash_path:
            raise Exception("Failed to find bash")
        p = Popen(
            [bash_path, f"-c", f". {exec_target}", str(self.path)],
            shell=False,
            encoding="utf-8",
            env={
                "PYRUN_EXEC_DIR": str(exec_dir),
                "PYRUN_PROLOG": str(self.prolog if self.prolog else ""),
                "PYRUN_PREFIX": colored(f"[{self.prefix}] ", "cyan"),
                "PYRUN_TARGET": str(self.path.absolute()),
            },
            cwd=self.cwd,
        )

        p.wait()
        if p.returncode > 0:
            redline = colored(
                f"      ↑ FAILED AT {self.prefix} ↑      ",
                on_color="on_red",
                color="black",
            )
            print(redline, "\n")
            exit(1)
