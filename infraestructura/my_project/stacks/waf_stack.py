from aws_cdk import (
    Stack,
    aws_wafv2 as waf
)

from constructs import Construct

from ..Helpers import CDKHelpers


class CDKWAFStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, configuracion: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        try:
            o_reglas_waf = []
            for regla in configuracion['reglas_waf']:
                regla_administrada = waf.CfnWebACL.RuleProperty(
                    name=regla['name_rule'],
                    priority=regla['priority'],
                    override_action={'none': {}},
                    statement=waf.CfnWebACL.StatementProperty(managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                        name=regla['name_rule'],
                        vendor_name='AWS',
                        excluded_rules=[]
                    )),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=regla['cloud_watch_metrics'],
                        metric_name=regla['metric_name'],
                        sampled_requests_enabled=regla['sampled_requests'],
                    )
                )
                o_reglas_waf.append(regla_administrada)
            _waf = waf.CfnWebACL(self, id=construct_id,
                                 name=configuracion['name'],
                                 default_action={'allow': {}},
                                 scope=str(configuracion['tipo']),
                                 visibility_config=configuracion['visibility_config'],
                                 rules=o_reglas_waf
                                 )
            self.o_waf = _waf
        except Exception as e:
            CDKHelpers.f_logs(e, self.stack_name)
