from conductor.client.workflow.task.do_while_task import DoWhileTask
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.task.sub_workflow_task import SubWorkflowTask

from includes.settings import VERSION
from includes.workflows.sub_round.workflow import START_SUB_ROUND_WORKFLOW_NAME


# get list of active players
get_list_of_active_players_v1: SimpleTask = SimpleTask(
    task_def_name="get_list_of_active_players_v1",
    task_reference_name="get_list_of_active_players_v1",
)
get_list_of_active_players_v1.input_parameters = {
    "game_id": "${workflow.input.game_id}"
}


# for each player, create a topic
create_player_topic_v1: SimpleTask = SimpleTask(
    task_def_name="create_player_topic_v1",
    task_reference_name="create_player_topic_v1",
)
create_player_topic_v1.input_parameters = {
    "game_id": "${workflow.input.game_id}",
    "iteration": "${create_player_topics_v1.output.iteration}",
    "players": "${get_list_of_active_players_v1.output.players}",
}

create_player_topics_v1: DoWhileTask = DoWhileTask(
    task_ref_name="create_player_topics_v1",
    termination_condition="$.create_player_topics_v1['iteration'] < $.players.length",
    tasks=create_player_topic_v1,
)
create_player_topics_v1.input_parameters = {
    "game_id": "${workflow.input.game_id}",
    "players": "${get_list_of_active_players_v1.output.players}",
}


# get topics
# TBD


# start a sub round
start_game_sub_round_workflow_task_v1: SubWorkflowTask = SubWorkflowTask(
    task_ref_name="start_game_sub_round_workflow_task_v1",
    workflow_name=START_SUB_ROUND_WORKFLOW_NAME,
    version=VERSION,
)
start_game_sub_round_workflow_task_v1.input_parameters = {
    "game_id": "${workflow.input.game_id}",
    "iteration": "${run_game_round_v1.output.iteration}",
    "players": "${get_list_of_active_players_v1.output.players}",
}


# for each iteration upon the same topic (=number of players) determined by the game setup,
# we must complete one sub workflow, meaning each player will make once contribution,
# each to a different topic
run_game_round_v1: DoWhileTask = DoWhileTask(
    task_ref_name="run_game_round_v1",
    termination_condition="$.run_game_round_v1['iteration'] < $.players.length",
    tasks=start_game_sub_round_workflow_task_v1,
)
run_game_round_v1.input_parameters = {
    "game_id": "${workflow.input.game_id}",
    "players": "${get_list_of_active_players_v1.output.players}",
}
