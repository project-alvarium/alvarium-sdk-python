# set project directory
import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)


# ------------------------ app starts here ----------------------- #
import json, logging

from typing import List
from alvarium.contracts.config import SdkInfo
from alvarium.annotators.interfaces import Annotator
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.default import DefaultSdk
from alvarium.annotators.contracts import Signable

with open("./tests/example/sdk-config.json", "r") as file:
    config = json.loads(file.read())

# construct sdk config
sdk_info = SdkInfo.from_json(json.dumps(config["sdk"]))

# construct logger
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.DEBUG)

# construct annotators
annotator_factory = AnnotatorFactory()
annotators: List[Annotator] = [annotator_factory.getAnnotator(kind=annotation_type, sdk_info=sdk_info) \
                               for annotation_type in sdk_info.annotators]

# construct sdk
sdk = DefaultSdk(annotators=annotators, logger=logger, config=sdk_info)

# construct sample data
# in this case, we'll use the Signable data class to ensure that the pki annotator
# will return satisfied annotation
signable = Signable(seed="helloo",
                signature="B9E41596541933DB7144CFBF72105E4E53F9493729CA66331A658B1B18AC6DF5DA991" + \
                          "AD9720FD46A664918DFC745DE2F4F1F8C29FF71209B2DA79DFD1A34F50C")
old_data = bytes(signable.to_json(), 'utf-8')
new_data = bytes(signable.to_json(), 'utf-8')

# call sdk methods
sdk.create(data=old_data)
sdk.mutate(old_data=old_data, new_data=new_data)
sdk.transit(data=new_data)

# dispose sdk
sdk.close()