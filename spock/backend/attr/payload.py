# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles payloads from markup files"""

from itertools import chain
from spock.backend.base import BasePayload


class AttrPayload(BasePayload):
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        """Call to allow self chaining

        *Args*:

            *args:
            **kwargs:

        *Returns*:

            Payload: instance of self

        """
        return AttrPayload()

    @staticmethod
    def _update_payload(base_payload, input_classes, payload):
        """Updates the payload

        Checks the parameters defined in the config files against the provided attr classes and if
        passable adds them to the payload

        *Args*:

            base_payload: current payload
            input_classes: attr classes to roll into
            payload: total payload

        *Returns*:

            payload: updated payload

        """
        # Get basic args
        attr_fields = {attr.__name__: [val.name for val in attr.__attrs_attrs__] for attr in input_classes}
        for keys, values in base_payload.items():
            # check if the keys, value pair is expected by a dataclass
            if keys != 'config':
                # Dict infers that we are overriding a global setting in a specific config
                if isinstance(values, dict):
                    # we're in a namespace
                    # Check for incorrect specific override of global def
                    if keys not in attr_fields:
                        raise TypeError(f'Referring to a class space {keys} that is undefined')
                    for i_keys in values.keys():
                        if i_keys not in attr_fields[keys]:
                            raise ValueError(f'Provided an unknown argument named {keys}.{i_keys}')
                else:
                    # Chain all the values from multiple spock classes into one list
                    if keys not in list(chain(*attr_fields.values())):
                        raise ValueError(f'Provided an unknown argument named {keys}')
            if keys in payload and isinstance(values, dict):
                payload[keys].update(values)
            else:
                payload[keys] = values
        return payload