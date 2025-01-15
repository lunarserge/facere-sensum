# SPDX-License-Identifier: MIT

"""
facere-sensum debug launcher.
Need to keep this separate to make sure fs.py is imported as a module and
not used as the main script.
"""

from facere_sensum import fs

fs.main()
