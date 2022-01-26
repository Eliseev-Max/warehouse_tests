import paramiko


class SSHConnect:

    def __init__(self, host, look_for_keys=False, allow_agent=False):
        self.hostname = host
        self.auth_keys = look_for_keys
        self.allow_agent = allow_agent
        self.client = None
        self.connection = False
        self.stdin = None
        self.stdout = None
        self.stderr = None

    def connect_to_server(self, user, passwd):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.hostname,
                                username=user,
                                password=passwd,
                                look_for_keys=self.auth_keys,
                                allow_agent=self.allow_agent)
        except Exception as err:
            print(f"Warning! Connection wasn't established! {err}")
        else:
            self.connection = True

    def close(self):
        if self.connection:
            self.client.close()
        else:
            return False

    def send_command(self, command):
        self.stdin, self.stdout, self.stderr = self.client.exec_command(command)
        return self

    def get_result(self):
        result = self.stdout.read() if self.stdout else self.stderr.read()
        return result.decode()


class ArisChannel:

    def __init__(self, channel):
        self.channel = channel
        #   self.logger = logging.getLogger(type(self).__name__)

    # Quality values:
    GOOD = 192
    SUBST = 216
    BAD = 0
    NOT_INIT = 64

    # Signal quality symbols
    GOOD_QUAL_SIGN = "+"
    BAD_QUAL_SIGN = "-"
    SUBST_SIGN = "*"
    NOT_INIT_SIGN = "0040"

    def warehouse_view(self):
        return "warehouse_view {}\n".format(self.channel)

    def warehouse_set(self, value, quality=GOOD):
        return "warehouse_set -n {} -v {} -q {}\n".format(self.channel, value, quality)

    def handle_warehouse_view(self, stdout):
        if type(stdout) != str:
            return False
        for line in stdout.split("\n"):
            if line.strip() == "":
                continue
            params_list = line.split()
            if not params_list[0].isdigit():
                continue
            else:
                channel_params = dict({"ID": params_list[0],
                                            "QUAL": params_list[1],
                                            "VALUE": int(params_list[2]),
                                            "DATE": params_list[3],
                                            "TIME": params_list[4],
                                            "NAME": params_list[5]
                                            })
        return channel_params
