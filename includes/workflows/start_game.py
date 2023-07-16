from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.do_while_task import DoWhileTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask

from includes.settings import VERSION
from includes.workflows.shared import workflow_executor
from includes.workflows.sub_round import START_SUB_ROUND_WORKFLOW_NAME

START_GAME_ROUND_WORKFLOW_NAME: str = "start_game_round"
start_game_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name=START_GAME_ROUND_WORKFLOW_NAME,
    description="play a round of the game",
    version=VERSION,
)

# start a sub round
start_game_sub_round_workflow_task_v1: SubWorkflowTask = SubWorkflowTask(
    task_ref_name="start_game_sub_round_workflow_task_v1",
    workflow_name=START_SUB_ROUND_WORKFLOW_NAME,
    version=VERSION,
)

# for each iteration upon the same topic (=number of players) determined by the game setup,
# we must complete one sub workflow
run_game_round_v1: DoWhileTask = DoWhileTask(
    task_ref_name="run_game_round_v1",
    termination_condition="$.run_game_round_v1['iteration'] < ${workflow.max_iterations}",
    tasks=start_game_sub_round_workflow_task_v1,
)
start_game_workflow.add(run_game_round_v1)


start_game_workflow.owner_email("fkauder@gmail.com")
start_game_workflow.register(True)
