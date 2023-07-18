from conductor.client.workflow.conductor_workflow import ConductorWorkflow

from includes.settings import VERSION
from includes.workflows.player_interaction.tasks import (
    prompt_player_interaction_v1,
    wait_for_player_interaction_v1,
    player_interaction_success_or_failure_switch_v1,
)
from includes.workflows.shared import workflow_executor


PLAYER_INTERACTION_WORKFLOW_NAME: str = "player_interaction"
player_interaction_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name=PLAYER_INTERACTION_WORKFLOW_NAME,
    description="a player interacts with a topic",
    version=VERSION,
)

player_interaction_workflow.add(prompt_player_interaction_v1)
player_interaction_workflow.add(wait_for_player_interaction_v1)
player_interaction_workflow.add(player_interaction_success_or_failure_switch_v1)

player_interaction_workflow.owner_email("fkauder@gmail.com")
player_interaction_workflow.register(True)
