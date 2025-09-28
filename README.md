# spack

A bash script runner using indexed scripts and folders and multiple configuration options. Written in Python.
## Usage
This will run scripts `1` and `2` in the root called `folder`, using the given config file. A config file can be specified using:

- The `-C` option which should appear before any command.
- The `SPACK_CONFIG` env var.

Examples:
```bash
spack -C example/config.yaml run root/1

export SPACK_CONFIG=example/config.yaml
spack run root/1
```

In the following examples, **we’ll assume SPACK_CONFIG is set accordingly.**
### Run
You run scripts using one or more *script selectors*, strings that determines which scripts to run. Each script selector is a glob-like path. Each path segment can be:

- A number, which matches the index
- A name, which matches the `*.NAME` 
- A filename

Several of these sub selectors can be combined using the `,` and `-` chars.

- `a,b` means run scripts `a` and `b`
- `1-9` means run scripts `1` through `9`.

Note that these sub selectors don’t expand across path segments.

For example, the following will run packs 1 to 5, and in each of those scripts 5 and 9:

```bash
spack run folder/1-5/5,9
```

You can use the `%` symbol as a wildcard like `*`. This lets you run *all the scripts in a folder*. This lets you do things like run script `4` inside every pack:

```bash
spack run folder/%/4
```

Note that using `%` will actually match all scripts and packs, including underscored ones.

You can also run multiple selectors:
```bash
spack run folder/1 folder/5
```
### List
Works like `run` but lists the names of scripts and packs that would be run by a list of selectors. This doesn’t run prerun scripts.

```bash
spack list folder/%/4
```

### Print
This prints scripts contents. All the matched scripts will be printed. For example, this will print script `2` in pack `1`:

```bash
spack print folder/1/2
```

## Script files
Spack runs *indexed script files* using `bash`. These files should end with `.bash` or `.sh`. Files should follow the standard `conf.d` Linux convention:

```
01-setup.bash
02-install.bash
```

Alternatively, they can also use periods:

```
01.setup.bash
02.install.bash
```

### Unnumbered files
Spack can run unnumbered scripts. These can’t be executed using ranges. They are either executed by name or using the `%` wildcard which matches them too.

Unnumbered command scripts should use `_` instead of a number:

```bash
_.do-stuff.bash
_-blah.bash
```

Other `bash` or `sh` files aren’t considered executable by Spack.
### Extra commands
Inside a script file, you have a few extra commands that are sourced into the script.
#### Echo Color
```bash
echo.red "This text will be red"
echo.green "This text will be green"
echo.yellow "This text will be yellow"
echo.white "This text will be white"
echo.blue "This text will be blue"
```

#### Echo Level, Section
These all echo to stdout but format the output based on the log level.
```bash
echo.info "Informational"
echo.warn "Warning"
echo.error "Error"
echo.section "Section named across several rows"
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

When a script pack is executed, all its *numbered* contents are executed recursively in lexicographic order. This doesn’t include `_` scripts or packs.

A pack can include other packs and scripts. They share the same ordering.

```bash
root/
	1.first/
		1.setup.bash
		2.install/
			1.packages.bash
```

### Unnumbered packs
Packs can be unnumbered like scripts. Unnumbered packs can only be executed explicitly by name. Unnumbered packs can contain numbered scripts.

```bash
root/
	_.unnumbered/
		1.install.bash
		2.setup.bash
```

### Prerun
Prerun script files are special files in a pack folder that determine whether to run the folder in the current environment. They can be used as failsafes.

A prerun script must be called `pre.spack.*`. Each pack can have one of these files, but a script can be affected by multiple preruns in nested folders. 

If any prerun script exits with a non-zero exit code no scripts belonging to its pack will be executed.

Here is an example of a pack structure using prerun files:

```bash
root/
	1.maybe/
		1.possibly/
			1.could-be.bash
			spack.pre.bash
		spack.pre.bash
		
```

The `1.could-be.bash` file can’t be executed unless both of the prerun files here are executed.

Prerun files can also be placed inside a root.
## Config
Spack uses a config file to tell which scripts to execute. Here is an example of a config file:

```yaml
before: ./before.bash
entrypoints:
  one:
    path: ./one
  two:
    path: ./two
  prerun-fail:
    path: ./prerun-fail
  prerun-succeed:
    path: ./prerun-pass
```

Each of the entrypoint paths is a *root* which works like a pack but doesn’t need to be indexed. The name of the root is the first path segment you give the `run` command. Using `%` here will run all the roots.

```bash
spack run one/1
spack run prerun-succeed/%
spack run %/1
```

The `before` script file is optional. If present, it will be sourced before each script execution. 

