# Render splash

Create icon PNG:
```
#!/bin/bash
inkscape -z -o ../../dcscope/img/icon.png -w 512 -h 512 dcscope_icon.svg >/dev/null 2>/dev/null

```


Create splash PNG:
```
#!/bin/bash
inkscape -z -o ../../dcscope/img/splash.png -w 410 -h 100 dcscope_splash.svg >/dev/null 2>/dev/null

```
