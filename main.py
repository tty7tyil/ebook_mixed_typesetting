#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# # SHELL COMMANDS IN THE PROCESS
#
# ebook-convert $input_file $intermediate_file --extra-css=$css_file $ec_cli_options_trivial
# zip -urj0 $intermediate_file $fonts_directory
# ebook-convert $intermediate_file $output_file $ec_cli_options_trivial
# rm $intermediate_file

# # EBOOK-CONVERT (EC) CLI OPTIONS TRIVIAL
# # search kw in help: `disable`, `don't`, `preserve`
#
# # epub_specific:
# --preserve-cover-aspect-ratio
# --no-default-epub-cover
# --epub-version="3"
#
# # azw3_specific:
# --no-inline-toc
#
# # general
# --disable-font-rescaling
# --minimum-line-height="0"
# --expand-css
# --margin-top="-1"
# --margin-left="-1"
# --margin-right="-1"
# --margin-bottom="-1"
# --keep-ligatures
# --chapter="/"
# --chapter-mark="none"
# --page-breaks-before="/"
# --disable-remove-fake-margins
# --max-toc-links="0"
# --no-chapters-in-toc

from typing import Mapping, Tuple
import os

EXECUTABLE_EBOOK_CONVERT = 'ebook-convert'
EXECUTABLE_ZIP = 'zip'

EC_CLI_OPTIONS_TRIVIAL: Tuple[str, ...] = (
    '--disable-font-rescaling',
    '--minimum-line-height="0"',
    '--expand-css',
    '--margin-top="-1"',
    '--margin-left="-1"',
    '--margin-right="-1"',
    '--margin-bottom="-1"',
    '--keep-ligatures',
    '--chapter="/"',
    '--chapter-mark="none"',
    '--page-breaks-before="/"',
    '--disable-remove-fake-margins',
    '--max-toc-links="0"',
    '--no-chapters-in-toc',
)
EC_CLI_OPTIONS_TRIVIAL_FORMAT_SPECIFIC: Mapping[str, Tuple[str, ...]] = {
    '.azw3': (
        '--no-inline-toc',
    ),
    '.epub': (
        '--preserve-cover-aspect-ratio',
        '--no-default-epub-cover',
        '--epub-version="3"',
    ),
}

EC_CLI_OPTIONS_REMOVE_ORIGINAL_TYPESETTING: Tuple[str, ...] = (
    '--filter-css="font-family, font-size"',
)

NAME_EBOOK_INPUT_DIRECTORY = 'ebook_input'
NAME_EBOOK_INTERMEDIATE_DIRECTORY = 'ebook_intermediate'
NAME_EBOOK_OUTPUT_DIRECTORY = 'ebook_output'
NAME_FONTS_DIRECTORY = 'source_fonts'
NAME_CSS_DIRECTORY = 'source_css'

FORMAT_EBOOK_INTERMEDIATE = '.epub'
FORMAT_EBOOK_OUTPUT = '.azw3'

working_dir = os.getcwd()


def ebook_convert(
    input_file: str,
    output_file: str,
    *ec_cli_options: str,
) -> None:
    format_output_file = os.path.splitext(output_file)[1]
    os.system(' '.join((
        EXECUTABLE_EBOOK_CONVERT,
        '"{}"'.format(input_file),
        '"{}"'.format(output_file),
        *EC_CLI_OPTIONS_TRIVIAL,
        *(
            EC_CLI_OPTIONS_TRIVIAL_FORMAT_SPECIFIC[
                format_output_file.lower()
            ] if (
                format_output_file.lower()
                in EC_CLI_OPTIONS_TRIVIAL_FORMAT_SPECIFIC
            ) else ()
        ),
        *ec_cli_options,
    )))


def main():
    # temp
    cli_options_keep_intermediate = False
    cli_options_remove_original_typesetting = True
    # temp

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
    ec_cli_options_extra_css = (
        '--extra-css="{}"'.format(css_file_path),
    )

    ebook_input_list = os.listdir(os.path.join(
        working_dir,
        NAME_EBOOK_INPUT_DIRECTORY,
    ))
    for ebook_input in ebook_input_list:
        name_ebook_input, format_ebook_input = os.path.splitext(ebook_input)

        # STAGE 0:
        # prepare input
        ebook_prepare: str = None
        if (cli_options_remove_original_typesetting):
            ebook_prepare = 'prepare_{}'.format(
                name_ebook_input + FORMAT_EBOOK_INTERMEDIATE
            )
            ebook_convert(
                os.path.join(
                    working_dir,
                    NAME_EBOOK_INPUT_DIRECTORY,
                    ebook_input,
                ),
                os.path.join(
                    working_dir,
                    NAME_EBOOK_INPUT_DIRECTORY,
                    ebook_prepare,
                ),
                *EC_CLI_OPTIONS_REMOVE_ORIGINAL_TYPESETTING,
            )
            ebook_input = ebook_prepare

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
        ebook_convert(
            os.path.join(
                working_dir,
                NAME_EBOOK_INPUT_DIRECTORY,
                ebook_input,
            ),
            os.path.join(
                working_dir,
                NAME_EBOOK_INTERMEDIATE_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_INTERMEDIATE,
            ),
            *ec_cli_options_extra_css,
        )

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
        ebook_convert(
            os.path.join(
                working_dir,
                NAME_EBOOK_INTERMEDIATE_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_INTERMEDIATE,
            ),
            os.path.join(
                working_dir,
                NAME_EBOOK_OUTPUT_DIRECTORY,
                name_ebook_input + FORMAT_EBOOK_OUTPUT,
            ),
        )

        # STAGE 4: (optional)
        # remove intermediate file
        if (cli_options_remove_original_typesetting):
            os.remove(os.path.join(
                working_dir,
                NAME_EBOOK_INPUT_DIRECTORY,
                ebook_prepare,
            ))
        if (not cli_options_keep_intermediate):
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
