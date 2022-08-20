#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/ArgParserBuilder.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                17.03.2021
# Last Modified Date:  20.08.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Any
from ampel.cli.AmpelArgumentParser import AmpelArgumentParser


class ArgParserBuilder:
	"""
	Creates one or many instances of AmpelArgumentParser
	"""

	def __init__(self, op: None | str = None) -> None:
		"""
		"""
		self.parsers: dict[str, AmpelArgumentParser] = {}
		self._op = op


	def add_parser(self, name: str, hlp: dict[str, str]) -> AmpelArgumentParser:
		parser = AmpelArgumentParser(ampel_op=self._op)
		parser.set_help_descr(hlp)
		setattr(parser, '_sub_op', name)
		self.parsers[name] = parser
		return parser


	def add_parsers(self, names: list[str], hlp: dict[str, str]) -> list[AmpelArgumentParser]:
		return [self.add_parser(el, hlp) for el in names]


	def get(self) -> dict[str, AmpelArgumentParser]:
		""" Returns parsers created during the build procedure """
		return self.parsers


	def add_group(self, group: str, title: str, sub_ops: str, **kwargs):
		"""
		:param sub_ops: see arg(...) docstring
		"""
		for p in self.get_parsers(sub_ops):
			p.groups[group] = p.add_argument_group(group, **kwargs)
			p.groups[group].title = title


	def set_group_defaults(self, group: str, sub_ops: str, **kwargs):
		"""
		:param sub_ops: see arg(...) docstring
		"""
		for p in self.get_parsers(sub_ops):
			p.groups[group].set_defaults(**kwargs)


	def description(self, descr: None | str | list[str], sub_ops: str) -> None:
		"""
		Calls method 'add_description' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param sub_ops: see arg(...) docstring
		"""

		for p in self.get_parsers(sub_ops):
			p.add_description(descr)


	def opt(self, opt_name: str, sub_ops: str = 'all', **kwargs):
		return self.arg(opt_name, 'optional', sub_ops, **kwargs)


	def req(self, opt_name: str, sub_ops: str = 'all', **kwargs):
		return self.arg(opt_name, 'required', sub_ops, **kwargs)


	def arg(self, opt_name: str, group: str, sub_ops: str = 'all', **kwargs):
		"""
		:param name: option name
		:param group: group name. Multiple sub-parsers can be targeted using '|'.
		If no is specified, option will be added to all existing subparsers.
		Ex: arg('to-json', 'show|export|tail')
		"""
		for p in self.get_parsers(sub_ops):
			p.arg(opt_name, group, **kwargs)


	def xargs(self, group: str, sub_ops: str, xargs: list[dict[str, Any]]) -> None:
		"""
		Calls method 'x_args' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param sub_ops: see arg(...) docstring
		"""
		for p in self.get_parsers(sub_ops):
			p.xargs(group, *xargs)


	def get_parsers(self, sub_ops: str = 'all') -> list[AmpelArgumentParser]:
		"""
		:param sub_ops: string containing one or more parser names.
		Multiple parsers can be retrieved using the separating character "|".
		"""

		if "|" in sub_ops:
			pp = sub_ops.split("|")
			for el in pp:
				if el not in self.parsers:
					raise ValueError(f"Unknown parser: '{el}', please create it using add_parser")

			ret1: list[AmpelArgumentParser] = [
				v for k, v in self.parsers.items()
				if k in pp
			]

		elif sub_ops == "all":
			ret1 = list(self.parsers.values())

		else:
			if sub_ops not in self.parsers:
				raise ValueError(f"Unknown parser: '{sub_ops}', please create it using add_parser")
			ret1 = [self.parsers[sub_ops]]

		return ret1


	def logic_args(self,
		base_name: str,
		descr: str,
		group: str,
		sub_ops: str = 'all',
		metavar: str = "#",
		required: bool = False,
		pos: None | int = None,
		ref: None | str = None,
		excl: bool = False,
		json: bool = True, **kwargs
	) -> None:
		"""
		Calls method 'create_logic_args' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param sub_ops: see arg() docstring
		"""
		for p in self.get_parsers(sub_ops):
			p.logic_args(base_name, group, descr, metavar, required, pos, ref, excl, json)


	def logic_args_opt(self,
		base_name: str, descr: str, sub_ops: str = 'all', metavar: str = "#", required: bool = False,
		pos: None | int = None, ref: None | str = None, excl: bool = False, json: bool = True, **kwargs
	) -> None:
		self.logic_args(
			base_name, descr, "optional", sub_ops, metavar, required,
			pos, ref, excl, json, **kwargs
		)


	def logic_args_req(self,
		base_name: str, descr: str, sub_ops: str = 'all', metavar: str = "#", required: bool = False,
		pos: None | int = None, ref: None | str = None, excl: bool = False, json: bool = True, **kwargs
	) -> None:
		self.logic_args(
			base_name, descr, "required", sub_ops, metavar, required,
			pos, ref, excl, json, **kwargs
		)


	def note(self,
		note: str,
		sub_ops: str = 'all',
		pos: None | int = None,
		ref: None | str = None
	) -> None:
		"""
		Calls method 'note' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param parsers: see _get_parsers() docstring
		"""
		for p in self.get_parsers(sub_ops):
			p.note(note, pos, ref)


	def example(self,
		sub_ops: str,
		ex: str,
		prepend = None,
		append="",
		auto_strip: bool = True, ref: None | str = None
	) -> None:
		"""
		Calls method 'example' (see AmpelArgumentParser docstring) for the selected parser(s).
		:param parsers: see _get_parsers() docstring
		"""
		for p in self.get_parsers(sub_ops):
			p.example(
				ex,
				prepend or f"ampel {self._op or ''} {getattr(p, '_sub_op', '')} ",
				append, auto_strip, ref
			)


	def hint_query_logic(self, sub_op: str, pos: None | int = None, ref: None | str = None):
		for p in self.get_parsers(sub_op):
			p.hint_query_logic(pos, ref)


	def hint_all_query_logic(self, pos: None | int = None, ref: None | str = None):
		for p in self.parsers.values():
			p.hint_query_logic(pos, ref)


	def hint_time_format(self, sub_ops: str, pos: None | int = None, ref: None | str = None):
		for p in self.get_parsers(sub_ops):
			p.hint_time_format(pos, ref)


	def hint_all_time_format(self, pos: None | int = None, ref: None | str = None):
		for p in self.parsers.values():
			p.hint_time_format(pos, ref)


	def hint_all_config_override(self, pos: None | int = None, ref: None | str = None):
		for p in self.parsers.values():
			p.hint_config_override(pos, ref)


	def notation_add_note_references(self):
		for p in self.parsers.values():
			p.notation_add_note_references()


	def notation_add_example_references(self):
		for p in self.parsers.values():
			p.notation_add_example_references()
