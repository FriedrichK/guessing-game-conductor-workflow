from conductor.client.workflow.task.do_while_task import DoWhileTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask

from includes.settings import VERSION
from includes.workflows.sub_round.workflow import START_SUB_ROUND_WORKFLOW_NAME


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
