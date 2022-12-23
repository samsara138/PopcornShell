class Payload:
    stdout = ""
    stderr = ""
    raw_packet = ""

    def __init__(self, stdout="", stderr="", raw_packet=""):
        self.stdout = stdout
        self.stderr = stderr
        self.raw_packet = raw_packet

    def get_packet(self):
        packet = str([self.stdout, self.stderr])
        self.raw_packet = bytes(packet, encoding="utf-8")
        return self.raw_packet

    def get_data(self):
        packet = self.raw_packet.decode('utf-8')
        packet = eval(packet)
        self.stdout, self.stderr = packet[0], packet[1]
        return self.stdout, self.stderr

    # Format payload to string output
    def format_output(self, output_style):
        self.get_data()
        if len(self.stdout) == 0 and len(self.stderr) == 0:
            return ""
        result = ""
        if output_style == "full":
            result += 'Received'.center(40, "=") + '\n'
            if len(self.stdout) != 0:
                result += ("Command stdout".center(20, "=")) + '\n'
                result += str(self.stdout) + '\n'
            if len(self.stderr) != 0:
                result += ("Command stderr".center(20, "=")) + '\n'
                result += str(self.stderr) + '\n'
        else:
            result += self.stdout + '\n' + self.stderr
        return result
