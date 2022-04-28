import datetime
from typing import List

from requests import Request
from alvarium.annotators.handler.interfaces import RequestHandler

from alvarium.sign.contracts import SignInfo, SignType
from io import StringIO

from alvarium.sign.factories import SignProviderFactory
from .utils import parseSignature


class Ed25519RequestHandler(RequestHandler):

    def __init__(self, request: Request) -> None:
        self.request = request

    def AddSignatureHeaders(self, ticks: datetime, fields: List[str], keys: SignInfo) -> None:
        headerValue = StringIO()
        
        for i in range(len(fields)):
            headerValue.write(f'"{str(fields[i])}"')
            if i < len(fields) - 1:
                headerValue.write(f' ')

        headerValue.write(f';created={str(int(ticks.timestamp()))};keyid="{str(keys.public.path)}";alg="{str(keys.public.type)}";')

        self.request.headers['Signature-Input'] = headerValue.getvalue()
        
        parsed = parseSignature(r=self.request)
        inputValue = bytes(parsed.seed, 'utf-8')
        p = SignProviderFactory().get_provider(sign_type=SignType.ED25519)
    
        with open(keys.private.path, 'r') as file:
            prv_hex = file.read()
            prv = bytes.fromhex(prv_hex)

        signature = p.sign(key=prv, content=inputValue)

        self.request.headers['Signature'] = str(signature)
