
import re
regexp = re.compile(r'.*From the file "(.*)"')

s = open("lemon.c")
out = open("preamble.c", "w")

for line in s:
    if line.startswith("/***"):
        out.close()
        if line.find("acttab") != -1:
            filename = "acttab.c"
        else:
            m = regexp.match(line)
            filename = m.group(1)
        out = open(filename, "w")
    else:
        out.write(line)

out.close()
s.close()

