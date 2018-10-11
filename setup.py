from distutils.core import setup

setup(name="dnf-plugin-txgraph",
      version="1.0.0",
      description="DNF plugin to create a dependency graph of a transaction",
      author="David Shea",
      author_email="dshea@redhat.com",
      url="https://github.com/dashea/dnf-plugin-txgraph",
      py_modules=["dnf-plugins/txgraph"],
      package_dir={"": "src"}
      )
