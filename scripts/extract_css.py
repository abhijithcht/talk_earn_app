html_path = 'www/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<style>')
end_idx = html.find('</style>')

if start_idx != -1 and end_idx != -1:
    css_content = html[start_idx+7:end_idx].strip()
    with open('www/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)

    new_html = html[:start_idx] + '<link rel="stylesheet" href="style.css?v=1">' + html[end_idx+8:]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('CSS extracted successfully.')
else:
    print('No <style> block found.')
