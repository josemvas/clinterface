Runtime Python utilities
#########################

RunUtils is a collection of Python utilities to display messages, launch interactive prompts and handle files. It is partly based on `bullet <https://github.com/Mckinsey666/bullet>`_.
 
Quick start
***********

Import the runutils module

.. code-block:: python

   import runutils

Create a default Selector instance

.. code-block:: python

   selector = runutils.Selector()

or create a customized Selector instance

.. code-block:: python

   selector = runutils.Selector(
      shift = 1,
      indent = 3,
      align = 2,
      margin = 1,
      pad_left = 1,
      pad_right = 1,
      radiobullet = '*',
      checkbullet = '+',
   )

Set label, options and default choice

.. code-block:: python

   selector.label = 'Choose the best day of the week:'
   selector.options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
   selector.default = 'Friday'

...and prompt for single choice

.. code-block:: python

   selector.singlechoice()

Then change label and default choices

.. code-block:: python

   selector.label = 'Choose the best days of the week:'
   selector.default = ['Friday', 'Saturday']

...and prompt for multiple choice

.. code-block:: python

   selector.multiplechoice()
