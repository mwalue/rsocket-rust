#!/usr/bin/env python3
"""
Reactive Stream Server Example
Demonstrates true reactive streaming with Python generators.
"""

import asyncio
import time
import rsocket_rust

def reactive_stream_handler(payload):
    """Generator that yields items over time - true reactive streaming"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📡 Starting reactive stream for: {data}")
    
    def stream_generator():
        for i in range(5):
            time.sleep(0.1)  # Small delay to demonstrate reactive nature
            response = (rsocket_rust.Payload.builder()
                        .set_data_utf8(f"Reactive item {i+1}: {data} (timestamp: {time.time():.3f})")
                        .set_metadata_utf8(f"stream-{i+1}")
                        .build())
            print(f"  📤 Yielding item {i+1}")
            yield response
    
    return stream_generator()

def simple_response_handler(payload):
    """Simple request-response handler"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📞 Request-Response: {data}")
    
    response = (rsocket_rust.Payload.builder()
                .set_data_utf8(f"Response: {data}")
                .build())
    return response

async def main():
    print("🚀 Starting Reactive Stream Server")
    print("🌊 Demonstrating true reactive streaming with Python generators")
    
    handler = (rsocket_rust.RSocketHandler()
               .request_response(simple_response_handler)
               .request_stream(reactive_stream_handler))
    
    tcp_transport = rsocket_rust.TcpServerTransport("127.0.0.1:7880")
    
    def on_start():
        print("🎉 Reactive Stream Server Started!")
        print("📋 Ready to accept connections on TCP 127.0.0.1:7880")
        print("🌊 Stream handler will yield items over time")
        print("🔄 Use Ctrl+C to stop the server")
    
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
