use pyo3::prelude::*;
use pyo3_async_runtimes::tokio::future_into_py;
use rsocket_rust::{MultiTransportServerBuilder};
use rsocket_rust::prelude::ServerResponder;
use rsocket_rust::utils::EchoRSocket;
use crate::transport::*;
use crate::payload::PyPayload;
use crate::py_rsocket::{PyRSocketHandler, PyRSocket};

#[pyclass(name = "MultiTransportServerBuilder")]
pub struct PyMultiTransportServerBuilder {
    inner: Option<MultiTransportServerBuilder>,
}

#[pymethods]
impl PyMultiTransportServerBuilder {
    #[new]
    pub fn new() -> Self {
        PyMultiTransportServerBuilder {
            inner: Some(MultiTransportServerBuilder::new()),
        }
    }

    fn add_tcp_transport(mut self_: PyRefMut<Self>, name: String, transport: PyTcpServerTransport) -> PyResult<PyRefMut<Self>> {
        if let Some(builder) = self_.inner.take() {
            self_.inner = Some(builder.add_transport(name, transport.to_rust()));
            Ok(self_)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn add_websocket_transport(mut self_: PyRefMut<Self>, name: String, transport: PyWebSocketServerTransport) -> PyResult<PyRefMut<Self>> {
        if let Some(builder) = self_.inner.take() {
            self_.inner = Some(builder.add_transport(name, transport.to_rust()));
            Ok(self_)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn add_quic_transport(mut self_: PyRefMut<Self>, name: String, transport: PyQuinnServerTransport) -> PyResult<PyRefMut<Self>> {
        if let Some(builder) = self_.inner.take() {
            self_.inner = Some(builder.add_transport(name, transport.to_rust()));
            Ok(self_)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn add_iroh_transport(mut self_: PyRefMut<Self>, name: String, transport: PyIrohServerTransport) -> PyResult<PyRefMut<Self>> {
        if let Some(builder) = self_.inner.take() {
            self_.inner = Some(builder.add_transport(name, transport.to_rust()));
            Ok(self_)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn acceptor(mut self_: PyRefMut<Self>, handler: Option<PyRSocketHandler>) -> PyResult<PyRefMut<Self>> {
        if let Some(builder) = self_.inner.take() {
            let acceptor: ServerResponder = if let Some(py_handler) = handler {
                Box::new(move |_setup, _socket| {
                    Ok(Box::new(PyRSocket::new(py_handler.clone())) as Box<dyn rsocket_rust::prelude::RSocket>)
                })
            } else {
                Box::new(move |_setup, _socket| {
                    Ok(Box::new(EchoRSocket) as Box<dyn rsocket_rust::prelude::RSocket>)
                })
            };

            self_.inner = Some(builder.acceptor(acceptor));
            Ok(self_)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn fragment(mut self_: PyRefMut<Self>, mtu: usize) -> PyResult<PyRefMut<Self>> {
        if let Some(builder) = self_.inner.take() {
            self_.inner = Some(builder.fragment(mtu));
            Ok(self_)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn on_start(mut self_: PyRefMut<Self>, handler: Option<PyObject>) -> PyResult<PyRefMut<Self>> {
        if let Some(builder) = self_.inner.take() {
            let start_handler = if let Some(h) = handler {
                Box::new(move || {
                    Python::with_gil(|py| {
                        let _ = h.call0(py);
                    });
                }) as Box<dyn FnMut() + Send + Sync>
            } else {
                Box::new(|| {}) as Box<dyn FnMut() + Send + Sync>
            };

            self_.inner = Some(builder.on_start(start_handler));
            Ok(self_)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn serve<'py>(&mut self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        if let Some(builder) = self.inner.take() {
            future_into_py(py, async move {
                builder.serve().await
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Server failed: {}", e)))
            })
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Builder already consumed"))
        }
    }

    fn __str__(&self) -> String {
        "MultiTransportServerBuilder".to_string()
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }
}
