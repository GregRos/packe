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


class BashPrefixExecutor:
    def __init__(self, before: Path | None = None):
        self.before = before

    def exec(
        self,
        path: Path,
        cwd: Path,
        prefix: str,
    ):
        exec_dir = package_root / "pyrun" / "bash-exec"
        exec_target = str(exec_dir / "exec.bash")
        bash_path = which("bash")
        if not bash_path:
            raise Exception("Failed to find bash")
        p = Popen(
            [bash_path, f"-c", f". {exec_target}", str(path)],
            shell=False,
            encoding="utf-8",
            env={
                "PYRUN_EXEC_DIR": str(exec_dir),
                "PYRUN_BEFORE": str(self.before if self.before else ""),
                "PYRUN_PREFIX": colored(f"[{prefix}] ", "cyan"),
                "PYRUN_TARGET": str(path.absolute()),
            },
            cwd=cwd,
        )

        p.wait()
        if p.returncode > 0:
            redline = colored(
                f"         ↑ FAILED AT {prefix} ↑         ",
                on_color="on_red",
                color="black",
            )
            print(redline, "\n")
            exit(1)
