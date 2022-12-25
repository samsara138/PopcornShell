import pickle


def parse_payload_to_output(raw_payload):
    payload = CommandPayload()
    payload.parse_packet(raw_payload)
    return payload


class CommandPayload:
    command = ""
    stdout = ""
    stderr = ""

    def __init__(self, stdout="", stderr="", command=""):
        self.stdout = stdout
        self.stderr = stderr
        self.command = command

    # Compile data to a low profile packet
    def pack(self):
        packet = [self.command, self.stdout, self.stderr]
        packet = pickle.dumps(packet)
        return packet

    # parse packet to data
    def parse_packet(self, packet):
        data = pickle.loads(packet)

        self.command = data[0]
        self.stdout = data[1]
        self.stderr = data[2]
        result = {
            "command": data[0],
            "stdout": data[1],
            "stderr": data[2]
        }
        return result

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
