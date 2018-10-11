dnf txgraph
===========

A [dnf](https://github.com/rpm-software-management/dnf) plugin to output a Graphviz formatted digraph
displaying the dependencies for a given set of packages.

Usage
-----

dnf [dnf options] txgraph [-t TEMPLATE_FILE] [-o OUTPUT_FILE] [PACKAGE ...]

The list of packages to include in the transaction can be specified either as
a list on the command line, or via a Mako template file such as the ones used
by [lorax](https://github.com/weldr/lorax).

If the output file is not specified, the graph file will be printed to standard out.
Note that dnf will print a "Last metadata expiration check" line to standard out by
default. This can be suppressed by adding `-q` to the command line, but this option
will also suppress any error output.

Install
-------
Install txgraph.py to your system's dnf pluginpath. By default the pluginpath is
/usr/lib/python<version>/site-packages/dnf-plugins. The plugin can be installed
by running:

```
python3 setup.py install --prefix /usr
```

The plugin can also be installed from copr:

```
dnf copr enable dshea/dnf-plugin-txgraph
dnf install python3-dnf-plugin-txgraph
```

To run the plugin locally, you will need to override dnf's pluginpath setting.

```
dnf --setopt=pluginpath=$PWD/src/dnf-plugins txgraph ...
```

Examples
--------

dnf txgraph -o deps.dot grep

dnf -q --disablerepo=\* --enablerepo=rawhide txgraph -t runtime-install.tmpl | dot -Tsvg > lorax.svg

Known issues
------------

The graph file does not include any attributes, so it might not be as pretty or as easy to render as it could.
Patches welcome.
