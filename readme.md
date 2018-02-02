# 基于BP神经网络的高频金融时间序列分析

#### 论文
> http://www.lin-baobao.com/static/files/graduate_paper.pdf

#### 演示视频
> http://www.lin-baobao.com/static/videos/graduate_project.flv

#### 应用地址
> http://www.lin-baobao.com/bp_finance/php/login/

### 项目分3个部分

- GetData

    数据爬取

    负责将近几年的股票高频数据爬取并处理成适当的数据格式

- predict

    核心算法

    使用了 bp （自己实现，没有借助任何框架）

- php

    集成系统

    将前两部分集成为一个系统

#### 项目描述
> 采用任意的上证或深证股票每天所有交易的数据作为样本，基于BP神经网络，对高频数据进行分析和预测。检验不同的数据预处理方法以及不同频率的金融数据对于预测未来价格效果的影响。结果发现，高频的数据更有利于预测，并根据此，完成了一个对上证或深证股票的实时预测系统。项目共分3个阶段：1、数据爬取；2、核心算法；3、系统集成。1和2阶段主要采用python实现，预测的方向准确率平均在55%-60%左右，实际价格的相对误差维持在0.015%左右，系统采用php实现。该项目也有尝试使用深度学习的方法，但当时没有采用任何框架，所有公式都自己推导并实现，可能是推导时出错了也可能是参数没调好问题，最终没有尝试成功。之后有时间会重新尝试改进。

#### 部署
> 需要部署 mysql，sql 文件在 [finance.sql](finance.sql)

#### 运行方式
> 直接调用 [run.py](run.py) 就可以了

