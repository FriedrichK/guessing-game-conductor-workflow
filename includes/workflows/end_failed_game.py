from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.dynamic_fork_task import DynamicForkTask
from conductor.client.workflow.task.join_task import JoinTask
from conductor.client.workflow.task.simple_task import SimpleTask

from includes.settings import VERSION
from includes.workflows.shared import workflow_executor

END_FAILED_GAME_WORKFLOW_NAME: str = "end_failed_game_round"
end_failed_game_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name=END_FAILED_GAME_WORKFLOW_NAME,
    description="wrap up a failed game",
    version=VERSION,
)


# tell a worker to inform a given player that the game has failed
inform_player_game_has_failed_v1: SimpleTask = SimpleTask(
    task_def_name="inform_player_game_has_failed_v1",
    task_reference_name="inform_player_game_has_failed_v1",
)


# join tasks
join_inform_player_game_has_failed_v1: JoinTask = JoinTask(
    task_ref_name="join_inform_player_game_has_failed_v1"
)


# execute the information task for each player
inform_players_game_has_failed_v1: DynamicForkTask = DynamicForkTask(
    task_ref_name="inform_players_game_has_failed_v1",
    pre_fork_task=inform_player_game_has_failed_v1,
    join_task=join_inform_player_game_has_failed_v1,
)
end_failed_game_workflow.add(inform_players_game_has_failed_v1)


end_failed_game_workflow.owner_email("fkauder@gmail.com")
end_failed_game_workflow.register(True)
