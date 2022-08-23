# Copyright 2021 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import List, Dict, Any, Type
from types import MethodType
from abc import ABC, abstractmethod


class MLRunInterface(ABC):
    """
    An abstract class for enriching an object interface with the properties, methods and functions written below. A
    class inheriting MLRun interface should insert what ever it needs to be inserted to the object to the following
    private attributes: '_PROPERTIES', '_METHODS' and '_FUNCTIONS'. Then it should implement 'add_interface' and call
    'super'.
    """

    # Properties attributes to be inserted so the mlrun interface will be fully enabled:
    _PROPERTIES = {}  # type: Dict[str, Any]

    # Methods attributes to be inserted so the mlrun interface will be fully enabled:
    _METHODS = []  # type: List[str]

    # Functions attributes to be inserted so the mlrun interface will be fully enabled:
    _FUNCTIONS = []  # type: List[str]

    @classmethod
    @abstractmethod
    def add_interface(cls, model: object, *args, **kwargs):
        """
        Enrich the model object with this class properties, methods and functions so it will have MLRun specific
        features.

        :param model: The object to enrich his interface
        """
        # Add the MLRun properties:
        cls._insert_properties(model=model, interface=cls)

        # Add the MLRun methods:
        cls._insert_methods(model=model, interface=cls)

        # Add the MLRun functions:
        cls._insert_functions(model=model, interface=cls)

    @staticmethod
    def _insert_properties(model, interface: Type["MLRunInterface"]):
        """
        Insert the properties of the given interface to the model.

        :param model:     The model to enrich.
        :param interface: The interface with the properties to use.
        """
        for property_name, default_value in interface._PROPERTIES.items():
            if property_name not in model.__dir__():
                setattr(model, property_name, default_value)

    @staticmethod
    def _insert_methods(model, interface: Type["MLRunInterface"]):
        """
        Insert the methods of the given interface to the model.

        :param model:     The model to enrich.
        :param interface: The interface with the methods to use.
        """
        for method_name in interface._METHODS:
            if method_name not in model.__dir__():
                setattr(
                    model,
                    method_name,
                    MethodType(getattr(interface, method_name), model),
                )

    @staticmethod
    def _insert_functions(model, interface: Type["MLRunInterface"]):
        """
        Insert the functions of the given interface to the model.

        :param model:     The model to enrich.
        :param interface: The interface with the functions to use.
        """
        for function_name in interface._FUNCTIONS:
            if function_name not in model.__dir__():
                setattr(
                    model,
                    function_name,
                    getattr(interface, function_name),
                )
