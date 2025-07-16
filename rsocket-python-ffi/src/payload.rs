use pyo3::prelude::*;
use pyo3::types::PyBytes;
use rsocket_rust::prelude::{Payload, PayloadBuilder};
use bytes::Bytes;

#[pyclass(name = "Payload")]
#[derive(Clone)]
pub struct PyPayload {
    inner: Payload,
}

#[pymethods]
impl PyPayload {
    #[new]
    fn new(data: Option<Vec<u8>>, metadata: Option<Vec<u8>>) -> Self {
        let data_bytes = data.map(Bytes::from);
        let metadata_bytes = metadata.map(Bytes::from);
        PyPayload {
            inner: Payload::new(data_bytes, metadata_bytes),
        }
    }

    #[staticmethod]
    fn builder() -> PyPayloadBuilder {
        PyPayloadBuilder {
            inner: Payload::builder(),
        }
    }

    fn data(&self) -> Option<Vec<u8>> {
        self.inner.data().map(|bytes| bytes.to_vec())
    }

    fn metadata(&self) -> Option<Vec<u8>> {
        self.inner.metadata().map(|bytes| bytes.to_vec())
    }

    fn data_buffer<'py>(&self, py: Python<'py>) -> Option<Bound<'py, PyBytes>> {
        self.inner.data().map(|bytes| {
            PyBytes::new_bound(py, bytes.as_ref())
        })
    }

    fn metadata_buffer<'py>(&self, py: Python<'py>) -> Option<Bound<'py, PyBytes>> {
        self.inner.metadata().map(|bytes| {
            PyBytes::new_bound(py, bytes.as_ref())
        })
    }

    fn data_memoryview<'py>(&self, py: Python<'py>) -> PyResult<Option<Bound<'py, PyAny>>> {
        if let Some(bytes) = self.inner.data() {
            let py_bytes = PyBytes::new_bound(py, bytes.as_ref());
            let memoryview = py.import_bound("builtins")?.getattr("memoryview")?.call1((py_bytes,))?;
            Ok(Some(memoryview))
        } else {
            Ok(None)
        }
    }

    fn metadata_memoryview<'py>(&self, py: Python<'py>) -> PyResult<Option<Bound<'py, PyAny>>> {
        if let Some(bytes) = self.inner.metadata() {
            let py_bytes = PyBytes::new_bound(py, bytes.as_ref());
            let memoryview = py.import_bound("builtins")?.getattr("memoryview")?.call1((py_bytes,))?;
            Ok(Some(memoryview))
        } else {
            Ok(None)
        }
    }

    fn data_utf8(&self) -> Option<String> {
        self.inner.data_utf8().map(|s| s.to_string())
    }

    fn metadata_utf8(&self) -> Option<String> {
        self.inner.metadata_utf8().map(|s| s.to_string())
    }

    fn is_empty(&self) -> bool {
        self.inner.is_empty()
    }

    fn len(&self) -> usize {
        self.inner.len()
    }

    fn __str__(&self) -> String {
        format!("Payload(data={:?}, metadata={:?})", 
                self.inner.data_utf8(), 
                self.inner.metadata_utf8())
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }

}

impl PyPayload {
    pub fn from_rust(payload: Payload) -> Self {
        PyPayload { inner: payload }
    }

    pub fn to_rust(self) -> Payload {
        self.inner
    }

    pub fn inner_ref(&self) -> &Payload {
        &self.inner
    }
}

#[pyclass(name = "PayloadBuilder")]
pub struct PyPayloadBuilder {
    inner: PayloadBuilder,
}

#[pymethods]
impl PyPayloadBuilder {
    #[new]
    fn new() -> Self {
        PyPayloadBuilder {
            inner: Payload::builder(),
        }
    }

    fn set_data(mut self_: PyRefMut<Self>, data: Vec<u8>) -> PyRefMut<Self> {
        self_.inner = std::mem::replace(&mut self_.inner, Payload::builder()).set_data(data);
        self_
    }

    fn set_metadata(mut self_: PyRefMut<Self>, metadata: Vec<u8>) -> PyRefMut<Self> {
        self_.inner = std::mem::replace(&mut self_.inner, Payload::builder()).set_metadata(metadata);
        self_
    }

    fn set_data_utf8<'a>(mut self_: PyRefMut<'a, Self>, data: &str) -> PyRefMut<'a, Self> {
        self_.inner = std::mem::replace(&mut self_.inner, Payload::builder()).set_data_utf8(data);
        self_
    }

    fn set_metadata_utf8<'a>(mut self_: PyRefMut<'a, Self>, metadata: &str) -> PyRefMut<'a, Self> {
        self_.inner = std::mem::replace(&mut self_.inner, Payload::builder()).set_metadata_utf8(metadata);
        self_
    }

    fn build(mut self_: PyRefMut<Self>) -> PyPayload {
        let builder = std::mem::replace(&mut self_.inner, Payload::builder());
        PyPayload {
            inner: builder.build(),
        }
    }
}
