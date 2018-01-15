# # !/usr/bin/env python
# # -*- coding: utf-8 -*-
import predict.lib.funcUtil as funcUtil
import neuralNetWork
from numpy import *
import pywt

'''
    Back Propagation Neural Network
'''
class BPNN(neuralNetWork.NN):
    # 数据预处理接口
    def preProcess(self):
        self.X_training, self.normalize_training, self.originalXStart_training, self.y_training, self.openY_training = self.__preProcess(self.X_training, self.y_training)
        self.X_val, self.normalize_val, self.originalXStart_val, self.y_val, self.openY_val = self.__preProcess(self.X_val, self.y_val)
        self.X_test, self.normalize_test, self.originalXStart_test, self.y_test, self.openY_test = self.__preProcess(self.X_test, self.y_test)

    '''
        对输入变量进行预处理
    '''
    def preProcessX(self, X):
        original_X_start = X[:, 0: 1]                   # 记录 X 中每天的开盘价
        X = (X - original_X_start) / original_X_start   # 将 X 中的所有价格序列，转换为对应当天变动的百分比
        X *= 100                                        # 将 小数 转换为 百分比

        # self.__conv(X, self.kernal)

        X = self.__dwt(X)
        X, normalize = self.__featureNormalize(X)       # 进行 标准化处理
        X = self.__dwt(X)
        return X, normalize, original_X_start

    '''
        数据预处理
    '''
    def __preProcess(self, X, y):
        X, normalize, original_X_start = self.preProcessX(X)

        y = (y - original_X_start) / original_X_start   # 预测的那天，也根据 X 的开盘价，转换为对应的变动的百分比
        y *= 100

        y = (y - normalize[:, 0:1]) / normalize[:, 1:2]

        open_y = y[:, 0: 1]
        y = y[:, 1: 2]

        return X, normalize, original_X_start, y, open_y

    '''
        对监督变量 y 或 预测值pred 还原预处理 （还原回实际价格）
    '''
    def revertProcessY(self, y, *args):
        normalize, original_X_start = args

        y = y * normalize[:, 1:] + normalize[:, 0: 1]  # 还原数据
        y /= 100.0
        y = y * original_X_start + original_X_start

        return y

    '''
        预测未来的数据接口
    '''
    def predictFuture(self):
        X, normalize, original_X_start = self.preProcessX(self.X_last)
        self.pred = self.predict(self.theta.getTheta(), X)
        self.pred = self.revertProcessY(self.pred, normalize, original_X_start)
        self.pred = self.pred.tolist()[0][0]
        print 'predict future result: ' + str(self.pred)

    '''
        卷积
    '''
    @staticmethod
    def __conv(X, kernal):
        for i, x in enumerate(X):
            X[i, :] = convolve(x, kernal, 'same')
        return X

    '''
        小波变换
    '''
    @staticmethod
    def __dwt(X):
        m, n = X.shape
        for i, x in enumerate(X):
            ca, cd = pywt.dwt(x, 'db1')
            tmp_a = pywt.upcoef('a', ca, 'db1', 1, n)
            X[i, :] = tmp_a
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
    def __featureNormalizeAll(X):
        _mean = X.mean()
        _std = X.std()
        if _std == 0:
            _std = 1
        X = (X - _mean) / _std
        return X, [_mean, _std]

    '''
        重载前向传递
    '''
    def feedForward(self, theta_list, X):
        m, n = X.shape
        z = X.transpose()
        Z = [z]
        A = []

        for tmp_theta in theta_list:
            a = vstack((ones((1, m)), z))
            A.append(a)

            z = dot(tmp_theta, a)
            Z.append(z)
        A.append(z)

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

        delta = h - y.transpose()
        J = 1 / (2.0 * m) * (delta * delta).sum() + self.lamda / (2.0 * m) * regular

        self.trainingRecord.append(J)
        self.hasIterTimes += 1
        funcUtil.recordStatus(self.id, 'Iteration %d|%d   Cost: %f' % (self.hasIterTimes, self.iterTimes, J))
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
            Delta.append(dot(tmp_theta.transpose(), Delta[-1]))

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

        regular = 0
        if self.lamda:
            for tmp_theta in theta_list:
                regular += (tmp_theta * tmp_theta).sum()

        m, n = X.shape

        delta = h - y.transpose()
        J = 1 / (2.0 * m) * (delta * delta).sum() + self.lamda / (2.0 * m) * regular

        Delta = [delta]

        for i in range(len(theta_list) - 1):
            tmp_theta = theta_list[-1 - i]
            tmp_theta = tmp_theta[:, 1:]
            Delta.append(dot(tmp_theta.transpose(), Delta[-1]))

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
        self.testRecord = {}
        self.__test((self.X_training, self.y_training, self.normalize_training, self.openY_training, self.originalXStart_training), 'Training')
        self.__test((self.X_val, self.y_val, self.normalize_val, self.openY_val, self.originalXStart_val), 'Validation')
        self.__test((self.X_test, self.y_test, self.normalize_test, self.openY_test, self.originalXStart_test), 'Test')

    '''
        测试：
            输出 cost
            输出 Accuracy
            输出 y == 1 Accuracy
            输出 预测结果 与 实际结果 的相似度 (越接近 0 越好，越接近 1 越差)
    '''
    def __test(self, data, data_set_name):
        X, y, normalize, open_y, original_X_start = data
        theta_list = self.theta.getTheta()

        J, grad = self.costFunc(theta_list, X, y)
        pred = self.predict(theta_list, X)

        open_y = self.revertProcessY(open_y, normalize, original_X_start)
        y = self.revertProcessY(y, normalize, original_X_start)
        pred = self.revertProcessY(pred, normalize, original_X_start)

        self.originalData[data_set_name] = {}
        self.originalData[data_set_name]['y'] = y.tolist()
        self.originalData[data_set_name]['pred'] = pred.tolist()
        self.originalData[data_set_name]['open'] = open_y.tolist()

        relative_cost = ((pred - y) / y).mean() * 100

        y = (y - open_y) / open_y * 100         # 将数据变成相对于当天的变动的百分比
        pred = (pred - open_y) / open_y * 100

        _diff = linalg.norm(y - pred) / linalg.norm(y + pred)   # 预测结果 与 实际结果 的相似度

        accuracy = (y * pred) >= 0
        accuracy = float(y[accuracy].size) / float(y.size) * 100    # 预测结果的准确率
        accuracy_equal_one = float(y[y >= 0].size) / float(y.size) * 100

        self.testRecord[data_set_name] = {}
        self.testRecord[data_set_name]['cost'] = J
        self.testRecord[data_set_name]['accuracy'] = accuracy
        self.testRecord[data_set_name]['accuracy_y'] = accuracy_equal_one
        self.testRecord[data_set_name]['diff'] = _diff
        self.testRecord[data_set_name]['relative_cost'] = relative_cost

        print '%s cost: %f' % (data_set_name, J)
        print '%s Set Accuracy: %f' % (data_set_name, accuracy)
        print '%s y == 1 Set Accuracy: %f' % (data_set_name, accuracy_equal_one)
        print '%s result diff: %f\n' % (data_set_name, _diff)
        print '%s relative_cost: %f\n' % (data_set_name, relative_cost)

    def plotAll(self):
        self.plotTrainingCurve()
        self.plotPriceCurve()

    def plotPriceCurve(self):
        import pylab
        data_set_name_list = ['Training', 'Validation', 'Test']

        for data_set_name in data_set_name_list:
            pylab.figure(self.figureNum)
            pylab.plot(self.originalData[data_set_name]['y'], 'b', label = 'y')
            pylab.plot(self.originalData[data_set_name]['pred'], 'r', label = 'predict')
            pylab.title('%s Set Price Curve' % data_set_name)
            pylab.xlabel('days')
            pylab.ylabel('price')
            self.figureNum += 1
