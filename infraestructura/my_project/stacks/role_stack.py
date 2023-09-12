from aws_cdk import (
    Stack
)
from aws_cdk.aws_iam import (
    Role,
    ServicePrincipal
)
from constructs import Construct

from ..Helpers import CDKHelpers

class CDKRoleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,configuracion :dict,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            # Se crea el rol
            _role = Role(self, construct_id,
                         assumed_by= ServicePrincipal(str(configuracion['o_assumedBy'])),
                         role_name= configuracion['o_roleName'],
                         managed_policies= configuracion['o_managedPolicies']                         
            )
            # finalmente asignamos el objeto final del KeyPair a nuestro objeto global.
            # Asi se puede interactuar con el desde donde de cree una instancia de esta clase.
            self.o_role = _role
        except Exception as e:
            CDKHelpers.f_logs(e,self.stack_name)
        