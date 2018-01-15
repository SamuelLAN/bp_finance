# !/usr/bin/env python
# -*- coding: utf-8 -*-
import predict.lib.baseObject as baseObject
import predict.lib.funcUtil as funcUtil
from numpy import *
# import pylab
import theta
import random
import platform

'''
    神经网络的基类，其他神经网络都需要继承该基类
    (里面的属性不使用私有，是为了能让子类继承)
'''
class NN(baseObject.base):
    def __init__(self, config):
        self.layerSize = config['layer_size']       # 网络的层级结构
        self.iterTimes = config['iter_times']       # 迭代次数
        self.lamda = config['lamda']                # 正则化的 lamda 参数
        self.kernal = config['kernal']              # 数据预处理时 用来 convolve 数据的矩阵
        self.id = config['id']

        self.theta = theta.Theta(self.layerSize)    # 初始化 theta

    '''
        提供外部加载 theta 的接口
    '''
    def loadTheta(self, theta_list):
        self.theta.setTheta(theta_list)

    '''
        加载数据的接口
        参数：训练集，校验集，测试集    (训练集是必须有的)
    '''
    def loadData(self, data_training, data_val=None, data_test=None, data_last=None):
        self.X_training, self.y_training = data_training
        if data_val:
            self.X_val, self.y_val = data_val
        if data_test:
            self.X_test, self.y_test = data_test
        if data_last:
            self.X_last = data_last[0]

    '''
        数据预处理接口
    '''
    def preProcess(self):
        pass

    def preProcessX(self, X):
        pass

    def revertProcessY(self, y, *args):
        pass

    def predictFuture(self):
        pass

    '''
        前向传递
    '''
    def feedForward(self, theta_list, X):
        Z = []
        A = []
        return A, Z

    '''
        costFunc 用于 randomGradient 或 globalGradient 所需
        参数：
            theta_list: [theta_1, theta_2, ...]   theta_i 为 第 i 层 与 第 i + 1 层之间的 theta，是二维矩阵
            X, y
    '''
    def costFunc(self, theta_list, X, y):
        J = 0
        grad = []
        return J, grad

    '''
        cost 用于 conjugateGradient 共轭梯度下降所需
        参数：
            theta_params : reshape 成一维向量的 theta
            *args : 其他参数
    '''
    def cost(self, theta_params, *args):
        J = 0
        return J

    '''
        costGrad 用于 conjugateGradient 共轭梯度下降所需
    '''
    def costGrad(self, theta_params, *args):
        grad = []
        return grad

    '''
        训练函数
    '''
    def train(self):
        try:
            from scipy import optimize
            self.conjugateGradient(self.X_training, self.y_training, self.iterTimes)    # 若引用 scipy.optimize 成功，则使用共轭梯度下降
        except Exception, ex:                                                           # 否则，使用全局梯度下降
            self.trainingRecord = self.globalGradient(self.X_training, self.y_training, self.iterTimes)
            # self.trainingRecord = self.randomGradient(self.X_training, self.y_training, self.iterTimes, 20, 20)

    '''
        预测函数
    '''
    def predict(self, theta_list, X):
        A, Z = self.feedForward(theta_list, X)
        return A[0].transpose()

    '''
        测试神经网络
    '''
    def test(self):
        pass

    '''
        画图接口
    '''
    def plot(self):
        os_system = platform.system()   # 只在 windows 系统时 画训练曲线，在 Linux 系统不画
        if os_system != 'Windows':
            return

        import pylab
        self.figureNum = 1

        self.plotAll()

        pylab.show()

    '''
        新增加的画图函数，可通过重载该函数而被调用
    '''
    def plotAll(self):
        self.plotTrainingCurve()

    '''
        画训练曲线
    '''
    def plotTrainingCurve(self):
        import pylab
        pylab.figure(self.figureNum)
        pylab.plot(self.trainingRecord)
        pylab.title('Training Curve')
        pylab.xlabel('Training times')
        pylab.ylabel('Error')
        self.figureNum += 1

    '''
        共轭梯度下降
    '''
    def conjugateGradient(self, X, y, iter_times):
        from scipy import optimize

        theta_params = self.reshapeParams(self.theta.getTheta())

        self.hasIterTimes = 0
        self.trainingRecord = []            # optimize.fmin_cg 为 共轭梯度下降函数
        theta_params_min = optimize.fmin_cg(self.cost, theta_params, fprime = self.costGrad, args = (self.X_training, self.y_training, self.layerSize), norm=-Inf,  gtol=1e-12, disp=0, maxiter = self.iterTimes)

        theta_list = self.reshapeList(theta_params_min, self.layerSize)
        self.theta.setTheta(theta_list)     # 更新 训练后的 theta

    '''
        随机梯度下降
    '''
    def randomGradient(self, X, y, iter_times, batch_base, batch_min):
        learning_rate = NN.getLearningRate()
        last_rate = [learning_rate[0], 0]
        J = 1000000000
        J_mean = 1000000000
        min_theta_list = []
        m = X.shape[0]

        cost_record = []

        for i in range(iter_times):
            batch_size = int(random.random() * batch_base + batch_min)  # 随机生成 batch_size 和 batch_num
            batch_num = int(m / batch_size)
            if m % batch_size != 0:
                batch_num += 1

            randice = funcUtil.getShuffleList(m)

            J_mean_list = []

            for b in range(batch_num):      # 根据 batch_size 随机去 batch_X 和 batch_y
                if b < batch_num - 1:
                    batch_X = funcUtil.getListFromList(X, randice[b * batch_size + 1: (b + 1) * batch_size])
                    batch_y = funcUtil.getListFromList(y, randice[b * batch_size + 1: (b + 1) * batch_size])
                else:
                    if not randice[b * batch_size + 1:]:
                        continue
                    batch_X = funcUtil.getListFromList(X, randice[b * batch_size + 1:])
                    batch_y = funcUtil.getListFromList(y, randice[b * batch_size + 1:])

                batch_X = array(batch_X)
                batch_y = array(batch_y)

                tmp_J, grad = self.costFunc(self.theta.getTheta(), batch_X, batch_y)
                cost_record.append(tmp_J)
                J_mean_list.append(tmp_J)
                # J = min(J, tmp_J)
                J = tmp_J

                for k, lr in enumerate(learning_rate):
                    tmp_theta_list = self.theta.minusGrad(grad, lr)
                    tmp_J, tmp_grad = self.costFunc(tmp_theta_list, batch_X, batch_y)
                    if tmp_J < J:
                        self.theta.setTheta(tmp_theta_list)
                        if lr == last_rate[0]:
                            last_rate[1] += 1
                            if last_rate[1] >= 4:
                                if learning_rate[0] > lr:
                                    l = learning_rate.index(lr)
                                    learning_rate = learning_rate[l:]
                                    last_rate[1] = 0
                                elif last_rate[1] >= 10:
                                    learning_rate.insert(0, random.random() * 0.0001 + lr)
                                    learning_rate.insert(0, random.random() * 0.001 + lr)
                                    learning_rate.insert(0, random.random() * 0.01 + lr)
                                    learning_rate.insert(0, random.random() * 0.1 + lr)
                        else:
                            last_rate[0] = lr
                            last_rate[1] = 1
                        break
                funcUtil.recordStatus(self.id, 'Iteration %d|%d   Batch_times: %d | %d    Cost: %f  learning_rate: %f' % (i, iter_times, b, batch_num, J, last_rate[0]))
                print 'Iteration %d|%d   Batch_times: %d | %d    Cost: %f  learning_rate: %f' % (i, iter_times, b, batch_num, J, last_rate[0])

            J_mean_tmp = array(J_mean_list)
            J_mean_tmp = J_mean_tmp.mean()
            if J_mean_tmp < J_mean:
                J_mean = J_mean_tmp
                min_theta_list = self.theta.getTheta()

            print 'Iteration %d|%d   Cost: %f  learning_rate: %f' % (i, iter_times, J, last_rate[0])

        self.theta.setTheta(min_theta_list)

        return cost_record

    '''
        全局梯度下降
    '''
    def globalGradient(self, X, y, iter_times):
        learning_rate = NN.getLearningRate()    # 生成学习率
        last_rate = [learning_rate[0], 0]       # 记录 最近一次迭代的学习率 和 已经使用该学习率的次数
        J = 1000000000

        cost_record = []

        for i in range(iter_times):
            tmp_J, grad = self.costFunc(self.theta.getTheta(), X, y)
            cost_record.append(tmp_J)
            J = min(J, tmp_J)               # 为了保证以下进行的权值更新，更新后的网络的 cost 必须比原来的 cost 小

            for k, lr in enumerate(learning_rate):
                tmp_theta_list = self.theta.minusGrad(grad, lr)         # 以当前的学习率进行更新，测试该更新是否让 cost 变小
                tmp_J, tmp_grad = self.costFunc(tmp_theta_list, X, y)
                if tmp_J < J:
                    self.theta.setTheta(tmp_theta_list)                 # 若 cost 变少了，则更新 theta
                    if lr == last_rate[0]:
                        last_rate[1] += 1
                        if last_rate[1] >= 4:
                            if learning_rate[0] > lr:   # 若当前近几次的学习率，都比 learning_rate 靠前的学习率小，则将比 当前学习率大的数值从 learning_rate 中删除
                                l = learning_rate.index(lr)
                                learning_rate = learning_rate[l:]
                                last_rate[1] = 0
                            elif last_rate[1] >= 10:    # 随机添加更大的学习率，以得到更高的学习效率
                                learning_rate.insert(0, random.random() * 0.0001 + lr)
                                learning_rate.insert(0, random.random() * 0.001 + lr)
                                learning_rate.insert(0, random.random() * 0.01 + lr)
                                learning_rate.insert(0, random.random() * 0.1 + lr)
                    else:
                        last_rate[0] = lr
                        last_rate[1] = 1
                    break

            print 'Iteration %d|%d   Cost: %f  learning_rate: %f' % (i, iter_times, J, last_rate[0])
            funcUtil.recordStatus(self.id, 'Iteration %d|%d   Cost: %f  learning_rate: %f' % (i, iter_times, J, last_rate[0]))
        print '\n'

        return cost_record

    '''
        将 theta_params 根据 layer_size 重新 reshape 出 theta_list
    '''
    @staticmethod
    def reshapeList(theta_params, layer_size):
        theta_list = []
        start = 0
        for i, v in enumerate(layer_size[0:-1]):
            tmp_theta = theta_params[start: start + (v + 1) * layer_size[i + 1]].reshape(layer_size[i + 1], (v + 1))
            theta_list.append(tmp_theta)
            start += (v + 1) * layer_size[i + 1]
        return theta_list

    '''
        将 grad_list reshape 成一维向量 grad_params
    '''
    @staticmethod
    def reshapeParams(grad):
        grad_params = grad[0].reshape(grad[0].size)
        for tmp_grad in grad[1:]:
            grad_params = hstack((grad_params, tmp_grad.reshape(tmp_grad.size)))
        return grad_params

    '''
        生成 随机梯度下降 或 全局梯度下降 所需的 学习率
    '''
    @staticmethod
    def getLearningRate():
        learning_rate = []
        funcUtil.getContinuousList(learning_rate, 1, 0.5, -0.1)
        funcUtil.getContinuousList(learning_rate, 0.45, 0.05, -0.05)
        funcUtil.getContinuousList(learning_rate, 0.04, 0.01, -0.01)
        funcUtil.getContinuousList(learning_rate, 0.009, 0.006, -0.001)
        funcUtil.getContinuousList(learning_rate, 0.0057, 0.003, -0.0003)
        funcUtil.getContinuousList(learning_rate, 0.0029, 0.0001, -0.0001)
        return learning_rate
