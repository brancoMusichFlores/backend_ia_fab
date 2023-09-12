from aws_cdk import (
    Stack,
    aws_elasticloadbalancingv2 as elb2
)

from constructs import Construct

from ..Helpers import CDKHelpers


class CDKTargetGroupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configuracion: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            _target_group = elb2.ApplicationTargetGroup(self, construct_id,
                                                        target_group_name=configuracion['tg_name'],
                                                        port=configuracion['port'],
                                                        target_type=configuracion['target_type'],
                                                        vpc=configuracion['vpc'],
                                                        health_check={
                                                            "path": "/healthy.html"
                                                        }
                                                        )
            self.o_target_group = _target_group
        except Exception as e:
            CDKHelpers.f_logs(e, self.stack_name)
