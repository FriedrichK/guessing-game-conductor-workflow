from conductor.client.http.models import EventHandler
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.event_task import ConductorEventTask
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.wait_task import WaitForDurationTask

from includes.settings import VERSION
from includes.workflows.end_failed_game import END_FAILED_GAME_WORKFLOW_NAME
from includes.workflows.shared import workflow_executor
from includes.workflows.start_game import START_GAME_ROUND_WORKFLOW_NAME

game_setup_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name="play_game_round",
    description="play a round of the game",
    version=VERSION,
)
game_setup_workflow.input_parameters(["min_players", "max_players"])

# notify backend there is a new game
create_game_in_backend_v1 = SimpleTask(
    task_def_name="create_game_in_backend_v1",
    task_reference_name="create_game_in_backend_v1",
)
game_setup_workflow.add(create_game_in_backend_v1)


# wait a pre defined period of time for players to join
wait_for_players_v1 = WaitForDurationTask(
    task_ref_name="wait_for_players_v1", duration_time_seconds="1m"
)
game_setup_workflow.add(wait_for_players_v1)


# # a new player is joining
# NEW_PLAYER_JOINED_EVENT_NAME: str = "new_player_joined"
# event_new_player: ConductorEventTask = ConductorEventTask(
#     task_ref_name="new_player_joined_event_v1",
#     event_name=NEW_PLAYER_JOINED_EVENT_NAME,
# )
#
# # when a new player is joining, process their registration in a separate sub workflow
# CONDITION_ALWAYS_HANDLE_EVENT: str = "1>0"
# event_handler_new_player: EventHandler = EventHandler(
#     name="listen_to_new_player_joining",
#     event=f"conductor:{NEW_PLAYER_JOINED_EVENT_NAME}",
#     condition=CONDITION_ALWAYS_HANDLE_EVENT,
#     actions=[
#         {
#             "action": "start_workflow",
#             "start_workflow": {"name": "player_joining", "version": 1},
#             "expandInlineJSON": True,
#         }
#     ],
#     active=True,
# )

# after the waiting period has elapsed, check if the game can begin
## ... the actual check is done in a worker
evaluate_games_starting_conditions_v1 = SimpleTask(
    task_def_name="evaluate_games_starting_conditions_v1",
    task_reference_name="evaluate_games_starting_conditions_v1",
)
game_setup_workflow.add(evaluate_games_starting_conditions_v1)


## ... on success, start the game!
start_game_round_sub_workflow_task_v1: SubWorkflowTask = SubWorkflowTask(
    task_ref_name="start_game_round_sub_workflow_task_v1",
    workflow_name=START_GAME_ROUND_WORKFLOW_NAME,
    version=VERSION,
)


## ... on failure, close the game down!
end_failed_game_round_sub_workflow_task_v1: SubWorkflowTask = SubWorkflowTask(
    task_ref_name="end_failed_game_round_sub_workflow_task_v1",
    workflow_name=END_FAILED_GAME_WORKFLOW_NAME,
    version=VERSION,
)


## ... the check detemines where to go next
start_or_end_game_switch_v1: SwitchTask = SwitchTask(
    task_ref_name="start_or_end_game_switch_v1",
    case_expression="$.evaluation_successful == true ? 'success' : 'failure'",
    use_javascript=True,
)
start_or_end_game_switch_v1.input_parameters = {
    "evaluation_successful": "${evaluate_games_starting_conditions_v1.output.evaluation_successful}"
}
start_or_end_game_switch_v1.default_case([end_failed_game_round_sub_workflow_task_v1])
# start_or_end_game_switch_v1.switch_case(
#    "failure", [end_failed_game_round_sub_workflow_task_v1]
# )
start_or_end_game_switch_v1.switch_case(
    "success", [start_game_round_sub_workflow_task_v1]
)
game_setup_workflow.add(start_or_end_game_switch_v1)

game_setup_workflow.owner_email("fkauder@gmail.com")
game_setup_workflow.register(True)
