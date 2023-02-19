import datetime
from typing import List

from requests import Request
from alvarium.annotators.handler.interfaces import RequestHandler
from alvarium.sign.contracts import SignType
from alvarium.sign.factories import SignProviderFactory

class NoneRequestHandler(RequestHandler):

    def __init__(self, request: Request) -> None:
        self.request = request

    def AddSignatureHeaders(self) -> None:

        #Adding the Signature-Input header
        self.request.headers['Signature-Input'] = ""

        #Adding the Signature header using the NoneSignProvider
        p = SignProviderFactory().get_provider(sign_type=SignType.NONE)

        inputValue = bytes("", 'utf-8')
        signature = p.sign(content=inputValue)

        self.request.headers['Signature'] = signature
        