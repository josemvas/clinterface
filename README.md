# CLInterface

*CLInterface* is a simple library to display tab-completion prompts
and interactive menus.

Import the module

    from clinterface import prompts

## Completer class

    completer = prompts.Completer()

### Binary choice completer

    completer.binary_choice(prompt='Do you want to continue?', truthy_options=[yes', 'ok'], falsy_options=['no'])

### Path completer

    completer.file_path('Write a file path (press TAB to autocomplete)')

## Selector class

Create a default selector instance

    selector = prompts.Selector()

or a customized selector instance

    selector = prompts.Selector(
        shift = 1,
        indent = 3,
        align = 2,
        margin = 1,
        pad_left = 1,
        pad_right = 1,
        radiobullet = '*',
        checkbullet = 'X',
    )

Define options with a list:

    option_list = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
    ]

or with a dictionary:

    option_dict = {
        'Mon':'Monday',
        'Tues':'Tuesday',
        'Wed':'Wednesday',
        'Thurs':'Thursday',
        'Fri':'Friday',
        'Sat':'Saturday',
        'Sun':'Sunday',
    }

### Single choice selector

    prompt = 'Choose the best day of the week:'
    selector.single_choice(prompt=prompt, options=option_list, default='Friday')
    selector.single_choice(prompt=prompt, options=option_dict, default='Fri')

### Multiple choice selector

    prompt = 'Choose the two best days of the week:'
    selector.multiple_choices(prompt=prompt, options=option_list, defaults=['Friday', 'Sunday'])
    selector.multiple_choices(prompt=prompt, options=option_dict, defaults=['Fri', 'Sun'])
