"""Start API, persistent production simulator and Vite. Run after installing requirements."""
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
from server.local_network import lan_ipv4_addresses

ROOT = Path(__file__).resolve().parent

def main():
    try:
        lan_ips = lan_ipv4_addresses()
    except ValueError:
        raise SystemExit('FLUIDMES_LAN_IP inválido. Informe somente o IPv4 do computador, sem http:// ou porta.') from None
    # Share the same snapshot with Django so hosts and CSRF origins match.
    if lan_ips:
        os.environ['FLUIDMES_LAN_IP'] = ','.join(lan_ips)
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    if not npm:
        raise SystemExit('Instale Node.js 22+ (com npm) e abra um terminal novo.')
    if not (ROOT / 'client/node_modules').is_dir():
        subprocess.run([npm, 'ci'], cwd=ROOT/'client', check=True)
    subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], cwd=ROOT/'server', check=True)
    jobs = [
        ([sys.executable, '-m', 'uvicorn', 'config.asgi:application', '--host', '127.0.0.1', '--port', '8000'], ROOT/'server'),
        ([sys.executable, 'manage.py', 'run_production'], ROOT/'server'),
        ([npm, 'run', 'dev', '--', '--host', '0.0.0.0', '--port', '5173', '--strictPort'], ROOT/'client'),
    ]
    processes = []
    try:
        for command, cwd in jobs:
            kwargs = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
            processes.append(subprocess.Popen(command, cwd=cwd, **kwargs))
        version = (ROOT / 'VERSION').read_text().strip()
        print(f'\nFluidMES {version}\nNeste computador: http://127.0.0.1:5173', flush=True)
        for address in lan_ips:
            print(f'Na rede LAN: http://{address}:5173', flush=True)
        if not lan_ips:
            print('IP da LAN não identificado. Consulte ipconfig; defina FLUIDMES_LAN_IP e reinicie.', flush=True)
        print('Permita o Node.js nas redes privadas do Firewall do Windows. Ctrl+C encerra os serviços.\n', flush=True)
        while all(process.poll() is None for process in processes):
            time.sleep(.5)
        if any(process.returncode not in (None,0) for process in processes):
            raise SystemExit('Um serviço parou. Veja o erro acima e confira se as portas 8000/5173 estão livres.')
    except KeyboardInterrupt:
        pass
    finally:
        for process in processes:
            if process.poll() is None:
                if os.name == 'nt':
                    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                else:
                    os.killpg(process.pid, signal.SIGTERM)
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

if __name__ == '__main__':
    main()
