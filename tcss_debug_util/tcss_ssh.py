import paramiko

class ssh:
	_ip = ""
	_username = ""
	_password = ""

	def __init__(self, ip, username, password) -> None:
		self._ip = ip
		self._username = username
		self._password = password

	def exec(self, cmd):
		
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(self._ip, username=self._username, password=self._password)
		stdin, stdout, stderr = client.exec_command(cmd)
		command_exit_status = stdout.channel.recv_exit_status()
		out = stdout.read().decode('utf-8').strip("\n")
		err = stderr.read().decode('utf-8').strip("\n")
		client.close()

		return out
		# return "Port 0: USB=1 DP=1 POLARITY=INVERTED HPD_IRQ=0 HPD_LVL=1 SAFE=0 TBT=0 USB4=0"
	