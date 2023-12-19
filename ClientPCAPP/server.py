from flask import Flask, jsonify
import subprocess
import platform
import psutil
import cpuinfo


def get_ip_address():
    try:
        command_output = subprocess.check_output(["ipconfig"], shell=True, stderr=subprocess.STDOUT).decode("cp866")
        lines = command_output.splitlines()
        ip_address = []
        for line in lines:
            if "IPv4-адрес" in line:
                ip_address.append(line.split(":")[1].strip())
        return ip_address
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return None


def get_local_host_info():
    host_name = platform.node()
    ip_address = get_ip_address()
    memory_info = psutil.virtual_memory()
    memory_gb = round(memory_info.total / (1024 ** 3), 2)
    disk_info = psutil.disk_usage('C://')
    total_disk_gb = round(disk_info.total / (1024 ** 3), 2)
    used_disk_gb = round(disk_info.used / (1024 ** 3), 2)
    free_disk_gb = round(disk_info.free / (1024 ** 3), 2)
    processor_name = cpuinfo.get_cpu_info()['brand_raw']
    return {
        "Host Name": host_name,
        "IP": ip_address,
        "Processor": processor_name,
        "Memory": memory_gb,
        "Total": total_disk_gb,
        "Used": used_disk_gb,
        "Free": free_disk_gb
    }


app = Flask(__name__)


@app.route('/get_info', methods=['GET'])
def get_info():
    pc_info = get_local_host_info()
    return jsonify(pc_info)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0",
                port=5200,
                debug=True,
                threaded=True)
    except OSError:
        pass
