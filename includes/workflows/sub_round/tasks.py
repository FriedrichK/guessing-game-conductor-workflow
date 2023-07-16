from conductor.client.workflow.task.dynamic_fork_task import DynamicForkTask
from conductor.client.workflow.task.join_task import JoinTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask

from includes.settings import VERSION
from includes.workflows.player_interaction.workflow import (
    PLAYER_INTERACTION_WORKFLOW_NAME,
)


# tell a worker to inform a given player that the game has failed
player_interaction_workflow_task_v1: SubWorkflowTask = SubWorkflowTask(
    task_ref_name="player_interaction_workflow_task_v1",
    workflow_name=PLAYER_INTERACTION_WORKFLOW_NAME,
    version=VERSION,
)


# join tasks
join_player_interaction_workflow_task_v1: JoinTask = JoinTask(
    task_ref_name="join_player_interaction_workflow_task_v1"
)


# execute the information task for each player
start_player_interactions_v1: DynamicForkTask = DynamicForkTask(
    task_ref_name="start_player_interactions_v1",
    pre_fork_task=player_interaction_workflow_task_v1,
    join_task=join_player_interaction_workflow_task_v1,
)
