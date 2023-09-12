from aws_cdk import (
    Stack,
    aws_elasticloadbalancingv2 as elb2
)

from constructs import Construct

from ..Helpers import CDKHelpers


class CDKELBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configuracion: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            _elb = elb2.ApplicationLoadBalancer(self, construct_id,
                                                vpc=configuracion['vpc'],
                                                internet_facing=True,
                                                security_group=configuracion['sg'],
                                                deletion_protection=False,
                                                http2_enabled=True,
                                                ip_address_type=elb2.IpAddressType.IPV4,
                                                load_balancer_name=configuracion['load_balancer_name']
                                                )

            listener = elb2.CfnListener(self, construct_id+'-listener',
                                        default_actions=[elb2.CfnListener.ActionProperty(
                                            type='forward',
                                            target_group_arn=configuracion['tg'])],
                                        load_balancer_arn=_elb.load_balancer_arn,
                                        port=80,
                                        protocol='HTTP')
            # _elb.add_listener(
            #     'listener',
            #     port=80,
            #     default_target_groups=configuracion['tg']
            # )

            self.o_elb = _elb
        except Exception as e:
            CDKHelpers.f_logs(e, self.stack_name)
