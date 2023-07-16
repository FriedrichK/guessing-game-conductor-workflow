from conductor.client.workflow.conductor_workflow import ConductorWorkflow

from includes.settings import VERSION
from includes.workflows.shared import workflow_executor
from includes.workflows.sub_round.tasks import start_player_interactions_v1

START_SUB_ROUND_WORKFLOW_NAME: str = "start_sub_round"
start_sub_round_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name="start_sub_round",
    description="start a round in which each player interacts with one of the topics once",
    version=VERSION,
)


start_sub_round_workflow.add(start_player_interactions_v1)


start_sub_round_workflow.owner_email("fkauder@gmail.com")
start_sub_round_workflow.register(True)
