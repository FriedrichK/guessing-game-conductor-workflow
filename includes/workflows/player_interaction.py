from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.switch_task import SwitchTask
from conductor.client.workflow.task.terminate_task import TerminateTask, WorkflowStatus
from conductor.client.workflow.task.wait_task import WaitForDurationTask

from includes.settings import VERSION
from includes.workflows.shared import workflow_executor

PLAYER_INTERACTION_WORKFLOW_NAME: str = "player_interaction"
player_interaction_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name="start_player_interaction",
    description="a player interacts with a topic",
    version=VERSION,
)


# trigger the player interaction process
prompt_player_interaction_v1 = SimpleTask(
    task_def_name="evaluate_games_starting_conditions_v1",
    task_reference_name="evaluate_games_starting_conditions_v1",
)
player_interaction_workflow.add(prompt_player_interaction_v1)


# the prompt will time out at some point
wait_for_player_interaction_v1: WaitForDurationTask = WaitForDurationTask(
    task_ref_name="wait_for_player_interaction_v1",
    duration_time_seconds="10s",
)
player_interaction_workflow.add(wait_for_player_interaction_v1)


# after the interaction has taken place, we evaluate and return the interaction result

## ... the interaction has taken place successfully
terminate_interaction_success_v1: TerminateTask = TerminateTask(
    task_ref_name="terminate_interaction_success_v1",
    termination_reason="player_interacted",
    status=WorkflowStatus.COMPLETED,
)


## ... the interaction has failed
terminate_interaction_failure_v1: TerminateTask = TerminateTask(
    task_ref_name="terminate_interaction_failure_v1",
    termination_reason="player_interaction_failed",
    status=WorkflowStatus.FAILED,
)


player_interaction_success_or_failure_switch_v1: SwitchTask = SwitchTask(
    task_ref_name="start_or_end_game_switch_v1",
    case_expression="",
    use_javascript=True,
)
player_interaction_success_or_failure_switch_v1.default_case(
    [terminate_interaction_failure_v1]
)
# player_interaction_success_or_failure_switch_v1.switch_case(
#    "failure", [terminate_interaction_failure_v1]
# )
player_interaction_success_or_failure_switch_v1.switch_case(
    "success", [terminate_interaction_success_v1]
)
player_interaction_workflow.add(player_interaction_success_or_failure_switch_v1)


player_interaction_workflow.owner_email("fkauder@gmail.com")
player_interaction_workflow.register(True)
