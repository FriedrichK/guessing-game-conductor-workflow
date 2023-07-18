from conductor.client.workflow.task.dynamic_fork_task import DynamicForkTask
from conductor.client.workflow.task.join_task import JoinTask
from conductor.client.workflow.task.simple_task import SimpleTask


# update the game to reflect failure
update_game_to_show_it_has_failed_v1: SimpleTask = SimpleTask(
    task_def_name="update_game_to_show_it_has_failed_v1",
    task_reference_name="update_game_to_show_it_has_failed_v1",
)
update_game_to_show_it_has_failed_v1.input_parameters = {
    "game_id": "${workflow.input.game_id}",
}

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
