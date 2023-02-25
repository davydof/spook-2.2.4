"""Spook - Not your homie."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components.number import DOMAIN, NumberEntity
from homeassistant.core import ServiceCall

from . import AbstractSpookEntityComponentService


class SpookService(AbstractSpookEntityComponentService):
    """Number entity service, decrease value by a single step."""

    domain = DOMAIN
    service = "decrease"
    schema = {vol.Optional("amount"): vol.Coerce(float)}

    async def async_handle_service(
        self, entity: NumberEntity, call: ServiceCall
    ) -> None:
        """Handle the service call."""
        if (amount := call.data.get("amount", entity.step)) % entity.step != 0:
            raise ValueError(
                f"Amount {amount} not valid for {entity.entity_id}, "
                f"it needs to be a multiple of {entity.step}"
            )
        await entity.set_native_value(
            min(entity.native_value - amount, entity.max_value)
        )
