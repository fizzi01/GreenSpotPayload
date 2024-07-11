import subprocess


class ProgramRunner:
    def __init__(self, path):
        self.path = path
        self.process = None

    def run(self):
        self.process = subprocess.Popen(self.path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if self.process is None:
            return None, None

        stdout = self.process.stdout
        stderr = self.process.stderr

        return stdout, stderr

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None

    def get_stdout(self):
        if self.process is not None:
            return self.process.stdout.read()
        return None

    def get_stderr(self):
        if self.process is not None:
            return self.process.stderr.read()
        return None
