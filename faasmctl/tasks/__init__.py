from invoke import Collection

from . import cli
from . import delete
from . import deploy
from . import flush
from . import generate
from . import invoke
from . import logs
from . import monitor
from . import restart
from . import scale
from . import status
from . import upload
from . import stream

task_ns = Collection(
    cli,
    delete,
    deploy,
    generate,
    flush,
    invoke,
    logs,
    monitor,
    restart,
    scale,
    status,
    upload,
    stream,
)
