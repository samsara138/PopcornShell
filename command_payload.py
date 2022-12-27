import pickle

def parse_payload_to_output(raw_payload):
    payload = CommandPayload()
    payload.parse_packet(raw_payload)
    return payload


class CommandPayload:
    command = []
    stdout = ""
    stderr = ""
    file = None
    file_name = ""

    def __init__(self, stdout="", stderr="", command=[], file=None, file_name=""):
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
        self.file = file
        self.file_name = file_name

    # Compile data to a low profile packet
    def pack(self):
        packet = [self.command, self.stdout, self.stderr, self.file, self.file_name]
        packet = pickle.dumps(packet)
        return packet

    # parse packet to data
    def parse_packet(self, packet):
        data = pickle.loads(packet)
        self.command, self.stdout, self.stderr, self.file, self.file_name = data

    # Format payload to string output
    def formatted_output(self, output_style):
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

    def __str__(self):
        result = ""
        result += "command -> " + str(self.command) + '\n'
        result += "stdout -> " + str(self.stdout) + '\n'
        result += "stderr -> " + str(self.stderr) + '\n'

        if self.file is not None:
            result += "file -> "
            for byte in self.file:
                result += f"{byte} "
            result += "\n\n"
            result += "file name -> " + str(self.file_name) + '\n'
        return result
