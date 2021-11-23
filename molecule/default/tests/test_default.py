import os
import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_run_backup(host):
    host.run("systemctl start restic-backup")


def test_backup_exists(host):
    resp = host.run(". /opt/restic/restic-config-source-local; /usr/local/bin/restic snapshots --latest 1 --tag files --json").stdout
    snapshots = json.loads(resp)
    assert snapshots[0]["paths"] == ["/usr", "/var/lib"]


def test_backup_norepo(host):
    resp = host.run(". /opt/restic/restic-config-source-local; /usr/local/bin/restic snapshots --latest 1 --tag nonexisting --json").stdout
    snapshots = json.loads(resp)
    assert len(snapshots) == 0


def test_backup_content(host):
    resp = host.run(". /opt/restic/restic-config-source-local; /usr/local/bin/restic dump -q latest echo.out").stdout
    assert "testing\n" == resp
