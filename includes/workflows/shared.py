from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor

from includes.configuration import conductor_configuration

workflow_executor: WorkflowExecutor = WorkflowExecutor(conductor_configuration)
