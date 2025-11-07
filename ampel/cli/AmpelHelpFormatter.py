#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/AmpelHelpFormatter.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.03.2021
# Last Modified Date:  30.10.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import re
from argparse import RawTextHelpFormatter

from ampel.cli.LoadAllOfAction import LoadAllOfAction
from ampel.cli.LoadAnyOfAction import LoadAnyOfAction
from ampel.cli.LoadJSONAction import LoadJSONAction

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')


class AmpelHelpFormatter(RawTextHelpFormatter):

	def __init__(self, prog, indent_increment=2, max_help_position=40, width=None):
		super().__init__(
			prog, indent_increment=indent_increment,
			max_help_position=max_help_position, width=width
		)

	def add_usage(self, usage, actions, groups, prefix=None):
		if prefix is None:
			prefix = 'Usage: '
		return super().add_usage(usage, actions, groups, prefix)


	def _format_args(self, action, default_metavar):
		"""
		Use custom representation arguments requiring 2 values or JSON string.
		Also, add two spaces to the left column by default
		for making room for potential mutual exclusivity symbol ("\u22BB")
		"""
		if isinstance(action, LoadAllOfAction | LoadAnyOfAction):
			return "# # ...  "
		if isinstance(action, LoadJSONAction):
			return "'{#}'  "
		return super()._format_args(action, default_metavar) + "  "


	def add_arguments(self, actions):
		for action in actions:
			invocation = super()._format_action_invocation(action)
			visible = ANSI_ESCAPE.sub('', invocation)
			self._custom_action_max_length = max(
				getattr(self, "_custom_action_max_length", 0), len(visible)
			)
		super().add_arguments(actions)


	def _format_action_invocation(self, action): # Replace "--" with "-"
		if len(action.option_strings) and action.option_strings[0][1] == '-':
			action.option_strings[0] = action.option_strings[0][1:]
		return super()._format_action_invocation(action)


	def _format_action(self, action):

		ret = super()._format_action(action)
		if ret.strip()[0] != '-' and "SUPPRESS" not in action.dest:
			ret = ret.replace(action.dest, '\033[1m\033[36m' + action.dest + '\033[0m', 1)

		try:
			# Remove {action1,action2,action3} line from help
			if ANSI_ESCAPE.sub('', ret).lstrip().startswith("{"):
				return "\n".join(ret.split("\n")[1:])
		except Exception:
			pass

		try:
			if (
				'_mutually_exclusive_groups' in (x := action.__dict__['container'].__dict__) and
				x['_mutually_exclusive_groups'] and
				action.metavar != "@"
			):
				for el in x['_mutually_exclusive_groups']:
					if action in el._group_actions: # noqa: SLF001
						insert_pos = len(ret.split('\n')[0])-len(action.help.split('\n')[0]) - 2
						return ret[0:insert_pos] + "\u22BB" + ret[insert_pos+1:]
						# return "\u22BB" + ret[1:]
		except Exception:
			pass

		return ret
