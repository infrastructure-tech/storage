#!/usr/bin/env python3
import eons
from fs.contrib.tahoelafs import TahoeLAFS
from pathlib import Path

# Expose a Tahoe LAFS web client via a FUSE mount on linux.
# This Functor will spawn a long running server process.
class Tahoe(eons.Functor):
    def __init__(this, name="Tahoe S3"):
        super().__init__(name)

        this.arg.kw.required.append('tahoe_cap')

        this.arg.kw.optional['tahoe_client_url'] = 'http://127.0.0.1:3456'
        this.arg.kw.optional['mount_point'] = Path('/mnt/tahoe')
        this.arg.kw.optional['mount_options'] = [
            'allow_other',
        ]


    def Function(this):
        tahoe = TahoeLAFS(this.tahoe_cap, webapi_url=this.tahoe_client_url, autorun=False)

        # Mount the Tahoe LAFS web client via FUSE
        tahoe.mount(this.mount_point, options=this.mount_options)


if (__name__ == '__main__'):
    executor = eons.Executor()
    executor()
    Tahoe()(executor=executor)