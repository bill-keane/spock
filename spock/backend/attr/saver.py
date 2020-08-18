# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles prepping and saving the Spock config"""

import attr
from spock.backend.base import BaseSaver
from spock.utils import add_info


class AttrSaver(BaseSaver):
    def __init__(self):
        super().__init__()

    def _clean_up_values(self, payload, extra_info, file_extension):
        out_dict = {}
        for key, val in vars(payload).items():
            # Append comment tag to the base class and convert the spock class to a dict
            if file_extension == '.json':
                out_dict.update({key: attr.asdict(val)})
            else:
                out_dict.update({('# ' + key): attr.asdict(val)})
        # Convert values
        clean_dict = self._clean_output(out_dict, extra_info)
        return clean_dict