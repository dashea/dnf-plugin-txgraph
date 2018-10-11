Name:           dnf-plugin-txgraph
Version:        1.0.0
Release:        1%{?dist}
Summary:        A DNF plugin to output a dependency graph from a package transaction.

License:        GPLv2+
URL:            https://github.com/dashea/dnf-plugin-txgraph
Source0:        https://github.com/dashea/dnf-plugin-txgraph/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
A dnf plugin to output a Graphviz formatted digraph displaying the dependencies
for a given set of packages.

%package -n python3-%{name}
Summary:        A DNF plugin to output a dependency graph from a package transaction.
%{?python_provide:%python_provide python3-%{name}}

BuildRequires:  python3-devel

Requires:       python3-dnf
Requires:       python3-hawkey

%description -n python3-%{name}
A dnf plugin to output a Graphviz formatted digraph displaying the dependencies
for a given set of packages.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%files -n python3-%{name}
%license COPYING
%doc README.md
%{python3_sitelib}/dnf-plugins/txgraph.py
%{python3_sitelib}/dnf-plugins/__pycache__/txgraph.*
%{python3_sitelib}/dnf_plugin_txgraph-%{version}-*.egg-info

%changelog
* Thu Oct 11 2018 David Shea <dshea@redhat.com> - 1.0.0-1
- Initial package
