# notify backend there is a new game
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.wait_task import WaitForDurationTask

from includes.settings import VERSION
from includes.workflows.end_failed_game.workflow import END_FAILED_GAME_WORKFLOW_NAME
from includes.workflows.start_game.workflow import START_GAME_ROUND_WORKFLOW_NAME

create_game_in_backend_v1 = SimpleTask(
    task_def_name="create_game_in_backend_v1",
    task_reference_name="create_game_in_backend_v1",
)
create_game_in_backend_v1.input_parameters = {
    "game_name": "${workflow.input.name}",
}


# wait a pre defined period of time for players to join
wait_for_players_v1 = WaitForDurationTask(
    task_ref_name="wait_for_players_v1", duration_time_seconds="1m"
)


# after the waiting period has elapsed, check if the game can begin
## ... the actual check is done in a worker
evaluate_games_starting_conditions_v1 = SimpleTask(
    task_def_name="evaluate_games_starting_conditions_v1",
    task_reference_name="evaluate_games_starting_conditions_v1",
)


## ... on success, start the game!
start_game_round_sub_workflow_task_v1: SubWorkflowTask = SubWorkflowTask(
    task_ref_name="start_game_round_sub_workflow_task_v1",
    workflow_name=START_GAME_ROUND_WORKFLOW_NAME,
    version=VERSION,
)
start_game_round_sub_workflow_task_v1.input_parameters = {
    "game_id": "${workflow.workflowId}",
}


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
