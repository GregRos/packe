# spack

Spack is a script runner for executing configuration scripts in bulk. Supports flexible script selection and hierachical structure.

## Features

- Execute indexed bash scripts in order.
- Script output prefixed with identifier.
- Organize scripts into indexed packs (folders).
- Use prerun scripts to conditionally run packs.
- Use a config file to define script roots.
- Flexible script selection using run selectors with ranges and wildcards.
- Extra bash commands for colored output in scripts.

## Script

A spack script is a bash file that is executed by spack. Spack script files must end with `.bash` or `.sh`. They also need to be indexed, kind of like `conf.d` files.

You can index scripts using `-` or `.` as separators. Scripts are normally indexed using numbers, but you can also use underscores. Underscored scripts can only be executed explicitly by name.

Here are some examples of valid script filenames:

```
01-setup.bash
02.install.bash
_.do-stuff.bash
_-do-more-stuff.sh
```

Files that aren't indexed using numbers or underscores aren't considered executable by spack.

### Script pack

A _script pack_ is an indexed folder that contains more indexed scripts or packs. Script packs are indexed using numbers or underscores, just like scripts.

Here is an example folder structure with several script packs:

```
root/
    1.first/
        001.setup.bash
        002.install.bash
    2.second/
        01.setup.bash
        02.install.bash
```

When a script pack is executed, all its _numbered_ contents are executed recursively in lexicographic order. This doesn’t include `_` scripts or packs.

Packs let you organize scripts into groups. For example, you can have a pack for setting up a database, and another for setting up a web server.

Folders that aren't indexed using numbers or underscores aren't considered executable by spack.

### Root

A _root_ is a special script pack that is defined in the config file. A root can contain other packs or scripts. It doesn't have any naming requirements.

### Run selector

A _run selector_ is a glob-like path that determines which scripts to run. It can include ranges and wildcards.

Run selectors are made of path segments separated by `/`. Each segment can be one or more references to a script or pack. There are several ways to reference scripts or packs.

Here are some examples of valid run selectors:

```
one/hello/1-5
folder/%/3
root/1,3,5
root/web,db/4-5/install
```

Run selectors match all scripts and packs that fit the criteria.

#### Numbers

Numbers match index of the script or pack. For example, `1` matches:

```
01-setup.bash
1-folder/
```

Numbers can still match multiple files.

#### Ranges

You can also use ranges. For example, `1-3` would match:

```
01-setup.bash
02-install.bash
03-configure.bash
```

#### Names

Names match the unindexed name part of the script or pack. For example, `run/setup` would match:

```
01-setup.bash
02-setup.bash
1-setup/
```

Names are the only way to match unnumbered scripts and packs. However, unnumbered packs can still contain numbered scripts that can be matched using numbers or ranges.

#### Commas

Commas let you combine multiple references. For example, `1,3,go` would match:

```
01-setup.bash
03-install.bash
1-go/
```

#### Wildcards

The `%` symbol acts as a wildcard that matches all _numbered_ scripts and packs in a folder. For example, `folder/%/3` would match:

```
root/1-first/03-configure.bash
root/2-second/03-configure.bash
```

## Config file

Spack uses a YAML file to define script roots. The config file is a YAML file.

Here is an example of a config file:

```yaml
before: ./before.bash
entrypoints:
  one:
    path: ./one
  two:
    path: ./two
```

You can pass the config file to spack using the `-C`/`--config` option or by setting the `SPACK_CONFIG` environment variable.

## Usage

First you need to give spack a config file. You can do this in two ways:

- The `-C`/`--config` option which should appear before any command.
- The `SPACK_CONFIG` env var.

Examples:

```bash
spack -C example/config.yaml run root/1

export SPACK_CONFIG=example/config.yaml
spack run root/1
```

In the following examples, **we’ll assume SPACK_CONFIG is set accordingly.**

### Run

This lets you run script based on run selectors. You can use more than one run selector, separated by spaces.

Scripts will be executed in the order specified and lexicographic order within each selector.

```bash
spack run SELECTOR1 [SELECTOR2 SELECTOR2 ...]
spack run folder/1-5,extra/5,9,db root/2/stuff
```

### List

Works like `run` but lists the names of scripts and packs that would be run by a list of selectors. This doesn’t run prerun scripts.

```bash
spack list SELECTOR1 [SELECTOR2 SELECTOR2 ...]
spack list folder/%/4
```

### Print

This pretty prints scripts contents with syntax highlighting. All the matched scripts will be printed. For example, this will print script `2` in pack `1`:

```bash
spack print SELECTOR1 [SELECTOR2 SELECTOR3 ...]
spack print folder/1/2
```

## Extra features

Spack scripts have some extra features that make them easier to use.

### Prerun scripts

A prerun script is a special script that determines whether to execute a given pack. They're used as a failsafe to make sure sensitive configuration scripts are only executed when certain conditions are met.

Prerun scripts must be named `spack.pre.bash` or `spack.pre.sh`.

When you execute a `run` command, spack will go down the pack tree and execute every prerun script it finds. If a prerun script exits with a non-zero status, the entire pack is skipped.

These prerun scripts will always be executed, no matter how you match the scripts.

For example, let's say you have:

```
root/
  spack.pre.bash
  1.first/
    spack.pre.bash
    001.setup.bash
    002.install.bash
  2.second/
    01.setup.bash
    02.install.bash
```

And you run the selector `root/1/setup`. Spack will execute the prerun files in the following order:

```
root/spack.pre.bash
root/1.first/spack.pre.bash
```

The script won't be executed if either of those files exits with a non-zero status.

Note that each prerun is executed only once per `run` command, even if multiple scripts in the pack are matched explicitly or you use multiple selectors.

### Echo with colors

Spack scripts can use special echo commands to print colored text to the terminal. These commands are:

```bash
echo.red "This text will be red"
echo.green "This text will be green"
echo.yellow "This text will be yellow"
echo.white "This text will be white"
echo.blue "This text will be blue"
```

### Echo with levels

Spack scripts can also use special echo commands to print text with different levels of importance. These commands are:

```bash
echo.info "Informational"
echo.warn "Warning"
echo.error "Error"
echo.section "Clearly visible section across several rows"
```

All of these commands print to standard output, but they format the output based on the log level.
