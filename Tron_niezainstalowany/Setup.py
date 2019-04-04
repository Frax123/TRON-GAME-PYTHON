# -*- coding: utf-8 -*-
import cx_Freeze

executables = [cx_Freeze.Executable('Tron.py')]

cx_Freeze.setup(name = 'Tron',
                options = {'build_exe':{'packages': ['pygame'], 'include_files' : ['Red_player.png', 'Blue_player.png', 'Icon.png', 'Wybuch.png']}},
                description = 'Tron: First Chapter',
                executables = executables)