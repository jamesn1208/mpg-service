from sqlalchemy import select, Numeric, literal, cast
from sqlalchemy.sql import bindparam, func

from api.core.models import MPGLog, Vehicles, VehicleOwnership
from .schemas import MetricQuery

# Available bind parameters:
# 'user_id'

metric_queries = [
    MetricQuery(
        title='Most Driven Vehicle',
        description='Vehicle with the most refuels logged.',
        query=select(
            MPGLog.registration,
            func.count(MPGLog.id)
        ).where(
            MPGLog.user_id == bindparam('user_id')
        ).group_by(
            MPGLog.registration
        ).order_by(
            func.count(MPGLog.id).desc()
        ).limit(1)
    ),

    MetricQuery(
        title='Total Spent',
        description='The total amount of money spent on fuel across all logged vehicles.',
        query=select(
            func.concat(
                "£",
                func.coalesce(
                    func.to_char(func.sum(MPGLog.total_cost), 'FM9999999990.00'),
                    '0.00'
                )
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='Total Miles',
        description='The total amount of miles driven across all logged vehicles.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(func.sum(MPGLog.miles), 'FM9999999990.0'),
                    '0.0`'
                ),
                "mi"
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    # TODO: Fix this, im fairly sure its g/km in database, maybe fixed?
    MetricQuery(
        title='Total CO²',
        description='The total amount of CO² released across all logged vehicles.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(
                        func.round(
                            cast(func.sum(((MPGLog.miles * literal(1.609)) * Vehicles.emissions) / literal(1000)), Numeric),
                            0
                        ),
                        'FM9999999990'
                    ),
                    '0'
                ),
                "kg"
            )
        ).join(Vehicles).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='Lowest p/L',
        description='The lowest p/L you have paid for fuel for any vehicle.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(func.min(MPGLog.price_per_litre), 'FM9999999990.0'),
                    '0.0'
                ),
                "p"
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='Highest p/L',
        description='The highest p/L you have paid for fuel for any vehicle.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(func.max(MPGLog.price_per_litre), 'FM9999999990.0'),
                    '0.0'
                ),
                "p"
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='# of Refuels',
        description='The number of refuel logs you have made for any vehicle.',
        query=select(
            func.count(MPGLog.id)
        ).where(
            MPGLog.user_id == bindparam('user_id'),
            MPGLog.registration.in_(select(VehicleOwnership.registration).where(VehicleOwnership.user_id == bindparam('user_id')))
        )
    ),

    MetricQuery(
        title='Average £/mi',
        description='The average cost per mile of driving for any vehicle.',
        query=select(
            func.concat(
                "£",
                func.coalesce(
                    func.to_char(
                        cast(func.avg(MPGLog.total_cost / MPGLog.miles), Numeric),
                        'FM9999999990.00'
                    ),
                    '0.00'
                )
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='Average p/L',
        description='The average price per litre for any vehicle.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(
                        cast(func.avg(MPGLog.price_per_litre), Numeric),
                        'FM9999999990.0'
                    ),
                    '0.0'
                ),
                "p"
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='Average MPG',
        description='The average miles per gallon for any vehicle.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(
                        cast(func.avg(MPGLog.mpg), Numeric),
                        'FM9999999990.00'
                    ),
                    '0.00'
                ),
                "mi/G"
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='Lowest MPG',
        description='The lowest miles per gallon paid for any vehicle.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(func.min(MPGLog.mpg), 'FM9999999990.00'),
                    '0.00'
                ),
                "mi/G"
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='Highest MPG',
        description='The highest miles per gallon paid for any vehicle.',
        query=select(
            func.concat(
                func.coalesce(
                    func.to_char(func.max(MPGLog.mpg), 'FM9999999990.00'),
                    '0.00'
                ),
                "mi/G"
            )
        ).where(
            MPGLog.user_id == bindparam('user_id')
        )
    ),

    MetricQuery(
        title='# of Owned Vehicles',
        description='The amount of vehicles registered with us.',
        query=select(
            func.count(VehicleOwnership.registration)
        ).where(
            VehicleOwnership.user_id == bindparam('user_id')
        )
    ),
]
