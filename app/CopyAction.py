from __future__ import annotations

import argparse


class CopyAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, True)
