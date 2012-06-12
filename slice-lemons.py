
import re
regexp = re.compile(r'# SNIP (.*)\n')

s = open("lemon.py")
out = open("preamble.py", "w")

for line in s:
    if line.startswith("# SNIP"):
        out.close()
        m = regexp.match(line)
        filename = m.group(1)
        out = open("lemonade/" + filename, "w")
    else:
        out.write(line)

out.close()
s.close()

