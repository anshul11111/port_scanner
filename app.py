import asyncio
from flask import Flask, render_template, request
from colorama import Fore, Style, init
import socket
import pyfiglet

init(autoreset=True)  # Initialize colorama

app = Flask(__name__)


async def scan_port(target, port):
    try:
        reader, writer = await asyncio.open_connection(target, port)
        writer.close()
        return f"{Fore.GREEN}Open{Style.RESET_ALL}"
    except (socket.gaierror, socket.error):
        pass  # Handle hostname resolution or server not responding errors
    return f"{Fore.RED}Closed{Style.RESET_ALL}"


async def port_scan(target):
    results = {}

    async def update_progress(port):
        status = await scan_port(target, port)
        results[port] = status

    tasks = [update_progress(port) for port in range(1, 1025)]
    await asyncio.gather(*tasks)

    # Filter open ports
    open_ports = {k: v for k, v in results.items() if "Open" in v}

    return open_ports


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = request.form['target']

        print(f"Received POST request with target: {target}")

        # Perform the port scanning operation
        results = asyncio.run(port_scan(target))

        print("Results:")
        for port, status in results.items():
            print(f"Port {port}: {status}")

        return render_template('results.html', target=target, results=results)

    return render_template('index.html', target=None, results=None)


# if __name__ == '__main__':
#     ascii_banner = pyfiglet.figlet_format("PORT SCANNER", font="slant")
#     print(f"{Fore.CYAN}{ascii_banner}{Style.RESET_ALL}")
#     app.run(debug=True, threaded=True)
