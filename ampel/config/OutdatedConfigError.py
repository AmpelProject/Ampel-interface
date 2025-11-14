#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/config/OutdatedConfigError.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                12.11.2025
# Last Modified Date:  13.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.config.InvalidConfigError import InvalidConfigError

class OutdatedConfigError(InvalidConfigError):
	"""
	Raised when the Ampel configuration is outdated.

	This error indicates that the versions of Ampel components recorded
	in the configuration no longer match the versions currently installed
	in the environment. It is typically triggered during configuration
	loading when version checks are enabled.
	"""
