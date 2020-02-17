#include "Logger.h"

#include <iostream>

Logger Logger::s_instance;

void Logger::pushMessage(LogLevel level, const std::string& str)
{
	const char* levelStr = "VERBOSE";

	switch (level)
	{
	case LOG_LEVEL_VERBOSE:
		levelStr = "VERBOSE";
		break;
	case LOG_LEVEL_DEBUG:
		levelStr = "DEBUG";
		break;
	case LOG_LEVEL_WARNING:
		levelStr = "WARNING";
		break;
	case LOG_LEVEL_ERROR:
		levelStr = "ERROR";
		break;
	}

	fprintf(stdout, "[%s] %s\n", levelStr, str.c_str());
}

void Logger::pause()
{
	std::cin.get();
}

Logger* Logger::singleton()
{
	return &s_instance;
}