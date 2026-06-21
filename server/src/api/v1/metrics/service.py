from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from . import schemas, helpers, models


async def get_metrics(session: AsyncSession, user_id: int) -> list[schemas.Metric]:
    metrics: list[schemas.Metric] = []

    for node in helpers.metric_queries:
        try:
            data = await models.get_metric(session=session,
                                           query=node.query,
                                           params={'user_id': user_id})
        except NoResultFound:
            logging.debug("No data found for this metric query, skipping.")
            continue
        except SQLAlchemyError:
            await session.rollback()
            logging.exception("Skipping this metric as error occurred in query.")
            continue

        metrics.append(schemas.Metric(title=node.title,
                                      value=str(data),
                                      description=node.description))

    return metrics
