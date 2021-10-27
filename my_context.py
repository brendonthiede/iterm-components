import asyncio

import iterm2


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='kubectl context',
        detailed_description='The currently configured Kubernetes context for kubectl',
        exemplar='☸️ docker-for-desktop',
        update_cadence=2,
        identifier='engineering.dane.iterm-components.kubectl-context',
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def kubectl_context_coroutine(knobs):
        proc = await asyncio.create_subprocess_shell(
            '/usr/local/bin/kubectl config current-context',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        kube_status = f'{stdout.decode().strip()}' if not stderr else '?'

        proc = await asyncio.create_subprocess_shell(
            '/usr/local/bin/shipa target list | grep "^*" | awk "{print \$2}"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        shipa_status = f'{stdout.decode().strip()}' if not stderr else '?'

        proc = await asyncio.create_subprocess_shell(
            '/usr/local/bin/terraform workspace show',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        tf_status = f'{stdout.decode().strip()}' if not stderr else '?'
        
        return f'☸️ {kube_status} | 📦 {shipa_status} | 🧱 {tf_status}'

    await component.async_register(connection, kubectl_context_coroutine)

iterm2.run_forever(main)
