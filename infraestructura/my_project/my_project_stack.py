from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elb2,
    aws_elasticloadbalancingv2_targets as elb2targets
)
from constructs import Construct

from .stacks import (
    CDKVPCStack,
    CDKSecurityGroupStack,
    CDKRoleStack,
    CDKKeyPairStack,
    CDKLaunchTemplateStack,
    CDKEC2Stack,
    CDKWAFStack,
    CDKTargetGroupStack,
    CDKELBStack,
    CDKDynamoDBStack
)

from .Helpers import CDKHelpers


class MyProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configuracion: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        nombre_proyecto = configuracion['project']['name']
        enviroment = kwargs['env']
        """ 
        Seccion VPC 
        """
        # si contamos con la propiedad VPC, configuramos el/los stacks necesarios
        if 'vpc' not in configuracion:
            CDKHelpers.f_falta_configuracion(
                'No se provee configuracion de vpc', 'vpc')
        # array donde pasaremos las subnets destinadas a la vpc.
        configSubnet = []
        # iteramos los datos en el JSON correspondientes a o_configuracion_subnets dentro de la propiedad VPC
        # asi podemos crear objetos individuales de cada tipo de subnet
        for config in configuracion['vpc']['o_configuracion_subnets']:
            config_type = config['type']
            configSubnet.append({'cidrMask': config['cidr'], 'name': 'Public' if config_type == 'Publica' else 'Private',
                                'subnetType': ec2.SubnetType.PUBLIC if config_type == 'Publica' else ec2.SubnetType.PRIVATE_WITH_EGRESS})  # Private with nat deprecated
        # Creamos el objeto para configurar un nuevo objeto de nuestro stack VPC
        configuracion_vpc = {
            # rango CIDR para la VPC
            'e_rango_cidr': configuracion['vpc']['e_rango_cidr'],
            # habilitar DNS HostNames
            'enableDnsHostnames': configuracion['vpc']['enableDnsHostnames'],
            # habilitar DNS support
            'enableDnsSupport': configuracion['vpc']['enableDnsSupport'],
            # cantidad de NAT
            'e_cantidad_de_NAT': configuracion['vpc']['e_cantidad_de_NAT'],
            # indica si un VPN Gateway sera creado y agregado a esta VPC
            'vpnGateway': configuracion['vpc']['vpnGateway'],
            'o_configuracion_subnets': configSubnet,
            'nombre_proyecto': nombre_proyecto
        }
        _vpc = CDKVPCStack(self, 'vpc', configuracion_vpc, env=enviroment)

        """ 
        Fin de Seccion VPC 
        """

        """
        Seccion LaunchTemplate App
        """
        # si contamos con la propiedad launchTemplate, configuramos el/los stacks necesarios
        if 'launchTemplate' in configuracion:
            confi_launch_template_app = configuracion['launchTemplate'][0]
            # Creamos el objeto para configurar un nuevo objeto de nuestro stack Security Group perteneciente al Launch Template
            configuracion_sg_app = {
                "vpc": _vpc.o_vpc,  # VPC para este Security Group
                "o_allowAllOutbound": True,  # permitir todas las salidas de este security group
                "o_disableInlineRules": True,
                # descripcion para este security group
                "o_description": 'Security Group for App Launch Template',
                "o_sg_name": construct_id + '-sg',  # nombre para este security group
                "o_name": construct_id + '-sg',
            }

            _sg_app = CDKSecurityGroupStack(
                self, 'app-sg', configuracion_sg_app, env=enviroment)
            # Tags.of(_sg_app.o_sg).add('Name', configuracionServicios.cliente.nombre + 'SG');

            # Se agregan reglas de ingreso a sus puertos de acuerdo a su protocolo
            # _sg_app.o_sg.add_ingress_rule(
            #     ec2.Peer.any_ipv4(), ec2.Port.tcp(80), 'sg-HTTP')
            # _sg_app.o_sg.add_ingress_rule(
            #     ec2.Peer.any_ipv4(), ec2.Port.tcp(443), 'sg-HTTPS')
            # Se agrega una regla de ingreso a la primera subnet publica para habilitar trafico.
            _sg_app.o_sg.add_ingress_rule(ec2.Peer.ipv4(
                _vpc.o_vpc.public_subnets[0].ipv4_cidr_block), ec2.Port.tcp(22), 'Public-1a')

            # Reglas de ingreso para cada subnet privada que tengamos. Esto varia segun la AZ.
            count = 0
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
            for subnet in _vpc.o_vpc.private_subnets:
                _sg_app.o_sg.add_ingress_rule(ec2.Peer.ipv4(
                    subnet.ipv4_cidr_block), ec2.Port.all_tcp(), 'Private-1'+letters[count])
                count += 1

            # Iteramos las politicas de nuestro archivo de configuracion JSON y las pasamos a un array
            policies = []
            for policies_role in confi_launch_template_app['role']['o_policies']:
                policies.append(policies_role)

            # Creamos el objeto para configurar un nuevo objeto de nuestro stack Role
            configuracion_role_app = {
                'o_assumedBy': confi_launch_template_app['role']['o_assumedBy'] if 'o_assumedBy' in confi_launch_template_app['role'] else None,
                'o_roleName': confi_launch_template_app['role']['o_roleName'] if 'o_roleName' in confi_launch_template_app['role'] else None,
                'o_managedPolicies': [
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        'AmazonS3FullAccess'),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        'AmazonSSMManagedInstanceCore'),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        'CloudWatchAgentServerPolicy'),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        'CloudWatchFullAccess'),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "AWSCloudFormationReadOnlyAccess"),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "SecretsManagerReadWrite"),
                ],
            }
            _role_app = CDKRoleStack(
                self, 'app-role', configuracion_role_app, env=enviroment)
            # Tags.of(_role_app.o_role).add('Name', configuracionServicios.cliente.nombre + 'ROLE');

            # Creamos el objeto para configurar un nuevo objeto de nuestro stack KeyPair
            configuracion_keypair_app = {
                'o_name': confi_launch_template_app['keyPair']['o_name'],
                'o_description': confi_launch_template_app['keyPair']['o_description'],
                'o_storePublicKey': confi_launch_template_app['keyPair']['o_storePublicKey']
            }

            _keypair_app = CDKKeyPairStack(
                self, 'kp', configuracion_keypair_app, env=enviroment)
            # Tags.of(_keyPair_app.o_keypair).add('Name', configuracionServicios.cliente.nombre + 'KP')

            # Obtenemos el objeto de nuestra AMI
            _machine_ami = ec2.MachineImage.from_ssm_parameter(
                '/aws/service/canonical/ubuntu/server/20.04/stable/current/amd64/hvm/ebs-gp2/ami-id',
                os=ec2.OperatingSystemType.LINUX,
            )

            ec2_instance_class = eval('ec2.InstanceClass.{}'.format(
                str(confi_launch_template_app['instanceClass']).upper()))
            ec2_instance_size = eval('ec2.InstanceSize.{}'.format(
                str(confi_launch_template_app['instanceSize']).upper()))

            configuracion_launch_template_app = {
                'o_vpc': _vpc.o_vpc,
                'sg': _sg_app.o_sg,
                'ami': _machine_ami,
                'role': _role_app.o_role,
                'keyName': _keypair_app.o_keypair.key_pair_name,
                'o_volumen': ec2.BlockDeviceVolume.ebs(50),
                'instanceType': ec2.InstanceType.of(ec2_instance_class, ec2_instance_size),
                'userData': "#!/bin/bash"
            }

            _launch_template_app = CDKLaunchTemplateStack(
                self, confi_launch_template_app['nombre']+'-lt', configuracion_launch_template_app, env=enviroment)
        """
        Fin de seccion LaunchTemplate App
        """

        """
        Inicio de seccion de Autoscaling Group
        """
        if 'autoScalingGroup' in configuracion:
            asg_app = configuracion['autoScalingGroup'][0]
            configuracion_target_group_app = {
                'port': asg_app['o_targetGroup']['o_port'],
                'o_tgname': asg_app['o_targetGroup']['nombre'],
                'targetType': elb2.TargetType.INSTANCE,
                'o_vpc': _vpc.o_vpc,
            }
        """
        Fin de seccion de Autoscaling Group
        """

        """
        Inicio de seccion de EC2
        """
        if 'ec2' in configuracion:

            configuracion_target_group_app = {
                'port': asg_app['o_targetGroup']['o_port'],
                'tg_name': asg_app['o_targetGroup']['nombre'],
                'target_type': elb2.TargetType.INSTANCE,
                'vpc': _vpc.o_vpc,
            }
            _target_group_app = CDKTargetGroupStack(
                self, asg_app['o_targetGroup']['nombre']+'-tg', configuracion_target_group_app, env=enviroment)
            instancias_ec2 = []
            for ec2_instance in configuracion['ec2']:
                configuracion_ec2 = {
                    'vpc': _vpc.o_vpc,
                    'ami': ec2_instance['ami'],
                    'instance_class': ec2_instance['instance_class'],
                    'instance_size': ec2_instance['instance_size'],
                    'instance_name': ec2_instance['instance_name'],
                    'role': _role_app.o_role,
                    'sg':  _sg_app.o_sg,
                    'key_name': _keypair_app.o_keypair.key_pair_name,
                    'volume': ec2_instance['volume']
                }
                _ec2 = CDKEC2Stack(
                    self, 'ec2-'+ec2_instance['instance_name'], configuracion_ec2, env=enviroment)
                _target_group_app.o_target_group.add_target(
                    elb2targets.InstanceTarget(_ec2.o_ec2))
                instancias_ec2.append(elb2targets.InstanceTarget(_ec2.o_ec2))
            # _target_group_app.o_target_group.add_target(
            #     targets=instancias_ec2
            # )

        """
        Fin de seccion de EC2
        """

        """
        Inicio de seccion de Elastic Load Balancer
        """
        if 'elasticLoadBalancer' in configuracion:
            for elb_configuracion in configuracion['elasticLoadBalancer']:
                # Creamos el objeto para configurar un nuevo objeto de nuestro stack Security Group perteneciente al Elastic Load Balancer
                configuracion_sg_elb = {
                    "vpc": _vpc.o_vpc,  # VPC para este Security Group
                    "o_allowAllOutbound": True,  # permitir todas las salidas de este security group
                    "o_disableInlineRules": True,
                    "o_description": 'Security Group ELB APP',
                    "o_sg_name": construct_id + '-elb-sg',  # nombre para este security group
                    "o_name": construct_id + '-elb-sg',
                }

                _sg_elb = CDKSecurityGroupStack(
                    self, 'elb-sg', configuracion_sg_elb, env=enviroment)
 
                # Tags.of(_sg_app.o_sg).add('Name', configuracionServicios.cliente.nombre + 'SG');

                # Se agregan reglas de ingreso a sus puertos de acuerdo a su protocolo
                _sg_elb.o_sg.add_ingress_rule(
                    ec2.Peer.any_ipv4(), ec2.Port.tcp(80), 'sg-HTTP')
                _sg_elb.o_sg.add_ingress_rule(
                    ec2.Peer.any_ipv4(), ec2.Port.tcp(443), 'sg-HTTPS')
                _sg_app.o_sg.add_ingress_rule(
                    _sg_elb.o_sg, ec2.Port.tcp(80), 'sg-HTTP')
                _sg_app.o_sg.add_ingress_rule(
                    _sg_elb.o_sg, ec2.Port.tcp(443), 'sg-HTTPS')
                configuracion_elb = {
                    'vpc': _vpc.o_vpc,
                    'sg': _sg_elb.o_sg,
                    'load_balancer_name': elb_configuracion['nombre'],
                    'tg': _target_group_app.o_target_group.target_group_arn
                }

                _elb_app = CDKELBStack(
                    self, elb_configuracion['nombre']+'-elb', configuracion_elb, env=enviroment)

        """
        Fin de seccion de Elastic Load Balancer
        """


        """
        Inicio de seccion de DynamoDB
        """
        # if 'dynamo' in configuracion:
        #     tables = []
        #     for table in configuracion['dynamo']:
        #         configuracion_dynamo_db = {
        #             'o_name': table['o_name'],
        #             'o_partition_name': table['o_partition_name']
        #         }
        #         _table = CDKDynamoDBStack(self, table['o_name'] + '-tb', configuracion_dynamo_db, env=enviroment)
                
        """
        Fin de seccion de DynamoDB
        """
        self.o_vpc = _vpc.o_vpc
        self.o_sg_app = _sg_app.o_sg
        self.o_role_app = _role_app.o_role
        self.o_keypair_app = _keypair_app.o_keypair
        self.o_launch_template_app = _launch_template_app
