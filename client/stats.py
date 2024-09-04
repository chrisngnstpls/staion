import psutil
import time
import requests
import client_config

NODE_ID = client_config.NODE_ID
SERVER_PORT = client_config.SERVER_PORT
SERVER_IP = client_config.SERVER_IP


def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
            temp = float(temp_file.read()) / 1000.0
        return temp
    except:
        return None
def write(payload):
	try:
		r = requests.get("http://{}:{}/report/".format(SERVER_IP,SERVER_PORT), params=payload)
		print('success')
		return 1
	except:
		print('error')
		return 0
	
def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    cpu_temp = get_cpu_temp()
    
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv
    
    return {
        "cpu_usage": cpu_percent,
        "memory_usage": memory_percent,
        "cpu_temp": cpu_temp,
        "network_sent": bytes_sent,
        "network_recv": bytes_recv
    }

if __name__ == "__main__":
    while True:
        stats = get_system_stats()
        print(f"CPU Usage: {stats['cpu_usage']}%")
        print(f"Memory Usage: {stats['memory_usage']}%")
        if stats['cpu_temp'] is not None:
            print(f"CPU Temperature: {stats['cpu_temp']}")
        else:
            print("CPU Temperature: Not available")
        print(f"Network Sent: {stats['network_sent']} bytes")
        print(f"Network Received: {stats['network_recv']} bytes")
        print("---")
        payload = {'node_id' : NODE_ID, 'cpu_use' : str(stats['cpu_usage']), 'cpu_temp' : str(stats['cpu_temp']), 'mem_use':str(stats['memory_usage']), 'net_in':str(stats['network_recv']), 'net_out':str(stats['network_sent'])}
        write(payload)
        time.sleep(10)  # Wait for 5 seconds before the next update
