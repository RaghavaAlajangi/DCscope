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


Create docs PNG
```
#!/bin/bash
inkscape -z -o dcscope_large_white.png -w 410 -h 100 dcscope_large_white.svg >/dev/null 2>/dev/null

```


Create favicon for docs
```
#!/bin/bash
# sudo apt-get install icoutils
for size in 16 32; do
    inkscape -z -o $size.png -w $size -h $size favicon.svg >/dev/null 2>/dev/null
done
icotool -c -o favicon.ico 16.png 32.png
rm 16.png 32.png

```
