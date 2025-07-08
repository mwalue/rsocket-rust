#!/usr/bin/env python3
"""
True Reactive RSocket Server Example
Demonstrates proper reactive streaming with Python generators.
"""

import asyncio
import time
import rsocket_rust

def reactive_request_response(payload):
    """Simple request-response handler"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📞 Request-Response: {data}")
    
    response = (rsocket_rust.Payload.builder()
                .set_data_utf8(f"Response: {data}")
                .build())
    return response

def reactive_request_stream(payload):
    """True reactive streaming with Python generator"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📡 Starting reactive stream for: {data}")
    
    def stream_generator():
        """Generator that yields items lazily - true reactive streaming"""
        for i in range(10):
            print(f"  📤 Yielding reactive item {i+1}")
            response = (rsocket_rust.Payload.builder()
                        .set_data_utf8(f"Reactive item {i+1}: {data} (generated at {time.time():.3f})")
                        .set_metadata_utf8(f"reactive-{i+1}")
                        .build())
            yield response
    
    return stream_generator()

def infinite_stream_handler(payload):
    """Infinite stream generator for testing cancellation"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"🔄 Starting infinite stream for: {data}")
    
    def infinite_generator():
        counter = 0
        while True:
            counter += 1
            print(f"  📤 Infinite item {counter}")
            response = (rsocket_rust.Payload.builder()
                        .set_data_utf8(f"Infinite item {counter}: {data}")
                        .set_metadata_utf8(f"infinite-{counter}")
                        .build())
            yield response
    
    return infinite_generator()

def batch_stream_handler(payload):
    """Fallback: static list for backward compatibility"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📦 Batch stream for: {data}")
    
    responses = []
    for i in range(3):
        response = (rsocket_rust.Payload.builder()
                    .set_data_utf8(f"Batch item {i+1}: {data}")
                    .build())
        responses.append(response)
    return responses

async def main():
    print("🚀 Starting True Reactive RSocket Server")
    print("🌊 Demonstrating real reactive streaming patterns")
    
    handler = (rsocket_rust.RSocketHandler()
               .request_response(reactive_request_response)
               .request_stream(reactive_request_stream))  # Uses generator
    
    tcp_transport = rsocket_rust.TcpServerTransport("127.0.0.1:7881")
    
    def on_start():
        print("🎉 True Reactive Server Started!")
        print("📋 Ready to accept connections on TCP 127.0.0.1:7881")
        print("🌊 Stream handlers use Python generators for true reactivity")
        print("🔄 Use Ctrl+C to stop the server")
        print()
        print("Test with:")
        print("  python examples/test_true_reactive.py")
    
    server = (rsocket_rust.MultiTransportServerBuilder()
              .add_tcp_transport("TCP", tcp_transport)
              .acceptor(handler)
              .on_start(on_start))
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
