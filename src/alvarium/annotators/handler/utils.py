from requests import Request, structures
from .exceptions import ParserException
from urllib.parse import urlparse
from .contracts import ParseResult, DerivedComponent
from io import StringIO

def parseSignature(r: Request) -> ParseResult:

    # Making the request headers case insensitive
    headers = structures.CaseInsensitiveDict(r.headers)

    # Signature Inputs Extraction
    signatureInput = headers.get("Signature-Input")
    try:
        signature = headers.get("Signature")
        if signature == None:
            signature = ""
    except KeyError:
        signature = ""

    signatureInputList = signatureInput.split(";",1)
    signatureInputHeader = signatureInputList[0].split(" ")
    signatureInputTail = signatureInputList[1]
    
    signatureInputParsedTail = signatureInputTail.split(";")

    algorithm = ""
    keyid = ""
    for s in signatureInputParsedTail:
        if "alg" in s:
            raw = s.split("=")[1]
            algorithm = raw[1:len(raw)-1]
        if "keyid" in s:
            raw = s.split("=")[1]
            keyid = raw[1:len(raw)-1]

    parsed_url = urlparse(r.url)

    signatureInputFields = {}
    signatureInputBody = StringIO()

    for field in signatureInputHeader:
        # Remove double quotes from the field to access it directly in the header map
        key = field[1 : len(field)-1]
        if key[0] == "@":
            if DerivedComponent(key) == DerivedComponent.Method:
                signatureInputFields[key] = [r.method]
            elif DerivedComponent(key) == DerivedComponent.TargetURI:
                signatureInputFields[key] = [r.url]
            elif DerivedComponent(key) == DerivedComponent.Authority:
                signatureInputFields[key] = [parsed_url.netloc]
            elif DerivedComponent(key) == DerivedComponent.Scheme:
                signatureInputFields[key] = [parsed_url.scheme]
            elif DerivedComponent(key) == DerivedComponent.Path:
                signatureInputFields[key] = [parsed_url.path]
            elif DerivedComponent(key) == DerivedComponent.Query:
                signatureInputFields[key] = ["?"+parsed_url.query]
            elif DerivedComponent(key) == DerivedComponent.QueryParams:
                queryParams = []
                rawQueryParams = parsed_url.query.split("&")
                for rawQueryParam in rawQueryParams:
                    if rawQueryParam != "":
                        parameter = rawQueryParam.split("=")
                        name = parameter[0]
                        value = parameter[1]
                        queryParam = f';name="{name}": {value}'
                        queryParams.append(queryParam)
                signatureInputFields[key] = queryParams
            else:
                raise ParserException(f"Unhandled Derived Component {key}")
        else:
            try:
                # Multi-value headers are not permitted in Python
                fieldValues = headers.get(key)
                # Removing leading and trailing whitespaces
                signatureInputFields[key] = [fieldValues.strip()]
            except KeyError:
                raise ParserException(f"Header field not found {key}")
    
        # Construct final output string
        keyValues = signatureInputFields[key]
        if len(keyValues) == 1:
            signatureInputBody.write(f'"{key}" {keyValues[0]}\n')
        else:
            for value in keyValues:
                signatureInputBody.write(f'"{key}"{value}\n')
   
    parsedSignatureInput = f"{signatureInputBody.getvalue()};{signatureInputTail}"
    s = ParseResult(seed=parsedSignatureInput, signature=signature, keyid=keyid, algorithm=algorithm)

    return s
   

