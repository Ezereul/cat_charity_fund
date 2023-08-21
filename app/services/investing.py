from datetime import datetime
from typing import List

from app.models.investment_base import InvestmentBase


def distribute_investment(
        source: InvestmentBase,
        targets: List[InvestmentBase]) -> List[InvestmentBase]:
    changed_targets = []
    for target in targets:
        investment = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        if investment == 0:
            break
        for unit in [source, target]:
            unit.invested_amount += investment
            if unit.full_amount == unit.invested_amount:
                unit.fully_invested = True
                unit.close_date = datetime.utcnow()
        changed_targets.append(target)

    return changed_targets
