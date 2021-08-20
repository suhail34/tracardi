from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result


class ParseURLParameters(ActionRunner):

    def __init__(self, *args, **kwargs):
        pass

    async def run(self, void):

        try:
            if not isinstance(self.session.context, dict):
                raise KeyError("No session context defined.")

            s_c = self.session.context

            response = {
                    "profile_id": s_c['profile']['id'],
                    "url": s_c['page']['url'],
                    "path": s_c['page']['path'],
                    "hash": s_c['page']['hash'],
                    "title": s_c['page']['title'],
                    "refer_host": s_c['page']['refer']['host'],
                    "refer_query": s_c['page']['refer']['query'],
                    "history_length": s_c['page']['history']['length'],
                    "local_tracardi_profile_id": s_c['storage']['local']['tracardi-profile-id']
                },
            }

        return Result(port="payload", value=response)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.parse_url_parameters_action',
            className='ParseURLParameters',
            inputs=[],
            outputs=['payload'],
        ),
        metadata=MetaData(
            name='Parse URL parameters',
            desc='Reads URL parameters form context, parses it and returns as dict.',
            type='flowNode',
            width=100,
            height=100,
            icon='json',
            group=["Read"]
        )
    )
