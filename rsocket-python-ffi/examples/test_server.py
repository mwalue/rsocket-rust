#!/usr/bin/env python3
"""
Simple RSocket test server for benchmarking
Starts TCP, WebSocket, and QUIC servers for testing
"""

import asyncio
import rsocket_rust

def echo_handler(setup_payload):
    """Simple echo handler that returns the same payload"""
    print(f"🔗 New connection with setup: {setup_payload}")
    return None

async def start_servers():
    print('🚀 Starting RSocket test servers...')
    
    try:
        tcp_transport = rsocket_rust.TcpServerTransport('127.0.0.1:7878')
        ws_transport = rsocket_rust.WebSocketServerTransport('127.0.0.1:7879')
        quic_transport = rsocket_rust.QuinnServerTransport('127.0.0.1:7880')
        
        server_builder = (rsocket_rust.MultiTransportServerBuilder()
                         .add_tcp_transport("TCP", tcp_transport)
                         .add_websocket_transport("WebSocket", ws_transport)
                         .add_quic_transport("QUIC", quic_transport)
                         .acceptor(echo_handler)
                         .on_start(lambda: print("🎉 Multi-Transport Server Started!")))
        
        print('✅ TCP server configured on 127.0.0.1:7878')
        print('✅ WebSocket server configured on 127.0.0.1:7879')
        print('✅ QUIC server configured on 127.0.0.1:7880')
        print('🎯 Starting server...')
        
        await server_builder.serve()
            
    except Exception as e:
        print(f'❌ Server startup failed: {e}')
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    asyncio.run(start_servers())
