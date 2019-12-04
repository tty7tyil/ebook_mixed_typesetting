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

TRIVIAL_CLI_OPTIONS = (
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
TRIVIAL_CLI_OPTIONS_HTMLZ_TO_AZW3 = (
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
        css_file_path = os.path.join(working_dir, NAME_CSS_DIRECTORY, css_file_list[0])
    else:
        pass  # TODO: raise error here
    cli_option_extra_css = '--extra-css="{}"'.format(css_file_path)

    ebook_input_list = os.listdir(os.path.join(working_dir, NAME_EBOOK_INPUT_DIRECTORY))
    for ebook_input in ebook_input_list:
        os.system(' '.join((
            EXECUTABLE_EBOOK_CONVERT,
            '"{}"'.format(os.path.join(working_dir, NAME_EBOOK_INPUT_DIRECTORY, ebook_input)),
            '"{}"'.format(os.path.join(working_dir, NAME_INTERMEDIATE_FILE)),
            cli_option_extra_css,
            *TRIVIAL_CLI_OPTIONS,
        )))

        os.system(' '.join((
            EXECUTABLE_ZIP,
            '-urj0',
            '"{}"'.format(os.path.join(working_dir, NAME_INTERMEDIATE_FILE)),
            '"{}"'.format(os.path.join(working_dir, NAME_FONTS_DIRECTORY)),
        )))

        ebook_output = os.path.splitext(ebook_input)[0] + FORMAT_EBOOK_OUTPUT
        os.system(' '.join((
            EXECUTABLE_EBOOK_CONVERT,
            '"{}"'.format(os.path.join(working_dir, NAME_INTERMEDIATE_FILE)),
            '"{}"'.format(os.path.join(working_dir, NAME_EBOOK_OUTPUT_DIRECTORY, ebook_output)),
            *TRIVIAL_CLI_OPTIONS,
            *TRIVIAL_CLI_OPTIONS_HTMLZ_TO_AZW3,
        )))

        os.remove(os.path.join(working_dir, NAME_INTERMEDIATE_FILE))


if (__name__ == '__main__'):
    main()
