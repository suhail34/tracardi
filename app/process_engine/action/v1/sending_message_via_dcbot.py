from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from sqlalchemy import create_engine
import discord
import logging
import asyncio
from discord.ext import tasks

client = discord.Client(
    activity=discord.Game(name='Good evening. Something ... something broke and I could not hear, '))
class Discord(ActionRunner):

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)
        client.run('')


    async def run(self, void):
        @client.event
        async def on_message(message):
            await message.channel.send(
                'test2')
        return Result(port='session', value=None)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.discord.send.message',
            className='Discord',
            inputs=["void"],
            outputs=['session'],
            init={''},
            version='0.1',
            license="MIT",
            author="Patryk Migaj"

        ),
        metadata=MetaData(
            name='Send message with DiscordBot',
            desc='Send message with DiscordBot',
            type='flowNode',
            width=100,
            height=100,
            icon='start',
            group=["Discord"]
        )
    )
