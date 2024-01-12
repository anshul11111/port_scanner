from flask import Flask, render_template, request
from colorama import Fore, Style
import concurrent.futures
import socket
from datetime import datetime
import pyfiglet
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

app = Flask(__name__)

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                return f"{Fore.GREEN}Port {port} is open{Style.RESET_ALL}"
    except (socket.gaierror, socket.error):
        pass  # Handle hostname resolution or server not responding errors




def port_scan(target, ipv6=False):
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Scan ports 1 to 65,535 concurrently
        results = list(executor.map(
            lambda port: scan_port(target, port), range(1, 65536)))

    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = request.form['target']
        ip_version = request.form['ip_version']
        results = port_scan(target, ipv6=(ip_version == '6'))
        return render_template('index.html', target=target, ip_version=ip_version, results=results)

    return render_template('index.html', target=None, ip_version=None, results=None)


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER", font="slant")
    print(f"{Fore.CYAN}{ascii_banner}{Style.RESET_ALL}")
    app.run(debug=True)
