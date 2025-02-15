import os
from pathlib import Path
from subprocess import STDOUT, Popen
from typing import Protocol

from termcolor import colored
from runner.root import package_root


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

    def must_be_linux_root(self):
        if os.name != "posix":
            print("Not a linux system")
            exit(2)
        if os.getuid() != 0:
            print("You must be root to run this script")
            exit(3)

    def exec(self):
        self.must_be_linux_root()

        p = Popen(
            ["/bin/bash", str(package_root / "runner_stub.bash")],
            stdout=STDOUT,
            stderr=STDOUT,
            shell=False,
            encoding="utf-8",
            env={
                "PYRUN_PROLOG": self.prolog if self.prolog else "",
                "PYRUN_PREFIX": self.prefix,
                "PYRUN_TARGET": str(self.path),
            },
            cwd=self.cwd,
        )
        stdout = p.stdout
        if not stdout:
            raise Exception(f"Failed to open {self.path}")
        p.wait()
        if p.returncode > 0:
            redline = colored(
                f"      ↑ FAILED AT {self.prefix} ↑      ",
                on_color="on_red",
                color="black",
            )
            print(redline, "\n")
            exit(1)
