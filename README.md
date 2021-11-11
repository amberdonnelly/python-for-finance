# python-for-finance

The work in this repo is guided by [Derek Banas'](https://www.youtube.com/c/derekbanas) playlist of YouTube tutorials on [Python for Finance](https://youtube.com/playlist?list=PLGLfVvz_LVvTHOWIEBAl-YOr_FC8lRmWX). His work is also hosted on Github [here](https://github.com/derekbanas/Python4Finance). Derek used a Jupyter notebook, but I wanted to work in VSCode and structure the code in my own way.

My motiviation for following these tutorials is to gain familiarity with the stock market, practice my python development, and expand my data science skillset.

Technologies:
- python
    - matplotlib
    - numpy
    - pandas

To run:
```
virtualenv myvenv
source myvenv/bin/activate

pip install -r requirements.txt

python src/<X>-python-for-finance.py
```
CSV's will be saved to the `data` folder, plots will be saves to the `plots` folder.

Future goals:
- implement a user-friendly web-app to make use of the python analysis backend
