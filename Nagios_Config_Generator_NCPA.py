#!/usr/bin/env python3
import argparse
import sys
import os
import requests
from requests.exceptions import RequestException

# Set to False if your certificate is self-signed
VERIFY_SSL = False
DEFAULT_TIMEOUT = 10  # seconds

def get_system_info(ncpa_host, token, timeout=DEFAULT_TIMEOUT):
    url = f"https://{ncpa_host}:5693/api/system"
    params = {'token': token}
    response = requests.get(url, params=params, verify=VERIFY_SSL, timeout=timeout)
    response.raise_for_status()
    return response.json()

def get_disk_info(ncpa_host, token, timeout=DEFAULT_TIMEOUT):
    url = f"https://{ncpa_host}:5693/api/disk/logical"
    params = {'token': token, 'units': 'G'}
    response = requests.get(url, params=params, verify=VERIFY_SSL, timeout=timeout)
    response.raise_for_status()
    return response.json()

def get_interface_info(ncpa_host, token, timeout=DEFAULT_TIMEOUT):
    url = f"https://{ncpa_host}:5693/api/interface"
    params = {'token': token}
    response = requests.get(url, params=params, verify=VERIFY_SSL, timeout=timeout)
    response.raise_for_status()
    return response.json()

def generate_disk_services(hostname, token, disk_data):
    """
    Generate a Nagios service block for each disk logical partition.
    The disk key (e.g. "|export") is used in the check_command,
    while the service_description shows a cleaned disk name.

    Any '|' character in the service description is replaced with '_'.
    """
    services = []
    logicals = disk_data.get("logical", {})
    # Sorting keys so that the root partition ("|") comes first
    for disk_key in sorted(logicals.keys()):
        # Remove the leading pipe; if empty, use "/" to indicate root.
        # Also replace any additional pipe characters with an underscore.
        raw_name = disk_key.lstrip("|")
        if not raw_name:
            display_name = "/"
        else:
            display_name = raw_name.replace("|", "_")
        service_block = f"""define service {{
        host_name                       {hostname}
        service_description             {display_name} Disk Usage
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693  -M 'disk/logical/{disk_key}' -w '90' -c '95' -u Gi
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
"""
        services.append(service_block)
    return services

def generate_static_services(hostname, token, interface_name):
    """
    Generate static Nagios service definitions.
    """
    services = []
    # CPU Usage
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             CPU Usage
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693 -M cpu/percent -w '90' -c '95' -q 'aggregate=avg'
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Memory Usage
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Memory Usage
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693 -M memory/virtual -u 'Gi' -w '90' -c '95'
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Ping
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Ping
        use                             generic-service
        check_command                   check-host-alive
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # System Node Status
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             System Node Status
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693 -M 'system/node'
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Login User Count
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Login User Count
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693 -M user/count -w '40' -c '45'
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # SSHD Service Status
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             SSHD Service Status
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693 -M 'services' -q 'service=network|ssh:default,status=running'
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Uptime
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Uptime
        use                             generic-service
        check_command                   check_ncpa!-t mytoken -T 60 -M 'system/uptime' -w @60:120 -c @1:60
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Interface Incoming Errors
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Interface {interface_name} Incoming Errors
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693  -M 'interface/{interface_name}/errin' -w 90 -c 95
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Interface Outgoing Errors
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Interface {interface_name} Outgoing Errors
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693  -M 'interface/{interface_name}/errout' -w 90 -c 95
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Interface Packets Sent
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Interface {interface_name} Packets Sent
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693  -M 'interface/{interface_name}/packets_sent'
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    # Interface Packets Received
    services.append(f"""define service {{
        host_name                       {hostname}
        service_description             Interface {interface_name} Packets Received
        use                             generic-service
        check_command                   check_ncpa!-t 'mytoken' -P 5693  -M 'interface/{interface_name}/packets_recv'
        contacts                        nagiosadmin
        contact_groups                  admins
        }}
""")
    return services

def process_server(ip_address, ncpa_host, token, dest_dir):
    try:
        print(f"Processing {ip_address} ...")
        system_data    = get_system_info(ncpa_host, token)
        disk_data      = get_disk_info(ncpa_host, token)
        interface_data = get_interface_info(ncpa_host, token)
    except RequestException as e:
        print(f"Error retrieving data from {ip_address}: {e}")
        return

    # Extract host name (XXXX) from the system API
    hostname = system_data.get("system", {}).get("node", "UNKNOWN_HOST")

    # Determine the network interface name (INTERFACENAME); pick the first available one.
    interfaces = list(interface_data.get("interface", {}).keys())
    if interfaces:
        interface_name = sorted(interfaces)[0]
    else:
        interface_name = "UNKNOWN_INTERFACE"

    # Build the host definition block
    host_definition = f"""###################################################
## Host Definationi: {hostname}
###################################################

define host {{
        host_name                       {hostname}
        use                             generic-host
        address                         {ip_address}
        alias                           {hostname} Server
        hostgroups                      allservers
        contacts                        nagiosadmin
        contact_groups                  admins
        first_notification_delay        0
        notifications_enabled           1
        }}
"""

    # Service header block
    service_header = """##############################
#### Service Defination   ####
##############################
"""

    # Generate disk logical service definitions
    disk_services = generate_disk_services(hostname, token, disk_data)
    # Generate static service definitions (CPU, Memory, Ping, etc.)
    static_services = generate_static_services(hostname, token, interface_name)

    # Combine all sections into one configuration output
    full_config = host_definition + "\n" + service_header + "\n"
    # First add all disk services
    full_config += "\n".join(disk_services) + "\n"
    # Then add the static service definitions
    full_config += "\n".join(static_services)

    # Define destination file path
    filename = os.path.join(dest_dir, f"{hostname}.cfg")
    try:
        with open(filename, "w") as cfg_file:
            cfg_file.write(full_config)
        print(f"Configuration for {hostname} saved to {filename}")
    except IOError as e:
        print(f"Error writing configuration file for {hostname}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate complete Nagios configurations using NCPA API data for multiple servers"
    )
    parser.add_argument("ip_addresses", nargs="+", help="One or more IP addresses to use in the Nagios host definitions")
    parser.add_argument("--ncpa-host", default="", help="NCPA API host (if different from the IP address)")
    parser.add_argument("--token", default="mytoken", help="NCPA API token (default: mytoken)")
    parser.add_argument("--dest-dir", default="/scripts/GenerateNCPALinux/Hosts", help="Destination directory for config files")
    args = parser.parse_args()

    # Use each IP address provided. If --ncpa-host is not given, use the IP address for API calls.
    dest_dir = args.dest_dir
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for ip in args.ip_addresses:
        # If ncpa_host is provided as an override, use it; otherwise use the IP address.
        host_for_api = args.ncpa_host if args.ncpa_host else ip
        process_server(ip, host_for_api, args.token, dest_dir)

if __name__ == "__main__":
    main()
