#include "ServerSocket.h"

#undef APIENTRY

#ifdef PLATFORM_WINDOWS

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#include <winsock2.h>
#include <WS2tcpip.h>
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

#pragma comment(lib, "Ws2_32.lib")

class WinSockWrapper
{
public:
	WinSockWrapper()
	{
		WSADATA wsaData;
		int result = WSAStartup(MAKEWORD(2, 2), &wsaData);

		if (result != 0)
		{
			LOG_ERROR("WSAStart failed: ", result);

			exit(5);
		}
		else
		{
			LOG_VERBOSE("Initialized Windows socket.");
		}
	}

	~WinSockWrapper()
	{
		WSACleanup();
	}
};

WinSockWrapper wrapper;

#endif

#include "Logger.h"

ServerSocket::ServerSocket()
{
	m_socket = socket(AF_INET, SOCK_STREAM, 0);

	if (m_socket == INVALID_SOCKET)
	{
		LOG_ERROR("Unable to initialize server socket!");

		exit(6);
	}
}

ServerSocket::~ServerSocket()
{
	close();
}

void ServerSocket::bind(int port)
{
	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(port);
	hint.sin_addr.S_un.S_addr = INADDR_ANY;

	if (::bind(m_socket, (sockaddr*)&hint, sizeof(hint)) == SOCKET_ERROR)
	{
		LOG_ERROR("Unable to bind server socket to port ", port);

		exit(7);
	}
}

void ServerSocket::listen(int backlog)
{
	if (::listen(m_socket, (backlog > 0) ? backlog : SOMAXCONN) == SOCKET_ERROR)
	{
		LOG_ERROR("Failed to set socket to listen mode.");

		exit(7);
	}

	m_closed = false;
}

Socket ServerSocket::accept()
{
	sockaddr_in client;
	int clientSize = sizeof(client);

	socket_t clientSocket = ::accept(m_socket, (sockaddr*)&client, &clientSize);
	if (clientSocket == INVALID_SOCKET)
	{
		if (!isClosed())
		{
			LOG_ERROR("Received invalid socket!");
		}

		return Socket(EMPTY_SOCKET, "", 0);
	}

	//Get address and port of the connected socket
	char clientHost[NI_MAXHOST];
	int clientPort = ntohs(client.sin_port);
	inet_ntop(AF_INET, &client.sin_addr, clientHost, NI_MAXHOST);

	return Socket(clientSocket, std::string(clientHost), clientPort);
}

void ServerSocket::close()
{
	if (!m_closed)
	{
		closesocket(m_socket);
		m_closed = true;
	}
}

int Socket::receive(char* buffer, int bufferSize)
{
	if (isClosed())
	{
		LOG_ERROR("Socket closed: Cannot receive from ", m_host, ":", m_port);

		return 0;
	}

	int bytesReceived = recv(m_socket, buffer, bufferSize, 0);
	if (bytesReceived == SOCKET_ERROR)
	{
		close();
		return 0;
	}

	return bytesReceived;
}

int Socket::send(const char* buffer, int bufferSize)
{
	if (isClosed())
	{
		LOG_ERROR("Socket closed: Cannot send to ", m_host, ":", m_port);

		return 0;
	}

	int bytesSent = ::send(m_socket, buffer, bufferSize, 0);
	if (bytesSent == SOCKET_ERROR)
	{
		close();
		return 0;
	}

	return bytesSent;
}

void Socket::close()
{
	if (!isClosed())
	{
		closesocket(m_socket);
		m_closed = true;
	}
}

Socket::~Socket()
{
	close();
}