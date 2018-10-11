# txgraph: DNF plugin to output a dependency graph from a package transaction.
# 
# Copyright (C) 2018 David Shea <dshea@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import dnf      # type: ignore

import hawkey   # type: ignore
import typing

def _mako_installpkg(pkg_file):
    """ Read a Mako template file and return a list of all the packages
        listed in the installpkg lines.
    """
    packages = []
    with open(pkg_file, "r") as f:
        for line in f.readlines():
            if line.startswith("installpkg"):
                packages += line.split()[1:]

    return packages

@dnf.plugin.register_command
class TxGraphCommand(dnf.cli.Command):
    aliases = ("txgraph",)
    summary = "Output the package dependcies for an install transaction in dot format"

    @staticmethod
    def set_argparser(parser):
        parser.add_argument("-t", "--template", dest="pkg_file", help="Read packages from a Mako template file")
        parser.add_argument("-o", "--output", help="Output file path (defaults to stdout)")
        parser.add_argument("packages", help="Packages to install", metavar="STRING", nargs="*", default=[])

    def configure(self):
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True
        demands.load_system_repo = False

    def run(self):
        packages = self.opts.packages
        if self.opts.pkg_file:
            packages += _mako_installpkg(self.opts.pkg_file)

        if len(packages) == 0:
            raise dnf.cli.CliError("Pass packages on cmdline or via Mako template using -t") # Add the packages to the transaction
        for pkg in packages:
            self.base.install(pkg)

        # Resolve dependencies
        self.base.resolve()

        # Spit out a graphviz file...
        output_file = sys.stdout
        try:
            if self.opts.output:
                output_file = open(self.opts.output, "w")

            solved = set()
            print("digraph {", file=output_file)
            for pkgname in packages:
                # Find the package object(s) to be installed corresponding to the package string
                pkg_objs = list(self._find_pkg_by_name(pkgname))

                if not pkg_objs:
                    raise dnf.cli.CliError("Unable to find package in transaction for %s" % pkgname)

                for pkg_obj in pkg_objs:
                    self._print_deps(pkg_obj, solved, output_file)
            print("}", file=output_file)
        finally:
            if self.opts.output:
                output_file.close()

    def _find_pkg_by_name(self, pkgname : str) -> typing.Iterator[hawkey.Package]:
        # If there is a '*' in the package name, do a glob query against names,
        # otherwise query the provides
        if '*' in pkgname:
            return self._tx_query(name__glob=pkgname)
        else:
            return self._tx_query(provides=pkgname)

    def _print_deps(self, pkg: hawkey.Package, solved: typing.MutableSet[hawkey.Package], output_file: typing.TextIO):
        # if we've already done this package, skip it so we don't get stuck in
        # a dependency cycle
        if pkg in solved:
            return

        solved.add(pkg)

        # For each of this package's requirements, find the package in the transaction
        # that provides the requirement
        for provider in self._tx_query(provides=pkg.requires):
            print("  \"%s\" -> \"%s\"" % (pkg.name, provider.name), file=output_file)
            self._print_deps(provider, solved, output_file)

    def _tx_query(self, **kwargs) -> typing.Iterator[hawkey.Package]:
        """Query packages in the transaction instead of against the whole sack"""
        return (p for p in self.base.sack.query().filter(**kwargs) if p in self.base.transaction.install_set)
