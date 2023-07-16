from conductor.client.workflow.conductor_workflow import ConductorWorkflow

from includes.settings import VERSION
from includes.workflows.add_player.tasks import add_player_v1
from includes.workflows.shared import workflow_executor

ADD_PLAYER_WORKFLOW_NAME: str = "add_player"
add_player_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name=ADD_PLAYER_WORKFLOW_NAME,
    description="add a player",
    version=VERSION,
)
add_player_workflow.input_parameters(["game_round_workflow_id", "player_name"])


add_player_workflow.add(add_player_v1)
add_player_workflow.add(check_if_max_player_count_is_reached_v1)


add_player_workflow.owner_email("fkauder@gmail.com")
add_player_workflow.register(True)
