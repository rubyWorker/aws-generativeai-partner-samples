import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as bedrockagentcore from 'aws-cdk-lib/aws-bedrockagentcore';
import { Construct } from 'constructs';

export interface GatewayProps {
  gatewayName: string;
  mcpRuntimeArns: { name: string; arn: string }[];
}

export class GatewayConstruct extends Construct {
  public readonly gateway: bedrockagentcore.CfnGateway;
  public readonly gatewayArn: string;
  public readonly gatewayId: string;
  public readonly gatewayUrl: string;
  public readonly targets: bedrockagentcore.CfnGatewayTarget[];

  constructor(scope: Construct, id: string, props: GatewayProps) {
    super(scope, id);

    const stack = cdk.Stack.of(this);

    // Gateway Role with permissions to invoke runtimes and Lambda functions
    const gatewayRole = new iam.Role(this, 'GatewayRole', {
      assumedBy: new iam.ServicePrincipal('bedrock-agentcore.amazonaws.com'),
      description: 'Execution role for AgentCore Gateway',
      inlinePolicies: {
        GatewayPolicy: new iam.PolicyDocument({
          statements: [
            // Bedrock AgentCore permissions (only if there are MCP runtimes)
            ...(props.mcpRuntimeArns.length > 0 ? [new iam.PolicyStatement({
              sid: 'BedrockAgentCoreAccess',
              effect: iam.Effect.ALLOW,
              actions: [
                'bedrock-agentcore:InvokeRuntime',
                'bedrock-agentcore:InvokeRuntimeWithResponseStream'
              ],
              resources: [
                ...props.mcpRuntimeArns.map(r => r.arn)
              ],
            })] : []),
            // Lambda invoke permissions (for future Lambda targets)
            new iam.PolicyStatement({
              sid: 'LambdaInvokeAccess',
              effect: iam.Effect.ALLOW,
              actions: ['lambda:InvokeFunction'],
              resources: [`arn:aws:lambda:${stack.region}:${stack.account}:function:*`],
            }),
            // Bedrock model access (for gateway operations)
            new iam.PolicyStatement({
              sid: 'BedrockModelAccess',
              effect: iam.Effect.ALLOW,
              actions: ['bedrock:InvokeModel', 'bedrock:InvokeModelWithResponseStream'],
              resources: [
                `arn:aws:bedrock:*::foundation-model/*`,
                `arn:aws:bedrock:*:${stack.account}:inference-profile/*`
              ],
            }),
            // CloudWatch Logs
            new iam.PolicyStatement({
              sid: 'CloudWatchLogsAccess',
              effect: iam.Effect.ALLOW,
              actions: [
                'logs:CreateLogGroup',
                'logs:CreateLogStream',
                'logs:PutLogEvents'
              ],
              resources: [`arn:aws:logs:${stack.region}:${stack.account}:log-group:/aws/bedrock-agentcore/*`],
            }),
          ],
        }),
      },
    });

    // Create Gateway with IAM auth
    this.gateway = new bedrockagentcore.CfnGateway(this, 'Gateway', {
      name: props.gatewayName,
      roleArn: gatewayRole.roleArn,
      protocolType: 'MCP',
      protocolConfiguration: {
        mcp: {
          supportedVersions: ['2025-03-26']
        }
      },
      authorizerType: 'NONE',
      description: 'AgentCore Gateway with MCP protocol and IAM auth'
    });

    this.gatewayArn = this.gateway.attrGatewayArn;
    this.gatewayId = this.gateway.attrGatewayIdentifier;
    this.gatewayUrl = this.gateway.attrGatewayUrl;

    // Create targets for MCP servers
    this.targets = [];

    props.mcpRuntimeArns.forEach((mcpRuntime, index) => {
      const mcpRuntimeUrl = this.constructRuntimeUrl(mcpRuntime.arn, stack.region);
      const mcpTarget = new bedrockagentcore.CfnGatewayTarget(this, `McpTarget${index}`, {
        gatewayIdentifier: this.gatewayId,
        name: mcpRuntime.name.toLowerCase().replace(/[^a-z0-9-]/g, '-'),
        description: `MCP Server: ${mcpRuntime.name}`,
        targetConfiguration: {
          mcp: {
            mcpServer: {
              endpoint: mcpRuntimeUrl
            }
          }
        },
      });
      mcpTarget.addDependency(this.gateway);
      this.targets.push(mcpTarget);
    });
  }

  /**
   * Constructs the runtime invocation URL with properly encoded ARN
   */
  private constructRuntimeUrl(runtimeArn: string, region: string): string {
    return cdk.Fn.join('', [
      `https://bedrock-agentcore.${region}.amazonaws.com/runtimes/`,
      cdk.Fn.join('%2F', cdk.Fn.split('/', cdk.Fn.join('%3A', cdk.Fn.split(':', runtimeArn)))),
      '/invocations'
    ]);
  }
}
