# High-frequency Financial Time Series Analysis Based on BP Neural Networks

#### Paper
> http://www.lin-baobao.com/static/files/graduate_paper.pdf

#### Video for Demonstration
> http://www.lin-baobao.com/static/videos/graduate_project.flv

#### Application
> http://www.lin-baobao.com/bp_finance/php/login/

### This project includes three sections.

- GetData

    Data crawling.

    Responsible for crawling and processing the high frequency data of stock transcation in recent years. And the data format would be converted to an appropriate format.

- predict

    Core algorithm.

    Implement the Back Propagation Neural Networks without using any framework (all code is completely written by myself).

- php

    System integration.

    Integrate the first two parts into a system.

#### Project description
> It included data crawling, model design, code implementation, result analysis,
experiments and system integration.
- 1. Crawled the data of some stocks’ transactions per day.
- 2. Chose BP Neural Network as model, deduced the formulas myself and implemented code
without using any framework.
- 3. The direction accuracy was about 55%-60% and the relative error between the actual and the
predicted price maintained at 0.015%. Reached the conclusion that high-frequency data is better for
stock price prediction via testing data’s impact at different frequencies.
- 4. Integrated the algorithm into a real-time stock price prediction system.

#### Deployment
> Need to deploy mysql, and the sql file is in [finance.sql](finance.sql)

#### Ways to run
> Just call the [run.py](run.py) directly.

