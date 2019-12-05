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

EC_CLI_OPTIONS_TRIVIAL = (
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
EC_CLI_OPTIONS_TRIVIAL_AZW3 = (
    '--no-inline-toc',
)

NAME_EBOOK_INPUT_DIRECTORY = 'ebook_input'
NAME_EBOOK_INTERMEDIATE_DIRECTORY = 'ebook_intermediate'
NAME_EBOOK_OUTPUT_DIRECTORY = 'ebook_output'
NAME_FONTS_DIRECTORY = 'source_fonts'
NAME_CSS_DIRECTORY = 'source_css'

FORMAT_EBOOK_INTERMEDIATE = '.epub'
FORMAT_EBOOK_OUTPUT = '.azw3'

working_dir = os.getcwd()


def main():
    # temp
    cli_options_keep_intermediate = True

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
    ec_cli_options_extra_css = '--extra-css="{}"'.format(css_file_path)

    ebook_input_list = os.listdir(os.path.join(
        working_dir,
        NAME_EBOOK_INPUT_DIRECTORY,
    ))
    for ebook_input in ebook_input_list:
        name_ebook_input, format_ebook_input = os.path.splitext(ebook_input)

        # STAGE 1:
        # convert from input to intermediate
        # embed extra css file
        print(''.join((
            '\n>> Converting \'{}\'\n'.format(name_ebook_input),
            '>> Stage: {} --> {} (intermediate)'.format(
                format_ebook_input[1:].upper(),
                FORMAT_EBOOK_INTERMEDIATE[1:].upper(),
            ),
            ', embedding extra css file\n',
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
                NAME_EBOOK_INTERMEDIATE_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_INTERMEDIATE,
            )),
            ec_cli_options_extra_css,
            *EC_CLI_OPTIONS_TRIVIAL,
        )))

        # STAGE 2:
        # embed font files
        print(''.join((
            '\n>> Converting \'{}\'\n'.format(name_ebook_input),
            '>> Stage: embedding font files\n',
        )))
        os.system(' '.join((
            EXECUTABLE_ZIP,
            '-urj0',
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_EBOOK_INTERMEDIATE_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_INTERMEDIATE,
            )),
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_FONTS_DIRECTORY,
            )),
        )))

        # STAGE 3:
        # convert from intermediate to output
        print(''.join((
            '\n>> Converting \'{}\'\n'.format(name_ebook_input),
            '>> Stage: {} (intermediate) --> {}\n'.format(
                FORMAT_EBOOK_INTERMEDIATE[1:].upper(),
                FORMAT_EBOOK_OUTPUT[1:].upper(),
            ),
        )))
        command = (' '.join((
            EXECUTABLE_EBOOK_CONVERT,
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_EBOOK_INTERMEDIATE_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_INTERMEDIATE,
            )),
            '"{}"'.format(os.path.join(
                working_dir,
                NAME_EBOOK_OUTPUT_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_OUTPUT,
            )),
            *EC_CLI_OPTIONS_TRIVIAL,
        )))
        if (FORMAT_EBOOK_OUTPUT.lower() == '.azw3'.lower()):
            command = (' '.join((
                command,
                *EC_CLI_OPTIONS_TRIVIAL_AZW3,
            )))
        os.system(command)

        # STAGE 4: (optional)
        # remove intermediate file
        if (cli_options_keep_intermediate is not True):
            print(''.join((
                '\n>> Converting \'{}\'\n'.format(name_ebook_input),
                '>> Stage: removing intermediate file\n',
            )))
            os.remove(os.path.join(
                working_dir,
                NAME_EBOOK_INTERMEDIATE_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_INTERMEDIATE,
            ))


if (__name__ == '__main__'):
    main()
