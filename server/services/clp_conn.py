from pymodbus.client import AsyncModbusTcpClient

class Conexao:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.porta = int(port)
        self.cliente = None

    async def Conectar(self):
        self.FecharConexao()
        self.cliente = AsyncModbusTcpClient(host=self.ip, port=self.porta, timeout=3, retries=1)
        if not await self.cliente.connect():
            self.FecharConexao()
            raise ConnectionError('Não foi possível conectar ao CLP.')
        return self.cliente

    def FecharConexao(self):
        if self.cliente:
            self.cliente.close()
        self.cliente = None
