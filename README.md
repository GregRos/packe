# spack

A bash script runner using indexed scripts and folders and multiple configuration options. Written in Python.

## Indexing

spack uses indexed scripts and folders to determine the order of execution. The index is a number followed by a dot (`.`) or a dash (`-`). For example:

```
001.setup.bash
002-install.bash
```

## Script pack

A script pack is a an indexed folder that contains more indexed scripts or packs:

```
root/
    1.first/
        001.setup.bash
        002.install.bash
    2.second/
        01.setup.bash
        02.install.bash
```

### Features

Each script can define a `spack`

```
setup.d/
  00.setup.sh
  10.install.sh
Runs the files in the [setup.d](../setup.d) folder in order, possibly filtered, and monitors execution.
```
