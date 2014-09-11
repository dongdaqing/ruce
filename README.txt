ruce testing  (the concise help)
====================================

To run the current demo tests, use::
   cd demo/
   python test_demo.py


Installation
------------

Install the webunit libraries with::

   python setup.py install

Then make a directory like the demo one in your application with tests in
it, and invoke with::

   python  <test>

<test>
   Run the test named - just like unittest.py.


Require Install
-------------
package:requests
you can use commond like:"easy_install -U requests "

What author do in ruce
-------------
add color output on unix like system
error:use red output
success:use green output
warning:use yellow output
add requests module as the default http module
you can test all of http services by requests
