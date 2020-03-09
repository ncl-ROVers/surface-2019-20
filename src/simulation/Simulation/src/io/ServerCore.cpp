#include "ServerCore.h"

#include "json/json11.hpp"

#define BUFFER_SIZE 4096

ServerCore::~ServerCore()
{
	
}

float normalize(float value, float currentMin, float currentMax, float intendedMin, float intendedMax)
{
	return intendedMin + (value - currentMin) * (intendedMax - intendedMin) / (currentMax - currentMin);
}

void ServerCore::processMessage(const char* inputBuffer, int inputLength, char* outputBuffer, int& outputLength)
{
	using namespace json11;

	std::string err;
	Json root = Json::parse(std::string(inputBuffer, inputLength), err);

	if (!err.empty())
	{
		LOG_ERROR("Error parsing input file: ", err);
		return;
	}

	for (int i = 0; i < THRUSTER_COUNT; ++i)
	{
		m_thrusterPowers[i] = 0.0f;
	}

	for (std::pair<std::string, Json> thruster : root.object_items())
	{
		//Calculate thruster index based on thruster name
		int index = 0;
		index += (thruster.first[2] == 'V') ? 4 : 0;
		index += (thruster.first[3] == 'A') ? 2 : 0;
		index += (thruster.first[4] == 'S') ? 1 : 0;

		m_thrusterPowers[index] = normalize((float)thruster.second.number_value(), 1100, 1900, -1, 1);
	}

	Json response = Json::object{
		{ "test", "empty" }
	};

	std::string responseStr = response.dump();

	memcpy(outputBuffer, responseStr.c_str(), responseStr.size());
	outputLength = responseStr.size();
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
		m_serverSocket->close();

		if (m_socket)
		{
			m_syncMutex.lock();
			m_socket->close();
			m_syncMutex.unlock();
		}

		//Wait for main server thread to finish
		m_mainThread->join();

		delete m_mainThread;
		delete m_socket;

		m_mainThread = nullptr;
		m_socket = nullptr;

		LOG_VERBOSE("Server shutdown complete");
	}
}