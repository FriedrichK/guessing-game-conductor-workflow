from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.event_task import ConductorEventTask
from conductor.client.workflow.task.simple_task import SimpleTask

from includes.settings import VERSION
from includes.workflows.shared import workflow_executor

ADD_PLAYER_WORKFLOW_NAME: str = "add_player"
add_player_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name=ADD_PLAYER_WORKFLOW_NAME,
    description="add a player",
    version=VERSION,
)
add_player_workflow.input_parameters(["game_round_workflow_id", "player_name"])

# trigger handling
add_player_v1 = SimpleTask(
    task_def_name="add_player_v1",
    task_reference_name="add_player_v1",
)
add_player_v1.input_parameters = {"game_round_workflow_id": "${workflow.input.game_round_workflow_id}", "player_name": "${workflow.input.player_name}"}
add_player_workflow.add(add_player_v1)

add_player_workflow.owner_email("fkauder@gmail.com")
add_player_workflow.register(True)
