import elasticsearch
from fastapi import APIRouter, Request
from fastapi import HTTPException, Depends

from .. import config
from ..domain.segment import Segment
from ..errors.errors import NullResponseError, RecordNotFound
from ..filters.datagrid import filter_segment
from ..globals.authentication import get_current_user
from ..globals.context_server import context_server_via_uql
from ..globals.elastic_client import elastic_client
from ..routers.misc import query
from ..storage.actions.segment import upsert_segment

router = APIRouter(
    prefix="/segment",
    # dependencies=[Depends(get_current_user)]
)


@router.get("/{id}")
async def segment_get(id: str, uql=Depends(context_server_via_uql), elastic=Depends(elastic_client)):
    q = f"SELECT SEGMENT WHERE id=\"{id}\""

    try:
        response_tuple = uql.select(q)
        result = uql.respond(response_tuple)

        if not result or 'list' not in result or not result['list']:
            raise HTTPException(status_code=404, detail="Item not found")

        try:
            elastic_result = elastic.get(config.index['segments'], id)
        except elasticsearch.exceptions.NotFoundError as e:
            elastic_result = RecordNotFound()
            elastic_result.message = "UQL Segment not found."

        result = {
            'meta': result['list'][0],
        }

        result['meta']['synchronized'] = True if not isinstance(elastic_result, RecordNotFound) else False

        if not isinstance(elastic_result, RecordNotFound):
            result['doc'] = {
                "condition": elastic_result['_source']['doc']["condition"],
                "uql": elastic_result['_source']['doc']["uql"],
            }
        else:
            result['meta']['error'] = elastic_result.message

        return result

    except NullResponseError as e:
        raise HTTPException(status_code=e.response_status, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def segment_create(segment: Segment, uql=Depends(context_server_via_uql), elastic=Depends(elastic_client)):
    q = f"CREATE SEGMENT \"{segment.name}\" DESCRIBE \"{segment.desc}\" IN SCOPE \"{segment.scope}\" " + \
        f"WHEN {segment.condition}"

    print(q)
    unomi_result = query(q, uql)
    print(unomi_result)
    upserted_records, errors = upsert_segment(elastic, q, segment)
    print(upserted_records, errors)

    return unomi_result


@router.delete("/{id}")
async def segment_delete(id: str,
                         uql=Depends(context_server_via_uql),
                         elastic=Depends(elastic_client)):
    try:
        index = config.index['segments']
        elastic_result = elastic.delete(index, id)
        print(elastic_result)
    except elasticsearch.exceptions.NotFoundError:
        # todo logging
        print("Record {} not found in elastic.".format(id))

    q = f"DELETE SEGMENT \"{id}\""
    response_tuple = uql.delete(q)
    print(response_tuple)
    return uql.respond(response_tuple)


@router.post("/select")
async def segment_select(request: Request, uql=Depends(context_server_via_uql)):
    try:
        q = await request.body()
        q = q.decode('utf-8')
        if q:
            q = f"SELECT SEGMENT WHERE {q}"
        else:
            q = "SELECT SEGMENT LIMIT 20"
        response_tuple = uql.select(q)
        result = uql.respond(response_tuple)
        result = list(filter_segment(result))
        return result
    except NullResponseError as e:
        raise HTTPException(status_code=e.response_status, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))