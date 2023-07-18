from conductor.client.workflow.conductor_workflow import ConductorWorkflow

from includes.settings import VERSION
from includes.workflows.game_setup.tasks import (
    create_game_in_backend_v1,
    wait_for_players_v1,
    evaluate_games_starting_conditions_v1,
    start_or_end_game_switch_v1,
)
from includes.workflows.shared import workflow_executor


game_setup_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name="play_game_round",
    description="play a round of the game",
    version=VERSION,
)
game_setup_workflow.input_parameters(["name", "min_players", "max_players"])


game_setup_workflow.add(create_game_in_backend_v1)
game_setup_workflow.add(wait_for_players_v1)
game_setup_workflow.add(evaluate_games_starting_conditions_v1)
game_setup_workflow.add(start_or_end_game_switch_v1)


game_setup_workflow.owner_email("fkauder@gmail.com")
game_setup_workflow.register(True)
