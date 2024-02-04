import os
import time
import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear_screen():
    console.clear()

def show_header():
    console.print(Panel("[bold cyan]WiFi-TxPower-Tuner[/bold cyan]", subtitle="[yellow]by PROFESOR[/yellow]"))

def get_wireless_interfaces():
    iwconfig_output = subprocess.check_output("iwconfig", shell=True, text=True).split('\n')
    interfaces = []
    for line in iwconfig_output:
        if 'IEEE' in line:
            interface = line.split()[0]
            interfaces.append(interface)
    return interfaces

def show_iwconfig():
    console.print("[bold green]Current wireless interfaces configuration:[/bold green]")
    interfaces = get_wireless_interfaces()
    for interface in interfaces:
        iwconfig_output = subprocess.check_output(f"iwconfig {interface}", shell=True, text=True)
        console.print(iwconfig_output)
    time.sleep(3.0)

def increase_txpower(interface_name):
    try:
        clear_screen()
        show_header()
        console.print(f"[bold blue]Setting Tx-Power for {interface_name} to 30dBm...[/bold blue]")
        os.system("sudo iw reg set BZ")
        os.system(f"sudo ip link set {interface_name} down")
        os.system(f"sudo iw dev {interface_name} set txpower fixed 30dBm")
        os.system(f"sudo ip link set {interface_name} up")
        console.print(f"[bold green]Tx-Power for {interface_name} successfully set to 30dBm.[/bold green]")
        console.print("[bold green]Operation completed.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

def txpower_default(interface_name):
    try:
        clear_screen()
        show_header()
        console.print(f"[bold blue]Resetting Tx-Power for {interface_name} to default settings...[/bold blue]")
        os.system(f"sudo ip link set {interface_name} down")
        os.system("sudo iw reg set 00")
        os.system(f"sudo iw dev {interface_name} set txpower fixed 20dBm")
        os.system(f"sudo ip link set {interface_name} up")
        console.print(f"[bold green]Tx-Power for {interface_name} successfully reset to default.[/bold green]")
        console.print("[bold green]Operation completed.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

def main():
    clear_screen()
    show_header()
    show_iwconfig()
    interfaces = get_wireless_interfaces()
    while True:
        interface_name = console.input("[bold green]Please enter the interface name you want to configure (e.g., wlan0): [/bold green]").strip()
        if interface_name in interfaces:
            break
        else:
            console.print("[bold red]Invalid interface name. Please enter a valid wireless interface name.[/bold red]")

    console.print("\n[bold]Options:[/bold]\n[bold cyan]1[/bold cyan] - Set Tx Power to 30dBm\n[bold cyan]2[/bold cyan] - Set to Default dBm")
    choice = console.input("[bold magenta]Please choose an option (1 or 2): [/bold magenta]")

    if choice == '1':
        increase_txpower(interface_name)
    elif choice == '2':
        txpower_default(interface_name)
    else:
        console.print("[bold red]Invalid choice. Exiting...[/bold red]")

    time.sleep(3.0)
    clear_screen()
    show_header()
    show_iwconfig()

if __name__ == "__main__":
    main()
