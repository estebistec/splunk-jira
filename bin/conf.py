# -*- coding: utf-8 -*-
"""
Provides functions for reading config about JIRA instances from the local config.ini file.

See `config.ini.sample` for an idea of how to define JIRA instances.

Each stanza that has a name beginning with `instance-`, e.g., `instance-main`, should contain the
options needed to define a JIRA instance. The options for an instance are:

* hostname
* username
* password
* jira_protocol
* jira_port
* soap_protocol
* soap_port

A special stanza named `default-instance` can provide an option `name` that names which of your
defined instances should be used as the default.

"""


import ConfigParser
import os


LOCAL_DIR = os.path.dirname(__file__)
LOCAL_INI_PATH = os.path.join(LOCAL_DIR, 'config.ini')
INSTANCE_SECTION_PREFIX = 'instance-'
INSTANCE_NAME_OFFSET = len(INSTANCE_SECTION_PREFIX)
DEFAULT_INSTANCE_SECTION = 'default-instance'


def get_local_conf():
    "Get configuration data from the local config.ini file."
    config = ConfigParser.ConfigParser()
    config.read(LOCAL_INI_PATH)
    return config


def get_jira_instances(config=None):
    """
    Get a dictionary containing all JIRA instances found in the local `config.ini` file, and the
    default instance if one was named.

    Each jira instance is keyed by its name. E.g., a config stanza named `instance-main` would
    have the name `'main'`. Additionally, if your config named a default JIRA instance, that
    instance's config is also provided as key `'default'`.

    Example of the structure returned::

        {
            'default': {
                'username': 'admin',
                'hostname': 'jira.example.com',
                'soap_port': '8080',
                'soap_protocol': 'https',
                'jira_protocol': 'https',
                'jira_port': '443',
                'password': 'changeme'
            },
            'other': {
                'username': 'admin',
                'hostname': 'jira.other.com',
                'soap_port': '8080',
                'soap_protocol': 'https',
                'jira_protocol': 'https',
                'jira_port': '443',
                'password': 'changeme'
            },
            'example': {
                'username': 'admin',
                'hostname': 'jira.example.com',
                'soap_port': '8080',
                'soap_protocol': 'https',
                'jira_protocol': 'https',
                'jira_port': '443',
                'password': 'changeme'
            }
        }

    """
    config = config or get_local_conf()
    instance_sections = [
        section for section in config.sections()
        if section.startswith(INSTANCE_SECTION_PREFIX)
    ]
    jira_instances = {
        section[INSTANCE_NAME_OFFSET:]:dict(config.items(section))
        for section in instance_sections
    }
    default_instance = (
        config.get(DEFAULT_INSTANCE_SECTION, 'name')
        if config.has_section(DEFAULT_INSTANCE_SECTION)
        and config.has_option(DEFAULT_INSTANCE_SECTION, 'name')
        else None
    )
    if default_instance:
        jira_instances['default'] = jira_instances[default_instance]

    return jira_instances


def get_jira_instance(name=None, config=None):
    """
    Get the specified JIRA instance's config, or else that of the default if no instance is named.

    An example of the returned structure::

        {
            'username': 'admin',
            'hostname': 'jira.example.com',
            'soap_port': '8080',
            'soap_protocol': 'https',
            'jira_protocol': 'https',
            'jira_port': '443',
            'password': 'changeme'
        }

    """
    jira_instances = get_jira_instances(config)
    return jira_instances[name or 'default']
