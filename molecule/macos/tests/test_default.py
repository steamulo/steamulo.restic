import os
import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_run_backup(host):
    host.run("/opt/restic/restic-backup-crontab.sh")


def test_backup_exists(host):
    resp = host.run("source /opt/restic/restic-config-source-local; /usr/local/bin/restic snapshots --tag files --json latest").stdout
    snapshots = json.loads(resp)
    assert snapshots[0]["paths"] == ["/usr", "/var/log"]


def test_files_in_backup(host):
    resp = host.run("source /opt/restic/restic-config-source-local; /usr/local/bin/restic ls latest --tag files -q").stdout
    assert '/var/log/dm/' in resp
    assert '/var/log/asl/' not in resp


def test_backup_norepo(host):
    resp = host.run("source /opt/restic/restic-config-source-local; /usr/local/bin/restic snapshots --tag nonexisting --json latest").stdout
    snapshots = json.loads(resp)
    assert len(snapshots) == 0


def test_backup_content(host):
    resp = host.run("source /opt/restic/restic-config-source-local; /usr/local/bin/restic dump -q latest echo.out").stdout
    assert "testing\n" == resp


def test_unused_repo(host):
    assert not host.file("/opt/restic/restic-backup-notused.sh").exists
    assert not host.file("/opt/restic/restic-config-source-notused").exists
    assert not host.file("/opt/restic/restic-password-notused").exists


def test_used_repo(host):
    assert host.file("/opt/restic/restic-backup-local.sh").exists
    assert host.file("/opt/restic/restic-config-source-local").exists
    assert host.file("/opt/restic/restic-password-local").exists
