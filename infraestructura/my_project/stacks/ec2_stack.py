from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from aws_cdk.aws_ec2 import (
    InstanceType,
    Instance,
)
from constructs import Construct

from ..Helpers import CDKHelpers


class CDKEC2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configuracion: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            ec2_class = eval('ec2.InstanceClass.{}'.format(
                str(configuracion['instance_class']).upper()))
            ec2_size = eval('ec2.InstanceSize.{}'.format(
                str(configuracion['instance_size']).upper()))
            instance_ec2_type = InstanceType.of(ec2_class, ec2_size)
            ami_id = configuracion['ami']
            ami = ec2.MachineImage.from_ssm_parameter(parameter_name=ami_id)

            _ec2 = Instance(self, construct_id,
                            vpc=configuracion['vpc'],
                            instance_type=instance_ec2_type,
                            machine_image=ami,
                            instance_name=configuracion['instance_name'] if configuracion['instance_name'] else None,
                            allow_all_outbound=True,
                            key_name=configuracion['key_name'] if configuracion['key_name'] else None,
                            role=configuracion['role'] if configuracion['role'] else None,
                            source_dest_check=False,
                            security_group=configuracion['sg'] if configuracion['sg'] else None,
                            block_devices=[ec2.BlockDevice(
                                device_name="/dev/sda1",
                                volume=ec2.BlockDeviceVolume.ebs(
                                    int(configuracion['volume']))
                            )]
                            )

            self.o_ec2 = _ec2
        except Exception as e:
            CDKHelpers.f_logs(e, self.stack_name)
