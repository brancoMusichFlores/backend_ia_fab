from aws_cdk import (
    Stack,
    Aspects,
    Tag
)
from aws_cdk.aws_ec2 import (
    Vpc,
    DefaultInstanceTenancy,
    SubnetType,
    GatewayVpcEndpointAwsService,
    IpAddresses
)
from constructs import Construct

from ..Helpers import CDKHelpers

class CDKVPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,configuracion :dict,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            _vpc = Vpc(self,construct_id,
                       ip_addresses= IpAddresses.cidr(configuracion['e_rango_cidr']) if configuracion['e_rango_cidr'] else None, # cidr deprecated
                       max_azs = len(self.availability_zones),
                       subnet_configuration = configuracion['o_configuracion_subnets'] if configuracion['o_configuracion_subnets'] else None,
                       nat_gateways = configuracion['e_cantidad_de_NAT'] if configuracion['e_cantidad_de_NAT'] else None,
                       nat_gateway_subnets = { 'subnet_type': SubnetType.PUBLIC },
                       enable_dns_hostnames = configuracion['enableDnsHostnames'] if configuracion['enableDnsHostnames'] else None,
                       enable_dns_support = configuracion['enableDnsSupport'] if configuracion['enableDnsSupport'] else None,
                       vpn_gateway = configuracion['vpnGateway'] if configuracion['vpnGateway'] else None,
                       default_instance_tenancy = DefaultInstanceTenancy.DEFAULT,
                       vpn_route_propagation = [ { 'subnet_type': SubnetType.PRIVATE_WITH_EGRESS } ], # private with nat deprecated
                       # gatewayEndpoints= {
                       # 	S3= { service= lib_ec2.GatewayVpcEndpointAwsService.S3 },
                       # 	DynamoDB= { service= lib_ec2.GatewayVpcEndpointAwsService.DYNAMODB }, 
            )

            # para cambiarle el nombre a las subnets publicas
            count= 0
            letters = ['a','b','c','d','e','f','g','h','i','j']
            for subnet in _vpc.public_subnets:
                Aspects.of(subnet).add(
                    Tag(
                        'Name',
                        'Public-1' + letters[count]
                    )
                )
                count += 1

            # para cambiarle el nombre a las subnets privadas
            count= 0
            for subnet in _vpc.private_subnets:
                Aspects.of(subnet).add(
                    Tag(
                        'Name',
                        'Private-1' + letters[count]
                    )
                )
                count += 1

            # agregar endpoint para S3
            _vpc.add_gateway_endpoint(configuracion['nombre_proyecto'] + '-s3-vpce',
                                      service= GatewayVpcEndpointAwsService.S3,
                                      subnets= [{
                                        'subnets': _vpc.private_subnets,
                                      }]

            )
            # finalmente asignamos el objeto final del security group a nuestro objeto global.
            # Asi se puede interactuar con el desde donde de cree una instancia de esta clase.
            self.o_vpc = _vpc
        except Exception as e:
            CDKHelpers.f_logs(e,self.stack_name)