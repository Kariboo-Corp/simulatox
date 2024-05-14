# Front README.md

<aside>
<img src="https://www.notion.so/icons/info-alternate_blue.svg" alt="https://www.notion.so/icons/info-alternate_blue.svg" width="40px" /> We’re using **Dash** as framework for the front in python, you can find its documentation bellow

</aside>

[Dash Documentation & User Guide | Plotly](https://dash.plotly.com/)

# App operating

<aside>
<img src="https://www.notion.so/icons/exclamation-mark_red.svg" alt="https://www.notion.so/icons/exclamation-mark_red.svg" width="40px" /> Before continue, we assume you’ve read Dash documentation

</aside>

- `[app.py](http://app.py)` : This is the starting point of the front, the variable `app` inside will be to define Dash App by `[main.py](http://main.py)` . It’s in this file that you will can add new features.
- `[modules.py](http://modules.py)` : This file is used by the back-end to produce some ui based on functionnal programming, meaning that it will produce always the same output with the same parameters. This is the only link between back-end → front-end