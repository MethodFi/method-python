import asyncio

async def sleep(ms: int):
    await asyncio.sleep(ms / 1000)  # Convert milliseconds to seconds

async def await_results(fn):
    result = None
    retries = 10
    while retries > 0:
        try:
            result = fn()
            if result['status'] in ['completed', 'failed']:
                break
            await sleep(5000)
        except Exception as error:
            print('Error occurred while retrieving account balances:', error)
            raise error  # Rethrow the error to fail the test
        retries -= 1

    return result
