from sobolanism.rpc import client


class FibRPCAPI(client.RPCClient):
    def fibonate(self, n):
        result = self.call("fibonate", n)
        return int(result)
