#  Copyright (c) 2022 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

import abc
from typing import TypeVar, Optional, TYPE_CHECKING, Generic, Dict, Any

import rdflib  # type: ignore
from rdflib.term import Node

from sds_aspect_meta_model_python.base.data_types.data_type import DataType
from sds_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from sds_aspect_meta_model_python.loader.rdf_helper import RdfHelper
from sds_aspect_meta_model_python.vocabulary.BAMM import BAMM
from sds_aspect_meta_model_python.vocabulary.BAMMC import BAMMC

if TYPE_CHECKING:
    # Only import the module during type checking and not during runtime.
    # Conditional imports are often classified as code smells but here
    # it is the only solution that allows consistent type hinting and avoids circular imports.
    # Do not remove this import even if it is marked as unused.
    from sds_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory

T = TypeVar("T")


class InstantiatorBase(Generic[T], metaclass=abc.ABCMeta):
    """Base class from which all instantiators inherit. It holds some relevant references
    and helper methods.
    The class is generic and holds a type variable T. Every inheriting class replaces
    the type variable with the responsible meta model element type.
    """

    def __init__(self, model_element_factory: "ModelElementFactory"):
        self._model_element_factory = model_element_factory
        """ reference to the element factory to delegate instantiation of
        child elements.
        """

        self._bamm = model_element_factory.get_bamm()
        self._bammc = model_element_factory.get_bammc()
        self._unit = model_element_factory.get_unit()
        self._meta_model_version = model_element_factory.get_meta_model_version()
        self._aspect_graph: rdflib.Graph = model_element_factory.get_aspect_graph()

        self._existing_instances: Dict[str, T] = {}
        """ A storage of all generated instances to prevent multiple
        instantiation of the same element.
        """

    def get_instance(self, element_node: Node) -> T:
        """
        returns a model instance of type T.
        The instance is either a newly created one or an already
        existing element.

        Args:
            element_node: Node in the aspect graph representing the element

        Returns:
            An instance of the model element
        """

        element_urn = RdfHelper.to_python(element_node)
        if self._existing_instances.keys().__contains__(element_urn):
            return self._existing_instances[element_urn]

        new_instance = self._create_instance(element_node)
        self._existing_instances[element_urn] = new_instance
        return new_instance

    @abc.abstractmethod
    def _create_instance(self, element_node: Node) -> T:
        """
        Creates an instance of the given element and returns it
        Args:
            element_node: Node in the aspect graph representing the element

        Returns:
            An instance of the model element
        """
        raise NotImplementedError

    def _get_base_attributes(self, element_subject: Node) -> MetaModelBaseAttributes:
        """creates an object with the base information of an element
        Arguments:
            element_subject: Element of the graph where the information should be extracted

        Returns:
            object that wraps all the information (bamm_version, urn, name, preferred_names, descriptions, see)
        """
        return MetaModelBaseAttributes.from_meta_model_element(element_subject, self._aspect_graph, self._bamm, self._meta_model_version)

    def _get_child(self, parent_subject: Node, child_predicate, required=False):
        """
        Searches for a child node of a parent node and returns an instance of it.
        The child can either be a Literal (e.g., a String) or a sub-element (e.g., Characteristic).

        Args:
            parent_subject: node in the aspect graph of the parent
            child_predicate: predicate that points from the parent to the child
            required: boolean value that determines whether the child is
                mandatory or not.

        Returns:
            An instance of the child if it exists or None if the child does not exist and is not required.

        Raises:
            ValueError: if the child is required but does not exist.
        """
        child_subject = self._aspect_graph.value(subject=parent_subject, predicate=child_predicate)
        if child_subject is None and required:
            raise ValueError(
                f"Child {child_predicate} is required \
                for element {RdfHelper.to_python(parent_subject)}"
            )
        elif child_subject is None:  # not required
            return None
        elif isinstance(child_subject, rdflib.Literal):
            return RdfHelper.to_python(child_subject)
        else:
            return self._model_element_factory.create_element(child_subject)

    def _get_list_children(self, element_subject: Node, list_predicate: rdflib.URIRef) -> list:
        """Extracts all children of an rdf list from the given element and
        returns a list of the instances. Used for bamm:properties, bamm:operations and bamm:events
        Arguments:
            element_subject: Element of the graph that has properties as children (e.g. aspect or entity)
            list_predicate: Predicate pointing from the parent to the list

        Returns:
            a list of the instantiated elements
        """
        children = []
        list_node = self._aspect_graph.value(subject=element_subject, predicate=list_predicate)
        children_nodes = RdfHelper.get_rdf_list_values(list_node, self._aspect_graph)

        for child_node in children_nodes:
            child: Any = self._model_element_factory.create_element(child_node)
            children.append(child)

        return children

    def _get_data_type(self, element_node: Node) -> Optional[DataType]:
        """
        Short style implementation to get a data type of a characteristic.
        This method would better fit in the characteristic instantiator.
        Unfortunately it is not possible to make other instantiators inherit from
        CharacteristicInstantiator because of the generics.
        Args:
            element_node: Node of the aspect graph representing the characteristic
        Returns:
            Data type object or none
        """
        element_characteristic_node = self._aspect_graph.value(subject=element_node, predicate=self._bammc.get_urn(BAMMC.element_characteristic))
        if element_characteristic_node is None:
            data_type_node = self._aspect_graph.value(subject=element_node, predicate=self._bamm.get_urn(BAMM.data_type))
        else:
            # some characteristics (Collection, List, TimeSeries, etc.) may have
            # an attribute "element_characteristic". If it is given, then take
            # the data type of the element_characteristic.
            data_type_node = self._aspect_graph.value(subject=element_characteristic_node, predicate=self._bamm.get_urn(BAMM.data_type))
        if data_type_node is None:
            return None
        else:
            return self._model_element_factory.create_element(data_type_node)
