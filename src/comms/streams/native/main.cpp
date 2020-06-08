#include <stdio.h>
#include <cassert>

//Documentation for pybind11: https://pybind11.readthedocs.io/en/master/index.html
#include <pybind11/pybind11.h>

//Documentation for libde265: https://github.com/strukturag/libde265/wiki/Decoder-API-Tutorial
#include <libde265/de265.h>

class DecodedFrame
{
private:
	const uint8_t* m_imgBuffer = nullptr;

	int m_width = 0;
	int m_height = 0;
public:
	DecodedFrame() {}
	DecodedFrame(const uint8_t* buffer, int width, int height) :
		m_imgBuffer(buffer), m_width(width), m_height(height) {}

	uint8_t* buffer() const { return const_cast<uint8_t*>(m_imgBuffer); }

	int width() const { return m_width; }
	int height() const { return m_height; }
};

//Define stream class
class H265Decoder
{
private:
	int m_rtpPort = 0;
	int m_rtcpPort = 0;

	uint8_t* m_data = nullptr;

	de265_decoder_context* m_decoder = nullptr;
public:
	H265Decoder(int rtpPort, int rtcpPort) :
		m_rtpPort(rtpPort), m_rtcpPort(rtcpPort) {}

	void open();
	void close();

	DecodedFrame acquireLatestFrame();
};

//Define pytohn bindings for streaming classes
namespace py = pybind11;

PYBIND11_MODULE(cstreaming, m)
{
	py::class_<DecodedFrame>(m, "DecodedFrame", py::buffer_protocol())
		.def(py::init<>())
		.def_buffer([](DecodedFrame& frame) -> py::buffer_info {
			return py::buffer_info(
				frame.buffer(),
				sizeof(uint8_t),
				py::format_descriptor<uint8_t>::format(),
				3,
				{ frame.width(), frame.height(), 3 },
				{ 3 * sizeof(uint8_t) * frame.height(),
				  3 * sizeof(uint8_t),
				  sizeof(uint8_t) }
			);
		});

	py::class_<H265Decoder>(m, "H265Decoder")
		.def(py::init<int, int>())
		.def("open", &H265Decoder::open)
		.def("close", &H265Decoder::close)
		.def("acquire_latest_frame", &H265Decoder::acquireLatestFrame);
}

#define DECODER_CHECK(x) assert(x == DE265_OK)

//Stream class implementation
void H265Decoder::open()
{
	m_decoder = de265_new_decoder();
	//de265_set_limit_TID

	m_data = new uint8_t[256 * 256 * 3];
	for (int i = 0; i < 256; ++i)
	{
		for (int j = 0; j < 256; ++j)
		{
			int index = j + 256 * i;

			m_data[3 * index] = j;
			m_data[3 * index + 1] = i;
			m_data[3 * index + 2] = 128;
		}
	}

	//DECODER_CHECK(de265_start_worker_threads(m_decoder, 2));
}

DecodedFrame H265Decoder::acquireLatestFrame()
{
	/*const de265_image* image = de265_get_next_picture(m_decoder);

	if (image)
	{
		return DecodedFrame(nullptr, 0, 0);
	}

	int width = de265_get_image_width(image, 0);
	int height = de265_get_image_height(image, 0);
	const uint8_t* buffer = de265_get_image_plane(image, 0, nullptr);

	return DecodedFrame(buffer, width, height);*/

	return DecodedFrame(m_data, 256, 256);
}

void H265Decoder::close()
{
	delete[] m_data;

	de265_free_decoder(m_decoder);
}