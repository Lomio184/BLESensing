import time
import asyncio
from bleak import BleakScanner, BleakClient

async def scanning():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)
        
async def connect( address ):
    async with BleakClient(address) as client:
        connected = await client.is_connected()
        print(f"Connected: {connected}")
        print(f"Connect Mac Adress : {address}")
        print(f"Connected Device Info : {client._backend}")
        disconnected = await client.disconnect()
        print(f"Disconnected : {disconnected}")
        
async def discover_services( address ):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}, Properties: {characteristic.properties}")
        
async def fetch_device_info(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}, Properties: {characteristic.properties}")
                descriptors = characteristic.descriptors
                for descriptor in descriptors:
                    print(f"    Descriptor: {descriptor.uuid}")
                    
def calculate_distance(RSSI_rx, RSSI_tx=-59, n=3):
    """
    Parameters:
    RSSI_rx (float): 수신기에서 측정된 RSSI 값(dBm).
    RSSI_tx (float): 1미터 거리에서의 송신기의 RSSI 값(dBm). 기본값은 -59dBm.
    n (float): 환경에 따라 달라지는 경로 손실 지수. 기본값은 3(실내 공간).
    
    Returns:
    float: 추산된 거리(미터 단위).
    """
    distance = 10 ** ((RSSI_tx - RSSI_rx) / (10 * n))
    return distance

async def run():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.address == 'write your device mac address':
            print("Device ({}): {}, RSSI: {}, Distance : {}".format(device.name, device.address, device.rssi, calculate_distance(device.rssi)))

def main():
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete( run() )
        time.sleep( 3 )

                
if __name__ == "__main__":
    main()