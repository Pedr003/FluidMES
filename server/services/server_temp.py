"""Simulador Modbus TCP local; endereços de protocolo 0–99, device_id=1."""
import argparse
import asyncio
from pymodbus.simulator import SimDevice, SimData, DataType
from pymodbus.server import StartAsyncTcpServer

def build_context():
    return SimDevice(id=1, simdata=(
        [SimData(address=0, values=[False]*100, datatype=DataType.BITS)],
        [SimData(address=0, values=[False]*100, datatype=DataType.BITS, readonly=True)],
        [SimData(address=0, values=list(range(1000,1100)), datatype=DataType.UINT16)],
        [SimData(address=0, values=list(range(100)), datatype=DataType.UINT16, readonly=True)],
    ))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5020)
    args=parser.parse_args()
    try:
        asyncio.run(StartAsyncTcpServer(context=build_context(), address=(args.host,args.port)))
    except KeyboardInterrupt:
        pass
