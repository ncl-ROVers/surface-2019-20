#include "EntityCamera.h"

#include "io/Logger.h"

#include "graphics/stb/stb_image_write.h"

#include <vector>

EntityCamera::EntityCamera(int width, int height, float fov, int port, int quality)
{
	m_framebuffer.create(width, height);

	CameraSettings settings;
	settings.allowLooking = false;
	settings.allowMovement = false;
	settings.fov = fov;
	
	m_camera.fromSettings(settings);
	m_camera.resize(width, height);

	//Move to better location
	m_socketRunning = true;
	m_streamingThread = new std::thread(&EntityCamera::streamConnection, this, port, quality);
}

EntityCamera::~EntityCamera()
{
	if (m_streamingThread)
	{
		//Close socket
		m_socketRunning = false;
		if (m_serverSocket)
		{
			m_serverSocket->close();
		}

		//Destroy thread
		m_streamingThread->join();
		delete m_streamingThread;
	}

	m_framebuffer.destroy();
}

void EntityCamera::render(RenderingEngine& renderer)
{
	//Set the camera's translation, rotation and scale to match the entity's
	m_camera.setViewMatrix(glm::inverse(m_transform.matrix()));

	renderer.enqueueRender(m_camera, m_framebuffer);
}

void EntityCamera::renderFinished()
{
	m_frameData.resize(4 * m_framebuffer.getWidth() * m_framebuffer.getHeight());
	m_framebuffer.readPixels(&m_frameData[0]);
}

void EntityCamera::streamConnection(int port, int quality)
{
	m_serverSocket = new ServerSocket();
	m_serverSocket->bind(port);
	m_serverSocket->listen();

	while (m_socketRunning)
	{
		Socket socket(m_serverSocket->accept());

		//Check if server socket was closed from main thread
		if (m_serverSocket->isClosed())
		{
			break;
		}

		//Send header
		char readBuffer[4096];
		int msgLength = socket.receive(readBuffer, 4096);

		if (msgLength <= 0) break;
		readBuffer[msgLength] = 0;

		std::stringstream header;
		header << "HTTP/1.0 200 OK\r\n";
		header << "Server: ROVSimulation\r\n";
		header << "Connection: close\r\n";
		header << "Max-Age: 0\r\n";
		header << "Expires: 0\r\n";
		header << "Cache-Control: no-cache, private\r\n";
		header << "Pragma: no-cache\r\n";
		header << "Content-Type: multipart/x-mixed-replace; boundary=mjpegstream\r\n\r\n";

		socket.send(header.str().c_str(), header.str().length());

		std::vector<char> imageData(1024);

		using namespace std::chrono_literals;
		std::this_thread::sleep_for(10ms);

		while (!socket.isClosed() && m_socketRunning)
		{
			//Encode image data
			imageData.clear();

			stbi_flip_vertically_on_write(true);
			stbi_write_jpg_to_func([](void* context, void* data, int size)
			{
				std::vector<unsigned char>* buffer = ((std::vector<unsigned char>*)context);

				size_t writeIndex = buffer->size();
				buffer->resize(writeIndex + size);

				memcpy(&buffer->at(writeIndex), data, size);
			}, &imageData, m_framebuffer.getWidth(), m_framebuffer.getHeight(), 4, m_frameData.data(), quality);

			//Send response
			std::stringstream frame;
			frame << "--mjpegstream\r\n";
			frame << "Content-type: image/jpeg\r\n";
			frame << "Content-Length: " << imageData.size() << "\r\n\r\n";

			socket.send(frame.str().c_str(), frame.str().size());
			socket.send(imageData.data(), imageData.size());

			std::this_thread::sleep_for(50ms);
		}

		socket.close();
	}
	
	m_serverSocket->close();
}
