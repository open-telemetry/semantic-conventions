# AWS ECS

**Status**: [Experimental][DocumentStatus]

**type:** `aws.ecs`

**Description:** Resources used by AWS Elastic Container Service (ECS).

<!-- semconv aws.ecs(full) -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`aws.ecs.task.id`](../../../attributes-registry/aws.md) | string | The ID of a running ECS task. The ID MUST be extracted from `task.arn`. | `10838bed-421f-43ef-870a-f43feacbbb5b`; `23ebb8ac-c18f-46c6-8bbe-d55d0e37cfbd` | `Conditionally Required` If and only if `task.arn` is populated. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.ecs.cluster.arn`](../../../attributes-registry/aws.md) | string | The ARN of an [ECS cluster](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/clusters.html). | `arn:aws:ecs:us-west-2:123456789123:cluster/my-cluster` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.ecs.container.arn`](../../../attributes-registry/aws.md) | string | The Amazon Resource Name (ARN) of an [ECS container instance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_instances.html). | `arn:aws:ecs:us-west-1:123456789123:container/32624152-9086-4f0e-acae-1a75b14fe4d9` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.ecs.launchtype`](../../../attributes-registry/aws.md) | string | The [launch type](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html) for an ECS task. | `ec2` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.ecs.task.arn`](../../../attributes-registry/aws.md) | string | The ARN of a running [ECS task](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-account-settings.html#ecs-resource-ids). | `arn:aws:ecs:us-west-1:123456789123:task/10838bed-421f-43ef-870a-f43feacbbb5b`; `arn:aws:ecs:us-west-1:123456789123:task/my-cluster/task-id/23ebb8ac-c18f-46c6-8bbe-d55d0e37cfbd` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.ecs.task.family`](../../../attributes-registry/aws.md) | string | The family name of the [ECS task definition](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html) used to create the ECS task. | `opentelemetry-family` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`aws.ecs.task.revision`](../../../attributes-registry/aws.md) | string | The revision for the task definition used to create the ECS task. | `8`; `26` | `Recommended` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`aws.ecs.launchtype` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `ec2` | ec2 | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `fargate` | fargate | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.26.0/specification/document-status.md
