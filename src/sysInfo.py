import platform
import subprocess
import GPUtil


class SystemInfo:
    def __init__(self):
        self.selected_resource = None
        self.resources_list = []

    @staticmethod
    def list_cpus():

        try:
            if platform.system() == 'Darwin':  # macOS
                result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    cpu_name = result.stdout.strip()
                else:
                    cpu_name = "Errore nel recuperare il nome della CPU"

            else:
                cpu_name = ""
                if platform.system() == 'Linux':
                    with open('/proc/cpuinfo') as f:
                        for line in f:
                            if 'model name' in line:
                                cpu_name = line.split(':')[1].strip()
                                break
                elif platform.system() == 'Windows':
                    cpu_name = subprocess.check_output(['wmic', 'cpu', 'get', 'name']).decode().split('\n')[1].strip()

            if "(R)" or "(TM)" in cpu_name:
                cpu_name = cpu_name.replace("(R)", "").replace("(TM)", "").strip()

            # Rimuove da Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz la parte CPU @ 2.60GHz
            if "CPU @" in cpu_name:
                cpu_name = cpu_name.split("CPU @")[0].strip()

            # Rimuove da 12th Gen Intel Core i5-12600K la parte prima d Intel ...
            if "Intel" in cpu_name:
                cpu_name = cpu_name.split("Gen")[1].strip()

            return [cpu_name]
        except Exception as e:
            return []

    @staticmethod
    def get_nvidia_gpu_names():
        try:
            gpus = GPUtil.getGPUs()
            gpu_names = [gpu.name.replace("NVIDIA ", "") for gpu in gpus]
            return gpu_names
        except Exception as e:
            return []

    @staticmethod
    def get_amd_gpu_names():
        try:
            if platform.system() == 'Darwin':  # macOS
                result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    raise Exception(result.stderr)

                gpu_names = []
                for line in result.stdout.split('\n'):
                    if "Chipset Model:" in line:
                        line = line.replace("Chipset Model: ", "").strip()
                        gpu_names.append(line)

                return gpu_names if gpu_names else ["Nessuna GPU AMD trovata"]
            elif platform.system() == 'Linux':
                result = subprocess.run(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    raise Exception(result.stderr)

                gpu_names = []
                for line in result.stdout.split('\n'):
                    if 'VGA' in line and 'AMD' in line:
                        gpu_names.append(line.strip())

                return gpu_names if gpu_names else ["Nessuna GPU AMD trovata"]
            else:
                return []
        except Exception as e:
            return []

    def get_all_resources(self):
        cpu_list = self.list_cpus()
        nvidia_gpus = self.get_nvidia_gpu_names()
        amd_gpus = self.get_amd_gpu_names()
        self.resources_list = cpu_list + nvidia_gpus + amd_gpus

    def display_resources(self):
        self.get_all_resources()

        print("Risorse disponibili:")
        for idx, resource in enumerate(self.resources_list):
            print(f"{idx + 1}. {resource}")

    def select_resource(self, resource_number):
        if 0 < resource_number <= len(self.resources_list):
            self.selected_resource = self.resources_list[resource_number - 1]
            print(f"Risorsa {resource_number} ({self.selected_resource}) selezionata.")
        else:
            print("Numero di risorsa non valido.")

    def select_resource_byname(self, resource_name):
        if resource_name == "":
            print("Nome della risorsa non valido.")
            return False
        resource_name_lower = resource_name.lower()
        for resource in self.resources_list:
            if resource_name_lower in resource.lower():
                self.selected_resource = resource
                print(f"Risorsa ({self.selected_resource}) selezionata.")
                return True
        return False
