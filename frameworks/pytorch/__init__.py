from typing import List, Dict, Union

import mlrun
import torch
from torch.nn import Module
from torch.utils.data import DataLoader
from torch.optim import Optimizer

from frameworks.pytorch.callbacks import (
    Callback,
    MetricFunctionType,
    MetricValueType,
    HyperparametersKeys,
    MLRunLoggingCallback,
    TensorboardLoggingCallback,
)
import frameworks.pytorch.callbacks
from frameworks.pytorch.model_handler import PyTorchModelHandler
from frameworks.pytorch.callbacks_handler import CallbacksHandler
from frameworks.pytorch.mlrun_interface import PyTorchMLRunInterface


def train(
    model: Module,
    training_set: DataLoader,
    loss_function: Module,
    optimizer: Optimizer,
    validation_set: DataLoader = None,
    metric_functions: List[MetricFunctionType] = None,
    scheduler=None,
    epochs: int = 1,
    training_iterations: int = None,
    validation_iterations: int = None,
    callbacks_list: List[Callback] = None,
    use_cuda: bool = True,
    use_horovod: bool = False,
    auto_log: bool = True,
    context: mlrun.MLClientCtx = None,
    custom_objects: Dict[Union[str, List[str]], str] = None,
):
    """
    Use MLRun's PyTorch interface to train the model.

    :param model:                 The model to train.
    :param training_set:          A data loader for the training process.
    :param loss_function:         The loss function to use during training.
    :param optimizer:             The optimizer to use during the training.
    :param validation_set:        A data loader for the validation process.
    :param metric_functions:      The metrics to use on training and validation.
    :param scheduler:             Scheduler to use on the optimizer at the end of each epoch. The scheduler must
                                  have a 'step' method with no input.
    :param epochs:                Amount of epochs to perform. Defaulted to a single epoch.
    :param training_iterations:   Amount of iterations (batches) to perform on each epoch's training. If 'None' the
                                  entire training set will be used.
    :param validation_iterations: Amount of iterations (batches) to perform on each epoch's validation. If 'None'
                                  the entire validation set will be used.
    :param callbacks_list:        The callbacks to use on this run.
    :param use_cuda:              Whether or not to use cuda. Only relevant if cuda is available. Defaulted to True.
    :param use_horovod:           Whether or not to use horovod - a distributed training framework. Defaulted to
                                  False.
    :param auto_log:              Whether or not to apply auto-logging (to both MLRun and Tensorboard). Defaulted to
                                  True.
    :param context:               The context to use for the logs.
    :param custom_objects:        Custom objects the model is using. Expecting a dictionary with the classes names to
                                  import as keys (if multiple classes needed to be imported from the same py file a list
                                  can be given) and the python file from where to import them as their values. The model
                                  class itself must be specified in order to properly save it for later being loaded
                                  with a handler. For example:
                                  {
                                      "class_name": "/path/to/model.py",
                                      ["layer1", "layer2"]: "/path/to/custom_layers.py"
                                  }

    :return: The initialized trainer.
    """
    trainer = PyTorchMLRunInterface.init_trainer(
        model=model,
        training_set=training_set,
        loss_function=loss_function,
        optimizer=optimizer,
        validation_set=validation_set,
        metric_functions=metric_functions,
        scheduler=scheduler,
        epochs=epochs,
        training_iterations=training_iterations,
        validation_iterations=validation_iterations,
        callbacks=callbacks_list,
        use_cuda=use_cuda,
        use_horovod=use_horovod,
    )
    if auto_log:
        trainer.add_auto_logging_callbacks(
            context=context, custom_objects=custom_objects
        )
    trainer.train()


def evaluate(
    model: Module,
    dataset: DataLoader,
    loss_function: Module = None,
    metric_functions: List[MetricFunctionType] = None,
    iterations: int = None,
    callbacks_list: List[Callback] = None,
    use_cuda: bool = True,
    use_horovod: bool = False,
    auto_log: bool = True,
    context: mlrun.MLClientCtx = None,
    custom_objects: Dict[Union[str, List[str]], str] = None,
) -> List[MetricValueType]:
    """
    Use MLRun's PyTorch interface to evaluate the model.

    :param model:            The model to evaluate.
    :param dataset:          A data loader for the validation process.
    :param loss_function:    The loss function to use during training.
    :param metric_functions: The metrics to use on training and validation.
    :param iterations:       Amount of iterations (batches) to perform on the dataset. If 'None' the entire dataset
                             will be used.
    :param callbacks_list:   The callbacks to use on this run.
    :param use_cuda:         Whether or not to use cuda. Only relevant if cuda is available. Defaulted to True.
    :param use_horovod:      Whether or not to use horovod - a distributed training framework. Defaulted to False.
    :param auto_log:         Whether or not to apply auto-logging (to both MLRun and Tensorboard). Defaulted to True.
    :param context:          The context to use for the logs.
    :param custom_objects:   Custom objects the model is using. Expecting a dictionary with the classes names to import
                             as keys (if multiple classes needed to be imported from the same py file a list can be
                             given) and the python file from where to import them as their values. The model class
                             itself must be specified in order to properly save it for later being loaded with a
                             handler. For example:
                             {
                                 "class_name": "/path/to/model.py",
                                 ["layer1", "layer2"]: "/path/to/custom_layers.py"
                             }

    :return: The initialized evaluator.
    """
    evaluator = PyTorchMLRunInterface.init_evaluator(
        model=model,
        dataset=dataset,
        loss_function=loss_function,
        metric_functions=metric_functions,
        iterations=iterations,
        callbacks=callbacks_list,
        use_cuda=use_cuda,
        use_horovod=use_horovod,
    )
    if auto_log:
        evaluator.add_auto_logging_callbacks(
            context=context, custom_objects=custom_objects
        )
    return evaluator.evaluate()
