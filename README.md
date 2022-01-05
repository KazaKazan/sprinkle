<h1 align="center" style="border-bottom: none"> <b>SPRINKLE</b> </h1>
<p align="center"><i>A command line tool for creating sprite sheets and tile sets from individual images.</i></p>
<hr>
Sprinkle is a python script that let's the user pack individual sprites into sprite sheets. It was designed to be used for creating sprite sheets to be used with <a href="https://github.com/Sprytile/Sprytile">Sprytile</a>, but can be utilized for more general purposes.
<br/><br/>
<h2>Features</h2>
<ul>
    <li>Pack sprites into sprite sheets with efficiency in mind.</li>
    <li>Option to preserve or seperate sprites into smaller sprites.</li>
    <li>Option to define the base sprite size.</li>
    <li>Option to force the script to create a sprite sheet with 1/1 aspect ratio</li>
</ul>
<br/>
<h2>Installation</h2>
Add the script to your path and make it executable. Remove `.py` from the filename if you want to call the script with just `sprinkle` instead of `sprinkle.py` in your command line.
<br/><br/>
<h2>Dependencies</h2>
<ul>
<li><a href="https://github.com/python-pillow/Pillow">Pillow</a></li>
</ul>
<h2>Usage</h2>
Call the script in the directory as the sprites that'll be packed. The command usage is as follows:

<br/>

```
sprinkle <OPTIONS> <ARGUMENTS> 
```

Arguments and options can be in any order, and they are all optional. If an argument is missing, the default values will be used.

<h3>Options</h3>

As of this version the options are as follows:
<ul>
    <li>`-v` or `--verbose`: Sets verbose mode to True.</li>
    <li>`-h` or `--help`: Displays the help message and exits the script. This option will override any other option.</li>
    <li>`-s` or `--square`: Forces the script to produce sprite sheets with 1/1 aspect ratio.</li>
</ul>

<h3> Arguments </h3>

As of this version the arguments are as follows:
<ul>
    <li><b>Sprite Sheet Mode:</b> `compact` or `intact`. In compact mode sprites larger than the sprite size provided will be sliced into smaller sprites of the sprite size provided. In intact mode, the sprites will be placed onto the sprite sheet as they are, which results in a more human readable but possibly larger sprite sheet. The default value is `compact`.</li>
    <li><b>Sprite Size:</b> A single integer representing the one side of the smallest sprite in the sprite sheet in pixels. The default value is `32`, which represents a 32x32px sprite.</li>
    <li><b>Output File:</b> The filename and the format of the resulting sprite sheet. The argument format is `<filename>.<format>`. The accepted formats are the same as <a href="https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html">Pillow</a>. The default value is `sheet.png`.</li>
</ul>

When called, the script will create a directory called `output` and put the resulting sprite sheet into this directory.
