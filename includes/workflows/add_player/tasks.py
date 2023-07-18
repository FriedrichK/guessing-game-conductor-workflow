from conductor.client.workflow.task.simple_task import SimpleTask


# add player in backend
add_player_v1 = SimpleTask(
    task_def_name="add_player_v1",
    task_reference_name="add_player_v1",
)
add_player_v1.input_parameters = {
    "game_round_workflow_id": "${workflow.input.game_round_workflow_id}",
    "player_name": "${workflow.input.player_name}",
}


# check if the maximum number of players has been reached
stop_waiting_to_start_game_if_max_player_count_is_reached_v1 = SimpleTask(
    task_def_name="stop_waiting_to_start_game_if_max_player_count_is_reached_v1",
    task_reference_name="stop_waiting_to_start_game_if_max_player_count_is_reached_v1",
)
stop_waiting_to_start_game_if_max_player_count_is_reached_v1.input_parameters = {
    "game_round_workflow_id": "${workflow.input.game_round_workflow_id}",
}
