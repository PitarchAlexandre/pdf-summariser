import asyncio

async def my_task(name):
    print(f"Task {name} started")
    await asyncio.sleep(2)
    print(f"Task {name} completed")

async def main():
    task1 = asyncio.create_task(my_task("A"))
    task2 = asyncio.create_task(my_task("B"))
    await task1
    await task2

asyncio.run(main())