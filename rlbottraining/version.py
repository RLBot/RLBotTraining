# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '0.3.4'

release_notes = {
    '0.3.4': '''
        - Added a website to summarize past runs - DomNomNom
        - Made this website pick up live changes (code and results) - DomNomNom
        - Added a syntax highlighting json viewer to view details of results - DomNomNom
        - Fix some directories missing __init__.py files - DomNomNom
        - Made line_goalie save shots on every location of the goal - DomNomNom
        - Provided example json of a Rocket League custom training - Bakkes
        - Added exercise code for Rocket League custom training - DomNomNom
    ''',

    '0.2.1': '''
        - Added support for writing to history_dir - DomNomNom
    ''',

    '0.1.6': '''
        - Started releasing to pypi - DomNomNom
        - Added versioned dependency on rlbot - DomNomNom
        - Allowed people to run the module without typing "python -m" - DomNomNom
        - Make MIT Licence show up in `pip show rlbottraining` - DomNomNom
        - Moved paths into the paths file - DomNomNom
        - Renamed exercises to give a slightly less arbitrary categorization - DomNomNom
        - Fixed goal grader not failing when there is a goal without a player touch - DomNomNom
    ''',

    '0.1.0': '''
        - Start doing release notes - DomNomNom
        - Add Metrics - DomNomNom
        - Big refactor including how MatchConfigs are handled - DomNomNom
    ''',
}


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def get_help_text():
    return 'Trouble? Ask on Discord at https://discord.gg/5cNbXgG ' \
           'or report an issue at https://github.com/RLBot/RLBotTraining/issues'


def print_current_release_notes():
    print(f'Version {__version__}')
    print(get_current_release_notes())
    print(get_help_text())
    print('')
