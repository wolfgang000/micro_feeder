from typing import Optional
import uuid
from result import Ok, Err, Result
import httpx
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


async def download_feed_file_async(feed_url: str) -> Result[tuple[str, str], str]:
    async with AsyncClient() as client:
        try:
            response = await client.get(
                feed_url,
                headers={"Accept": ACCEPT_HEADER},
                follow_redirects=True,
            )
            if response.status_code == 200:
                temp_file_name = f"/tmp/{uuid.uuid4()}"
                async with aiofiles.open(temp_file_name, mode="wb") as f:
                    await f.write(response.content)
                return Ok((temp_file_name, str(response.url)))
            else:
                return Err("We couldn't find the file")
        except ConnectTimeout:
            return Err("we couldn't find the file")
        except Exception as err:
            return Err("general error")

def download_feed_file(
    url: str, etag: Optional[str], last_modified: Optional[str]
) -> Result[str, str]:
    temp_file_name = f"/tmp/{uuid.uuid4()}"
    headers = {"Accept": ACCEPT_HEADER}

    if etag:
        headers["If-None-Match"] = etag

    if last_modified:
        headers["If-Modified-Since"] = last_modified

    responce = httpx.get(url, headers=headers)

    if responce.status_code == 304:
        return Err("Not Modified")

    # Some times the servers has the Last-Modified header but doesn't implement the If-Modified-Since validation logic
    if responce.headers.get("Last-Modified") == last_modified:
        return Err("Not Modified")

    if responce.status_code == 200:
        with open(temp_file_name, "wb") as f:
            f.write(responce.content)
        return Ok(temp_file_name)
    else:
        return Err(f"Error: {responce.status_code}")
