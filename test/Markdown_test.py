import markdown


with open("some_file.txt", "r", encoding="utf-8") as input_file:
    text = input_file.read()
input_file.close()
html = markdown.markdown(text, extensions=['tables'])
with open("mark_test.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(html)
output_file.close()
