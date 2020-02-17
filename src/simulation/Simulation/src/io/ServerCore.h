#pragma once

#include "ServerSocket.h"

#include "physics/entities/RovSetup.h"

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

	float m_thrusterPowers[THRUSTER_COUNT];
private:
	void processMessage(const char* inputBuffer, int inputLength, char* outputBuffer, int& outputLength);
	void run();
public:
	ServerCore() {}
	ServerCore(const ServerCore& other) = delete;
	~ServerCore();

	void launchServer(int port);
	void shutdownServer();

	inline float getThrusterPower(int index) const { return m_thrusterPowers[index]; }

	inline ServerCore& operator=(const ServerCore& other) = delete;
};