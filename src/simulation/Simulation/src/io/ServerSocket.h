#pragma once

#if defined(_WIN32) || defined(_WIN64)
#ifdef _WIN64
#define PLATFORM_WINDOWS _WIN64
#else 
#define PLATFORM_WINDOWS _WIN32
#endif
#elif defined(__APPLE__) || defined(__MACH__)
#ifdef __APPLE__
#define PLATFORM_MACOS __APPLE__
#else
#define PLATFORM_MACOS __MACH__
#endif
#elif defined(__linux__)
#define PLATFORM_LINUX
#endif

#ifdef PLATFORM_WINDOWS
typedef unsigned int socket_t;
#else
#endif

#include "Common.h"

class Socket;

class ServerSocket
{
private:
	socket_t m_socket;

	bool m_closed = true;
public:
	ServerSocket();
	~ServerSocket();

	void bind(int port);
	void listen(int backlog = -1);

	Socket accept();

	void close();
};

class Socket
{
private:
	socket_t m_socket;
	std::string m_host;
	int m_port;

	bool m_closed = false;
private:
	Socket(socket_t socket, std::string host, int port) :
		m_socket(socket), m_host(host), m_port(port) {}
public:
	~Socket();

	int receive(char* buffer, int bufferSize);
	int send(const char* buffer, int bufferSize);

	void close();

	friend class ServerSocket;
};