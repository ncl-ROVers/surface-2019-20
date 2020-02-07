#pragma once

#include "ServerSocket.h"

#include <thread>
#include <memory>
#include <mutex>

class ServerCore
{
private:
	ServerSocket* m_serverSocket = nullptr;
	Socket* volatile m_socket = nullptr;

	std::mutex m_syncMutex;
	std::thread* m_mainThread = nullptr;
private:
	void processMessage(const char* inputBuffer, int inputLength, char* outputBuffer, int& outputLength);
	void run();
public:
	ServerCore() {}
	ServerCore(const ServerCore& other) = delete;
	~ServerCore();

	void launchServer(int port);
	void shutdownServer();

	inline ServerCore& operator=(const ServerCore& other) = delete;
};