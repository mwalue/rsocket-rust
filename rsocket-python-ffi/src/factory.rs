use pyo3::prelude::*;
use pyo3_async_runtimes::tokio::future_into_py;
use rsocket_rust::prelude::RSocketFactory;
use crate::client::PyClient;
use crate::server::PyMultiTransportServerBuilder;
use crate::transport::*;

#[pyclass(name = "RSocketFactory")]
pub struct PyRSocketFactory;


#[pymethods]
impl PyRSocketFactory {
    #[new]
    fn new() -> Self {
        PyRSocketFactory
    }

    #[staticmethod]
    fn connect_tcp<'py>(py: Python<'py>, transport: PyTcpClientTransport) -> PyResult<Bound<'py, PyAny>> {
        future_into_py(py, async move {
            match RSocketFactory::connect()
                .transport(transport.to_rust())
                .start()
                .await
            {
                Ok(client) => Ok(PyClient::from_rust(client)),
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("TCP connection failed: {}", e))),
            }
        })
    }

    #[staticmethod]
    fn connect_websocket<'py>(py: Python<'py>, transport: PyWebSocketClientTransport) -> PyResult<Bound<'py, PyAny>> {
        future_into_py(py, async move {
            match RSocketFactory::connect()
                .transport(transport.to_rust())
                .start()
                .await
            {
                Ok(client) => Ok(PyClient::from_rust(client)),
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("WebSocket connection failed: {}", e))),
            }
        })
    }

    #[staticmethod]
    fn connect_quic<'py>(py: Python<'py>, transport: PyQuinnClientTransport) -> PyResult<Bound<'py, PyAny>> {
        future_into_py(py, async move {
            match RSocketFactory::connect()
                .transport(transport.to_rust())
                .start()
                .await
            {
                Ok(client) => Ok(PyClient::from_rust(client)),
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("QUIC connection failed: {}", e))),
            }
        })
    }

    #[staticmethod]
    fn connect_iroh<'py>(py: Python<'py>, transport: PyIrohClientTransport) -> PyResult<Bound<'py, PyAny>> {
        future_into_py(py, async move {
            match RSocketFactory::connect()
                .transport(transport.to_rust())
                .start()
                .await
            {
                Ok(client) => Ok(PyClient::from_rust(client)),
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Iroh connection failed: {}", e))),
            }
        })
    }

    #[staticmethod]
    fn receive_multi_transport() -> PyMultiTransportServerBuilder {
        PyMultiTransportServerBuilder::new()
    }

    fn __str__(&self) -> String {
        "RSocketFactory".to_string()
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }
}
