from aws_cdk import (
    Stack
)
from aws_cdk.aws_ec2 import (
    SecurityGroup
)
from constructs import Construct

from ..Helpers import CDKHelpers

class CDKSecurityGroupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,configuracion :dict,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            # Creacion y configuracion para el security group
            _sg = SecurityGroup(self, construct_id,
                                vpc= configuracion['vpc'],
                                allow_all_outbound= configuracion['o_allowAllOutbound'] if configuracion['o_allowAllOutbound'] else False,
                                description= configuracion['o_description'] if configuracion['o_description'] else None,
                                security_group_name= configuracion['o_sg_name'] if configuracion['o_sg_name'] else None,
                                # disable_inline_rules= configuracion['o_disableInlineRules']
            )
            # finalmente asignamos el objeto final del security group a nuestro objeto global.
            # Asi se puede interactuar con el desde donde de cree una instancia de esta clase.
            self.o_sg = _sg
        except Exception as e:
            CDKHelpers.f_logs(e,self.stack_name)
        