
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from farmer.ext.area import Area
from farmer.ext.asset import Asset, Equipment
from farmer.ext.farmobj import FarmObj, FileFarmObj
from farmer.ext.others import Inventory, Quantity, Soil
from farmer.ext.term import Category, Unit


# pylint: disable=too-many-public-methods
class Log(FileFarmObj):

    def __init__(self, farm, keys: Dict):
        if 'resource' not in keys:
            super().__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'log':
            super().__init__(
                farm, farm.log.get({'id': keys['id']})['list'][0])
        else:
            raise KeyError('Key resource does not have value log')

    @property
    def id(self) -> Optional[int]:  # pylint: disable=invalid-name
        return self.attr('id', int)

    @property
    def type(self) -> str:
        return self.attr('type', str)

    @property
    def timestamp(self) -> Optional[datetime]:
        return FarmObj.timestamp_to_datetime(self._keys['timestamp'])

    @property
    def done(self) -> bool:
        return bool(self.attr('done', int))

    @property
    def notes(self) -> Optional[str]:
        return self._keys['notes']['value'] if self._keys['notes'] else None

    @property
    def asset(self) -> List[Asset]:
        key = self.key('asset')
        return self.farm.assets(key, Asset) if key else []

    @property
    def equipment(self) -> List[Equipment]:
        key = self.key('equipment')
        return self.farm.assets(key, Equipment) if key else []

    @property
    def area(self) -> List[Area]:
        key = self.key('area')
        return self.farm.areas(key, Area) if key else []

    @property
    def geofield(self) -> str:
        return self.attr('geofield', str)

    @property
    def movement(self) -> List[Area]:
        key = self.key('movement')['area']
        return self.farm.areas(key, Area) if key else []

    @property
    def membership(self):
        return self.attr('membership', str)

    @property
    def quantity(self) -> List[Quantity]:
        if self._keys['quantity']:
            ret = []
            for quantity in self._keys['quantity']:
                ret.append(Quantity(measure=quantity['measure'],
                                    label=quantity['label'],
                                    value=quantity['value'],
                                    unit=quantity['unit'] if 'unit' in quantity else None))
            return ret
        return []

    @property
    def flags(self) -> str:
        return self.attr('flags', str)

    @property
    def categories(self) -> List[Category]:
        key = self._keys['log_category']
        return [Category(self._farm, x) for x in key]

    @property
    def owner(self):
        return self.attr('log_owner', str)

    @property
    def created(self) -> Optional[datetime]:
        return FarmObj.timestamp_to_datetime(self._keys['created'])

    @property
    def changed(self) -> Optional[datetime]:
        return FarmObj.timestamp_to_datetime(self._keys['changed'])

    @property
    def uid(self) -> Optional[int]:
        key = self._keys['uid']
        return int(key) if key else None

    @property
    def data(self) -> str:
        return self.attr('data', str)

    @property
    def inventory(self) -> List[Inventory]:
        if self._keys['inventory']:
            ret = []
            for inventory in self._keys['inventory']:
                ret.append(Inventory(inventory['value'], inventory['asset']['id']))
            return ret
        return []


class LotLog(Log):

    @property
    def lot_number(self) -> str:
        return self.attr('lot_number', str)


class MoneyLog(LotLog):

    @property
    def units(self) -> List[Unit]:
        return []

    @property
    def values(self) -> List:
        return []

    @property
    def total_price(self) -> float:
        return self.attr('total_price', float)

    @property
    def unit_price(self) -> float:
        return self.attr('unit_price', float)


class Input(LotLog):

    @property
    def material(self) -> str:
        return self.attr('material', str)

    @property
    def purpose(self) -> str:
        return self.attr('input_purpose', str)

    @property
    def method(self) -> str:
        return self.attr('input_method', str)

    @property
    def source(self) -> str:
        return self.attr('input_source', str)

    @property
    def date_purchase(self) -> Optional[datetime]:
        return FarmObj.timestamp_to_datetime(self._keys['date_purchase'])


class Seeding(LotLog):

    @property
    def seed_source(self) -> str:
        return self.attr('seed_source', str)


class Transplanting(Log):
    pass


class Harvest(LotLog):
    pass


class Observation(Log):
    pass


class Maintenance(Log):
    pass


class Purchase(MoneyLog):

    @property
    def seller(self) -> str:
        return self.attr('seller', str)


class Birth(Log):
    pass


class Medical(Log):
    pass


class Sale(Log):

    @property
    def invoice_number(self) -> str:
        return self.attr('invoice_number', str)

    @property
    def customer(self) -> str:
        return self.attr('customer', str)


class Activity(Log):
    pass


class SoilTest(Log):

    @property
    def soil_lab(self) -> str:
        return self.attr('soil_lab', str)

    @property
    def soil_names(self) -> List[Soil]:
        return []
