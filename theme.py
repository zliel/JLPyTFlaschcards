from PySide6.QtGui import QPalette, QColor, QFont

# noinspection PyUnresolvedReference
from __feature__ import snake_case, true_property

large_label_font = QFont("Times New Roman", 18)
default_text_font = QFont("Times New Roman", 12)
card_text_font = QFont("Times New Roman", 18)
deck_list_item_font = QFont("Times New Roman", 14)
card_list_item_font = QFont("Times New Roman", 14)
filter_list_item_font = QFont("Times New Roman", 12)
button_font = QFont("Times New Roman", 12)

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
    'highlight': QColor('#0a74a6'),
    'pass': QColor('#23ebcd'),
    'fail': QColor('#ff599c'),
}

# Change "dark" to "background" and have multiple palettes

class PaletteFactory:

    @staticmethod
    def create_palette(theme_name: str) -> QPalette:

        # blue, green, purple, pink
        palettes = {
            'dark_blue': {
                'primary_100': QColor('#76c4e8'),
                'primary_200': QColor('#88caeb'),
                'primary_300': QColor('#98d1ed'),
                'primary_400': QColor('#a8d8f0'),
                'primary_500': QColor('#b7def2'),
                'primary_600': QColor('#c6e5f5'),
                'background_100': QColor('#121212'),
                'background_200': QColor('#282828'),
                'background_300': QColor('#3f3f3f'),
                'background_400': QColor('#575757'),
                'background_500': QColor('#717171'),
                'background_600': QColor('#8b8b8b'),
                'text': QColor('#e8eaf6'),
                'highlight': QColor('#0a74a6'),
                'pass': QColor('#23ebcd'),
                'fail': QColor('#ff599c')
            },
            'dark_purple': {
                'primary_100': QColor('#7b24ff'),
                'primary_200': QColor('#8f43ff'),
                'primary_300': QColor('#a15dff'),
                'primary_400': QColor('#b275ff'),
                'primary_500': QColor('#c18cff'),
                'primary_600': QColor('#cfa3ff'),
                'background_100': QColor('#121212'),
                'background_200': QColor('#282828'),
                'background_300': QColor('#3f3f3f'),
                'background_400': QColor('#575757'),
                'background_500': QColor('#717171'),
                'background_600': QColor('#8b8b8b'),
                'text': QColor('#a15dff'),
                'highlight': QColor('#F6F6F6'),
                'pass': QColor('#23ebcd'),
                'fail': QColor('#ff599c'),
            }
        }

        new_palette = QPalette()
        palette_to_use = palettes[theme_name]

        role_to_color_map = {
            QPalette.ColorRole.Window: palette_to_use['background_100'],
            QPalette.ColorRole.WindowText: palette_to_use['text'],
            QPalette.ColorRole.Base: palette_to_use['background_200'],
            QPalette.ColorRole.AlternateBase: palette_to_use['background_300'],
            QPalette.ColorRole.ToolTipBase: palette_to_use['background_300'],
            QPalette.ColorRole.ToolTipText: palette_to_use['text'],
            QPalette.ColorRole.Text: palette_to_use['text'],
            QPalette.ColorRole.Button: palette_to_use['background_200'],
            QPalette.ColorRole.ButtonText: palette_to_use['primary_500'],
            QPalette.ColorRole.BrightText: palette_to_use['primary_500'],
            QPalette.ColorRole.Highlight: palette_to_use['highlight'],
            QPalette.ColorRole.HighlightedText: palette_to_use['text'],
            QPalette.ColorRole.Accent: palette_to_use['primary_200'],
        }

        for role, color in role_to_color_map.items():
            new_palette.set_color(role, color)

        return new_palette
