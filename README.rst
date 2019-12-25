################################################
bulletIn: Interactive Python prompts made simple
################################################

`bulletIn <https://github.com/cronofugo/bulletin>`_ is a fork of `bullet. <https://github.com/Mckinsey666/bullet>`_
 
Usage examples
***************

Import module and initialize class

.. code-block:: python

   import bulletin
   # Dialog aspect is set at initialization
   dialog = bulletin.Dialog(margin=1, pad_right=1, check='>', nocheck=None)

Choose only one option

.. code-block:: python

   dialog.optone(
       prompt='Choose one working day:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
       default='Tuesday')

Choose one or more options

.. code-block:: python

   dialog.optany(
       prompt='Choose your working days:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
       default=['Monday', 'Wednesday'])

