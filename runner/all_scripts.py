from pathlib import Path
from runner import root
from runner.scripts.pack import Pack
from runner.root import package_root

root = Pack.root()
root.add(
    Pack.from_indexed_dir(root, package_root / "svc.d", "svc"),
    Pack.from_indexed_dir(root, package_root / "sys.d", "sys"),
)
