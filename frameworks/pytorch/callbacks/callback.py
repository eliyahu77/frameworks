from typing import Union, List, Callable
from abc import ABC, abstractmethod

import numpy as np

from torch import Tensor
from torch.nn import Module
from torch.optim import Optimizer
from torch.utils.data import DataLoader

# Supported types of loss and metrics values:
MetricValueType = Union[int, float, np.ndarray, Tensor]

# Supported types of metrics:
MetricFunctionType = Union[Callable[[Tensor, Tensor], MetricValueType], Module]


class Callback(ABC):
    """
    Abstract class for a callback to mlrun's pytorch framework package. Each callback must implement this class so it
    could be used in the trainer and evaluator classes. If implementing a custom trainer, one should consider using the
    'CallbacksHandler' class.
    """

    class _ObjectKeys:
        """
        Keys for the objects dictionary of the callback. Each callback can choose what to store in its objects
        dictionary.
        """

        MODEL = "model"
        TRAINING_SET = "training_set"
        VALIDATION_SET = "validation_set"
        LOSS_FUNCTION = "loss_function"
        OPTIMIZER = "optimizer"
        METRIC_FUNCTIONS = "metric_functions"
        SCHEDULER = "scheduler"

    @abstractmethod
    def __init__(self):
        """
        Initialize the callback with an empty objects dictionary. The objects should be registered on setup.
        """
        self._objects = {}

    def on_horovod_check(self, rank: int) -> bool:
        """
        Check whether this callback is fitting to run by the given horovod rank (worker).

        :param rank: The horovod rank (worker) id.

        :return: True if the callback is ok to run on this rank and false if not.
        """
        pass

    def on_setup(
        self,
        model: Module = None,
        training_set: DataLoader = None,
        validation_set: DataLoader = None,
        loss_function: Module = None,
        optimizer: Optimizer = None,
        metric_functions: List[MetricFunctionType] = None,
        scheduler=None,
    ):
        """
        Basic setup command, storing all the given objects in the callback's objects dictionary.
        :param model:            The model to be stored in this callback.
        :param training_set:     The training set to be stored in this callback.
        :param validation_set:   The validation set to be stored in this callback.
        :param loss_function:    The loss function to be stored in this callback.
        :param optimizer:        The optimizer to be stored in this callback.
        :param metric_functions: The metric functions to be stored in this callback.
        :param scheduler:        The scheduler to be stored in this callback.
        """
        self._objects[self._ObjectKeys.MODEL] = model
        self._objects[self._ObjectKeys.TRAINING_SET] = training_set
        self._objects[self._ObjectKeys.VALIDATION_SET] = validation_set
        self._objects[self._ObjectKeys.LOSS_FUNCTION] = loss_function
        self._objects[self._ObjectKeys.OPTIMIZER] = optimizer
        self._objects[self._ObjectKeys.METRIC_FUNCTIONS] = metric_functions
        self._objects[self._ObjectKeys.SCHEDULER] = scheduler

    def on_run_begin(self):
        """
        After the trainer / evaluator run begins, this method will be called.
        """
        pass

    def on_run_end(self):
        """
        Before the trainer / evaluator run ends, this method will be called.
        """
        pass

    def on_epoch_begin(self, epoch: int):
        """
        After the trainer epoch begins, this method will be called.
        :param epoch: The epoch that is about to begin.
        """
        pass

    def on_epoch_end(self, epoch: int):
        """
        Before the trainer epoch ends, this method will be called.
        :param epoch: The epoch that has just ended.
        """
        pass

    def on_train_begin(self):
        """
        After the trainer training of the current epoch begins, this method will be called.
        """
        pass

    def on_train_end(self):
        """
        Before the trainer training of the current epoch ends, this method will be called.
        """
        pass

    def on_validation_begin(self):
        """
        After the trainer / evaluator validation (in a trainer's case it will be per epoch) begins, this method will be
        called.
        """
        pass

    def on_validation_end(
        self, loss_value: MetricValueType, metric_values: List[float]
    ):
        """
        Before the trainer / evaluator validation (in a trainer's case it will be per epoch) ends, this method will be
        called.
        :param loss_value:    The loss summary of this validation.
        :param metric_values: The metrics summaries of this validation.
        """
        pass

    def on_train_batch_begin(self, batch: int, x: Tensor, y_true: Tensor):
        """
        After the trainer training of the given batch begins, this method will be called.
        :param batch:  The current batch iteration of when this method is called.
        :param x:      The input part of the current batch.
        :param y_true: The true value part of the current batch.
        """
        pass

    def on_train_batch_end(self, batch: int, x: Tensor, y_true: Tensor, y_pred: Tensor):
        """
        Before the trainer training of the given batch ends, this method will be called.
        :param batch:  The current batch iteration of when this method is called.
        :param x:      The input part of the current batch.
        :param y_true: The true value part of the current batch.
        :param y_pred: The prediction (output) of the model for this batch's input ('x').
        """
        pass

    def on_validation_batch_begin(self, batch: int, x: Tensor, y_true: Tensor):
        """
        After the trainer / evaluator validation of the given batch begins, this method will be called.
        :param batch:  The current batch iteration of when this method is called.
        :param x:      The input part of the current batch.
        :param y_true: The true value part of the current batch.
        """
        pass

    def on_validation_batch_end(
        self, batch: int, x: Tensor, y_true: Tensor, y_pred: Tensor
    ):
        """
        Before the trainer / evaluator validation of the given batch ends, this method will be called.
        :param batch:  The current batch iteration of when this method is called.
        :param x:      The input part of the current batch.
        :param y_true: The true value part of the current batch.
        :param y_pred: The prediction (output) of the model for this batch's input ('x').
        """
        pass

    def on_train_loss_begin(self):
        """
        Before the trainer training calculation of the loss, this method will be called.
        """
        pass

    def on_train_loss_end(self, loss_value: MetricValueType):
        """
        After the trainer training calculation of the loss, this method will be called.
        :param loss_value: The recent loss value calculated during training.
        """
        pass

    def on_validation_loss_begin(self):
        """
        Before the trainer / evaluator validating calculation of the loss, this method will be called.
        """
        pass

    def on_validation_loss_end(self, loss_value: MetricValueType):
        """
        After the trainer / evaluator validating calculation of the loss, this method will be called.
        :param loss_value: The recent loss value calculated during validation.
        """
        pass

    def on_train_metrics_begin(self):
        """
        Before the trainer training calculation of the metrics, this method will be called.
        """
        pass

    def on_train_metrics_end(self, metric_values: List[MetricValueType]):
        """
        After the trainer training calculation of the metrics, this method will be called.
        :param metric_values: The recent metric values calculated during training.
        """
        pass

    def on_validation_metrics_begin(self):
        """
        Before the trainer / evaluator validating calculation of the metrics, this method will be called.
        """
        pass

    def on_validation_metrics_end(self, metric_values: List[MetricValueType]):
        """
        After the trainer / evaluator validating calculation of the metrics, this method will be called.
        :param metric_values: The recent metric values calculated during validation.
        """
        pass

    def on_backward_begin(self):
        """
        Before the backward propagation of the loss function, this method will be called.
        """
        pass

    def on_backward_end(self):
        """
        After the backward propagation of the loss function, this method will be called.
        """
        pass

    def on_optimizer_step_begin(self):
        """
        Before the optimizer 'step' and 'zero_grad' methods are called, this method will be called.
        """
        pass

    def on_optimizer_step_end(self):
        """
        After the optimizer 'step' and 'zero_grad' methods are called, this method will be called.
        """
        pass

    def on_scheduler_step_begin(self):
        """
        Before the scheduler 'step' method is called, this method will be called.
        """
        pass

    def on_scheduler_step_end(self):
        """
        After the scheduler 'step' method is called, this method will be called.
        """
        pass

    def on_call_check(self) -> bool:
        """
        Before the loggers handler is calling its loggers, this method will be called to know if this callback
        should run. For example, in case of multiprocessing, logging should happen only for loggers who are called
        from worker 0. The worker id check should be done here.
        :return: True if the call is ok to run and false if not.
        """
        return True
