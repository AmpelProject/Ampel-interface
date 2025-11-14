#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File:                Ampel-interface/ampel/config/InvalidConfigError.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.11.2025
# Last Modified Date:  13.11.2025
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

class InvalidConfigError(Exception):
	"""
	Raised when the Ampel configuration is invalid.

	This error indicates that the configuration structure is incomplete
	or malformed. For example, it may be triggered when the required
	``build`` section is missing, or when other mandatory sections are
	absent or incorrectly defined.
	"""
