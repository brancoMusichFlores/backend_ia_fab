from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb
)

from constructs import Construct

from ..Helpers import CDKHelpers


class CDKDynamoDBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configuracion: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            # Creacion y configuracion para el key-pair
            _dynamo_tb = dynamodb.Table(self, "Table",
                                        table_name=configuracion['o_name'],
                                        partition_key=dynamodb.Attribute(name=configuracion['o_partition_name'], type=dynamodb.AttributeType.STRING)
            )

            # finalmente asignamos el objeto final del DynamoDB a nuestro objeto global.
            # Asi se puede interactuar con el desde donde de cree una instancia de esta clase.
            self.o_dynamo_tb = _dynamo_tb
        except Exception as e:
            CDKHelpers.f_logs(e, self.stack_name)
