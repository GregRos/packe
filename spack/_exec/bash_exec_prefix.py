import os
from pathlib import Path
from shutil import which
from subprocess import STDOUT, Popen
from typing import Protocol

from termcolor import colored
from spack._root import package_root


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

    def _build_env(self, prefix: str, path: Path):
        env_exec_dir = str(package_root / "pyrun" / "bash-exec")
        env_before = str(self.before if self.before else "")
        env_prefix = colored(f"[{prefix}] ", "cyan")
        env_target = str(path.absolute())
        env = {
            "PYRUN_EXEC_DIR": env_exec_dir,
            "PYRUN_BEFORE": env_before,
            "PYRUN_PREFIX": env_prefix,
            "PYRUN_TARGET": env_target,
            "SPACK_EXEC_DIR": env_exec_dir,
            "SPACK_BEFORE": env_before,
            "SPACK_PREFIX": env_prefix,
            "SPACK_TARGET": env_target,
            **os.environ,
        }
        return env

    def try_exec(
        self,
        path: Path,
        cwd: Path,
        prefix: str,
    ):
        exec_dir = package_root / "spack" / "bash-exec"
        exec_target = str(exec_dir / "exec.bash")
        bash_path = which("bash")
        if not bash_path:
            raise Exception("Failed to find bash")
        env = self._build_env(prefix, path)

        p = Popen(
            [bash_path, f"-c", f". {exec_target}", str(path)],
            shell=False,
            encoding="utf-8",
            env=env,
            cwd=cwd,
        )

        p.wait()
        return p

    def must_exec(
        self,
        path: Path,
        cwd: Path,
        prefix: str,
    ):
        p = self.try_exec(path, cwd, prefix)
        if p.returncode > 0:
            redline = colored(
                f"         ↑ FAILED AT {prefix} ↑         ",
                on_color="on_red",
                color="black",
            )
            print(redline, "\n")
            exit(1)
