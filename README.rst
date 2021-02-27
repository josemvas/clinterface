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

   choose = runutils.Choose()

or create a customized Choose instance

.. code-block:: python

   choose = bulletin.Choose(
      shift = 1,
      indent = 3,
      align = 2,
      margin = 1,
      pad_left = 1,
      pad_right = 1,
      check = 'X',
      nocheck = 'O')

Launch a dialog to select one or more options

.. code-block:: python

   choose.some(
       prompt='Choose good days:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
       default=['Friday', 'Saturday', 'Sunday'])

Launch a dialog to select only one option

.. code-block:: python

   choose.one(
       prompt='Choose the best day:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
       default='Friday')

