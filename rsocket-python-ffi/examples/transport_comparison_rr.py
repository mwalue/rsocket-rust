#!/usr/bin/env python3
"""
Transport Performance Comparison
Compares performance across different transport types.
"""

import asyncio
import time
import rsocket_rust

URL = "127.0.0.1"
# URL = "3.67.9.236"

print(f"URL = {URL}")

async def benchmark_transport(transport_name, client_factory, num_requests=10000):
    """Benchmark a specific transport"""
    print(f"\n🏃 Benchmarking {transport_name} Transport ({num_requests} requests)")
    
    try:
        client = await client_factory()
        
        payload = (rsocket_rust.Payload.builder()
                   .set_data_utf8(f"Benchmark payload from {transport_name}")
                   .build())
        
        start_time = time.time()
        
        for i in range(num_requests):
            response = await client.request_response(payload)
            if not response:
                print(f"❌ Request {i+1} failed")
                return None
        
        end_time = time.time()
        duration = end_time - start_time
        rps = num_requests / duration
        
        print(f"✅ {transport_name}: {duration:.3f}s total, {rps:.1f} req/s")
        return rps
        
    except Exception as e:
        print(f"❌ {transport_name} benchmark failed: {e}")
        return None


async def benchmark_concurrent(transport_name, client_factory, num_requests=10000, concurrency=100):
    try:
        client = await client_factory()

        sem = asyncio.Semaphore(concurrency)

        async def send_request(i):
            async with sem:
                payload = (rsocket_rust.Payload.builder()
                        .set_data_utf8(f"Benchmark payload {i} from {transport_name}")
                        .build())
                response = await client.request_response(payload)
                if not response:
                    print(f"❌ Request {i+1} failed")
                    return False
                return True

        start_time = time.time()
        
        # Dispatch all requests concurrently, but only `concurrency` at a time
        tasks = [asyncio.create_task(send_request(i)) for i in range(num_requests)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        success = sum(results)
        rps = success / duration

        print(f"✅ Sent: {success}, ❌ Failed: {num_requests - success}")
        print(f"✅ Concurrent {transport_name}: {duration:.3f}s total, {rps:.1f} req/s")
        return rps
    except Exception as e:
        print(f"❌ {transport_name} benchmark failed: {e}")
        return None


async def benchmark_unbounded(transport_name, client_factory, num_requests=10000):

    try:
        client = await client_factory()

        async def send_request(i):
            payload = (rsocket_rust.Payload.builder()
                    .set_data_utf8(f"Benchmark payload {i} from {transport_name}")
                    .build())
            response = await client.request_response(payload)
            if not response:
                print(f"❌ Request {i+1} failed")
                return False
            return True

        start_time = time.time()

        tasks = [asyncio.create_task(send_request(i)) for i in range(num_requests)]
        results = await asyncio.gather(*tasks)

        end_time = time.time()
        duration = end_time - start_time
        success = sum(results)
        rps = success / duration

        print(f"✅ Sent: {success}, ❌ Failed: {num_requests - success}")
        print(f"✅ Unbounded {transport_name}: {duration:.3f}s total, {rps:.1f} req/s")
        return rps
    except Exception as e:
        print(f"❌ {transport_name} benchmark failed: {e}")
        return None
    


async def main():
    print("🏁 RSocket Transport Performance Comparison")
    
    await asyncio.sleep(2)
    
    transports = [
        ("TCP", lambda: rsocket_rust.RSocketFactory.connect_tcp(rsocket_rust.TcpClientTransport(f"{URL}:7878"))),
        ("WebSocket", lambda: rsocket_rust.RSocketFactory.connect_websocket(rsocket_rust.WebSocketClientTransport(f"ws://{URL}:7879"))),
        ("QUIC", lambda: rsocket_rust.RSocketFactory.connect_quic(rsocket_rust.QuinnClientTransport(f"{URL}:7880"))),
    ]
    
    results = {}
    
    for transport_name, client_factory in transports:
        # rps = await benchmark_transport(transport_name, client_factory)
        # rps = await benchmark_concurrent(transport_name, client_factory)
        rps = await benchmark_unbounded(transport_name, client_factory)
        if rps:
            results[transport_name] = rps
    
    if results:
        print("\n📊 Performance Results:")
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        for i, (transport, rps) in enumerate(sorted_results, 1):
            print(f"  {i}. {transport}: {rps:.1f} req/s")
    else:
        print("\n❌ No successful benchmarks")

if __name__ == "__main__":
    asyncio.run(main())
