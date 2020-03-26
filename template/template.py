from string import Template

with open('template.ml', 'r') as template_file:
    template_text = template_file.read()

template = Template(template_text)

text1 = 'Hello and welcome!'
text2 = 'It is nice seeing you here, mate.'

output = template.substitute(heading = text1, paragraph = text2)

print(output, end='')
