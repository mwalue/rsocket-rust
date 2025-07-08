use pyo3::prelude::*;

mod payload;
mod client;
mod server;
mod transport;
mod factory;
mod py_rsocket;

use payload::{PyPayload, PyPayloadBuilder};
use client::PyClient;
use server::PyMultiTransportServerBuilder;
use transport::*;
use factory::PyRSocketFactory;
use py_rsocket::PyRSocketHandler;

#[pymodule]
fn rsocket_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyPayload>()?;
    m.add_class::<PyPayloadBuilder>()?;
    m.add_class::<PyClient>()?;
    m.add_class::<PyMultiTransportServerBuilder>()?;
    m.add_class::<PyRSocketFactory>()?;
    m.add_class::<PyRSocketHandler>()?;
    
    m.add_class::<PyTcpClientTransport>()?;
    m.add_class::<PyTcpServerTransport>()?;
    m.add_class::<PyWebSocketClientTransport>()?;
    m.add_class::<PyWebSocketServerTransport>()?;
    m.add_class::<PyQuinnClientTransport>()?;
    m.add_class::<PyQuinnServerTransport>()?;
    m.add_class::<PyIrohClientTransport>()?;
    m.add_class::<PyIrohServerTransport>()?;
    
    Ok(())
}
