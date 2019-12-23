################################################
Bulletin: Interactive Python prompts made simple
################################################

`Bulletin <https://github.com/cronofugo/bulletin>`_ is a fork of `bullet. <https://github.com/Mckinsey666/bullet>`_
 
Usage examples
***************

Choose only one option:
.. code-block:: python
   import bulletin
   dialogs = bulletin.Dialogs(margin=1, pad_right=1)
   dialogs.optone(prompt='Choose one working day:', choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], default='Tuesday')

Choose one or more options:
.. code-block:: python
   import bulletin
   dialogs = bulletin.Dialogs(margin=1, pad_right=1)
   dialogs.optany(prompt='Choose two working days:', choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], default=['Monday', 'Wednesday'])

