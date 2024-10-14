import subprocess
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class SevenZip:
    def __init__(self):
        self.executable = "7z"  # Assuming 7z is in the system PATH

    def compress(self, input_path, output_path, options):
        # Start with basic command
        command = [self.executable, "a", "-t" + options["format"]]
        
        # Add compression level
        command.extend(["-mx=" + self._get_compression_level(options["level"])])
        
        # Add password if provided
        if options["password"]:
            command.extend(["-p" + options["password"]])
        
        # Add output and input paths
        command.extend([output_path, input_path])
        
        return self._run_command(command)

    def extract(self, input_path, output_dir, password=None):
        command = [self.executable, "x", input_path, f"-o{output_dir}", "-y"]
        
        if password:
            if input_path.lower().endswith(('.7z', '.zip')):
                # For 7z and zip, use a separate password file
                password_file = self._create_password_file(password)
                command.extend(["-p@" + password_file])
            else:
                # For other formats, use the password directly
                command.extend(["-p" + password])
        else:
            command.append("-p")  # This will prompt for password if needed
        
        result = self._run_command(command)
        
        # Clean up the password file if it was created
        if password and input_path.lower().endswith(('.7z', '.zip')):
            os.remove(password_file)
        
        return result

    def _create_password_file(self, password):
        password_file = "temp_password.txt"
        with open(password_file, "w") as f:
            f.write(password)
        return password_file

    def _run_command(self, command):
        try:
            logging.debug(f"Executing command: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                logging.error(f"Command failed with return code {result.returncode}")
                logging.error(f"Error output: {result.stderr}")
                return f"Error: {result.stderr}"
            logging.debug(f"Command output: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {e.stderr}")
            return f"Error: {e.stderr}"

    def _get_compression_level(self, level):
        levels = {"Store": "0", "Fastest": "1", "Fast": "3", "Normal": "5", "Maximum": "7", "Ultra": "9"}
        return levels.get(level, "5")

    def _get_dict_size(self, size):
        sizes = {"64 KB": "64k", "1 MB": "1m", "2 MB": "2m", "4 MB": "4m", "8 MB": "8m", "16 MB": "16m", "32 MB": "32m", "64 MB": "64m"}
        return sizes.get(size, "16m")

    def _get_solid_block(self, size):
        if size == "Non-solid":
            return "off"
        return size.lower().replace(" ", "")
