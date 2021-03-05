Runtime Python utilities
#########################

RunUtils is a collection of Python utilities to display messages, launch interactive prompts and handle files. It is partly based on `bullet <https://github.com/Mckinsey666/bullet>`_.
 
Quick start
***********

Import the runutils module

.. code-block:: python

   import runutils

Create a default Choose instance

.. code-block:: python

   prompt = runutils.Choose()

or create a customized Choose instance

.. code-block:: python

   prompt = runutils.Choose(
      radiobullet = '*',
      checkbullet = '+',
      uncheckbullet = '-'
   )

Set label, choices and defaults

.. code-block:: python

   prompt.set_label('Choose the best day of the week:')
   prompt.set_choices('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
   prompt.set_defaults('Friday')

Prompt for only one option

.. code-block:: python

   prompt.one()

Update label and prompt for one or more options

.. code-block:: python

   prompt.set_label('Choose good days of the week:')
   prompt.some()
