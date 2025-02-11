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

from rdflib.term import Node

from sds_aspect_meta_model_python.base.contraints.length_constraint import LengthConstraint
from sds_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from sds_aspect_meta_model_python.vocabulary.BAMMC import BAMMC
from sds_aspect_meta_model_python.impl.constraints.default_length_constraint import DefaultLengthConstraint


class LengthConstraintInstantiator(InstantiatorBase[LengthConstraint]):
    def _create_instance(self, element_node: Node) -> LengthConstraint:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        min_value = self._aspect_graph.value(subject=element_node, predicate=self._bammc.get_urn(BAMMC.min_value)).toPython()
        max_value = self._aspect_graph.value(subject=element_node, predicate=self._bammc.get_urn(BAMMC.max_value)).toPython()
        return DefaultLengthConstraint(meta_model_base_attributes, min_value, max_value)
