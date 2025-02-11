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

from sds_aspect_meta_model_python.base.data_types.scalar import Scalar


class DefaultScalar(Scalar):
    def __init__(self, urn: str, meta_model_version: str):
        self._urn = urn
        self._meta_model_version = meta_model_version

    @property
    def urn(self) -> str:
        return self._urn

    @property
    def meta_model_version(self) -> str:
        return self._meta_model_version
