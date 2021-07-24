#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/cli/AmpelArgumentParser.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.03.2021
# Last Modified Date: 22.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import textwrap
from os import environ
from os.path import isfile
from typing import Dict, Optional, List, Union, Set, Any, Tuple
from ampel.cli.MaybeIntAction import MaybeIntAction
from ampel.cli.LoadJSONAction import LoadJSONAction
from ampel.cli.LoadAnyOfAction import LoadAnyOfAction
from ampel.cli.LoadAllOfAction import LoadAllOfAction
from argparse import ArgumentParser, _ArgumentGroup
from ampel.cli.AmpelHelpFormatter import AmpelHelpFormatter


class AmpelArgumentParser(ArgumentParser):
	"""
	Argument parser with additional features.
	Supports adding notes and examples.

	Some differences with ArgumentParser:
	- The "required argument" group is placed first
	- The "-h --help" line is not printed
	- Every section is capitalized
	- Argument values are represented by hash rather than capitalized argument names:
		* ArgumentParser: -parameter PARAMETER [PARAMETER ...]
		* This:           -parameter # [# ...]
	- New representations were added:
		* Arguments requiring at least two values: -parameter # # ...
		* Arguments requiring a JSON string: -parameter '{#}'
	- A "notation section" is generated dynamically and added automatically
	- The arguments column (left) is larger (width of 40 vs 27 for ArgumentParser's default formatter)

	Note:
	The parameter -config (path to an ampel config file) is automatically moved from the
	*required* argument group to the *optional* argument group if the environment variable
	AMPELCONF exists and points to a valid file. In this case, a note is added and
	"-config ampel_conf.yaml" is stripped out of added examples automatically (deactivable)

	Conveniences methods:
	- move_group_up: moves a group up in order
	- create_logic_args: creates 4 arguments for a given name.
	  For example, parser.create_opt_logic_args("channel", "Channel") will create:
	  -channel #                 Channel to be matched (non-exclusively)
	  -channels-or # # ...       Channels to be matched (OR connected)
	  -channels-and # # ...      Channels to be matched (AND connected)
	  -channels-json '{#}'       Channels to be matched (JSON, see note below)
	  whereby a note regarding parameters with suffix *-json is added automatically.
	  The values of channels-or, channels-and and channels-json have 'channel' as destination
	  so that the calling code should not have to differenciate between these.
	  Moreover, each generated argument is associated with a dedicated action:
	  MaybeIntAction, LoadAnyOfAction, LoadAllOfAction and LoadJSONAction in ampel/cli

	See the class ampel.cli.T2Command for an full utilization of this class
	"""

	def __init__(self, ampel_op: Optional[str] = None, **kwargs) -> None:

		super().__init__(formatter_class=AmpelHelpFormatter, **kwargs)
		self.notes: List[str] = []
		self.examples: List[str] = []
		self.args_descr: Dict[str, str] = {}
		self._logic_ops_note_added = False
		self.notations: Set[Union[str, Tuple[str, str]]] = set()
		self.has_env_conf = False
		self.groups: Dict[str, _ArgumentGroup] = {}
		self.bullet = "\u2022"
		self.usage = "" # required by argparse (AssertionError), unclear why
		self._ampel_op = ampel_op

		self.spacer = "  "
		self.note_open = "["
		self.note_close = "]"
		self.ex_open = "|"
		self.ex_close = "|"


		# Pop optional group to reorder it, putting required arguments first (really questionable defaults there...)
		optional_group = self._action_groups.pop()

		# Add a reference by name
		self.groups["optional"] = optional_group

		# Suppress "-h, --help show this help message and exit" (chicken and egg)
		# optional._option_string_actions = {}
		optional_group._group_actions = []

		# Capitalize title
		optional_group.title = optional_group.title.capitalize() # type: ignore

		# Add required argument group (first pos)
		self.groups["required"] = self.add_argument_group('Required arguments')

		# Re-insert optional group
		self._action_groups.append(optional_group)

		if "AMPELCONF" in environ and environ["AMPELCONF"]:
			if isfile(environ["AMPELCONF"]):
				self.has_env_conf = True
			else:
				print("\n=================================================================")
				print("Warning: environment variable AMPELCONF points to an invalid file")
				print("=================================================================")


	def set_ampel_sub_op(self, name: str) -> None:
		self.ampel_sub_op = name
	

	def set_bullet(self, bullet: str) -> None:
		""" Used for notes and examples. Bots might require markdown """
		self.bullet = bullet


	def add_group(self, name: str, title: str, **kwargs):
		self.groups[name] = self.add_argument_group(name, **kwargs)
		self.groups[name].title = title


	def set_group_defaults(self, name: str, **kwargs):
		self.groups[name].set_defaults(**kwargs)


	def add_description(self, descr: Optional[Union[str, List[str]]]) -> None:

		if not descr:
			return

		if isinstance(descr, str):
			descr = [
				ell for el in descr.split("\n")
				for ell in textwrap.wrap(el, width=100)
			]

		if self.description is None:
			self.description = self.spacer

		self.description += f"\n{self.spacer}".join(descr)


	def move_group_up(self, group: _ArgumentGroup):
		if (p := self.get_group_index_pos(group)) > 0:
			self._action_groups.remove(group)
			self._action_groups.insert(p - 1, group)


	def get_group_index_pos(self, group: _ArgumentGroup) -> int:
		for i, el in enumerate(self._action_groups):
			if el == group:
				return i
		return -1


	def get_group(self, name: str) -> Optional[_ArgumentGroup]:
		return self.groups.get(name)


	def add_arg(self,
		name: str, group: Union[str, _ArgumentGroup] = "optional",
		help: Optional[str] = None, **kwargs
	) -> None:
		"""
		:param target:
		Example:
			- add_arg("verbose", "optional")
			- add_arg("out", "required")
		"""

		self._auto_metavar(kwargs)

		# Add only the nomemclature elements that are actually used
		if "const" in kwargs:
			self.notations.add(("-argument [#]", "Argument with an overridable default value"))
		elif kwargs.get("nargs") == "+":
			self.notations.add(("-argument # [# ...]", "Argument accepting one or more values"))
		elif isinstance(kwargs.get("action"), str):
			self.notations.add(("-argument", "Argument without value (flag)"))
		else:
			self.notations.add(("-argument #", "Argument requiring one value"))

		if name == "config" and group == "required" and self.has_env_conf:
			self.add_note(f"{environ['AMPELCONF']} will be used unless an override using -config is specified")
			group = "optional"

		if isinstance(group, str):
			group = self.groups[group]

		group.add_argument(
			f"--{name}", help=help or self.args_descr.get(name),
			required=True if group == self.groups["required"] else False, **kwargs
		)


	def add_x_args(self, group: str = "optional", *args: Dict[str, Any]):
		"""
		Create a mutually exclusive group, attach it to the group defined in 'target'
		and add arguments to it according to provided definitions (*args)
		"""
		self.notation_add_mutual_exclusivity()

		try:
			# Add newline between mutually excl groups
			if (
				self.groups[group]._mutually_exclusive_groups[-1]._actions[-1].dest ==
				self.groups[group]._actions[-1].dest
			):
				last_args = self.groups[group]._option_string_actions[
					list(self._option_string_actions.keys())[-1]
				]
				last_args.help = (last_args.help or "") + "\n\n"
		except Exception:
			pass
		x = self.groups[group].add_mutually_exclusive_group()
		for arg in args:
			self.add_arg(group=x, **arg)


	def _auto_metavar(self, kw: Dict) -> None:
		if "dest" in kw or "metavar" in kw:
			return
		if (a := kw.get("action")) and a != MaybeIntAction:
			return
		kw['metavar'] = "#"


	def set_help_descr(self, args_descr: Dict) -> None:
		""" Sets help parameter descriptions """
		self.args_descr = args_descr


	def add_note(self, note: str, pos: Optional[int] = None, ref: Optional[str] = None) -> None:
		""" Newlines in note are supported and will be properly formatted """

		notes = note.split("\n")
		for i in range(len(notes)):
			if len(notes[i]) > 100:
				notes[i:i+1] = textwrap.wrap(notes[i], width=100)

		start = f"{self.spacer}{self.bullet} "
		content = start

		if ref:
			if ref == "#":
				raise ValueError("Hash sign cannot be used as ref")
			content += f"{self.note_open}{ref}{self.note_close} "

		for i, el in enumerate(notes):
			if i > 0:
				content += "\n" + " " * len(start)
			content += el

		if pos is not None:
			self.notes.insert(pos, content)
		else:
			self.notes.append(content)


	def add_notes(self, notes: List[str]) -> None:
		""" Each note will start with a bullet """
		for el in notes:
			self.add_note(el)


	def add_example(self,
		ex: str, prepend="ampel ", append="", auto_strip_config: bool = True,
		ref: Optional[str] = None
	) -> None:
		if ref:
			prepend = f"{self.ex_open}{ref}{self.ex_close} {prepend}"
		payload = f"{self.spacer}{self.bullet} {prepend}{ex}{append}"
		if auto_strip_config and self.has_env_conf:
			self.examples.append(payload.replace(" -config ampel_conf.yaml ", " "))
		else:
			self.examples.append(payload)


	def create_logic_args(self,
		name: str, group: str, descr: str, metavar: str = "#",
		required: bool = False, pos: Optional[int] = None,
		ref: Optional[str] = None, excl: bool = False,
		**kwargs
	) -> None:
		"""
		Ex: channel, channels-and, channels-or, channels-json
		Ex: with-tag, with-tags-and, with-tags-or, with-tags-json
		"""
		
		what = "excluded" if excl else "matched"
		dest = name.replace("-", "_")

		# Cosmetic
		if not self._logic_ops_note_added:
			last_args = self.groups[group]._option_string_actions[
				list(self._option_string_actions.keys())[-1]
			]
			last_args.help = (last_args.help or "") + "\n\n"

		self.notation_add_mutual_exclusivity()
		self.notations.add(("-argument # # ...", "Argument requiring at least two values"))
		
		mux = self.groups[group].add_mutually_exclusive_group(required=required)
		mux.add_argument(
			f"--{name}", metavar=metavar,
			type=str, nargs=1, default=None, action=MaybeIntAction,
			help=f"{descr} to be {what} (non-exclusively)"
		)

		mux.add_argument(
			f"--{name}s-or", dest=dest, action=LoadAnyOfAction,
			metavar=metavar, type=str, default=None, nargs="+",
			help=f"{descr}s to be {what} (OR connected)"
		)

		mux.add_argument(
			f"--{name}s-and", dest=dest, action=LoadAllOfAction,
			metavar=metavar, type=str, default=None, nargs="+",
			help=f"{descr}s to be {what} (AND connected)"
		)

		suffix = f"{self.note_open}{ref}{self.note_close}" if ref else ""
		mux.add_argument(
			f"--{name}s-json", dest=dest, action=LoadJSONAction,
			metavar=metavar, type=str, default=None,
			help=f"{descr}s to be {what} {suffix}\n\n"
		)

		# Add note about JSON arg
		if not self._logic_ops_note_added:
			self.add_note(
				"Allows the use of logic operators such as:\n" +
				"Nested logic: \'{\"any_of\": [\"VAL1\", {\"all_of\": [\"VAL2\", \"VAL3\"]}]}\'\n" +
				"Exclusive match: \'{\"one_of\": [\"VAL1\"]}\'", pos=pos, ref=ref
			)
			self._logic_ops_note_added = True


	# Cosmetic
	def error(self, message: str) -> Any:
		""" As for now, there is no better way to do this  """
		if "-" in message:
			message = message.replace(" --", " -")
		if message.startswith("the following arguments are required:"):
			if len(message.split("-")) == 2:
				return super().error(message.replace("arguments are", "argument is"))
		return super().error(message)


	def notation_add_note_references(self):
		self.notations.add(f"{self.spacer}Note references are marked with [ ]")


	def notation_add_example_references(self):
		self.notations.add(f"{self.spacer}Example references are marked with | |")


	def notation_add_mutual_exclusivity(self):
		self.notations.add(
			f"{self.spacer}Consecutive mutually exclusive arguments are marked with \u22BB"
		)
		

	def hint_query_logic(self, pos: Optional[int] = None, ref: Optional[str] = None):
		self.add_note(
			"Matching criteria related to different keys are AND-combined with each other",
			pos, ref
		)


	def hint_time_format(self, pos: Optional[int] = None, ref: Optional[str] = None):
		self.add_note(
			"Date-time strings are parsed using datetime.fromisoformat(<value>).\n" +
			"Example of supported formats (unexhaustive): 2011-11-04 or 2011-11-04T00:05:23",
			pos, ref
		)


	def hint_config_override(self, pos: Optional[int] = None, ref: Optional[str] = None):
		self.add_note(
			"Any existing config parameter can be overriden using -path.to.config.key value\n" +
			"Example: -db.prefix AmpelTest",
			pos, ref
		)


	def print_help(self,  # type: ignore[override]
		show_description: bool = True,
		show_usage: bool = True,
		show_notation: bool = True,
		show_arguments: bool = True,
		show_notes: bool = True,
		show_examples: bool = True
	):

		if show_description and self.description:
			print("\nOperation:\n" + self.description)

		if show_usage:
			print("\nUsage:")
			sub_op = getattr(self, "ampel_sub_op", None) # ex: show
			if self._ampel_op:
				if sub_op: # "ampel log show"
					print(f"{self.spacer}ampel {self._ampel_op} {sub_op} <arguments>")
				else: # "ampel run" (No sub-op/action defined)
					print(f"{self.spacer}ampel {self._ampel_op} <arguments>")
			else: # "ampel"
				print(f"{self.spacer}ampel <operation> <arguments>")

		# Core (arguments) help section
		formatter = self._get_formatter()
		for action_group in self._action_groups:
			formatter.start_section(action_group.title)
			formatter.add_text(action_group.description)
			formatter.add_arguments(action_group._group_actions)
			formatter.end_section()

		fh = formatter.format_help()

		# Cosmetic: use numbers for references
		fh = self._numerate(fh, self.notes, self.note_open, self.note_close)
		fh = self._numerate(fh, self.examples, self.ex_open, self.ex_open)

		if show_notation and self.notations:
			cw = getattr(formatter, "_action_max_length", 30) # col width
			print("\nNotation:")
			if (x := sorted([v for v in self.notations if isinstance(v, str)], key=lambda x: len(x))):
				print("\n".join(x) + "\n")
			raw_not = sorted(
				[v for v in self.notations if isinstance(v, tuple)],
				key=lambda x: len(x[0])
			)
			print("\n".join([self._format(v[0], v[1], cw) for v in raw_not]))

		if show_arguments:
			print("\n" + fh, end="")

		if show_notes and self.notes:
			# Put numerated notes first
			print("\nNote%s:" % ("s" if len(self.notes) > 1 else ""))
			print("\n".join(self._sort(self.notes)))

		if show_examples and self.examples:
			print("\nExample%s:" % ("s" if len(self.examples) > 1 else ""))
			print("\n".join(self._sort(self.examples)) + "\n")

		if self.epilog:
			print(self.epilog.strip())

		print("")


	def _format(self, k: str, v: str, l: int) -> str:
		filler = (l - len(k) - 1) * " "
		return self.spacer + k + filler + v


	def _numerate(self, fh: str, target: List[Any], open_key: str, close_key: str) -> str:
		try:
			l: List[str] = []
			y = 1
			for i, el in enumerate(target):
				if isinstance(el, str) and el[4] == open_key:
					l.append(el[5])
					target[i] = el[:5] + str(y) + el[6:]
					y += 1
			for i, el in enumerate(l, 1):
				fh = fh.replace(
					open_key + el + close_key,
					open_key + str(i) + close_key
				)
		except Exception:
			pass

		return fh

	def _sort(self, target: List[Any]) -> List[str]:
		""" # Put numerated notes/examples first. If not notes, then examples """
		opn = self.note_open if target == self.notes else self.ex_open
		return [el for el in target if el[4] == opn] + \
			[el for el in target if el[4] != opn]


	@classmethod
	def build_choice_help(cls,
		op: str, sub_ops: List[str], hlp: Dict[str, str],
		description: Optional[str] = None
	) -> 'AmpelArgumentParser':

		parser = AmpelArgumentParser(ampel_op=op)
		parser.set_ampel_sub_op("<action>")

		if description:
			parser.add_description(description)

		sp_action = parser.add_subparsers(parser_class=cls)
		parser._action_groups[0].title = "Actions"

		for s in sub_ops:
			sp_action.add_parser(s, help=hlp.get(s))

		return parser
