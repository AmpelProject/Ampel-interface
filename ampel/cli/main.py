#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/cli/main.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.03.2021
# Last Modified Date: 23.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import importlib, sys, re
from os import environ
from pkg_resources import ( # type: ignore[attr-defined]
	get_distribution, AvailableDistributions
)
from typing import Dict, Tuple
from ampel.abstract.AbsCLIOperation import AbsCLIOperation
from ampel.cli.AmpelArgumentParser import AmpelArgumentParser

# key: op name, value: (potential short descr, fqn of corresponding module/class [subclass of AbsCLIOperation])
clis: Dict[str, Tuple[str, str]] = {
	(x := ep.name.split(" "))[0]: (" ".join(x[1:]) if len(x) > 1 else "", ep.module_name)
	for dist_name in AvailableDistributions() if "ampel-" in dist_name
	for ep in get_distribution(dist_name).get_entry_map().get('cli', {}).values()
}

double_minus = re.compile("--([A-z])")

def main() -> None:

	if len(sys.argv) == 1:
		return show_help()

	elif len(sys.argv) == 2:
		if sys.argv[1] in ("-h", "--help", "help"):
			return show_help()
		sys.argv += ["--help"]

	if sys.argv[-1] == 'help':
		sys.argv[-1] = "--help"

	elif len(sys.argv) == 3:
		if not sys.argv[-1].startswith("--"):
			sys.argv += ["--help"]

	# Remove first arg (op name such as 'log' or 'run')
	op_name = sys.argv[1]
	del sys.argv[1]

	# Check if operation is known
	if op_name not in clis:
		return show_help()

	# Remove second arg if sub-opeartion (such as 'show' in 'ampel log show')
	if sys.argv[1][0] == "-":
		sub_op = None
	else:
		sub_op = sys.argv[1]
		del sys.argv[1]

	if env_opts := environ.get("AMPEL_CLI_OPTS"):
		if "--debug" in sys.argv:
			print("[DEBUG] Incorperating options defined by env var AMPEL_CLI_OPTS")
		for el in env_opts.split(" "):
			sys.argv.append(el)

	# Convert "-" to "--" for argparse
	for i in range(len(sys.argv)):
		if sys.argv[i][0] == '-' and sys.argv[i][1] != '-':
			sys.argv[i] = "-" + sys.argv[i]



	try:

		fqn = clis[op_name][1]
		cli_op: AbsCLIOperation = getattr(
			importlib.import_module(fqn),
			fqn.split(".")[-1]
		)()

		parser = cli_op.get_parser(sub_op)
		args, unknown_args = parser.parse_known_args()

		#if not args.config:
		#	return

		if "-debug" in sys.argv:
			print("[DEBUG] Loaded argument parameters")
			for k, v in vars(args).items():
				print(f"  {k}: {v}")

		cli_op.run(vars(args), unknown_args, sub_op)

	except Exception:
		import traceback
		traceback.print_exc(file=sys.stderr)
	return


def show_help() -> None:

	from random import random

	if random() < 0.9:
		print("                                                                                      ")
		print("                               .:-=+++**+++=-:.                                       ")
		print("                            :=******************+-                                    ")
		print("                         .=************************=.                                 ")
		print("                       .+****************************+.                               ")
		print("                      -***********#%%@@%%#*************-                              ")
		print("                     =**********%@@%-.-#%@@%*##%%%%%****+                             ")
		print("                    =**********@@#        @@@@@@@@@@%****=                            ")
		print("                   .**********%@#       #@@@@@@@@@@%******:                           ")
		print("                   =**********%@#   ..%@@@@@@@@@@@#*******=                           ")
		print("                   ************@@%@@@@@@@@@@@@@%#**********                           ")
		print("                   **********%@@@@@@@@@@@@@@%#*************                           ")
		print("                   +*******#@@@@@@@@@@@@@%#***************+                           ")
		print("                   :******#@@@@@@@@@@%#*******************:                           ")
		print("                    =******%@@@%%##**********************+                            ")
		print("                     +**********************************+                             ")
		print("               .::--=======+++*******************+==---##--:::..                      ")
		print("           .:-==================++***********+=--------@@--------:.                   ")
		print("         :=========================+******+=-----------@@=-----------:                ")
		print("       :===+=========================+***=#@*=---------@@+--------=#@#-.              ")
		print("      -====+@#*=========================---+%@%+-------@@*------=#@@+---:             ")
		print("    .=======+@@@%*+===================-------+%@%+-----@@*----=#@@*-------            ")
		print("    =========+@@@@@@#+===============----------+@@%+---#@+---#@@#=--------:           ")
		print("   :===========%@@@@@@@#*============------------+#@#---+--=@@*------------:          ")
		print("   =============#@@@@@@@@@%*+=======------------------=*#*=-=---------------          ")
		print("  .==============#@@@@@@@@@@@%+=====-+*##%%%%%%%%#=--+@@@@@+-+##%%%%%%%%%%#+          ")
		print("  .===========+%#*#@@@@@@@@@@@@%+===-+***********+---=@@@@@=-=++*****++++==-          ")
		print("   ============+@@@@@@@@@@@@@@@@@+==---------------=---+*+--==--------------          ")
		print("   :============+@@@@@@@@@@@@@@@@@+==-----------=#@@=---+---#@%+-----------:          ")
		print("    =============+@@@@@@@@@@@@@@@@%==---------=#@@#----%@+---+%@@*---------           ")
		print("    .=============+@@@@@@@@@@@@@@@%===-------#@@#=-----@@*-----+@@@+------            ")
		print("      -=============#@@@@@@@@@@@@@+====:---+@@#=-------@@*-------+%@@+--:             ")
		print("       :==============+#@@@@@@@@#====-   :=%*=---------@@*---------=*#-.              ")
		print("         :===============++**++====:       :-----------@@*----------:.                ")
		print("           .:===================-.           .:--------#@*-------:.                   ")
		print("               .:--=======--:.                   ..::---+--:::..                      ")

	else:

		print("                              .:-=+++**+++=-:.                                       ")
		print("                           :=******************+-                                    ")
		print("                        .=************************=.                                 ")
		print("                      .+*********##%%%@%%%#*********+.                               ")
		print("                     -*********%@@@@@@@@@@@@%#********-                              ")
		print("                    =********#@@@@@@@@@@@@@@@@@#*******+                             ")
		print("                   =********#@@@@@@@@@@@@@@@@@@@********=                            ")
		print("                  .*********@@@@@@@@@@@@@@@@@@@@%********:                           ")
		print("                  =*********@@@@@@@@@@@@@@@@@@@@%********=                           ")
		print("                  **********@@#***#%@@@@@%****@@%*********                           ")
		print("                  **********#@@*****#@@@*****#@@**********                           ")
		print("                  +**********%@@%#***@@%***#%@@#*********+                           ")
		print("                  :***********%@@@@@@@@@@@@@@@%**********:                           ")
		print("                   =***********%@@@@@@@@@@@@@#**********+                            ")
		print("                    +***********#%@@@@@@@@@%***********+                             ")
		print("              .::--=======+++******%@@@@%#******+==---##--:::..                      ")
		print("          .:-==================++*****#*****+=--------@@--------:.                   ")
		print("        :=========================+******+=-----------@@=-----------:                ")
		print("      :===+=========================+***=#@*=---------@@+--------=#@#-.              ")
		print("     -====+@#*=========================---+%@%+-------@@*------=#@@+---:             ")
		print("   .=======+@@@%*+===================-------+%@%+-----@@*----=#@@*-------            ")
		print("   =========+@@@@@@#+===============----------+@@%+---#@+---#@@#=--------:           ")
		print("  :===========%@@@@@@@#*============------------+#@#---+--=@@*------------:          ")
		print("  =============#@@@@@@@@@%*+=======------------------=*#*=-=---------------          ")
		print(" .==============#@@@@@@@@@@@%+=====-+*##%%%%%%%%#=--+@@@@@+-+##%%%%%%%%%%#+          ")
		print(" .===========+%#*#@@@@@@@@@@@@%+===-+***********+---=@@@@@=-=++*****++++==-          ")
		print("  ============+@@@@@@@@@@@@@@@@@+==---------------=---+*+--==--------------          ")
		print("  :============+@@@@@@@@@@@@@@@@@+==-----------=#@@=---+---#@%+-----------:          ")
		print("   =============+@@@@@@@@@@@@@@@@%==---------=#@@#----%@+---+%@@*---------           ")
		print("   .=============+@@@@@@@@@@@@@@@%===-------#@@#=-----@@*-----+@@@+------            ")
		print("     -=============#@@@@@@@@@@@@@+====:---+@@#=-------@@*-------+%@@+--:             ")
		print("      :==============+#@@@@@@@@#====-   :=%*=---------@@*---------=*#-.              ")
		print("        :===============++**++====:       :-----------@@*----------:.                ")
		print("          .:===================-.           .:--------#@*-------:.                   ")
		print("              .:--=======--:.                   ..::---+--:::..                      ")

	parser = AmpelArgumentParser()
	parser._action_groups.pop()
	ops = parser.add_argument_group("Known operations")
	ops._group_actions = []
	for k, v in clis.items():
		ops.add_argument(k, help=clis[k][0])
	parser.add_note("Type 'ampel <operation> --help' for more info (ex: ampel run --help)")
	parser.print_help()
