#!/usr/bin/env python3
"""
Test Custom Handlers Example
Tests custom Python handlers with a simple client.
"""

import asyncio
import rsocket_rust

def echo_handler(payload):
    """Simple echo handler for request-response"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"🔄 Server received: {data}")
    
    response = (rsocket_rust.Payload.builder()
                .set_data_utf8(f"Server says: {data}")
                .build())
    return response

def stream_handler(payload):
    """Handler that returns multiple items for request-stream"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📡 Stream request: {data}")
    
    responses = []
    for i in range(5):
        response = (rsocket_rust.Payload.builder()
                    .set_data_utf8(f"Stream {i+1}: {data}")
                    .build())
        responses.append(response)
    return responses

async def run_server():
    """Run the custom server"""
    print("🚀 Starting test server with custom handlers...")
    
    handler = (rsocket_rust.RSocketHandler()
               .request_response(echo_handler)
               .request_stream(stream_handler))
    
    tcp_transport = rsocket_rust.TcpServerTransport("127.0.0.1:7879")
    
    server = (rsocket_rust.MultiTransportServerBuilder()
              .add_tcp_transport("TCP", tcp_transport)
              .acceptor(handler)
              .on_start(lambda: print("✅ Test server started!")))
    
    await server.serve()

async def run_client():
    """Run test client"""
    await asyncio.sleep(2)
    
    print("🔗 Connecting to test server...")
    
    try:
        client = await rsocket_rust.RSocketFactory.connect_tcp(
            rsocket_rust.TcpClientTransport("127.0.0.1:7879")
        )
        
        print("✅ Connected successfully!")
        
        payload = (rsocket_rust.Payload.builder()
                   .set_data_utf8("Hello from test client!")
                   .build())
        
        print("📤 Testing request-response...")
        response = await client.request_response(payload)
        if response:
            print(f"📥 Response: {response.data_utf8()}")
        
        print("📤 Testing request-stream...")
        stream_payload = (rsocket_rust.Payload.builder()
                          .set_data_utf8("Stream test")
                          .build())
        
        responses = await client.request_stream(stream_payload)
        print(f"📥 Received {len(responses)} stream items:")
        for i, resp in enumerate(responses):
            print(f"   {i+1}: {resp.data_utf8()}")
            
    except Exception as e:
        print(f"❌ Client error: {e}")

async def main():
    """Main test function"""
    print("🧪 Testing Custom Python Handlers")
    
    server_task = asyncio.create_task(run_server())
    client_task = asyncio.create_task(run_client())
    
    try:
        await asyncio.wait_for(client_task, timeout=10.0)
        print("✅ Test completed successfully!")
    except asyncio.TimeoutError:
        print("⏰ Test timed out")
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
