<div align="center" >
<a target="blank" >
<img src="https://github.com/user-attachments/assets/bc3f7094-ffa8-4d6d-aadd-7a51fa5aaf69" width="15%" >
</a>
</div>
<div align="center" >
<h1>Temel</h1>



🚀 *Html elements server side renderer* ️🚀

<div align="center" >
<a href="https://pypi.org/project/temel/" target="blank" >
<img src="https://img.shields.io/badge/pip_install-temel-blue" width="20%" >
</a>

<a href="https://discord.gg/e2XwPNTBBr" target="blank" >
<img src="https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white" >
</a>

<a target="blank" >
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" >
</a>
</div>
</div>

# Introduction

Have you ever felt that `Jinja` templates are too harsh to work with, however
making frontend in `JavaScript` frameworks makes you 🤮? If so, you’ve come to the right place!



<br>

Temel is hybrid combines the flexibility of React-like components with the simplicity of Jinja templates.
It allows you to define elements as HTML files, and then use those elements as custom HTML tags named according to their respective file names.
[Check out an example to see how it works!](#define-templates)

<br>


Join the support [discord](https://discord.gg/2hu6fPPeF7) and visit the `#programming` channel for questions,
contributions and ideas. Feel free to make pull requests with missing/new features, fixes, etc

## Getting started

1. #### Install the dependencie

```xml
pip install temel
```

<br>

2. #### Define templates

`CustomButton.html`

```html

<div id="custom-button" style="background-color: green">
    <button>{{name}}</button>
</div>
```

`Layout.html`

```html

<div id="layout">
    <header>
        Header section
        <slot.header/>
    </header>
    <article>
        <slot.content/>
    </article>
</div>
```

`Page.html`

```html

<layout>

    <layout.header>
        Page Header Message
    </layout.header>

    <layout.content>
        {{% for button in buttons %}}
        <CustomButton name={{button.name}}/>
            {{% endfor %}}
    </layout.content>
</layout>
```

<br>

3. Call the renderer. Let's render `Page.html`

```python

import temel

if __name__ == '__main__':
    context = {
        'buttons': [
            {
                'name': 'Home'
            },
            {
                'name': 'Settings'
            },
            {
                'name': 'Profile'
            }]
    }
   
    temel.load_templates('C:\\templates')
    output = temel.parse("Page.html", context)
    with open('output.html', 'w') as f:
        f.write(output)
```

4. See the output file

```html

<div id="layout">
    <header>
        Header section
        <layout.header>
            Page Header Message
        </layout.header>
    </header>
    <article>
        <layout.content>
            <div id="custom-button" style="background-color: green">
                <button>Home</button>
            </div>
            <div id="custom-button" style="background-color: green">
                <button>Settings</button>
            </div>
            <div id="custom-button" style="background-color: green">
                <button>Profile</button>
            </div>
        </layout.content>
    </article>
</div>
```

## Contributing

[Library documentation for contributors](https://github.com/jwdeveloper/Temel)

Your improvements are welcome! Feel free to open an <a href="https://github.com/jwdeveloper/Temel/issues">issue</a>
or <a href="https://github.com/jwdeveloper/Temel/pulls">pull request</a>.
