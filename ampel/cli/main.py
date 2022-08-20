#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/cli/main.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.03.2021
# Last Modified Date:  20.08.2022
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

import os, sys, re, importlib
from pkg_resources import ( # type: ignore[attr-defined]
	get_distribution, AvailableDistributions
)
from ampel.abstract.AbsCLIOperation import AbsCLIOperation
from ampel.cli.AmpelArgumentParser import AmpelArgumentParser

# key: op name, value: (potential short descr, fqn of corresponding module/class [subclass of AbsCLIOperation])
clis: dict[str, tuple[str, str]] = {
	(x := ep.name.replace("_", " ").split(" "))[0]: (" ".join(x[1:]) if len(x) > 1 else "", ep.module_name)
	for dist_name in AvailableDistributions() if "ampel-" in dist_name
	for ep in get_distribution(dist_name).get_entry_map().get('cli', {}).values()
}

double_minus = re.compile("--([A-z])")

def main() -> None:

	# did we implicitly add --help to an otherwise invalid command?
	ambiguous_help = False

	if len(sys.argv) == 1:
		show_help()
		sys.exit(2)

	elif len(sys.argv) == 2:
		if sys.argv[1] in ("-h", "--help", "help"):
			return show_help()
		sys.argv += ["--help"]
		ambiguous_help = True

	if sys.argv[-1] == 'help':
		sys.argv[-1] = "--help"

	elif len(sys.argv) == 3:
		if not sys.argv[-1].startswith("-"):
			sys.argv += ["--help"]
			ambiguous_help = True

	# Remove first arg (op name such as 'log' or 'run')
	op_name = sys.argv[1]
	del sys.argv[1]

	# Check if operation is known
	if op_name not in clis:
		show_help()
		sys.exit(2)

	fqn = clis[op_name][1]
	cli_op: AbsCLIOperation = getattr(
		importlib.import_module(fqn),
		fqn.split(".")[-1]
	)()

	# Remove second arg if sub-opeartion (such as 'show' in 'ampel log show')
	if sys.argv[1][0] == "-" or not cli_op.get_sub_ops():
		sub_op = None
	else:
		sub_op = sys.argv[1]
		del sys.argv[1]

	if env_opts := os.environ.get("AMPEL_CLI_OPTS"):
		if "--debug" in sys.argv:
			print("[DEBUG] Incorporating options defined by env var AMPEL_CLI_OPTS")
		for el in env_opts.split(" "):
			sys.argv.append(el)

	# Convert "-" to "--" for argparse
	for i in range(len(sys.argv)):
		if len(sys.argv[i]) > 2 and sys.argv[i][0] == '-' and sys.argv[i][1] != '-':
			sys.argv[i] = "-" + sys.argv[i]

	parser = cli_op.get_parser(sub_op)
	if ambiguous_help and getattr(parser, 'args_not_required', False):
		del sys.argv[-1]
	try:
		args, unknown_args = parser.parse_known_args()
	except SystemExit as exc:
		# intercept ArgumentParser.exit if we added --help ourselves
		sys.exit(exc.code or (2 if ambiguous_help else 0))

	#if not args.config:
	#	return

	if "-debug" in sys.argv:
		print("[DEBUG] Loaded argument parameters")
		for k, v in vars(args).items():
			print(f"  {k}: {v}")

	cli_op.run(vars(args), unknown_args, sub_op)

	return


def show_help() -> None:

	from random import random

	if random() < 0.7:
		print("                                                                                      ")
		print("\033[1;91m                               .:-**********-:.                                       ")
		autocolor("                            :=*******************-                                    ")
		autocolor("                         .=*************************.                                 ")
		autocolor("                       .+************++***************.                               ")
		autocolor("                      -***********########*************-                              ")
		autocolor("                     =**********####+.+#############****+                             ")
		autocolor("                    =**********###        ###########****=                            ")
		autocolor("                   .**********###       ############******:                           ")
		autocolor("                   =**********###   .+#############*******=                           ")
		autocolor("                   ************##################**********                           ")
		autocolor("                   **********#################*************                           ")
		autocolor("                   +*******################***************+                           ")
		autocolor("                   :******#############*******************:                           ")
		autocolor("                    =******########**********************+                            ")
		autocolor("                     +**********************************+                             ")
		autocolor("               .::--///////*************************===+#+==::..                      ")
		autocolor("           .:-//////////////////***************========###=======:.                   ")
		autocolor("         ://///////////////////////*********===========###===========:                ")
		autocolor("       :///#//////////////////////////***+###+=========###========+###=.              ")
		autocolor("      -////####////////////////////////*===#####=======###======+####===:             ")
		autocolor("    .///////#######///////////////////=======#####=====###====+####=======            ")
		autocolor("    /////////#########///////////////==========#####===###===####+========:           ")
		autocolor("   :///////////##########////////////============####=======###============:          ")
		autocolor("   /////////////#############///////==================#####=================          ")
		autocolor("  .//////////////##############/////=#############+==#######==+############=          ")
		autocolor("  .///////////###################///=#############+==#######==+############=          ")
		autocolor("   ////////////###################//==================#####=================          ")
		autocolor("   :////////////###################//===========+###+=======####===========:          ")
		autocolor("    /////////////##################//=========+####====###===#####=========           ")
		autocolor("    ./////////////#################///=======####+=====###=====#####======            ")
		autocolor("      -/////////////###############////:===####+=======###=======#####==:             ")
		autocolor("       ://////////////###########////.   :+##+=========###=========+##+.              ")
		autocolor("         :///////////////######////:       :===========###==========:.                ")
		autocolor("           .:////////////////////.           .:========###=======:.                   ")
		autocolor("               .:///////////:.                   ..:===+#+===:..                      ")
	else:
		print("                                                                                      ")
		print("\033[1;91m                              .:-**********-:.                                       ")
		autocolor("                           :=*******************-                                    ")
		autocolor("                        .=*************************.                                 ")
		autocolor("                      .+*********##########**********.                               ")
		autocolor("                     -*********###############********-                              ")
		autocolor("                    =********###################*******+                             ")
		autocolor("                   =********####################********=                            ")
		autocolor("                  .*********#####################********:                           ")
		autocolor("                  =*********#####################********=                           ")
		autocolor("                  **********###***########****###*********                           ")
		autocolor("                  **********###*****####*****###**********                           ")
		autocolor("                  +**********####+***###***+####*********+                           ")
		autocolor("                  :***********#################**********:                           ")
		autocolor("                   =***********###############**********+                            ")
		autocolor("                    +***********############***********+                             ")
		autocolor("              .::--///////*********#######**********==+#+==::..                      ")
		autocolor("          .:-//////////////////******###*******=======###=======:.                   ")
		autocolor("        ://///////////////////////****V*****==========###===========:                ")
		autocolor("      :///#/////////////////////////*****+##+=========###========+###=.              ")
		autocolor("     -////####////////////////////////*===#####=======###======+####===:             ")
		autocolor("   .///////#######///////////////////=======#####=====###====+####=======            ")
		autocolor("   /////////#########///////////////==========#####===###===####+========:           ")
		autocolor("  :///////////##########////////////============####======+###============:          ")
		autocolor("  /////////////#############///////==================#####=================          ")
		autocolor(" .//////////////##############/////=#############+==#######==+############=          ")
		autocolor(" .///////////###################///=#############+==#######==+############=          ")
		autocolor("  ////////////###################//==================#####=================          ")
		autocolor("  :////////////###################//===========+###+=======####===========:          ")
		autocolor("   /////////////##################//=========+####====###===#####=========           ")
		autocolor("   ./////////////#################///=======####+=====###=====#####======            ")
		autocolor("     -/////////////###############////:===####+=======###=======#####==:             ")
		autocolor("      ://////////////###########////.   :+##+=========###=========+##+.              ")
		autocolor("        :///////////////######////:       :===========###==========:.                ")
		autocolor("          .:////////////////////.           .:========###=======:.                   ")
		autocolor("              .:///////////:.                   ..:===+#+===:..                      ")

	parser = AmpelArgumentParser()
	parser._action_groups.pop()
	ops = parser.add_argument_group("Known operations")
	ops._group_actions = []

	# Prioretize certain keys
	keys: list[str] = list(clis.keys())
	for el in reversed(['config', 'db', 'job', 'plot', 'log', 't2', 'view']):
		if el in keys:
			keys.insert(0, keys.pop(keys.index(el)))
	for k in keys:
		ops.add_argument('\033[1m\033[36m' + k + '\033[0m', help='\033[1;3m' + clis[k][0] + '\033[0m')
	parser.note("Type \033[1;3m'ampel \033[1m\033[36m<operation>\033[0m\033[1;3m help'\033[0m for more info\n(ex: \033[1;3mampel job help\033[0m)")
	parser.print_help()

def autocolor(txt):

	idx = 0

	idx = len(txt) - len(txt.lstrip())
	last_idx = len(txt.rstrip())
	for i in range(idx, len(txt), 1):
		if txt[i] == '*' and txt[i+1] == '*':
			prev_color = '\033[1;91m'
			break
		elif txt[i] == '/' and txt[i+1] == '/':
			prev_color = '\033[1;93m'
			break
	idx = i
	print(prev_color + txt[0:idx], end='')
	prev_main_color = None

	for i in range(idx, len(txt), 1):
		if i == len(txt) - 1:
			print(prev_color + txt[i:-1], end='')
			break
		if i >= last_idx - 1:
			print(prev_main_color + '\033[1m' + txt[i], end='')
			continue
		elif txt[i] in ('=', '*', '/'):
			if txt[i] == '*':
				prev_color = '\033[1;91m'
			elif txt[i] == '/':
				prev_color = '\033[0;93m'
			elif txt[i] == '=':
				prev_color = '\033[1;92m'
			print(prev_color + '\033[1m' + txt[i], end='')
			prev_main_color = prev_color
		elif txt[i] in (':', '.') and prev_main_color:
			if txt[i-1] == ' ' and '==' in txt[i:]: # quick n dirty
				prev_main_color = '\033[1;92m'
			print(prev_main_color + txt[i], end='')
		else:
			prev_color = '\033[0m'
			print(prev_color + '\033[1m' + txt[i], end='')

	print('\033[0m' + "")
