Category is for classifying scrubbed words; Type is for classifying categories.

This program takes input from all files ending with ".type", which should include 2n lines, indicating that there are n categories in a type. The part of the file name before the extension name should match the name of the type. A valid example of a type file is like this:
~~~
category 1 name (without space)
category 1 alias (user-friendly display_name)
category 2 name (without space)
category 2 alias (user-friendly display_name)
...
category 2n name (without space)
category 2n alias (user-friendly display_name)
~~~

This program generates the corresponding Javascript code to initialyze these variables with sorted initial value. The first argument of the program is the output file (e.g. output.js); if there is no arguments, normal stdout will be used.

The generated result should be copied into the crowd interface main js file.
