from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from aws_cdk.aws_ec2 import (
    LaunchTemplate
)
from constructs import Construct

from ..Helpers import CDKHelpers

class CDKLaunchTemplateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,configuracion :dict,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            # Creacion y configuracion para la Launch Template
            _launch_template = LaunchTemplate(self, construct_id,
                                      launch_template_name= construct_id,
                                      instance_type= configuracion['instanceType'],
                                      machine_image= configuracion['ami'],
                                      user_data= ec2.UserData.for_linux(shebang=configuracion['userData']),
                                      role= configuracion['role'],
                                      security_group= configuracion['sg'],
                                      key_name= configuracion['keyName'],
                                      block_devices= [{'deviceName': '/dev/sda1','volume': configuracion['o_volumen']}],
                                      # cpuCredits: lib_ec2.CpuCredits.STANDARD,
                                      # disableApiTermination: false,
                                      ebs_optimized= False,
                                      # nitroEnclaveEnabled: false,
                                      # hibernationConfigured: false,
                                      # instanceInitiatedShutdownBehavior: lib_ec2.InstanceInitiatedShutdownBehavior.STOP,
                                      # spotOptions: {blockDuration: cdk.Duration.hours(1), interruptionBehavior: lib_ec2.SpotInstanceInterruption.STOP, maxPrice: 0.01, requestType: lib_ec2.SpotRequestType.ONE_TIME, validUntil: cdk.Expiration.atTimestamp(10987639289)},                                                                
            )
            # finalmente asignamos el objeto final del KeyPair a nuestro objeto global.
            # Asi se puede interactuar con el desde donde de cree una instancia de esta clase.
            self.o_launch_template = _launch_template
        except Exception as e:
            CDKHelpers.f_logs(e,self.stack_name)
        