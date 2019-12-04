#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# # shell commands for ebook conversion
#
# ebook-convert
# $/path/to/input_file
# $/path/to/intermediate.htmlz
# --extra-css=$/path/to/css_file
#
# # search for `disable`, `preserve`, `don't`
#
# --no-inline-toc
# --disable-font-rescaling
# --minimum-line-height=0
# --expand-css
# --margin-top=-1
# --margin-left=-1
# --margin-right=-1
# --margin-bottom=-1
# --keep-ligatures
# --chapter="/"
# --chapter-mark="none"
# --page-breaks-before="/"
# --disable-remove-fake-margins
# --max-toc-links=0
# --no-chapters-in-toc
#
#
# zip -urj0 $/path/to/intermediate.htmlz $/path/to/fonts_directory
# ebook-convert $/path/to/intermediate.htmlz $/path/to/output_file $trivial_options
# rm $/path/to/intermediate.htmlz

import os

EXECUTABLE_EBOOK_CONVERT = 'ebook-convert'
EXECUTABLE_ZIP = 'zip'

CLI_OPTIONS_TRIVIAL = (
    '--disable-font-rescaling',
    '--minimum-line-height=0',
    '--expand-css',
    '--margin-top=-1',
    '--margin-left=-1',
    '--margin-right=-1',
    '--margin-bottom=-1',
    '--keep-ligatures',
    '--chapter="/"',
    '--chapter-mark="none"',
    '--page-breaks-before="/"',
    '--disable-remove-fake-margins',
    '--max-toc-links=0',
    '--no-chapters-in-toc',
)
CLI_OPTIONS_TRIVIAL_HTMLZ_TO_AZW3 = (
    '--no-inline-toc',
)

NAME_INTERMEDIATE_FILE = 'intermediate.htmlz'
NAME_EBOOK_INPUT_DIRECTORY = 'ebook_input'
NAME_EBOOK_OUTPUT_DIRECTORY = 'ebook_output'
NAME_FONTS_DIRECTORY = 'source_fonts'
NAME_CSS_DIRECTORY = 'source_css'

FORMAT_EBOOK_OUTPUT = '.azw3'

working_dir = os.getcwd()


def main():
    css_file_list = os.listdir(os.path.join(working_dir, NAME_CSS_DIRECTORY))
    css_file_path: str = None
    if (len(css_file_list) == 1):
        css_file_path = os.path.join(
            working_dir,
            NAME_CSS_DIRECTORY,
            css_file_list[0],
        )
    else:
        pass  # TODO: raise error here
    cli_option_extra_css = '--extra-css="{}"'.format(css_file_path)

    ebook_input_list = os.listdir(os.path.join(
        working_dir,
        NAME_EBOOK_INPUT_DIRECTORY,
    ))
    for ebook_input in ebook_input_list:
        ebook_name, format_ebook_input = os.path.splitext(ebook_input)

        print(''.join((
            '\n>> Converting \'{}\'\n'.format(ebook_name),
            '>> State: {} --> {}, embedding css file\n'.format(
                format_ebook_input.upper(),
                '.HTMLZ (intermediate)',
            ),
        )))
        os.system(' '.join((
            EXECUTABLE_EBOOK_CONVERT,
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_EBOOK_INPUT_DIRECTORY,
                ebook_input,
            )),
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_INTERMEDIATE_FILE,
            )),
            cli_option_extra_css,
            *CLI_OPTIONS_TRIVIAL,
        )))

        print(''.join((
            '\n>> Converting \'{}\'\n'.format(ebook_name),
            '>> State: embedding font files\n',
        )))
        os.system(' '.join((
            EXECUTABLE_ZIP,
            '-urj0',
            '"{}"'.format(os.path.join(working_dir, NAME_INTERMEDIATE_FILE)),
            '"{}"'.format(os.path.join(working_dir, NAME_FONTS_DIRECTORY)),
        )))

        print(''.join((
            '\n>> Converting \'{}\'\n'.format(ebook_name),
            '>> State: {} --> {}\n'.format(
                '.HTMLZ (intermediate)',
                FORMAT_EBOOK_OUTPUT.upper(),
            ),
        )))
        os.system(' '.join((
            EXECUTABLE_EBOOK_CONVERT,
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_INTERMEDIATE_FILE,
            )),
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_EBOOK_OUTPUT_DIRECTORY,
                ebook_name + FORMAT_EBOOK_OUTPUT,
            )),
            *CLI_OPTIONS_TRIVIAL,
            *CLI_OPTIONS_TRIVIAL_HTMLZ_TO_AZW3,
        )))

        print(''.join((
            '\n>> Converting \'{}\'\n'.format(ebook_name),
            '>> State: removing intermediate file\n',
        )))
        os.remove(os.path.join(working_dir, NAME_INTERMEDIATE_FILE))


if (__name__ == '__main__'):
    main()
