################################################
bulletIn: Interactive Python prompts made simple
################################################

`bulletIn <https://github.com/cronofugo/bulletin>`_ is a fork of `bullet. <https://github.com/Mckinsey666/bullet>`_
 
Quick start
***********

Import the bulletin module

.. code-block:: python

   import bulletin

Instantiate a dialog object

.. code-block:: python

   dialog = bulletin.Dialog()

or instantiate a customized dialog object

.. code-block:: python

   dialog = bulletin.Dialog(
      shift = 1,
      indent = 3,
      align = 2,
      margin = 1,
      pad_left = 1,
      pad_right = 1,
      check = 'X',
      nocheck = 'O')

Launch a dialog to select only one option

.. code-block:: python

   dialog.optone(
       prompt='Choose one working day:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
       default='Tuesday')

or launch a dialog to select one or more option

.. code-block:: python

   dialog.optany(
       prompt='Choose your working days:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
       default=['Monday', 'Wednesday'])

