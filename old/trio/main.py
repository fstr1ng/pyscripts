import trio

async def async_double(x):
	return x*2

trio.run(async_double, 3)