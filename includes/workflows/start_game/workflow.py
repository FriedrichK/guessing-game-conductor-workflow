from conductor.client.workflow.conductor_workflow import ConductorWorkflow

from includes.settings import VERSION
from includes.workflows.shared import workflow_executor
from includes.workflows.start_game.tasks import (
    run_game_round_v1,
    get_list_of_active_players_v1,
    create_player_topics_v1,
)

START_GAME_ROUND_WORKFLOW_NAME: str = "start_game_round"
start_game_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name=START_GAME_ROUND_WORKFLOW_NAME,
    description="play a round of the game",
    version=VERSION,
)

start_game_workflow.add(get_list_of_active_players_v1)
start_game_workflow.add(create_player_topics_v1)
start_game_workflow.add(run_game_round_v1)


start_game_workflow.owner_email("fkauder@gmail.com")
start_game_workflow.register(True)
