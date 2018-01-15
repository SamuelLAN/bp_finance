# !/usr/bin/env python
# -*- coding: utf-8 -*-
import neuralNetWork
from numpy import *
import pylab

'''
    Back Propagation Neural Network
'''
class BPNN(neuralNetWork.NN):
    # 数据预处理接口
    def preProcess(self):
        self.X_training, self.y_training = self.__preProcess(self.X_training, self.y_training)
        self.X_val, self.y_val = self.__preProcess(self.X_val, self.y_val)
        self.X_test, self.y_test = self.__preProcess(self.X_test, self.y_test)

    '''
        数据预处理
    '''
    def __preProcess(self, X, y):
        # original_X_start = X[:, 0: 1]                   # 记录 X 中每天的开盘价
        # X = (X - original_X_start) / original_X_start   # 将 X 中的所有价格序列，转换为对应当天变动的百分比

        # X *= 10000                                        # 将 小数 转换为 百分比

        self.__conv(X, self.kernal)

        X, normalize = self.__featureNormalize(X)       # 进行 标准化处理

        y = (y[:, 1: 2] - y[:, 0: 1]) >= 0              # 将 y 转换为 0 或 1
        y = ones(y.size).reshape((y.size, 1)) * y

        return X, y

    @staticmethod
    def __conv(X, kernal):
        step = (len(kernal) - 1) / 2

        for i, x in enumerate(X):
            tmp_x = x
            for j in range(step):
                tmp_x = hstack((x[0], tmp_x))
                tmp_x = hstack((tmp_x, x[-1]))
            X[i, :] = convolve(tmp_x, kernal, 'valid')

            # X[i, :] = convolve(x, kernal, 'same')
        return X

    '''
        数据标准化处理
        公式：X = (X - mean(X)) / std(X)

        该标准化处理，并不是对所有的数据一起标准化，只对 每天对应的数据 以及 它对应需要预测的数据 进行标准化处理
    '''
    @staticmethod
    def __featureNormalize(X):
        normalize = []                      # 记录 每个处理对应的 mean, std 值，以便最后还原数据
        for i, x in enumerate(X):
            _mean = x.mean()
            _std = x.std()
            if _std == 0:                   # 若 std == 0，则将它置为 1 ，以防除 0 出错
                _std = 1.0
            X[i, :] = (x - _mean) / _std
            normalize.append([_mean, _std])
        normalize = array(normalize)
        return X, normalize

    @staticmethod
    def sigmoid(z):
        return 1.0 / (1.0 + exp(z))

    @staticmethod
    def sigmoidGradient(z):
        return BPNN.sigmoid(z) * (1.0 - BPNN.sigmoid(z))

    '''
        重载前向传递
    '''
    def feedForward(self, theta_list, X):
        m, n = X.shape
        z = X.transpose()
        Z = [z]
        a = z
        A = []

        for tmp_theta in theta_list:
            a = vstack((ones(m).reshape((1, m)), a))
            A.append(a)

            z = dot(tmp_theta, a)
            Z.append(z)
            a = self.sigmoid(z)

        A.append(a)

        Z.reverse()
        A.reverse()
        return A, Z

    '''
        重载 cost ，用于 conjugateGradient 共轭梯度下降所需
    '''
    def cost(self, theta_params, *args):
        X, y, layer_size = args

        theta_list = self.reshapeList(theta_params, layer_size)

        A, Z = self.feedForward(theta_list, X)
        h = A[0]

        regular = 0
        if self.lamda:
            for tmp_theta in theta_list:
                regular += tmp_theta.sum()

        m, n = X.shape

        y = y.transpose()
        J = -1.0 / m * ((y * log(h)).sum() + ((1 - y) * log(1 - h)).sum()) + self.lamda / (2.0 * m) * regular

        self.trainingRecord.append(J)
        return J

    '''
        重载 costGrad ，用于 conjugateGradient 共轭梯度下降所需
    '''
    def costGrad(self, theta_params, *args):
        X, y, layer_size = args

        theta_list = self.reshapeList(theta_params, layer_size)

        A, Z = self.feedForward(theta_list, X)
        h = A[0]

        m, n = X.shape

        delta = h - y.transpose()
        Delta = [delta]

        for i in range(len(theta_list) - 1):
            tmp_theta = theta_list[-1 - i]
            tmp_theta = tmp_theta[:, 1:]
            Delta.append(dot(tmp_theta.transpose(), Delta[-1]) * self.sigmoidGradient(Z[1 + i]))

        grad = []
        for index, tmp_theta in enumerate(theta_list):
            tmp_grad = 1.0 / m * dot(Delta[-1 - index], A[-1 - index].transpose())
            if self.lamda:
                tmp_grad += self.lamda / m * tmp_theta
                tmp_grad[:, 0: 1] -= self.lamda / m * tmp_theta[:, 0: 1]
            grad.append(tmp_grad)

        grad_params = self.reshapeParams(grad)
        return grad_params

    '''
        重载 costFunc 用于 randomGradient 或 globalGradient 所需
    '''
    def costFunc(self, theta_list, X, y):
        grad = []

        A, Z = self.feedForward(theta_list, X)
        h = A[0]

        m, n = X.shape

        regular = 0
        if self.lamda:
            for tmp_theta in theta_list:
                regular += (tmp_theta * tmp_theta).sum()

        y = y.transpose()
        J = -1.0 / m * ((y * log(h)).sum() + ((1 - y) * log(1 - h)).sum()) + self.lamda / (2.0 * m) * regular

        delta = h - y
        Delta = [delta]

        for i in range(len(theta_list) - 1):
            tmp_theta = theta_list[-1 - i]
            tmp_theta = tmp_theta[:, 1:]
            Delta.append(dot(tmp_theta.transpose(), Delta[-1]) * self.sigmoidGradient(Z[1 + i]))

        for index, tmp_theta in enumerate(theta_list):
            tmp_grad = 1.0 / m * dot(Delta[-1 - index], A[-1 - index].transpose())
            if self.lamda:
                tmp_grad += self.lamda / m * tmp_theta
                tmp_grad[:, 0: 1] -= self.lamda / m * tmp_theta[:, 0: 1]
            grad.append(tmp_grad)

        return J, grad

    '''
        重载 测试
    '''
    def test(self):
        self.originalData = {}
        self.__test((self.X_training, self.y_training), 'Training')
        self.__test((self.X_val, self.y_val), 'Validation')
        self.__test((self.X_test, self.y_test), 'Test')

    '''
        测试：
            输出 cost
            输出 Accuracy
            输出 y == 1 Accuracy
            输出 预测结果 与 实际结果 的相似度 (越接近 0 越好，越接近 1 越差)
    '''
    def __test(self, data, data_set_name):
        X, y = data
        theta_list = self.theta.getTheta()

        J, grad = self.costFunc(theta_list, X, y)
        pred = self.predict(theta_list, X)

        precision = 0.5
        pred = pred.transpose()
        pred = ones(pred.size).reshape((pred.size, 1)) * (pred >= precision)

        self.originalData[data_set_name] = {}
        self.originalData[data_set_name]['y'] = y
        self.originalData[data_set_name]['pred'] = pred

        accuracy = float(pred[pred == 1].size) / float(pred.size) * 100    # 预测结果的准确率
        accuracy_equal_one = float(y[y == 1].size) / float(y.size) * 100

        print '%s cost: %f' % (data_set_name, J)
        print '%s Set Accuracy: %f' % (data_set_name, accuracy)
        print '%s y == 1 Set Accuracy: %f' % (data_set_name, accuracy_equal_one)

    def plotAll(self):
        self.plotTrainingCurve()
        self.plotPriceCurve()

    def plotPriceCurve(self):
        data_set_name_list = ['Training', 'Validation', 'Test']

        for data_set_name in data_set_name_list:
            pylab.figure(self.figureNum)
            pylab.plot(self.originalData[data_set_name]['y'], 'b', label = 'y')
            pylab.plot(self.originalData[data_set_name]['pred'], 'r', label = 'predict')
            pylab.title('%s Set Predict Curve' % data_set_name)
            pylab.xlabel('days')
            pylab.ylabel('raise or fall')
            self.figureNum += 1
