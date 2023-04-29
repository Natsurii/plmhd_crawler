import os
import pytest
from dotenv import load_dotenv
from crawler.crawler import Crawler


load_dotenv()
pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_login():
    crawler = Crawler()
    await crawler.login(os.environ.get("TEST_LOGIN"),
                        os.environ.get("TEST_PASSWORD"))


@pytest.mark.asyncio
async def test_fillup():
    crawler = Crawler()
    await crawler.fillup(os.environ.get("TEST_LOGIN"), 
                         os.environ.get("TEST_PASSWORD"))
