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
