from aws_cdk import (
    Stack,
)
from cdk_ec2_key_pair import (
    KeyPair
)
from constructs import Construct

from ..Helpers import CDKHelpers


class CDKKeyPairStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configuracion: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            # Creacion y configuracion para el key-pair
            _keypair = KeyPair(self, construct_id,
                               name=configuracion['o_name'],
                               description=configuracion['o_description'],
                               store_public_key=configuracion['o_storePublicKey'],
                               )
            # finalmente asignamos el objeto final del KeyPair a nuestro objeto global.
            # Asi se puede interactuar con el desde donde de cree una instancia de esta clase.
            self.o_keypair = _keypair
        except Exception as e:
            CDKHelpers.f_logs(e, self.stack_name)
