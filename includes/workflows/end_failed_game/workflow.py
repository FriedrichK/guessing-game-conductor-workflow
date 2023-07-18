from conductor.client.workflow.conductor_workflow import ConductorWorkflow

from includes.settings import VERSION
from includes.workflows.end_failed_game.tasks import inform_players_game_has_failed_v1, \
    update_game_to_show_it_has_failed_v1
from includes.workflows.shared import workflow_executor

END_FAILED_GAME_WORKFLOW_NAME: str = "end_failed_game_round"
end_failed_game_workflow: ConductorWorkflow = ConductorWorkflow(
    executor=workflow_executor,
    name=END_FAILED_GAME_WORKFLOW_NAME,
    description="wrap up a failed game",
    version=VERSION,
)
end_failed_game_workflow.input_parameters(["game_id"])

end_failed_game_workflow.add(update_game_to_show_it_has_failed_v1)
end_failed_game_workflow.add(inform_players_game_has_failed_v1)

end_failed_game_workflow.owner_email("fkauder@gmail.com")
end_failed_game_workflow.register(True)
