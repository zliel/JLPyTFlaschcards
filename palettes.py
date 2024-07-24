from PySide6.QtGui import QPalette, QColor, QFont

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

large_label_font = QFont("Times New Roman", 18)
default_text_font = QFont("Times New Roman", 12)

palette = {
    'primary_100': QColor('#76c4e8'),
    'primary_200': QColor('#88caeb'),
    'primary_300': QColor('#98d1ed'),
    'primary_400': QColor('#a8d8f0'),
    'primary_500': QColor('#b7def2'),
    'primary_600': QColor('#c6e5f5'),
    'dark_100': QColor('#121212'),
    'dark_200': QColor('#282828'),
    'dark_300': QColor('#3f3f3f'),
    'dark_400': QColor('#575757'),
    'dark_500': QColor('#717171'),
    'dark_600': QColor('#8b8b8b'),
    'text': QColor('#e8eaf6'),
    'highlight': QColor('#0a74a6')
}

role_to_color_map = {
    QPalette.ColorRole.Window: palette['dark_100'],
    QPalette.ColorRole.WindowText: palette['text'],
    QPalette.ColorRole.Base: palette['dark_200'],
    QPalette.ColorRole.AlternateBase: palette['dark_300'],
    QPalette.ColorRole.ToolTipBase: palette['dark_300'],
    QPalette.ColorRole.ToolTipText: palette['text'],
    QPalette.ColorRole.Text: palette['text'],
    QPalette.ColorRole.Button: palette['dark_300'],
    QPalette.ColorRole.ButtonText: palette['primary_500'],
    QPalette.ColorRole.BrightText: palette['primary_500'],
    QPalette.ColorRole.Highlight: palette['highlight'],
    QPalette.ColorRole.HighlightedText: palette['text'],
    QPalette.ColorRole.Accent: palette['primary_200'],
}

blue_dark_palette = QPalette()

for role, color in role_to_color_map.items():
    blue_dark_palette.set_color(role, color)