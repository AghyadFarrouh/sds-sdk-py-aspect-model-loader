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

from sds_aspect_meta_model_python.base.contraints.language_constraint import LanguageConstraint
from sds_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from sds_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint


class DefaultLanguageConstraint(DefaultConstraint, LanguageConstraint):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, language_code: str):
        super().__init__(meta_model_base_attributes)
        self._language_code = language_code

    @property
    def language_code(self) -> str:
        return self._language_code
