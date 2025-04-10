# CLInterface

*CLInterface* is a simple library to display tab-completion prompts
and interactive menus.

## Preliminary steps

Import modules

    from clinterface.completion import *
    from clinterface.selection import *

Define options

    option_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    option_dict = {'Mon':'Monday', 'Tues':'Tuesday', 'Wed':'Wednesday', 'Thurs':'Thursday', 'Fri':'Friday', 'Sat':'Saturday', 'Sun':'Sunday'}

## Completion

Complete a file path

    complete_filepath(prompt='Write path to file (press TAB to autocomplete)')

Complete a directory path

    complete_dirpath(prompt='Write path to directory (press TAB to autocomplete)')

Complete a binary choice

    complete_binary_choice(prompt='Do you want to continue?', truthy_options=['yes', 'ok'], falsy_options=['no'])

Complete one or several choices

    complete_choices(prompt='Choose the best day of the week:', options=option_list, num_choices=1)
    complete_choices(prompt='Choose the three best days of the week:', options=option_list, num_choices=3)

## Selection

Select a single option:

    select_option(prompt='Choose the best day of the week:', options=option_dict)
    select_option(prompt='Choose the best day of the week:', options=option_dict, default='Fri')
    select_option(prompt='Choose the best day of the week:', options=option_list, default='Friday')

Select multiple options:

    select_options(prompt='Choose the three best days of the week:', options=option_dict)
    select_options(prompt='Choose the three best days of the week:', options=option_dict, defaults=['Fri','Sat','Sun'])
    select_options(prompt='Choose the three best days of the week:', options=option_list, defaults=['Friday','Saturday','Sunday'])
    select_options(prompt='Choose the three best days of the week:', options=option_dict, defaults=['Fri','Sat','Sun'], num_choices=3)

Create a customized selector and pass it to the function:

    customized_selector = Selector(radiobullet = '>', checkbullet = 'X')
    select_options(prompt='Choose the three best days of the week:', options=option_dict, defaults=['Fri','Sat','Sun'], selector=customized_selector)