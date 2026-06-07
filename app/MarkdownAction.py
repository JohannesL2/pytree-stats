from __future__ import annotations

import argparse

class MarkdownAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values if values is not None else True)
