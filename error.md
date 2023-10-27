Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=timestamp&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
Oct 26 07:44:17 PM      response = await func(request)
Oct 26 07:44:17 PM                 ^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
Oct 26 07:44:17 PM      raw_response = await run_endpoint_function(
Oct 26 07:44:17 PM                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
Oct 26 07:44:17 PM      return await run_in_threadpool(dependant.call, **values)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
Oct 26 07:44:17 PM      return await anyio.to_thread.run_sync(func, *args)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
Oct 26 07:44:17 PM      return await get_async_backend().run_sync_in_worker_thread(
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2106, in run_sync_in_worker_thread
Oct 26 07:44:17 PM      return await future
Oct 26 07:44:17 PM             ^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 833, in run
Oct 26 07:44:17 PM      result = context.run(func, *args)
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in search_orders
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in <listcomp>
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM                ^^^^^^^^^
Oct 26 07:44:17 PM  ValueError: dictionary update sequence element #0 has length 17; 2 is required
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=customer_name&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
Oct 26 07:44:17 PM      response = await func(request)
Oct 26 07:44:17 PM                 ^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
Oct 26 07:44:17 PM      raw_response = await run_endpoint_function(
Oct 26 07:44:17 PM                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
Oct 26 07:44:17 PM      return await run_in_threadpool(dependant.call, **values)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
Oct 26 07:44:17 PM      return await anyio.to_thread.run_sync(func, *args)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
Oct 26 07:44:17 PM      return await get_async_backend().run_sync_in_worker_thread(
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2106, in run_sync_in_worker_thread
Oct 26 07:44:17 PM      return await future
Oct 26 07:44:17 PM             ^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 833, in run
Oct 26 07:44:17 PM      result = context.run(func, *args)
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in search_orders
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in <listcomp>
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM                ^^^^^^^^^
Oct 26 07:44:17 PM  ValueError: dictionary update sequence element #0 has length 17; 2 is required
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "OPTIONS /carts/search/?sort_col=line_item_total&sort_order=desc HTTP/1.1" 200 OK
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=timestamp&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
Oct 26 07:44:17 PM      response = await func(request)
Oct 26 07:44:17 PM                 ^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
Oct 26 07:44:17 PM      raw_response = await run_endpoint_function(
Oct 26 07:44:17 PM                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
Oct 26 07:44:17 PM      return await run_in_threadpool(dependant.call, **values)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
Oct 26 07:44:17 PM      return await anyio.to_thread.run_sync(func, *args)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
Oct 26 07:44:17 PM      return await get_async_backend().run_sync_in_worker_thread(
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2106, in run_sync_in_worker_thread
Oct 26 07:44:17 PM      return await future
Oct 26 07:44:17 PM             ^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 833, in run
Oct 26 07:44:17 PM      result = context.run(func, *args)
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in search_orders
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in <listcomp>
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM                ^^^^^^^^^
Oct 26 07:44:17 PM  ValueError: dictionary update sequence element #0 has length 17; 2 is required
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=item_sku&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
Oct 26 07:44:17 PM      response = await func(request)
Oct 26 07:44:17 PM                 ^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
Oct 26 07:44:17 PM      raw_response = await run_endpoint_function(
Oct 26 07:44:17 PM                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
Oct 26 07:44:17 PM      return await run_in_threadpool(dependant.call, **values)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
Oct 26 07:44:17 PM      return await anyio.to_thread.run_sync(func, *args)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
Oct 26 07:44:17 PM      return await get_async_backend().run_sync_in_worker_thread(
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2106, in run_sync_in_worker_thread
Oct 26 07:44:17 PM      return await future
Oct 26 07:44:17 PM             ^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 833, in run
Oct 26 07:44:17 PM      result = context.run(func, *args)
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in search_orders
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in <listcomp>
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM                ^^^^^^^^^
Oct 26 07:44:17 PM  ValueError: dictionary update sequence element #0 has length 13; 2 is required
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=line_item_total&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
Oct 26 07:44:17 PM      response = await func(request)
Oct 26 07:44:17 PM                 ^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
Oct 26 07:44:17 PM      raw_response = await run_endpoint_function(
Oct 26 07:44:17 PM                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
Oct 26 07:44:17 PM      return await run_in_threadpool(dependant.call, **values)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
Oct 26 07:44:17 PM      return await anyio.to_thread.run_sync(func, *args)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
Oct 26 07:44:17 PM      return await get_async_backend().run_sync_in_worker_thread(
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2106, in run_sync_in_worker_thread
Oct 26 07:44:17 PM      return await future
Oct 26 07:44:17 PM             ^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 833, in run
Oct 26 07:44:17 PM      result = context.run(func, *args)
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in search_orders
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in <listcomp>
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM                ^^^^^^^^^
Oct 26 07:44:17 PM  ValueError: dictionary update sequence element #0 has length 11; 2 is required
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=customer_name&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
Oct 26 07:44:17 PM      response = await func(request)
Oct 26 07:44:17 PM                 ^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
Oct 26 07:44:17 PM      raw_response = await run_endpoint_function(
Oct 26 07:44:17 PM                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
Oct 26 07:44:17 PM      return await run_in_threadpool(dependant.call, **values)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
Oct 26 07:44:17 PM      return await anyio.to_thread.run_sync(func, *args)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
Oct 26 07:44:17 PM      return await get_async_backend().run_sync_in_worker_thread(
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2106, in run_sync_in_worker_thread
Oct 26 07:44:17 PM      return await future
Oct 26 07:44:17 PM             ^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 833, in run
Oct 26 07:44:17 PM      result = context.run(func, *args)
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in search_orders
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in <listcomp>
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM                ^^^^^^^^^
Oct 26 07:44:17 PM  ValueError: dictionary update sequence element #0 has length 17; 2 is required
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=timestamp&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app
Oct 26 07:44:17 PM      response = await func(request)
Oct 26 07:44:17 PM                 ^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 235, in app
Oct 26 07:44:17 PM      raw_response = await run_endpoint_function(
Oct 26 07:44:17 PM                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 163, in run_endpoint_function
Oct 26 07:44:17 PM      return await run_in_threadpool(dependant.call, **values)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/concurrency.py", line 41, in run_in_threadpool
Oct 26 07:44:17 PM      return await anyio.to_thread.run_sync(func, *args)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/to_thread.py", line 33, in run_sync
Oct 26 07:44:17 PM      return await get_async_backend().run_sync_in_worker_thread(
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 2106, in run_sync_in_worker_thread
Oct 26 07:44:17 PM      return await future
Oct 26 07:44:17 PM             ^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/anyio/_backends/_asyncio.py", line 833, in run
Oct 26 07:44:17 PM      result = context.run(func, *args)
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in search_orders
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/src/api/carts.py", line 75, in <listcomp>
Oct 26 07:44:17 PM      orders = [dict(row) for row in result]
Oct 26 07:44:17 PM                ^^^^^^^^^
Oct 26 07:44:17 PM  ValueError: dictionary update sequence element #0 has length 17; 2 is required
Oct 26 07:44:17 PM  INFO:     129.65.145.157:0 - "GET /carts/search/?sort_col=customer_name&sort_order=desc HTTP/1.1" 500 Internal Server Error
Oct 26 07:44:17 PM  ERROR:    Exception in ASGI application
Oct 26 07:44:17 PM  Traceback (most recent call last):
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 407, in run_asgi
Oct 26 07:44:17 PM      result = await app(  # type: ignore[func-returns-value]
Oct 26 07:44:17 PM               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
Oct 26 07:44:17 PM      return await self.app(scope, receive, send)
Oct 26 07:44:17 PM             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 270, in __call__
Oct 26 07:44:17 PM      await super().__call__(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 124, in __call__
Oct 26 07:44:17 PM      await self.middleware_stack(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 184, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 162, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, _send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 92, in __call__
Oct 26 07:44:17 PM      await self.simple_response(scope, receive, send, request_headers=headers)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 147, in simple_response
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
Oct 26 07:44:17 PM      raise exc
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, sender)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 21, in __call__
Oct 26 07:44:17 PM      raise e
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 706, in __call__
Oct 26 07:44:17 PM      await route.handle(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 276, in handle
Oct 26 07:44:17 PM      await self.app(scope, receive, send)
Oct 26 07:44:17 PM    File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 66, in app