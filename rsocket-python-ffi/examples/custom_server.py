#!/usr/bin/env python3
"""
Custom RSocket Server Example
Demonstrates custom Python handlers for all RSocket interaction patterns.
"""

import asyncio
import rsocket_rust

def custom_metadata_push(payload):
    """Handle metadata push requests"""
    metadata = payload.metadata_utf8() if payload.metadata_utf8() else "No metadata"
    print(f"📋 Metadata Push: {metadata}")

def custom_fire_and_forget(payload):
    """Handle fire-and-forget requests"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"🔥 Fire and Forget: {data}")

def custom_request_response(payload):
    """Handle request-response requests"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📞 Request-Response: {data}")
    
    response = (rsocket_rust.Payload.builder()
                .set_data_utf8(f"Custom Echo: {data}")
                .set_metadata_utf8("custom-response")
                .build())
    return response

def custom_request_stream(payload):
    """Handle request-stream requests with true reactive streaming"""
    data = payload.data_utf8() if payload.data_utf8() else "No data"
    print(f"📡 Request-Stream: {data}")
    
    def stream_generator():
        """Python generator for true reactive streaming"""
        for i in range(5):
            print(f"  📤 Generating stream item {i+1}")
            response = (rsocket_rust.Payload.builder()
                        .set_data_utf8(f"Reactive stream item {i+1}: {data}")
                        .set_metadata_utf8(f"stream-{i+1}")
                        .build())
            yield response
    
    return stream_generator()

def custom_request_channel(payloads):
    """Handle request-channel requests"""
    print(f"🔄 Request-Channel: {len(payloads)} items")
    
    responses = []
    for i, payload in enumerate(payloads):
        data = payload.data_utf8() if payload.data_utf8() else f"No data {i}"
        response = (rsocket_rust.Payload.builder()
                    .set_data_utf8(f"Channel response {i+1}: {data}")
                    .set_metadata_utf8(f"channel-{i+1}")
                    .build())
        responses.append(response)
    return responses

async def main():
    print("🚀 Starting Custom RSocket Server")
    print("🎯 Using custom Python handlers for all interaction patterns")
    
    handler = (rsocket_rust.RSocketHandler()
               .metadata_push(custom_metadata_push)
               .fire_and_forget(custom_fire_and_forget)
               .request_response(custom_request_response)
               .request_stream(custom_request_stream)
               .request_channel(custom_request_channel))
    
    tcp_transport = rsocket_rust.TcpServerTransport("127.0.0.1:7879")
    
    def on_start():
        print("🎉 Custom Server Started!")
        print("📋 Ready to accept connections on TCP 127.0.0.1:7878")
        print("🔄 Use Ctrl+C to stop the server")
    
    server = (rsocket_rust.MultiTransportServerBuilder()
              .add_tcp_transport("TCP", tcp_transport)
              .acceptor(handler)
              .on_start(on_start))
    
    print("🔧 Server configured with custom Python handlers")
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
