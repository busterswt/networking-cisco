try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
import os
import subprocess
from quantum import version


def run_git_command(cmd):
    output = subprocess.Popen(["/bin/sh", "-c", cmd],
                              stdout=subprocess.PIPE)
    return output.communicate()[0].strip()


if os.path.isdir('.git'):
    branch_nick_cmd = 'git branch | grep -Ei "\* (.*)" | cut -f2 -d" "'
    branch_nick = run_git_command(branch_nick_cmd)
    revid_cmd = "git --no-pager log --max-count=1 | cut -f2 -d' ' | head -1"
    revid = run_git_command(revid_cmd)
    revno_cmd = "git --no-pager log --oneline | wc -l"
    revno = run_git_command(revno_cmd)
    with open("quantum/vcsversion.py", 'w') as version_file:
        version_file.write("""
# This file is automatically generated by setup.py, So don't edit it. :)
version_info = {
    'branch_nick': '%s',
    'revision_id': '%s',
    'revno': %s
}
""" % (branch_nick, revid, revno))

Name = 'quantum'
Url = "https://launchpad.net/quantum"
Version = version.canonical_version_string()
License = 'Apache License 2.0'
Author = 'Netstack'
AuthorEmail = 'netstack@lists.launchpad.net'
Maintainer = ''
Summary = 'Quantum (virtual network service)'
ShortDescription = Summary
Description = Summary

requires = [
    'Paste',
    'PasteDeploy',
    'Routes>=1.12.3',
    'eventlet>=0.9.12',
    'lxml==2.3',
    'pep8>=0.6.1',
    'python-gflags',
    'simplejson',
    'sqlalchemy',
    'webob',
    'webtest'
]

EagerResources = [
    'quantum',
]

ProjectScripts = [
]

config_path = 'etc/quantum/'
init_path = 'etc/init.d'
ovs_plugin_config_path = 'etc/quantum/plugins/openvswitch'
cisco_plugin_config_path = 'etc/quantum/plugins/cisco'

DataFiles = [
    (config_path,
        ['etc/quantum.conf', 'etc/quantum.conf.test', 'etc/plugins.ini']),
    (init_path, ['etc/init.d/quantum-server']),
    (ovs_plugin_config_path,
        ['etc/quantum/plugins/openvswitch/ovs_quantum_plugin.ini']),
    (cisco_plugin_config_path,
        ['etc/quantum/plugins/cisco/credentials.ini',
         'etc/quantum/plugins/cisco/l2network_plugin.ini',
         'etc/quantum/plugins/cisco/nexus.ini',
         'etc/quantum/plugins/cisco/ucs.ini',
         'etc/quantum/plugins/cisco/cisco_plugins.ini',
         'etc/quantum/plugins/cisco/db_conn.ini']),
]

setup(
    name=Name,
    version=Version,
    url=Url,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    license=License,
    scripts=ProjectScripts,
    install_requires=requires,
    include_package_data=False,
    packages=find_packages('.'),
    data_files=DataFiles,
    eager_resources=EagerResources,
    entry_points={
        'console_scripts': [
            'quantum-server = quantum.server:main',
        ]
    },
)