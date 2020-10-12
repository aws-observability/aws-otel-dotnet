# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from enum import Enum


# application type
class Type(Enum):
    WEBAPP = 'webapp'
    LAMBDA = 'lambda'
