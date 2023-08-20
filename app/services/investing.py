from datetime import datetime


def distribute_investment(investment_source, investment_targets):
    available_amount = investment_source.full_amount - investment_source.invested_amount

    for target in investment_targets:
        required_amount = target.full_amount - target.invested_amount
        investment = min(available_amount, required_amount)

        target.invested_amount += investment
        investment_source.invested_amount += investment
        available_amount -= investment

        if target.full_amount == target.invested_amount:
            target.fully_invested = True
            target.close_date = datetime.utcnow()

        if available_amount == 0:
            investment_source.fully_invested = True
            investment_source.close_date = datetime.utcnow()
            break

    return investment_source
