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

from typing import Set, Optional

from sds_aspect_meta_model_python.base.quantity_kind import QuantityKind
from sds_aspect_meta_model_python.base.unit import Unit
from sds_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from sds_aspect_meta_model_python.impl.base_impl import BaseImpl


class DefaultUnit(BaseImpl, Unit):
    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        symbol: Optional[str],
        code: Optional[str],
        reference_unit: Optional[str],
        conversion_factor: Optional[str],
        quantity_kinds: Set[QuantityKind],
    ):
        super().__init__(meta_model_base_attributes)
        self._symbol = symbol
        self._code = code
        self._reference_unit = reference_unit
        self._conversion_factor = conversion_factor
        self._quantity_kinds = quantity_kinds
        self._set_parent_element_on_child_elements()

    def _set_parent_element_on_child_elements(self) -> None:
        for quantity_kind in self.quantity_kinds:
            quantity_kind.append_parent_element(self)

    @property
    def symbol(self) -> Optional[str]:
        return self._symbol

    @property
    def code(self) -> Optional[str]:
        return self._code

    @property
    def reference_unit(self) -> Optional[str]:
        return self._reference_unit

    @property
    def conversion_factor(self) -> Optional[str]:
        return self._conversion_factor

    @property
    def quantity_kinds(self) -> Set[QuantityKind]:
        return self._quantity_kinds
