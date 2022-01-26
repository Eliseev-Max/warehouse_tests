import logging
import os
import os.path as op
import pytest
from SSH_Connect import SSHConnect, ArisChannel


LOGFILE_NAME = os.getcwd() + op.normpath("/logs/warehouse.log")

if not op.exists("logs"):
    os.mkdir("logs")
else:
    if not op.exists("logs/warehouse.log"):
        with open(LOGFILE_NAME, "w+", encoding="utf-8") as f:
            f.write("")

logging.basicConfig(level=logging.INFO,
                    filename="logs/warehouse.log",
                    format='%(asctime)s %(levelname)s::%(name)s: %(message)s',
                    datefmt='%I:%M:%S')


def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="10.1.32.253")
    parser.addoption("--user", action="store", default="root")
    parser.addoption("--passwd", action="store", default="fhbc'rcg")
    parser.addoption("--channel", action="store", default="LOC.Control.Alarm")


# scope="function" - вызов функции ssh_connection() (установление SSH-соединения, закрытие соединения) для каждого теста
# scope="module" - вызов функции ssh_connection() для всего модуля (один раз)
@pytest.fixture(scope="module")
def ssh_connection(request):
    host = request.config.getoption("--host")
    username = request.config.getoption("--user")
    password = request.config.getoption("--passwd")
    logger = logging.getLogger("SSHLogger")
    test_name = request.node.name

    logger.info("Test module \"{}\" is running".format(test_name))

    ssh = SSHConnect(host)
    logger.info("SSH connection established")
    ssh.connect_to_server(username, password)

    def final():
        logger.info("SSH connection is closed.\nTest module \"{}\" completed\n".format(test_name))
        ssh.close()

    request.addfinalizer(final)
    return ssh


@pytest.fixture
def channel_indicator(request):
    channel = request.config.getoption("--channel")
    return ArisChannel(channel)


@pytest.fixture
def channel(request):
    return request.config.getoption("--channel")
