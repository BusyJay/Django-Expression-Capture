Django-Expression-Capture
=========================

An capture using expression for validation.

Here is an example:

![example](https://raw.github.com/BusyJay/Django-Expression-Capture/master/capture.png "An example for the effect")

Structure
---------
Application tests shows how the project works, and the utils is the core package.

Dependence
----------
test under Django 1.2.7, [PIL 1.5](http://www.pythonware.com/products/pil/)

Usage
-----
For convenient, you can just inherit the ExpressionCaptureForm in application utils, and do what you wanna do. For details, see the forms.py in tests application.

Also, you can implement your own form. But keep in mind that you must set the widget to the field and initial url of the widget after parent's initiation. For details, see the forms.py in utils application.

License
-------
This software is released under the [MIT License](http://opensource.org/licenses/MIT). See LICENSE.txt.
