from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import time

def generate_urls(base, num):
    for i in xrange(1, num):
        yield base + str(i)

# configure HTTP client backend library, and number of requests to batch together
AsyncHTTPClient.configure("tornado.simple_httpclient.SimpleAsyncHTTPClient", max_clients=10)

# Coroutines may “return” by raising the special exception Return(value)
# Functions with this decorator return a Future.
@gen.coroutine
def run():
    http_client = AsyncHTTPClient()
    urls = generate_urls('http://redmine.scienbizip.com/news/', 100)
    # AsyncHTTPClient.fetch: Executes a request, asynchronously returning an HTTPResponse.
    # We construct an HTTPRequest using any additional kwargs: HTTPRequest(request, **kwargs).
    # This method returns a Future whose result is an HTTPResponse.
    # By default, the Future will raise an HTTPError if the request returned a non-200 response code.
    resp_generator = yield [http_client.fetch(url) for url in urls]
    # HTTP Response object:
    #    request: HTTPRequest object
    #    code: numeric HTTP status code, e.g. 200 or 404
    #    reason: human-readable reason phrase describing the status cod
    #    headers: tornado.httputil.HTTPHeaders object
    #    effective_url: final location of the resource after following any redirects
    #    body: response body as string (created on demand from self.buffer)
    #    request_time: seconds from request start to finish
    resp_sum = sum(len(r.body) for r in resp_generator)
    # gen.Return: Special exception to return a value from a coroutine.
    # If this exception is raised, its value argument is used as the result of the coroutine.
    raise gen.Return(value=resp_sum)

if __name__ == "__main__":
    # Most applications have a single, global IOLoop running on the main thread.
    # Use this method to get this instance from another thread.
    # In most other cases, it is better to use current() to get the current thread’s IOLoop.
    _ioloop = ioloop.IOLoop.instance()
    start = time.time()
    # run_sync: Starts the IOLoop, runs the given function, and stops the loop.
    # If the function returns a Future, the IOLoop will run until the future is resolved.
    # If it raises an exception, the IOLoop will stop and the exception will be re-raised to the caller.
    _ioloop.run_sync(run)
    print time.time() - start


