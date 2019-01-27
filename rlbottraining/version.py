# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '0.1.0'

release_notes = {

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
