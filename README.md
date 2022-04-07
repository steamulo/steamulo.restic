![Build Status](https://github.com/STEAMULO/steamulo.restic/actions/workflows/test.yml/badge.svg?branch=master)

Steamulo Restic
=========

Production grade installation and deployment of restic

Role Variables
------------

Here are the main variables that should be set :

```yaml
restic_repositories: {}
  example:
    location: /backup
    password: password
    check: true
    check_args: "--read-data-subset=10%"
    forget: true
    forget_args: "--prune --group-by paths,tags --keep-within-daily 14d --keep-within-weekly 4m --keep-within-monthly 1y"
    environment_variables: {}

restic_folders: []
  - paths: []
    excludes: []
    repositories: []
    tags: ""
    pre_backup_cmd: ""
    post_backup_cmd: ""

restic_stdouts: []
  - cmd: ""
    temp_files:
      - filename: ""
        content: ""
    filename: ""
    repositories: []
    tags: ""
```

Example Playbook
------------

Example can be found under the [molecule folder](molecule/default/converge.yml)


Development
------------

This role use the [molecule framework](https://molecule.readthedocs.io/en/stable/) in order to simplify the development process.

Requirements:
* [Python 3](https://www.python.org/download)
* [Docker](https://docs.docker.com/get-docker/)

Setup your local environnement with python virtualenv prior to using molecule : `. venv.sh`

This command will create a virtual env, activate it and download python dependencies.

Use ```molecule converge``` to create a local environnement and ```molecule login``` to log into the test machine.

Before any commit ensure that every test are passing with ```molecule test```

License
------------

BSD

Author Information
------------

Steamulo - www.steamulo.com

Sources and Inspirations
------------
- https://blog.cubieserver.de/2021/restic-backups-with-systemd-and-prometheus-exporter/
- https://github.com/arillso/ansible.restic
- https://github.com/angristan/ansible-restic
