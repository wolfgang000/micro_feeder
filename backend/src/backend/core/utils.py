import uuid
from result import Ok, Err, Result
from httpx import AsyncClient, ConnectTimeout
import aiofiles

# HTTP "Accept" header to send to servers when downloading feeds.
ACCEPT_HEADER: str = (
    "application/atom+xml"
    ",application/rdf+xml"
    ",application/rss+xml"
    ",application/x-netcdf"
    ",application/xml"
    ";q=0.9,text/xml"
    ";q=0.2,*/*"
    ";q=0.1"
)


async def download_feed_file(feed_url: str) -> Result[str, str]:
    async with AsyncClient() as client:
        try:
            result = await client.get(
                feed_url,
                headers={"Accept": ACCEPT_HEADER},
            )
            if result.status_code == 200:
                temp_file_name = f"/tmp/{uuid.uuid4()}"
                async with aiofiles.open(temp_file_name, mode="wb") as f:
                    await f.write(result.content)
                return Ok(temp_file_name)
            else:
                return Err("we couldn't find the file")
        except ConnectTimeout:
            return Err("we couldn't find the file")
        except Exception as err:
            return Err("general error")
