from sqlalchemy import select
from sqlalchemy.sql import bindparam, func

from api.core.models import MPGLog, Vehicles, VehicleOwnership
from .schemas import MetricQuery


# Available bind parameters:
# 'user_id'

metric_queries = [
    MetricQuery(title='Most Driven Vehicle',
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
                ).limit(1)),
]