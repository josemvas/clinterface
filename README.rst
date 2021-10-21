Runtime Python utilities
#########################

RunUtils is a collection of Python utilities to display messages, launch interactive prompts and handle files. It is partly based on `bullet <https://github.com/Mckinsey666/bullet>`_.
 
Quick start
***********

Import the runutils module

.. code-block:: python

   import runutils

Create a default Chooser instance

.. code-block:: python

   prompt = runutils.Chooser()

or create a customized Chooser instance

.. code-block:: python

   prompt = runutils.Chooser(
      shift = 1,
      indent = 3,
      align = 2,
      margin = 1,
      pad_left = 1,
      pad_right = 1,
      radiobullet = '*',
      checkbullet = '+',
   )

Set label, choices and defaults

.. code-block:: python

   prompt.set_label('Choose the best day of the week:')
   prompt.set_choices('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
   prompt.set_defaults('Friday')

Prompt for single option

.. code-block:: python

   prompt.single()

Update label and prompt for multiple options

.. code-block:: python

   prompt.set_label('Choose good days of the week:')
   prompt.multiple()
