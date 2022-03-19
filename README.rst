Console utilities for command line interfaces
#############################################

A collection of console utilities to display messages and interactive prompts. It is partly based on `bullet <https://github.com/Mckinsey666/bullet>`_.
 
Quick start
***********

Import the consoleutils module

.. code-block:: python

   import consoleutils

Create a default Selector instance

.. code-block:: python

   selector = consoleutils.Selector()

or create a customized Selector instance

.. code-block:: python

   selector = consoleutils.Selector(
      shift = 1,
      indent = 3,
      align = 2,
      margin = 1,
      pad_left = 1,
      pad_right = 1,
      radiobullet = '*',
      checkbullet = '+',
   )

Set the message, options and default choice

.. code-block:: python

   selector.message = 'Choose the best day of the week:'
   selector.options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
   selector.default = 'Friday'

and prompt for a single choice

.. code-block:: python

   selector.single_choice()

Set the message and default choices but use the same options

.. code-block:: python

   selector.message = 'Choose the best days of the week:'
   selector.default = ['Friday', 'Saturday']

and prompt for multiple choices

.. code-block:: python

   selector.multiple_choice()
