import asyncio

import iterm2


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='shipa target',
        detailed_description='The currently set target for shipa',
        exemplar='📦 shipa-101',
        update_cadence=2,
        identifier='com.digestibledevops.iterm-components.shipa-target',
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def shipa_target_coroutine(knobs):
        proc = await asyncio.create_subprocess_shell(
            '/usr/local/bin/shipa target list | grep "^*" | awk "{print \$2}"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return f'📦 {stdout.decode().strip()}' if not stderr else '📦 not installed!'

    @iterm2.RPC
    async def shipa_target_click_handler(session_id):
        # When you click the status bar it opens a popover with the
        # message "Hello World"
        await component.async_open_popover(
                session_id,
                "Hello, world",
                iterm2.Size(200, 200))

    await component.async_register(connection, shipa_target_coroutine, onclick = shipa_target_click_handler)

iterm2.run_forever(main)
