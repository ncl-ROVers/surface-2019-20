#include "ServerCore.h"

#define BUFFER_SIZE 4096

ServerCore::~ServerCore()
{
	
}

void ServerCore::processMessage(const char* inputBuffer, int inputLength, char* outputBuffer, int& outputLength)
{
	//Copy input message to output
	memcpy(outputBuffer, inputBuffer, inputLength);
	outputLength = inputLength;
}

void ServerCore::launchServer(int port)
{
	if (!m_mainThread)
	{
		LOG_VERBOSE("Launching server on port ", port);

		m_serverSocket = new ServerSocket();
		m_serverSocket->bind(port);
		m_serverSocket->listen();

		m_mainThread = new std::thread(&ServerCore::run, this);
	}
	else
	{
		LOG_WARN("Attempting to launch the server while it is already running.");
	}
}

void ServerCore::run()
{
	m_syncMutex.lock();
	m_socket = new Socket(m_serverSocket->accept());
	m_syncMutex.unlock();

	char readBuffer[BUFFER_SIZE];
	char writeBuffer[BUFFER_SIZE];

	while (true)
	{
		//Receive message
		int msgLength = m_socket->receive(readBuffer, BUFFER_SIZE);
		if (msgLength <= 0)
		{
			break;
		}

		//Process message
		int outputLength = 0;
		processMessage(readBuffer, msgLength, writeBuffer, outputLength);

		//Send response
		m_socket->send(writeBuffer, outputLength);
	}
}

void ServerCore::shutdownServer()
{
	if (m_mainThread)
	{
		LOG_VERBOSE("Shutting down server...");

		//Delete sockets
		m_syncMutex.lock();

		m_serverSocket->close();
		if (m_socket)
		{
			m_socket->close();
		}

		m_syncMutex.unlock();

		//Wait for main server thread to finish
		m_mainThread->join();

		delete m_mainThread;
		delete m_socket;

		m_mainThread = nullptr;
		m_socket = nullptr;

		LOG_VERBOSE("Server shutdown complete");
	}
}