# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '0.6.1'

release_notes = {
    '0.6.1': '''
        - New kickoff training added. - ViliamVadocz
        - Added fast test for all common exercises. - DomNomNom
        - Updates to common exercises. - jeroen11dijk, tarehart
        - Don't reload the agent if the reload policy is set to never - RLMarvin
    ''',
    '0.5.1': '''
        - Allowed rendering to be disabled via and argument. - DomNomNom
        - Version bump to fix encoding errors in the linkuru challenge. - DomNomNom
    ''',
    '0.4.3': '''
        - Added an `on_briefing` phase to provide parameters to bots using matchcomms - DomNomNom
        - Fix trying to use a closed matchcomms - DomNomNom
        - Checked the assumption that graders are always reset due to exercises being used once - DomNomNom
    ''',

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
