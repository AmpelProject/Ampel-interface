#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/cli/ArgParserBuilder.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 17.03.2021
# Last Modified Date: 23.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Union, Any, Tuple
from ampel.cli.AmpelArgumentParser import AmpelArgumentParser


class ArgParserBuilder:
	"""
	Creates one or many instances of AmpelArgumentParser
	"""

	def __init__(self, op: Optional[str] = None) -> None:
		"""
		"""
		self.parsers: dict[str, AmpelArgumentParser] = {}
		self._op = op


	def add_parser(self, name: str, hlp: dict[str, str]):
		self.parsers[name] = AmpelArgumentParser(ampel_op=self._op)
		self.parsers[name].set_help_descr(hlp)
		setattr(self.parsers[name], '_sub_op', name)


	def add_parsers(self, names: list[str], hlp: dict[str, str]):
		for el in names:
			self.add_parser(el, hlp)


	def get(self) -> dict[str, AmpelArgumentParser]:
		""" Returns parsers created during the build procedure """
		return self.parsers


	def add_group(self, target: str, title: str, **kwargs):
		"""
		:param target: see add_arg(...) docstring
		"""
		parsers, group = self.get_targets(target, False)
		for p in parsers:
			p.groups[group] = p.add_argument_group(group, **kwargs)
			p.groups[group].title = title


	def set_group_defaults(self, target: str, **kwargs):
		"""
		:param target: see add_arg(...) docstring
		"""
		parsers, group = self.get_targets(target, True)
		for p in parsers:
			p.groups[group].set_defaults(**kwargs)


	def add_description(self, target: str, descr: Optional[Union[str, list[str]]]) -> None:
		"""
		Calls method 'add_description' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param target: see add_arg(...) docstring
		"""

		parsers, _ = self.get_targets(target, False)
		for p in parsers:
			p.add_description(descr)


	def add_arg(self, target: str, name: str, **kwargs):
		"""
		:param target:
		- str:
			ex: add_arg('optional', 'verbose')
			Adds the argument to the provided group ('target' value) of all underlying parsers.
			For example, if two sub-parsers exist (say one for operation 'show' and one for 'write'),
			both subparsers will feature the argument 'verbose'
		- str.str:
			ex: add_arg('write.required', 'out-file')
			The first part of the string, delimited by '.', targets a sub-parser by name.
			The second part targets an argument group (by name) of the specified subparser(s).
			In the example above, the argument 'out-file' will be added to the group
			with name 'required' of sub-parser with name 'write'.
		- all.str:
			ex: add_arg('all.required', 'out-file'). Same as the first case (str), only explicit
		- str|str.str:
			ex: add_arg('write|show|tail.optional', 'to-json')
			Multiple sub-parsers can be targeted using '|'.
			In the example above, the argument 'to-json' will be added to the
			argument group 'optional' of the sub-parser of the 'write', 'show' and 'tail' sub-operations
		"""

		parsers, group = self.get_targets(target, True)
		for p in parsers:
			p.add_arg(name, group, **kwargs)


	def add_x_args(self, target: str, *args: dict[str, Any]) -> None:
		"""
		Calls method 'add_x_args' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param target: see add_arg(...) docstring
		"""
		parsers, group = self.get_targets(target, True)
		for p in parsers:
			p.add_x_args(group, *args)


	def get_targets(self, target: str, check_group: bool = True) -> tuple[list[AmpelArgumentParser], str]:
		"""
		:param target: see add_arg(...) docstring
		"""
		if "." in target:
			sp = target.split(".")
			parsers = self._get_parsers(sp[0])
			group = sp[1]
		else:
			parsers = self._get_parsers("all")
			group = target

		if check_group:
			for p in parsers:
				if group not in p.groups:
					raise ValueError(
						f"Group '{group}' unknown in parser with name "
						f"\'{getattr(p, '_sub_op')}\', please create it first\n"
					)

		return parsers, group


	def _get_parsers(self, arg: str) -> list[AmpelArgumentParser]:
		"""
		:param arg: string containing one or more parser names.
		Multiple parser names mst be separated by the character "|".
		Unlike parameter 'target' of add_arg(...), not dot ('.') can be used with 'arg'.
		"""

		if "|" in arg:
			pp = arg.split("|")
			for el in pp:
				if el not in self.parsers:
					raise ValueError(f"Unknown parser: '{el}', please create it using add_parser")

			ret1: list[AmpelArgumentParser] = [
				v for k, v in self.parsers.items()
				if k in pp
			]

		elif arg == "all":
			ret1 = list(self.parsers.values())

		else:
			if arg not in self.parsers:
				raise ValueError(f"Unknown parser: '{arg}', please create it using add_parser")
			ret1 = [self.parsers[arg]]

		return ret1


	def create_logic_args(self,
		target: str, name: str, descr: str, metavar: str = "#",
		required: bool = False, pos: Optional[int] = None,
		ref: Optional[str] = None, excl: bool = False,
		json: bool = True, **kwargs
	) -> None:
		"""
		Calls method 'create_logic_args' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param target: see add_arg() docstring
		"""
		parsers, group = self.get_targets(target, True)
		for p in parsers:
			p.create_logic_args(name, group, descr, metavar, required, pos, ref, excl, json)


	def add_note(self, parsers: str, note: str, pos: Optional[int] = None, ref: Optional[str] = None) -> None:
		"""
		Calls method 'add_note' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param parsers: see _get_parsers() docstring
		"""
		for p in self._get_parsers(parsers):
			p.add_note(note, pos, ref)


	def add_all_note(self, note: str, pos: Optional[int] = None, ref: Optional[str] = None) -> None:
		"""
		Calls method 'add_note' (see AmpelArgumentParser docstring) of all the underlying parsers.
		"""
		for p in self.parsers.values():
			p.add_note(note, pos, ref)


	def add_example(self,
		parsers: str, ex: str, prepend=None, append="",
		auto_strip: bool = True, ref: Optional[str] = None
	) -> None:
		"""
		Calls method 'add_example' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param parsers: see _get_parsers() docstring
		"""
		for p in self._get_parsers(parsers):
			p.add_example(
				ex,
				prepend or f"ampel {self._op or ''} {getattr(p, '_sub_op', '')} ",
				append, auto_strip, ref
			)


	def add_all_example(self,
		ex: str, prepend="ampel ", append="", auto_strip: bool = True, ref: Optional[str] = None
	) -> None:
		"""
		Calls method 'add_example' (see AmpelArgumentParser docstring) of all the underlying parsers.
		"""
		for p in self.parsers.values():
			p.add_example(ex, prepend, append, auto_strip, ref)


	def hint_query_logic(self, parsers: str, pos: Optional[int] = None, ref: Optional[str] = None):
		for p in self._get_parsers(parsers):
			p.hint_query_logic(pos, ref)


	def hint_all_query_logic(self, pos: Optional[int] = None, ref: Optional[str] = None):
		for p in self.parsers.values():
			p.hint_query_logic(pos, ref)


	def hint_time_format(self, parsers: str, pos: Optional[int] = None, ref: Optional[str] = None):
		for p in self._get_parsers(parsers):
			p.hint_time_format(pos, ref)


	def hint_all_time_format(self, pos: Optional[int] = None, ref: Optional[str] = None):
		for p in self.parsers.values():
			p.hint_time_format(pos, ref)


	def hint_all_config_override(self, pos: Optional[int] = None, ref: Optional[str] = None):
		for p in self.parsers.values():
			p.hint_config_override(pos, ref)


	def notation_add_note_references(self):
		for p in self.parsers.values():
			p.notation_add_note_references()


	def notation_add_example_references(self):
		for p in self.parsers.values():
			p.notation_add_example_references()
