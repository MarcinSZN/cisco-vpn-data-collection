from ncclient import manager
from ncclient.transport.errors import AuthenticationError, TransportError, NCClientError, SSHError
import xml.etree.ElementTree as ET
from getpass import getpass
import pandas as pd
import os
import csv
import logging


# Logging section to gather failures into a file
logging.basicConfig(
    filename = 'vpn_config_errors.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Providing filter for NETCONF
schema = '''
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <crypto>
        </crypto>
    </native>
</filter>
'''

# Preparing a list of devices to be used later for config collection
FILENAME_DEVICE = 'devices.csv'
list_of_devices = []
with open(FILENAME_DEVICE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        list_of_devices.append(row)

USERNAME = input("Please provide username: ").strip()
PASSWORD = getpass("Please provide password: ")


DEVICE_PARAMS = {
    'username': USERNAME,
    'password': PASSWORD,
    'port': 830,
    'hostkey_verify': False
}

ns_crypto = {
    'crypto': 'http://cisco.com/ns/yang/Cisco-IOS-XE-crypto'
}

def get_xml_element(element, path, namespace):
    found = element.find(path, namespace)
    return found.text if found is not None else None

for device in list_of_devices:
    try:
        FILENAME_OUTPUT = f"vpn_output_{device['host']}.csv"
        print(f"\nConnecting to the device {device['host']} {device['ip_addr']}")
        with manager.connect(host=device['ip_addr'], **DEVICE_PARAMS) as m:
            output_config_xml = m.get_config(source='running', filter=schema).data_xml
            root = ET.fromstring(output_config_xml)

        # Creating dictionary for pandas 'pd' module
        # Looking up needed values in the xml file based on etree module and XPath
        vpn_list_ike = []
        for elements in root.findall('.//crypto:ikev2/crypto:profile', ns_crypto):
            crypto_ike_dictionary = {
                'VPN_NAME': get_xml_element(elements, './/crypto:name', ns_crypto),
                'LOCAL_IP_ADDR': get_xml_element(elements, './/crypto:address', ns_crypto),
                '3rdParty_REMOTE_ADDRESS': get_xml_element(elements, './/crypto:ipv4-address', ns_crypto),
                "IKE_LIFETIME": get_xml_element(elements, './/crypto:seconds', ns_crypto),
                "IKE_AUTH_TYPE": 'pre-share' if elements.find('.//crypto:pre-share', ns_crypto) is not None else "other"
            }

            vpn_list_ike.append(crypto_ike_dictionary)
        if not vpn_list_ike:
            print(f"[{device['host']}] No IKE profiles found - skipping")
            continue
        
        df_ike = pd.DataFrame(vpn_list_ike)

        vpn_list_ipsec = []
        for elements_map in root.findall('.//crypto:map-seq/crypto:map', ns_crypto):
            crypto_ipsec_dictionary = {
                'VPN_NAME': get_xml_element(elements_map, './/crypto:ikev2-profile', ns_crypto),
                'CRYPTO_MAP_PFS_GROUP': get_xml_element(elements_map, './/crypto:group', ns_crypto),
                "IPSEC_TRANSFORM_SET": get_xml_element(elements_map, './/crypto:transform-set', ns_crypto),
                'IPSEC_LIFETIME': get_xml_element(elements_map, './/crypto:seconds', ns_crypto),
            }
            vpn_list_ipsec.append(crypto_ipsec_dictionary)

        df_ipsec = pd.DataFrame(vpn_list_ipsec)

        # Merging two DataFrames into single on based on "VPN_NAME" columnt to have a single one combined with all needed data.
        crypto_merged_df = pd.merge(df_ike, df_ipsec, on='VPN_NAME', how='left')
        print(crypto_merged_df.to_string(index=False))

        crypto_merged_df.to_csv(FILENAME_OUTPUT, index=False)
        print("\nFile saved to:", os.path.abspath(FILENAME_OUTPUT))

    except AuthenticationError:
        logging.error(f"Authentication failed for device {device['host']}.")
        print(f"Authentication failed for device [{device['host']}] - please check credentials.")
    except SSHError:
        logging.error(f"\nUnable to connect to device {device['host']} via SSH.")
        print(f"\nSSH connection failed - [{device['host']}] unreachable or port 830 blocked.")
    except TransportError as e:
        logging.error(f"Transport error for device [{device['host']}]: {e}")
        print(f"Transport error for device [{device['host']}]: {e}")
    except NCClientError as e:
        logging.error(f"ncclient error for device [{device['host']}]: {e}")
        print(f"ncclient error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error for device [{device['host']}]")
        print(f"Unexpected error: {e}")
